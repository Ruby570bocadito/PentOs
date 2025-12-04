"""
Helpers adicionales para progress bars y visualización mejorada
"""

import sys
import time
from datetime import datetime, timedelta


class ProgressBar:
    """Barra de progreso para operaciones largas"""
    
    def __init__(self, total, description="", bar_length=50):
        self.total = total
        self.current = 0
        self.description = description
        self.bar_length = bar_length
        self.start_time = time.time()
    
    def update(self, increment=1):
        """Actualiza la barra de progreso"""
        self.current += increment
        self.display()
    
    def display(self):
        """Muestra la barra de progreso"""
        if self.total == 0:
            percent = 100
        else:
            percent = (self.current / self.total) * 100
        
        filled = int(self.bar_length * self.current / self.total) if self.total > 0 else self.bar_length
        bar = '█' * filled + '░' * (self.bar_length - filled)
        
        # Tiempo estimado
        elapsed = time.time() - self.start_time
        if self.current > 0:
            eta_seconds = (elapsed / self.current) * (self.total - self.current)
            eta = str(timedelta(seconds=int(eta_seconds)))
        else:
            eta = "calculando..."
        
        # Imprimir
        sys.stdout.write(f'\r{self.description} |{bar}| {percent:.1f}% ETA: {eta}')
        sys.stdout.flush()
        
        if self.current >= self.total:
            print()  # Nueva línea al terminar


class Spinner:
    """Spinner para indicar actividad"""
    
    def __init__(self, message="Procesando"):
        self.message = message
        self.spinning = False
        self.chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.idx = 0
    
    def spin(self):
        """Muestra el spinner"""
        if self.spinning:
            sys.stdout.write(f'\r{self.message} {self.chars[self.idx % len(self.chars)]}')
            sys.stdout.flush()
            self.idx += 1
    
    def start(self):
        """Inicia el spinner"""
        self.spinning = True
    
    def stop(self, final_message="Completado"):
        """Detiene el spinner"""
        self.spinning = False
        sys.stdout.write(f'\r{final_message}' + ' ' * 20 + '\n')
        sys.stdout.flush()


class SmartRecommender:
    """Sistema de recomendaciones inteligentes"""
    
    @staticmethod
    def recommend_next_steps(findings):
        """Recomienda próximos pasos basado en hallazgos"""
        recommendations = []
        
        # Basado en puertos abiertos
        if 'ports' in findings:
            for port_info in findings['ports']:
                port = port_info.get('port')
                service = port_info.get('service', '').lower()
                
                if port == 22:
                    recommendations.append({
                        'action': 'Brute force SSH',
                        'command': f'pentops.py exploit -t {{target}} --bruteforce ssh',
                        'priority': 'medium',
                        'reason': 'Puerto SSH abierto'
                    })
                
                elif port in [80, 443, 8080]:
                    recommendations.append({
                        'action': 'Enumeración web completa',
                        'command': f'pentops.py enum -t {{target}} -s http -p {port}',
                        'priority': 'high',
                        'reason': f'Servidor web en puerto {port}'
                    })
                    
                    recommendations.append({
                        'action': 'Escaneo de vulnerabilidades web',
                        'command': f'pentops.py vulnscan -t {{target}} --web -p {port}',
                        'priority': 'high',
                        'reason': 'Detectar vulns web comunes'
                    })
                
                elif port == 445:
                    recommendations.append({
                        'action': 'Enumeración SMB',
                        'command': 'pentops.py enum -t {target} -s smb',
                        'priority': 'high',
                        'reason': 'Puerto SMB abierto'
                    })
        
        # Basado en vulnerabilidades detectadas
        if 'vulnerabilities' in findings:
            for vuln in findings['vulnerabilities']:
                if 'RCE' in vuln.get('cve', ''):
                    recommendations.append({
                        'action': f"Explotar {vuln.get('cve')}",
                        'command': f"searchsploit {vuln.get('cve')}",
                        'priority': 'critical',
                        'reason': 'Vulnerabilidad de ejecución remota detectada'
                    })
        
        # Ordenar por prioridad
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 999))
        
        return recommendations
    
    @staticmethod
    def suggest_wordlists(service):
        """Sugiere wordlists apropiadas para un servicio"""
        wordlist_map = {
            'http': [
                '/usr/share/wordlists/dirb/common.txt',
                '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
                '/usr/share/seclists/Discovery/Web-Content/common.txt'
            ],
            'ssh': [
                '/usr/share/wordlists/rockyou.txt',
                '/usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-1000.txt'
            ],
            'ftp': [
                '/usr/share/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt'
            ]
        }
        
        return wordlist_map.get(service.lower(), [])


def format_bytes(bytes_num):
    """Formatea bytes a formato legible"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.2f} TB"


def format_duration(seconds):
    """Formatea duración en formato legible"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def create_boxed_text(text, width=60, char='='):
    """Crea texto en caja"""
    lines = text.split('\n')
    box = char * width + '\n'
    for line in lines:
        padding = width - len(line) - 4
        box += f"  {line}{' ' * padding}  \n"
    box += char * width
    return box


def display_attack_surface(findings):
    """Muestra superficie de ataque visual"""
    from config import Config
    
    print(f"\n{Config.Colors.CYAN}{Config.Colors.BOLD}╔════════════════════════════════════════════════════════════╗{Config.Colors.RESET}")
    print(f"{Config.Colors.CYAN}{Config.Colors.BOLD}║              SUPERFICIE DE ATAQUE DETECTADA                ║{Config.Colors.RESET}")
    print(f"{Config.Colors.CYAN}{Config.Colors.BOLD}╚════════════════════════════════════════════════════════════╝{Config.Colors.RESET}\n")
    
    # Puertos abiertos
    if 'ports' in findings:
        print(f"{Config.Colors.YELLOW}🔓 Puertos Abiertos:{Config.Colors.RESET}")
        for port_info in findings['ports'][:10]:
            port = port_info.get('port')
            service = port_info.get('service', 'unknown')
            print(f"   • Puerto {port:5} → {service}")
    
    # Servicios críticos
    print(f"\n{Config.Colors.RED}🎯 Servicios de Alto Valor:{Config.Colors.RESET}")
    high_value = ['ssh', 'rdp', 'smb', 'mysql', 'postgres', 'mongodb']
    found_high_value = []
    
    if 'services' in findings:
        for port, service_info in findings['services'].items():
            service = service_info.get('name', '').lower()
            if any(hv in service for hv in high_value):
                found_high_value.append(f"{service.upper()} (:{port})")
    
    if found_high_value:
        for svc in found_high_value:
            print(f"   ⚠️  {svc}")
    else:
        print(f"   {Config.Colors.GREEN}Ninguno detectado{Config.Colors.RESET}")
    
    # Vector de ataque recomendado
    print(f"\n{Config.Colors.MAGENTA}💥 Vector de Ataque Recomendado:{Config.Colors.RESET}")
    print(f"   1. Enumeración exhaustiva de servicios web")
    print(f"   2. Búsqueda de vulnerabilidades conocidas")
    print(f"   3. Brute force en servicios de autenticación")
    print(f"   4. Explotación de vulns encontradas")
    print()
