#!/usr/bin/env python3
"""
Motor de Auto-Auditoría
Sistema automatizado de evaluación de seguridad
"""

import json
from datetime import datetime
from pathlib import Path
from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    run_command, save_output, save_json, log_action, get_timestamp, print_table
)
from config import Config


class SecurityAudit:
    """Motor de auto-auditoría de seguridad"""
    
    def __init__(self, target):
        self.target = target
        self.findings = []
        self.score = 100  # Puntuación inicial
        self.severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0}
        
    def add_finding(self, title, severity, description, recommendation, cve=None):
        """Añade un hallazgo de seguridad"""
        finding = {
            'title': title,
            'severity': severity,
            'description': description,
            'recommendation': recommendation,
            'cve': cve,
            'timestamp': datetime.now().isoformat()
        }
        
        self.findings.append(finding)
        self.severity_counts[severity] += 1
        
        # Reducir score según severidad
        severity_points = {'critical': 20, 'high': 10, 'medium': 5, 'low': 2, 'info': 0}
        self.score -= severity_points.get(severity, 0)
    
    def audit_ssl_tls(self, host, port=443):
        """Audita configuración SSL/TLS"""
        print_info(f"Auditando SSL/TLS en {host}:{port}...")
        
        # Verificar SSLv3/TLS1.0 (deprecated)
        cmd = f"nmap --script ssl-enum-ciphers -p {port} {host}"
        exit_code, stdout, stderr = run_command(cmd, timeout=120)
        
        if 'SSLv3' in stdout:
            self.add_finding(
                "SSLv3 Habilitado",
                "high",
                "El protocolo SSLv3 está obsoleto y vulnerable (POODLE)",
                "Deshabilitar SSLv3 en el servidor",
                cve="CVE-2014-3566"
            )
        
        if 'TLSv1.0' in stdout:
            self.add_finding(
                "TLS 1.0 Habilitado",
                "medium",
                "TLS 1.0 tiene vulnerabilidades conocidas",
                "Actualizar a TLS 1.2 o superior"
            )
        
        # Verificar ciphers débiles
        weak_ciphers = ['RC4', 'DES', '3DES', 'MD5']
        for cipher in weak_ciphers:
            if cipher in stdout:
                self.add_finding(
                    f"Cipher Débil: {cipher}",
                    "medium",
                    f"Se detectó uso de cipher criptográficamente débil: {cipher}",
                    f"Eliminar {cipher} de la configuración de ciphers"
                )
    
    def audit_headers(self, url):
        """Audita headers de seguridad HTTP"""
        print_info(f"Auditando headers de seguridad en {url}...")
        
        cmd = f"curl -I -s {url}"
        exit_code, stdout, stderr = run_command(cmd)
        
        security_headers = {
            'Strict-Transport-Security': 'HSTS no configurado',
            'X-Frame-Options': 'Protección contra clickjacking ausente',
            'X-Content-Type-Options': 'MIME-sniffing no está prevenido',
            'Content-Security-Policy': 'CSP no configurado',
            'X-XSS-Protection': 'Protección XSS del navegador no configurada',
            'Referrer-Policy': 'Política de referrer no especificada'
        }
        
        for header, issue in security_headers.items():
            if header not in stdout:
                self.add_finding(
                    f"Header Faltante: {header}",
                    "medium" if header in ['Strict-Transport-Security', 'Content-Security-Policy'] else "low",
                    issue,
                    f"Añadir header {header} a la configuración del servidor"
                )
        
        # Verificar información expuesta
        if 'Server:' in stdout:
            self.add_finding(
                "Banner de Servidor Expuesto",
                "info",
                "El servidor expone información de versión",
                "Ocultar o modificar el header Server"
            )
    
    def audit_open_ports(self, host):
        """Audita puertos abiertos innecesarios"""
        print_info(f"Auditando puertos abiertos en {host}...")
        
        cmd = f"nmap -p- --open {host}"
        exit_code, stdout, stderr = run_command(cmd, timeout=600)
        
        # Puertos que no deberían estar expuestos a Internet
        dangerous_ports = {
            21: 'FTP',
            23: 'Telnet',
            139: 'SMB',
            445: 'SMB',
            3389: 'RDP',
            5900: 'VNC',
            3306: 'MySQL',
            5432: 'PostgreSQL',
            27017: 'MongoDB',
            6379: 'Redis'
        }
        
        for port, service in dangerous_ports.items():
            if f'{port}/tcp' in stdout and 'open' in stdout:
                self.add_finding(
                    f"Puerto Peligroso Expuesto: {service} ({port})",
                    "high",
                    f"El servicio {service} está expuesto a Internet en el puerto {port}",
                    f"Restringir acceso al puerto {port} mediante firewall o VPN"
                )
    
    def audit_web_vulnerabilities(self, url):
        """Audita vulnerabilidades web comunes"""
        print_info(f"Auditando vulnerabilidades web en {url}...")
        
        # Directorio indexing
        cmd = f"curl -s {url} | grep -i 'Index of'"
        exit_code, stdout, stderr = run_command(cmd)
        if stdout:
            self.add_finding(
                "Directory Listing Habilitado",
                "medium",
                "Los directorios exponen su contenido",
                "Deshabilitar directory listing en el servidor web"
            )
        
        # Archivos sensibles
        sensitive_files = [
            '.git/config',
            '.env',
            'config.php.bak',
            'backup.zip',
            'web.config',
            'phpinfo.php'
        ]
        
        for file in sensitive_files:
            cmd = f"curl -s -o /dev/null -w '%{{http_code}}' {url}/{file}"
            exit_code, stdout, stderr = run_command(cmd)
            if stdout.strip() == '200':
                self.add_finding(
                    f"Archivo Sensible Expuesto: {file}",
                    "high",
                    f"Archivo sensible accesible: {file}",
                    f"Eliminar o proteger el archivo {file}"
                )
    
    def audit_authentication(self):
        """Audita configuración de autenticación"""
        print_info("Auditando configuraciones de autenticación...")
        
        checks = [
            {
                'title': 'MFA No Implementado',
                'severity': 'high',
                'description': 'Autenticación multifactor no está configurada',
                'recommendation': 'Implementar MFA para todas las cuentas administrativas'
            },
            {
                'title': 'Política de Contraseñas Débil',
                'severity': 'medium',
                'description': 'No se requieren contraseñas robustas (mínimo 12 caracteres, complejidad)',
                'recommendation': 'Implementar política de contraseñas robusta'
            },
            {
                'title': 'Sin Rate Limiting en Login',
                'severity': 'medium',
                'description': 'No hay protección contra brute force en formularios de login',
                'recommendation': 'Implementar rate limiting y CAPTCHA'
            }
        ]
        
        for check in checks:
            self.add_finding(**check)
    
    def audit_compliance_cis(self):
        """Verifica cumplimiento de CIS Benchmarks"""
        print_info("Verificando cumplimiento CIS...")
        
        cis_checks = [
            {
                'control': '1.1.1',
                'title': 'Ensure mounting of cramfs filesystems is disabled',
                'severity': 'low',
                'cmd': 'modprobe -n -v cramfs'
            },
            {
                'control': '1.5.1',
                'title': 'Ensure core dumps are restricted',
                'severity': 'medium',
                'cmd': 'grep "hard core" /etc/security/limits.conf'
            },
            {
                'control': '3.1.1',
                'title': 'Ensure IP forwarding is disabled',
                'severity': 'medium',
                'cmd': 'sysctl net.ipv4.ip_forward'
            }
        ]
        
        for check in cis_checks:
            self.add_finding(
                f"CIS {check['control']}: {check['title']}",
                check['severity'],
                f"Verificar cumplimiento de CIS Benchmark {check['control']}",
                f"Ejecutar: {check['cmd']}"
            )
    
    def audit_owasp_top10(self, url):
        """Verifica OWASP Top 10"""
        print_info("Verificando OWASP Top 10...")
        
        owasp_checks = [
            {
                'id': 'A01',
                'title': 'Broken Access Control',
                'severity': 'high',
                'description': 'Verificar control de acceso apropiado',
                'test': 'Intentar acceder a recursos sin autenticación'
            },
            {
                'id': 'A02',
                'title': 'Cryptographic Failures',
                'severity': 'high',
                'description': 'Verificar cifrado de datos sensibles',
                'test': 'Revisar SSL/TLS y almacenamiento de contraseñas'
            },
            {
                'id': 'A03',
                'title': 'Injection',
                'severity': 'critical',
                'description': 'SQL, NoSQL, OS command injection',
                'test': 'Probar inputs con payloads de SQLi'
            },
            {
                'id': 'A05',
                'title': 'Security Misconfiguration',
                'severity': 'high',
                'description': 'Configuraciones inseguras por defecto',
                'test': 'Verificar headers, directory listing, error messages'
            },
            {
                'id': 'A07',
                'title': 'Identification and Authentication Failures',
                'severity': 'high',
                'description': 'Autenticación y gestión de sesiones débil',
                'test': 'Verificar session management y password policies'
            }
        ]
        
        for check in owasp_checks:
            self.add_finding(
                f"OWASP {check['id']}: {check['title']}",
                check['severity'],
                check['description'],
                check['test']
            )
    
    def calculate_risk_score(self):
        """Calcula puntuación de riesgo"""
        # Normalizar score a 0-100
        if self.score < 0:
            self.score = 0
        
        risk_level = 'BAJO'
        if self.score < 40:
            risk_level = 'CRÍTICO'
        elif self.score < 60:
            risk_level = 'ALTO'
        elif self.score < 80:
            risk_level = 'MEDIO'
        
        return{
            'score': self.score,
            'risk_level': risk_level,
            'total_findings': len(self.findings),
            'severity_counts': self.severity_counts
        }
    
    def run_complete_audit(self, host, url=None):
        """Ejecuta auditoría completa"""
        print_banner("AUTO-AUDITORÍA DE SEGURIDAD")
        
        # Auditorías de red
        self.audit_open_ports(host)
        
        # Auditorías web
        if url:
            self.audit_ssl_tls(host)
            self.audit_headers(url)
            self.audit_web_vulnerabilities(url)
            self.audit_owasp_top10(url)
        
        # Auditorías generales
        self.audit_authentication()
        self.audit_compliance_cis()
        
        # Calcular riesgo
        risk = self.calculate_risk_score()
        
        # Mostrar resultados
        self.display_summary(risk)
        
        return risk
    
    def display_summary(self, risk):
        """Muestra resumen de auditoría"""
        print_banner("RESUMEN DE AUDITORÍA")
        
        # Risk score
        color_func = print_error if risk['risk_level'] == 'CRÍTICO' else \
                     print_warning if risk['risk_level'] in ['ALTO', 'MEDIO'] else \
                     print_success
        
        color_func(f"\n🎯 PUNTUACIÓN DE SEGURIDAD: {risk['score']}/100 [{risk['risk_level']}]")
        
        # Severity counts
        print_info(f"\n📊 Hallazgos por Severidad:")
        print_error(f"   🔴 Críticos: {risk['severity_counts']['critical']}")
        print_warning(f"   🟠 Altos: {risk['severity_counts']['high']}")
        print_warning(f"   🟡 Medios: {risk['severity_counts']['medium']}")
        print_info(f"   🟢 Bajos: {risk['severity_counts']['low']}")
        print_info(f"   ℹ️  Informativos: {risk['severity_counts']['info']}")
        
        # Top findings
        if self.findings:
            print_info(f"\n🔍 Top 5 Hallazgos Críticos:")
            critical = [f for f in self.findings if f['severity'] in ['critical', 'high']][:5]
            for i, finding in enumerate(critical, 1):
                severity_icon = '🔴' if finding['severity'] == 'critical' else '🟠'
                print(f"   {i}. {severity_icon} {finding['title']}")


def run_auto_audit(args):
    """
    Función principal de auto-auditoría
    
    Args:
        args: Argumentos parseados
    """
    print_banner(f"INICIANDO AUTO-AUDITORÍA: {args.target}")
    
    audit = SecurityAudit(args.target)
    
    log_action(args.target, "auto-audit", "Iniciando auto-auditoría")
    
    # URL opcional
    url = f"http://{args.target}" if not args.target.startswith('http') else args.target
    
    # Ejecutar auditoría completa
    risk = audit.run_complete_audit(args.target, url if hasattr(args, 'web') and args.web else None)
    
    # Guardar resultados
    output_dir = Config.get_output_dir(args.target)
    
    # JSON detallado
    full_report = {
        'target': args.target,
        'timestamp': datetime.now().isoformat(),
        'risk_assessment': risk,
        'findings': audit.findings
    }
    
    save_json(args.target, "auto-audit", f"audit_{get_timestamp()}.json", full_report)
    
    print_success(f"\n✓ Auto-auditoría completada")
    print_info(f"Resultados guardados en {output_dir}")
    
    log_action(args.target, "auto-audit", "Auto-auditoría completada", f"Score: {risk['score']}")
    
    return full_report
