#!/usr/bin/env python3
"""
Módulo de Auto-Detección e Inteligencia
Detecta automáticamente tecnologías, vulnerabilidades y sugiere acciones
"""

import re
import json
from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    run_command, save_output, save_json, log_action, get_timestamp
)
from config import Config


class AutoDetector:
    """Sistema de auto-detección inteligente"""
    
    def __init__(self, target):
        self.target = target
        self.detected = {
            'technologies': [],
            'vulnerabilities': [],
            'suggestions': [],
            'ports': [],
            'services': {}
        }
    
    def detect_technologies_from_headers(self, headers):
        """Detecta tecnologías desde headers HTTP"""
        tech_patterns = {
            'Apache': r'Apache/([\d.]+)',
            'nginx': r'nginx/([\d.]+)',
            'PHP': r'PHP/([\d.]+)',
            'Express': r'Express',
            'ASP.NET': r'ASP\.NET',
            'IIS': r'Microsoft-IIS/([\d.]+)',
            'WordPress': r'WordPress',
            'Drupal': r'Drupal',
            'Joomla': r'Joomla',
        }
        
        for tech, pattern in tech_patterns.items():
            match = re.search(pattern, headers, re.IGNORECASE)
            if match:
                version = match.group(1) if match.groups() else 'Unknown'
                self.detected['technologies'].append({
                    'name': tech,
                    'version': version,
                    'confidence': 'high'
                })
    
    def suggest_actions_for_service(self, service, port):
        """Sugiere acciones basadas en el servicio detectado"""
        suggestions = []
        
        service_actions = {
            'ssh': [
                'Probar autenticación con claves débiles',
                'Brute force con usuarios comunes',
                'Verificar versión para exploits conocidos',
                'Enumerar métodos de autenticación'
            ],
            'http': [
                'Enumerar directorios con gobuster',
                'Escanear con Nikto',
                'Buscar paneles de administración',
                'Probar inyecciones SQL',
                'Verificar archivos robots.txt y sitemap.xml',
                'Fuzzing de parámetros'
            ],
            'smb': [
                'Enumerar shares con enum4linux',
                'Verificar acceso anónimo',
                'Probar EternalBlue (MS17-010)',
                'Enumerar usuarios del dominio',
                'Verificar permisos de escritura'
            ],
            'ftp': [
                'Probar login anónimo',
                'Verificar versión para exploits',
                'Enumerar archivos disponibles',
                'Intentar subida de archivos'
            ],
            'mysql': [
                'Probar credenciales por defecto (root:root, root:)',
                'Brute force de contraseñas',
                'Verificar autenticación externa',
                'UDF injection si tienes acceso'
            ],
            'rdp': [
                'Brute force con usuarios comunes',
                'Verificar BlueKeep (CVE-2019-0708)',
                'Intentar autenticación NLA bypass'
            ]
        }
        
        if service.lower() in service_actions:
            for action in service_actions[service.lower()]:
                suggestions.append({
                    'service': service,
                    'port': port,
                    'action': action,
                    'priority': 'high' if 'exploit' in action.lower() or 'vulnerability' in action.lower() else 'medium'
                })
        
        return suggestions
    
    def detect_cve_from_version(self, service, version):
        """Detecta CVEs conocidos basados en versión (simplificado)"""
        # Base de datos simplificada de CVEs conocidos
        known_vulns = {
            'Apache': {
                '2.4.49': ['CVE-2021-41773 - Path Traversal'],
                '2.4.50': ['CVE-2021-42013 - Path Traversal RCE'],
            },
            'OpenSSH': {
                '7.2': ['CVE-2016-10012 - Untrusted pointer dereference'],
                '7.4': ['CVE-2018-15473 - Username enumeration'],
            },
            'ProFTPD': {
                '1.3.5': ['CVE-2015-3306 - RCE via mod_copy'],
            },
            'Samba': {
                '3.5.0': ['CVE-2017-7494 - SambaCry RCE'],
            }
        }
        
        vulnerabilities = []
        
        if service in known_vulns:
            if version in known_vulns[service]:
                for vuln in known_vulns[service][version]:
                    vulnerabilities.append({
                        'service': service,
                        'version': version,
                        'cve': vuln,
                        'severity': 'critical' if 'RCE' in vuln else 'high'
                    })
        
        return vulnerabilities
    
    def analyze_target(self, scan_results):
        """Analiza resultados de scan y genera recomendaciones"""
        print_info("Auto-detección inteligente")
        
        # Procesar puertos y servicios
        for port_info in scan_results:
            port = port_info.get('port')
            service = port_info.get('service', 'unknown')
            version = port_info.get('version', '')
            
            self.detected['ports'].append(port)
            self.detected['services'][port] = {
                'name': service,
                'version': version
            }
            
            # Detectar vulnerabilidades conocidas
            if version:
                vulns = self.detect_cve_from_version(service, version)
                self.detected['vulnerabilities'].extend(vulns)
            
            # Generar sugerencias
            suggestions = self.suggest_actions_for_service(service, port)
            self.detected['suggestions'].extend(suggestions)
        
        # Mostrar resultados
        self.display_findings()
        
        return self.detected
    
    def display_findings(self):
        """Muestra los hallazgos de forma visual"""
        
        # Tecnologías detectadas
        if self.detected['technologies']:
            print_info("\n🔍 Tecnologías Detectadas:")
            for tech in self.detected['technologies']:
                print_success(f"  • {tech['name']} {tech['version']} (Confianza: {tech['confidence']})")
        
        # Vulnerabilidades conocidas
        if self.detected['vulnerabilities']:
            print_warning("\n⚠️  Vulnerabilidades Conocidas:")
            for vuln in self.detected['vulnerabilities']:
                severity_color = print_error if vuln['severity'] == 'critical' else print_warning
                severity_color(f"  • [{vuln['severity'].upper()}] {vuln['service']} {vuln['version']}: {vuln['cve']}")
        
        # Sugerencias de acciones
        if self.detected['suggestions']:
            print_info("\n💡 Acciones Sugeridas:")
            
            # Agrupar por prioridad
            high_priority = [s for s in self.detected['suggestions'] if s['priority'] == 'high']
            medium_priority = [s for s in self.detected['suggestions'] if s['priority'] == 'medium']
            
            if high_priority:
                print_warning("  ALTA PRIORIDAD:")
                for sug in high_priority[:5]:  # Top 5
                    print_warning(f"    → [{sug['service']}:{sug['port']}] {sug['action']}")
            
            if medium_priority:
                print_info("\n  MEDIA PRIORIDAD:")
                for sug in medium_priority[:5]:  # Top 5
                    print_info(f"    → [{sug['service']}:{sug['port']}] {sug['action']}")
    
    def generate_attack_plan(self):
        """Genera un plan de ataque automatizado basado en los hallazgos"""
        plan = {
            'phases': []
        }
        
        # Fase 1: Explotar vulnerabilidades conocidas
        if self.detected['vulnerabilities']:
            phase = {
                'name': 'Explotación de Vulnerabilidades Conocidas',
                'priority': 1,
                'tasks': []
            }
            for vuln in self.detected['vulnerabilities']:
                phase['tasks'].append({
                    'target': f"{vuln['service']} {vuln['version']}",
                    'action': f"Buscar exploit para {vuln['cve']}",
                    'command': f"searchsploit {vuln['cve']}"
                })
            plan['phases'].append(phase)
        
        # Fase 2: Enumeración profunda
        phase = {
            'name': 'Enumeración Profunda',
            'priority': 2,
            'tasks': []
        }
        for port, service_info in self.detected['services'].items():
            service = service_info['name']
            if service in ['http', 'https']:
                phase['tasks'].append({
                    'target': f"Port {port}",
                    'action': 'Directory enumeration',
                    'command': f"gobuster dir -u http://{self.target}:{port} -w /path/to/wordlist"
                })
        plan['phases'].append(phase)
        
        return plan


def run_auto_detect(target, scan_results_file=None):
    """
    Ejecuta auto-detección en un target
    
    Args:
        target: IP o dominio
        scan_results_file: Archivo JSON con resultados de scan previo
    """
    detector = AutoDetector(target)
    
    # Si hay archivo de resultados, cargarlo
    if scan_results_file:
        try:
            with open(scan_results_file, 'r') as f:
                scan_results = json.load(f)
        except:
            print_error(f"No se pudo cargar {scan_results_file}")
            return None
    else:
        # Realizar scan rápido
        print_info("Realizando scan rápido para auto-detección...")
        from modules.recon import run_nmap_quick
        output_dir = Config.get_output_dir(target)
        scan_results = run_nmap_quick(target, output_dir)
    
    # Analizar
    findings = detector.analyze_target(scan_results)
    
    # Guardar resultados
    output_dir = Config.get_output_dir(target)
    save_json(target, "auto-detect", f"findings_{get_timestamp()}.json", findings)
    
    # Generar plan de ataque
    attack_plan = detector.generate_attack_plan()
    save_json(target, "auto-detect", f"attack_plan_{get_timestamp()}.json", attack_plan)
    
    print_success(f"\n✓ Auto-detección completada. Resultados guardados en {output_dir}")
    
    return findings
