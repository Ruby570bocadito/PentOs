#!/usr/bin/env python3
"""
Motor de Automatización Inteligente
Orquesta pentesting completo con decisiones adaptativas
"""

import json
import time
from pathlib import Path
from datetime import datetime
from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    run_command, save_output, save_json, log_action, get_timestamp
)
from config import Config


class IntelligentAutomation:
    """Motor de automatización con inteligencia adaptativa"""
    
    def __init__(self, target, mode='comprehensive'):
        self.target = target
        self.mode = mode  # comprehensive, fast, stealth
        self.results = {}
        self.discovered_services = []
        self.vulnerabilities = []
        self.next_actions = []
        self.timeline = []
        
    def log_step(self, phase, action, status='completed'):
        """Registra cada paso del proceso"""
        self.timeline.append({
            'timestamp': datetime.now().isoformat(),
            'phase': phase,
            'action': action,
            'status': status
        })
    
    def run_comprehensive_pentest(self):
        """Ejecuta pentesting completo y adaptativo"""
        print_banner(f"PENTESTING AUTOMATIZADO COMPLETO: {self.target}")
        
        print_info(f"""
╔═══════════════════════════════════════════════════════════╗
║          MODO: {self.mode.upper()}                        
║          TARGET: {self.target}                            
║          INICIO: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
╚═══════════════════════════════════════════════════════════╝
""")
        
        # FASE 1: Reconnaissance Adaptativo
        self.phase_1_reconnaissance()
        
        # FASE 2: Intelligence Gathering
        self.phase_2_intelligence()
        
        # FASE 3: Enumeración Dirigida
        self.phase_3_enumeration()
        
        # FASE 4: Vulnerability Assessment
        self.phase_4_vulnerability_assessment()
        
        # FASE 5: Auto-Auditoría
        self.phase_5_auto_audit()
        
        # FASE 6: Análisis y Recomendaciones
        self.phase_6_analysis()
        
        # FASE 7: Reporte Final
        self.phase_7_reporting()
        
        # Resumen final
        self.print_final_summary()
    
    def phase_1_reconnaissance(self):
        """Fase 1: Reconnaissance con auto-detección"""
        print_banner("FASE 1: RECONNAISSANCE")
        self.log_step('Phase 1', 'Starting reconnaissance')
        
        # Scan inicial
        print_info("1.1 - Escaneo rápido de puertos críticos...")
        from modules.recon import run_nmap_quick
        output_dir = Config.get_output_dir(self.target)
        
        try:
            scan_results = run_nmap_quick(self.target, output_dir)
            self.results['nmap_quick'] = scan_results
            print_success(f"✓ Scan rápido completado: {len(scan_results)} puertos detectados")
            self.log_step('Phase 1', 'Quick scan', 'success')
        except Exception as e:
            print_error(f"Error en scan rápido: {e}")
            self.log_step('Phase 1', 'Quick scan', 'failed')
        
        # Auto-detección
        print_info("\n1.2 - Auto-detección de tecnologías y vulnerabilidades...")
        from modules.autodetect import run_auto_detect
        
        try:
            findings = run_auto_detect(self.target, None)
            self.results['autodetect'] = findings
            
            if findings:
                # Extraer servicios descubiertos
                if 'services' in findings:
                    for port, service_info in findings['services'].items():
                        self.discovered_services.append({
                            'port': port,
                            'service': service_info.get('name'),
                            'version': service_info.get('version')
                        })
                
                # Extraer vulnerabilidades
                if 'vulnerabilities' in findings:
                    self.vulnerabilities.extend(findings['vulnerabilities'])
                
                print_success(f"✓ Auto-detección: {len(self.discovered_services)} servicios, {len(self.vulnerabilities)} vulns")
            self.log_step('Phase 1', 'Auto-detection', 'success')
        except Exception as e:
            print_warning(f"Auto-detección fallo: {e}")
            self.log_step('Phase 1', 'Auto-detection', 'failed')
        
        time.sleep(2)
    
    def phase_2_intelligence(self):
        """Fase 2: Intelligence Gathering con APIs"""
        print_banner("FASE 2: INTELLIGENCE GATHERING")
        self.log_step('Phase 2', 'Starting intelligence gathering')
        
        import os
        
        # Shodan
        if os.getenv('SHODAN_API_KEY'):
            print_info("2.1 - Consultando Shodan...")
            from modules.api_intel import APIIntegrator
            
            try:
                integrator = APIIntegrator()
                shodan_data = integrator.shodan_lookup(self.target)
                if shodan_data:
                    self.results['shodan'] = shodan_data
                    print_success("✓ Datos de Shodan obtenidos")
                    self.log_step('Phase 2', 'Shodan lookup', 'success')
            except Exception as e:
                print_warning(f"Shodan no disponible: {e}")
                self.log_step('Phase 2', 'Shodan lookup', 'skipped')
        else:
            print_info("2.1 - Shodan API key no configurada (skipping)")
            self.log_step('Phase 2', 'Shodan lookup', 'skipped')
        
        # VirusTotal
        if os.getenv('VT_API_KEY'):
            print_info("\n2.2 - Consultando VirusTotal...")
            from modules.api_intel import APIIntegrator
            
            try:
                integrator = APIIntegrator()
                vt_data = integrator.virustotal_lookup(self.target, 'ip')
                if vt_data:
                    self.results['virustotal'] = vt_data
                    print_success("✓ Análisis de VirusTotal obtenido")
                    self.log_step('Phase 2', 'VirusTotal lookup', 'success')
            except Exception as e:
                print_warning(f"VirusTotal no disponible: {e}")
                self.log_step('Phase 2', 'VirusTotal lookup', 'skipped')
        else:
            print_info("2.2 - VirusTotal API key no configurada (skipping)")
            self.log_step('Phase 2', 'VirusTotal lookup', 'skipped')
        
        time.sleep(2)
    
    def phase_3_enumeration(self):
        """Fase 3: Enumeración dirigida basada en servicios"""
        print_banner("FASE 3: ENUMERACIÓN DIRIGIDA")
        self.log_step('Phase 3', 'Starting targeted enumeration')
        
        if not self.discovered_services:
            print_warning("No hay servicios detectados para enumerar")
            return
        
        # Enumerar servicios web
        web_ports = [80, 443, 8080, 8443]
        web_services = [s for s in self.discovered_services if int(s['port']) in web_ports]
        
        if web_services:
            print_info(f"3.1 - Enumeración web ({len(web_services)} servicios)...")
            from modules.enumeration import enumerate_http
            
            for service in web_services:
                port = service['port']
                print_info(f"   → Puerto {port}")
                
                try:
                    output_dir = Config.get_output_dir(self.target) / 'enumeration' / 'http'
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Gobuster directory enumeration
                    enumerate_http(self.target, port, str(output_dir))
                    print_success(f"   ✓ Puerto {port} enumerado")
                    self.log_step('Phase 3', f'HTTP enum port {port}', 'success')
                except Exception as e:
                    print_error(f"   Error enumerando puerto {port}: {e}")
                    self.log_step('Phase 3', f'HTTP enum port {port}', 'failed')
        
        # Enumerar SMB si existe
        smb_services = [s for s in self.discovered_services if s['service'] and 'smb' in s['service'].lower()]
        
        if smb_services:
            print_info("\n3.2 - Enumeración SMB...")
            from modules.enumeration import enumerate_smb
            
            try:
                output_dir = Config.get_output_dir(self.target) / 'enumeration' / 'smb'
                output_dir.mkdir(parents=True, exist_ok=True)
                
                enumerate_smb(self.target, str(output_dir))
                print_success("✓ SMB enumerado")
                self.log_step('Phase 3', 'SMB enumeration', 'success')
            except Exception as e:
                print_error(f"Error en SMB: {e}")
                self.log_step('Phase 3', 'SMB enumeration', 'failed')
        
        time.sleep(2)
    
    def phase_4_vulnerability_assessment(self):
        """Fase 4: Evaluación de vulnerabilidades"""
        print_banner("FASE 4: VULNERABILITY ASSESSMENT")
        self.log_step('Phase 4', 'Starting vulnerability assessment')
        
        # Web vulnerability scanning
        web_ports = [80, 443, 8080]
        has_web = any(int(s['port']) in web_ports for s in self.discovered_services)
        
        if has_web:
            print_info("4.1 - Escaneo de vulnerabilidades web con Nikto...")
            from modules.vulnscan import run_nikto
            
            try:
                output_dir = Config.get_output_dir(self.target)
                run_nikto(self.target, 80, output_dir)
                print_success("✓ Nikto scan completado")
                self.log_step('Phase 4', 'Nikto scan', 'success')
            except Exception as e:
                print_warning(f"Nikto falló: {e}")
                self.log_step('Phase 4', 'Nikto scan', 'failed')
        
        # Nmap vulnerability scripts
        print_info("\n4.2 - Scripts NSE de vulnerabilidades...")
        from modules.vulnscan import run_nmap_vulnscan
        
        try:
            output_dir = Config.get_output_dir(self.target)
            run_nmap_vulnscan(self.target, output_dir)
            print_success("✓ NSE vulnscan completado")
            self.log_step('Phase 4', 'NSE vulnscan', 'success')
        except Exception as e:
            print_warning(f"NSE vulnscan falló: {e}")
            self.log_step('Phase 4', 'NSE vulnscan', 'failed')
        
        time.sleep(2)
    
    def phase_5_auto_audit(self):
        """Fase 5: Auto-auditoría de seguridad"""
        print_banner("FASE 5: AUTO-AUDITORÍA")
        self.log_step('Phase 5', 'Starting security audit')
        
        print_info("5.1 - Ejecutando auto-auditoría de seguridad...")
        from modules.autoaudit import SecurityAudit
        
        try:
            audit = SecurityAudit(self.target)
            
            # Determinar si es web
            has_web = any(int(s['port']) in [80, 443, 8080] for s in self.discovered_services)
            url = f"http://{self.target}" if has_web else None
            
            # Ejecutar auditoría
            risk = audit.run_complete_audit(self.target, url)
            
            self.results['auto_audit'] = {
                'risk_assessment': risk,
                'findings': audit.findings
            }
            
            print_success(f"✓ Auto-auditoría: Score {risk['score']}/100 [{risk['risk_level']}]")
            self.log_step('Phase 5', 'Security audit', 'success')
        except Exception as e:
            print_error(f"Auto-auditoría falló: {e}")
            self.log_step('Phase 5', 'Security audit', 'failed')
        
        time.sleep(2)
    
    def phase_6_analysis(self):
        """Fase 6: Análisis y recomendaciones"""
        print_banner("FASE 6: ANÁLISIS Y RECOMENDACIONES")
        self.log_step('Phase 6', 'Analyzing results')
        
        print_info("6.1 - Analizando hallazgos y generando recomendaciones...")
        
        # Contar hallazgos por severidad
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        if 'auto_audit' in self.results:
            audit_results = self.results['auto_audit']
            if 'risk_assessment' in audit_results:
                severity_counts = audit_results['risk_assessment'].get('severity_counts', severity_counts)
        
        print_info("\n📊 Resumen de Hallazgos:")
        print_error(f"   🔴 Críticos: {severity_counts['critical']}")
        print_warning(f"   🟠 Altos: {severity_counts['high']}")
        print_warning(f"   🟡 Medios: {severity_counts['medium']}")
        print_info(f"   🟢 Bajos: {severity_counts['low']}")
        
        # Generar próximos pasos
        self.generate_next_actions()
        
        self.log_step('Phase 6', 'Analysis completed', 'success')
        time.sleep(2)
    
    def generate_next_actions(self):
        """Genera lista de próximas acciones recomendadas"""
        self.next_actions = []
        
        # Basado en vulnerabilidades críticas
        if self.vulnerabilities:
            for vuln in self.vulnerabilities:
                if 'RCE' in vuln.get('cve', ''):
                    self.next_actions.append({
                        'priority': 'CRITICAL',
                        'action': f"Investigar y explotar {vuln.get('cve')}",
                        'target': f"{vuln.get('service')} {vuln.get('version')}"
                    })
        
        # Basado en servicios
        for service in self.discovered_services:
            if service['service'] == 'ssh':
                self.next_actions.append({
                    'priority': 'MEDIUM',
                    'action': 'Brute force SSH con usuarios comunes',
                    'target': f"Puerto {service['port']}"
                })
            
            elif service['service'] in ['http', 'https']:
                self.next_actions.append({
                    'priority': 'HIGH',
                    'action': 'Probar SQLi, XSS, y otras vulns web',
                    'target': f"Puerto {service['port']}"
                })
        
        # Mostrar próximos pasos
        if self.next_actions:
            print_info("\n💡 Próximas Acciones Recomendadas:")
            for i, action in enumerate(self.next_actions[:5], 1):
                priority_icon = {'CRITICAL': '🚨', 'HIGH': '⚠️', 'MEDIUM': '📌', 'LOW': '💡'}.get(action['priority'], '📌')
                print(f"   {i}. {priority_icon} [{action['priority']}] {action['action']}")
                print(f"      Target: {action['target']}")
    
    def phase_7_reporting(self):
        """Fase 7: Generación de reporte completo"""
        print_banner("FASE 7: GENERACIÓN DE REPORTE")
        self.log_step('Phase 7', 'Generating reports')
        
        print_info("7.1 - Compilando todos los resultados...")
        
        # Guardar timeline
        output_dir = Config.get_output_dir(self.target)
        timeline_file = output_dir / f"automation_timeline_{get_timestamp()}.json"
        
        with open(timeline_file, 'w', encoding='utf-8') as f:
            json.dump(self.timeline, f, indent=2, ensure_ascii=False)
        
        print_success(f"✓ Timeline guardado: {timeline_file}")
        
        # Generar reporte avanzado
        print_info("\n7.2 - Generando informe completo...")
        from modules.advanced_report import AdvancedReportGenerator
        
        try:
            generator = AdvancedReportGenerator(self.target)
            reports = generator.generate_complete_report()
            
            print_success("✓ Informes generados:")
            print_info(f"   • Markdown: {reports['markdown']}")
            print_info(f"   • HTML: {reports['html']}")
            print_info(f"   • JSON: {reports['json']}")
            
            self.log_step('Phase 7', 'Report generation', 'success')
        except Exception as e:
            print_error(f"Error generando reportes: {e}")
            self.log_step('Phase 7', 'Report generation', 'failed')
        
        time.sleep(2)
    
    def print_final_summary(self):
        """Imprime resumen final del pentesting"""
        print_banner("✅ PENTESTING AUTOMATIZADO COMPLETADO")
        
        duration = len(self.timeline)
        successful_steps = len([s for s in self.timeline if s['status'] == 'success'])
        failed_steps = len([s for s in self.timeline if s['status'] == 'failed'])
        
        print_info(f"""
╔═══════════════════════════════════════════════════════════╗
║                  RESUMEN FINAL                            ║
╠═══════════════════════════════════════════════════════════╣
║  Target:              {self.target:30s}          ║
║  Modo:                {self.mode:30s}          ║
║  Pasos totales:       {duration:30d}          ║
║  Exitosos:            {successful_steps:30d}          ║
║  Fallidos:            {failed_steps:30d}          ║
║                                                           ║
║  Servicios:           {len(self.discovered_services):30d}          ║
║  Vulnerabilidades:    {len(self.vulnerabilities):30d}          ║
║  Próximas acciones:   {len(self.next_actions):30d}          ║
╚═══════════════════════════════════════════════════════════╝
""")
        
        # Risk level
        if 'auto_audit' in self.results:
            risk = self.results['auto_audit'].get('risk_assessment', {})
            risk_level = risk.get('risk_level', 'UNKNOWN')
            score = risk.get('score', 0)
            
            color_func = print_error if risk_level == 'CRÍTICO' else \
                        print_warning if risk_level in ['ALTO', 'MEDIO'] else \
                        print_success
            
            color_func(f"\n🎯 NIVEL DE RIESGO: {risk_level} (Score: {score}/100)")
        
        print_success(f"\n✓ Todos los resultados en: {Config.get_output_dir(self.target)}")
        print_info("\n📄 Revisa el informe completo en formato HTML para detalles visuales")


def run_full_automation(args):
    """
    Ejecuta automatización completa
    
    Args:
        args: Argumentos parseados
    """
    mode = args.mode if hasattr(args, 'mode') else 'comprehensive'
    
    automation = IntelligentAutomation(args.target, mode)
    
    log_action(args.target, "automation", f"Iniciando pentesting automatizado [{mode}]")
    
    # Ejecutar pentesting completo
    automation.run_comprehensive_pentest()
    
    log_action(args.target, "automation", "Pentesting automatizado completado")
    
    return automation.results
