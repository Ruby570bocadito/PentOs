#!/usr/bin/env python3
"""
PentOps - Professional Pentesting Operations CLI Tool
Herramienta de orquestación y automatización para pentesting
"""

import argparse
import sys
import os
from datetime import datetime
from config import Config
from utils import print_banner, print_success, print_error, print_info, print_warning

__version__ = "1.0.0"
__author__ = "PentOps Team"

def show_banner():
    """Muestra el banner ASCII con calavera estilo Metasploit"""
    banner = r"""
    ____             __  ____            
   / __ \___  ____  / /_/ __ \____  _____
  / /_/ / _ \/ __ \/ __/ / / / __ \/ ___/
 / ____/  __/ / / / /_/ /_/ / /_/ (__  ) 
/_/    \___/_/ /_/\__/\____/ .___/____/  
                          /_/            

        ⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢰⡿⠋⠁⠀⠀⠈⠉⠙⠻⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢀⣿⠇⠀⢀⣴⣶⡾⠿⠿⠿⢿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⣀⣀⣸⡿⠀⠀⢸⣿⣇⠀⠀⠀⠀⠀⠀⠙⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⣾⡟⠛⣿⡇⠀⠀⢸⣿⣿⣷⣤⣤⣤⣤⣶⣶⣿⠇⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀
        ⢀⣿⠀⢀⣿⡇⠀⠀⠀⠻⢿⣿⣿⣿⣿⣿⠿⣿⡏⠀⠀⠀⠀⢴⣶⣶⣿⣿⣿⣆
        ⢸⣿⠀⢸⣿⡇⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⣿⡇⣀⣠⣴⣾⣮⣝⠿⠿⠿⣻⡟
        ⢸⣿⠀⠘⣿⡇⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠉⠀
        ⠸⣿⠀⠀⣿⡇⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⠀
        ⠀⠻⣷⣶⣿⣇⠀⠀⠀⢠⣼⣿⣿⣿⣿⣿⣿⣿⣛⣛⣻⠉⠁⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢸⣿⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢸⣿⣀⣀⣀⣼⡿⢿⣿⣿⣿⣿⣿⡿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠙⠛⠛⠛⠋⠁⠀⠙⠻⠿⠟⠋⠑⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

    """
    
    print("\033[91m" + banner + "\033[0m")  # Red color
    print("\033[93m" + "="*60 + "\033[0m")
    print(f"\033[96m  PentOps v{__version__} - Pentesting Orchestration Tool\033[0m")
    print(f"\033[96m  Automatiza tu proceso de pentesting\033[0m")
    print("\033[93m" + "="*60 + "\033[0m\n")


def main():
    """Función principal de la CLI"""
    
    # Crear parser principal
    parser = argparse.ArgumentParser(
        description='PentOps - Herramienta de orquestación para pentesting',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  pentops.py recon -t 192.168.1.100 --quick
  pentops.py enum -t 192.168.1.100 -p 80,445
  pentops.py workflow -w hybrid -t 192.168.1.100
  pentops.py report -t 192.168.1.100 -o pdf
        """
    )
    
    parser.add_argument('-v', '--version', action='version', version=f'PentOps v{__version__}')
    parser.add_argument('--no-banner', action='store_true', help='No mostrar el banner')
    parser.add_argument('--verbose', action='store_true', help='Modo verbose')
    
    # Crear subparsers para módulos
    subparsers = parser.add_subparsers(dest='module', help='Módulos disponibles')
    
    # ====================
    # MÓDULO: RECON
    # ====================
    recon_parser = subparsers.add_parser('recon', help='Módulo de reconocimiento')
    recon_parser.add_argument('-t', '--target', required=True, help='IP o dominio objetivo')
    recon_parser.add_argument('--quick', action='store_true', help='Scan rápido (top 1000 puertos)')
    recon_parser.add_argument('--full', action='store_true', help='Scan completo (todos los puertos)')
    recon_parser.add_argument('--udp', action='store_true', help='Incluir scan UDP')
    recon_parser.add_argument('--scripts', action='store_true', help='Ejecutar scripts NSE')
    recon_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: ENUM
    # ====================
    enum_parser = subparsers.add_parser('enum', help='Módulo de enumeración')
    enum_parser.add_argument('-t', '--target', required=True, help='IP o dominio objetivo')
    enum_parser.add_argument('-p', '--ports', help='Puertos a enumerar (ej: 80,443,445)')
    enum_parser.add_argument('-s', '--service', help='Servicio específico (http, smb, ftp, etc)')
    enum_parser.add_argument('--auto', action='store_true', help='Auto-detectar servicios')
    enum_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: VULNSCAN
    # ====================
    vuln_parser = subparsers.add_parser('vulnscan', help='Módulo de análisis de vulnerabilidades')
    vuln_parser.add_argument('-t', '--target', required=True, help='IP o dominio objetivo')
    vuln_parser.add_argument('-p', '--ports', help='Puertos específicos')
    vuln_parser.add_argument('--web', action='store_true', help='Análisis web (Nikto)')
    vuln_parser.add_argument('--searchsploit', action='store_true', help='Buscar exploits con searchsploit')
    vuln_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: EXPLOIT
    # ====================
    exploit_parser = subparsers.add_parser('exploit', help='Módulo de explotación')
    exploit_parser.add_argument('-t', '--target', required=True, help='IP o dominio objetivo')
    exploit_parser.add_argument('--bruteforce', help='Servicio para brute force (ssh, ftp, smb)')
    exploit_parser.add_argument('-u', '--userlist', help='Lista de usuarios')
    exploit_parser.add_argument('-p', '--passlist', help='Lista de contraseñas')
    exploit_parser.add_argument('--sqli', help='URL para SQL injection')
    exploit_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: POSTEXPLOIT
    # ====================
    post_parser = subparsers.add_parser('postexploit', help='Módulo de post-explotación')
    post_parser.add_argument('-t', '--target', required=True, help='IP del objetivo comprometido')
    post_parser.add_argument('--linpeas', action='store_true', help='Ejecutar LinPEAS')
    post_parser.add_argument('--winpeas', action='store_true', help='Ejecutar WinPEAS')
    post_parser.add_argument('--enum', action='store_true', help='Enumeración del sistema')
    post_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: WORKFLOW
    # ====================
    workflow_parser = subparsers.add_parser('workflow', help='Ejecutar workflow automatizado')
    workflow_parser.add_argument('-w', '--workflow', required=True, 
                                  choices=['hybrid', 'quick', 'full', 'custom'],
                                  help='Tipo de workflow')
    workflow_parser.add_argument('-t', '--target', required=True, help='IP o dominio objetivo')
    workflow_parser.add_argument('-c', '--config', help='Archivo de workflow personalizado')
    workflow_parser.add_argument('--dry-run', action='store_true', help='Mostrar pasos sin ejecutar')
    workflow_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: REPORT
    # ====================
    report_parser = subparsers.add_parser('report', help='Generar reportes')
    report_parser.add_argument('-t', '--target', required=True, help='IP o dominio objetivo')
    report_parser.add_argument('-o', '--output-format', choices=['html', 'pdf', 'markdown'],
                                default='html', help='Formato del reporte')
    report_parser.add_argument('--template', help='Template personalizado')
    
    # ====================
    # MÓDULO: AUTODETECT
    # ====================
    autodetect_parser = subparsers.add_parser('autodetect', help='Auto-detección inteligente')
    autodetect_parser.add_argument('-t', '--target', required=True, help='IP o dominio objetivo')
    autodetect_parser.add_argument('-s', '--scan-file', help='Archivo JSON con resultados de scan previo')
    autodetect_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: CREDENTIALS
    # ====================
    creds_parser = subparsers.add_parser('credentials', help='Credential harvesting')
    creds_parser.add_argument('-t', '--target', required=True, help='IP o dominio objetivo')
    creds_parser.add_argument('-d', '--directory', help='Directorio para buscar credenciales')
    creds_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: API-INTEL
    # ====================
    api_parser = subparsers.add_parser('api-intel', help='Búsqueda en APIs de seguridad')
    api_parser.add_argument('-t', '--target', required=True, help='IP, dominio o email objetivo')
    api_parser.add_argument('--shodan', action='store_true', help='Consultar Shodan')
    api_parser.add_argument('--virustotal', action='store_true', help='Consultar VirusTotal')
    api_parser.add_argument('--type', choices=['ip', 'domain', 'file'], default='ip', help='Tipo de target para VT')
    api_parser.add_argument('--exploitdb', action='store_true', help='Buscar en ExploitDB')
    api_parser.add_argument('--query', help='Query para ExploitDB')
    api_parser.add_argument('--cve', help='CVE ID para consultar')
    api_parser.add_argument('--hibp', action='store_true', help='HaveIBeenPwned check')
    api_parser.add_argument('--email', help='Email para HIBP')
    api_parser.add_argument('--all', action='store_true', help='Todas las búsquedas disponibles')
    
    # ====================
    # MÓDULO: WIFI
    # ====================
    wifi_parser = subparsers.add_parser('wifi', help='Auditoría de redes WiFi')
    wifi_parser.add_argument('-t', '--target', default='wifi-audit', help='Nombre del audit')
    wifi_parser.add_argument('-i', '--interface', default='wlan0', help='Interfaz inalámbrica')
    wifi_parser.add_argument('--scan', action='store_true', help='Escanear redes WiFi')
    wifi_parser.add_argument('--wpa-crack', action='store_true', help='Capturar y crackear WPA')
    wifi_parser.add_argument('--wps', action='store_true', help='Ataque WPS con Reaver')
    wifi_parser.add_argument('--evil-twin', action='store_true', help='Evil Twin attack')
    wifi_parser.add_argument('--dos', action='store_true', help='Denial of Service')
    wifi_parser.add_argument('--bssid', help='BSSID del AP target')
    wifi_parser.add_argument('-c', '--channel', help='Canal WiFi', type=int)
    wifi_parser.add_argument('--output', help='Archivo de salida')
    wifi_parser.add_argument('--capture-file', help='Archivo .cap para cracke')
    
    # ====================
    # MÓDULO: ACTIVE DIRECTORY
    # ====================
    ad_parser = subparsers.add_parser('ad', help='Pentesting de Active Directory')
    ad_parser.add_argument('-d', '--domain', required=True, help='Dominio objetivo')
    ad_parser.add_argument('--dc-ip', required=True, help='IP del Domain Controller')
    ad_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: AUTO-AUDIT
    # ====================
    autoaudit_parser = subparsers.add_parser('auto-audit', help='Auto-auditoría de seguridad')
    autoaudit_parser.add_argument('-t', '--target', required=True, help='IP o dominio objetivo')
    autoaudit_parser.add_argument('--web', action='store_true', help='Incluir auditoría web')
    autoaudit_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: ADVANCED-REPORT
    # ====================
    advreport_parser = subparsers.add_parser('advanced-report', help='Informe completo de auditoría')
    advreport_parser.add_argument('-t', '--target', required=True, help='IP o dominio objetivo')
    advreport_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: FULL-AUTO
    # ====================
    fullauto_parser = subparsers.add_parser('full-auto', help='Pentesting completamente automatizado')
    fullauto_parser.add_argument('-t', '--target', required=True, help='IP o dominio objetivo')
    fullauto_parser.add_argument('--mode', choices=['comprehensive', 'fast', 'stealth'], default='comprehensive', help='Modo de pentesting')
    fullauto_parser.add_argument('-o', '--output', help='Directorio de salida')
    
    # ====================
    # MÓDULO: CONFIG
    # ====================
    config_parser = subparsers.add_parser('config', help='Configuración de PentOps')
    config_parser.add_argument('--show', action='store_true', help='Mostrar configuración actual')
    config_parser.add_argument('--check', action='store_true', help='Verificar herramientas instaladas')
    config_parser.add_argument('--setup', action='store_true', help='Configuración inicial')
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Mostrar banner (a menos que se especifique lo contrario)
    if not args.no_banner:
        show_banner()
    
    # Si no se especifica módulo, mostrar ayuda
    if not args.module:
        parser.print_help()
        sys.exit(0)
    
    # Configurar verbose
    Config.VERBOSE = args.verbose
    
    # Enrutar a módulos
    try:
        if args.module == 'recon':
            from modules.recon import run_recon
            run_recon(args)
            
        elif args.module == 'enum':
            from modules.enumeration import run_enumeration
            run_enumeration(args)
            
        elif args.module == 'vulnscan':
            from modules.vulnscan import run_vulnscan
            run_vulnscan(args)
            
        elif args.module == 'exploit':
            from modules.exploit import run_exploit
            run_exploit(args)
            
        elif args.module == 'postexploit':
            from modules.postexploit import run_postexploit
            run_postexploit(args)
            
        elif args.module == 'workflow':
            from workflows.engine import run_workflow
            run_workflow(args)
            
        elif args.module == 'report':
            from modules.report import generate_report
            generate_report(args)
        
        elif args.module == 'autodetect':
            from modules.autodetect import run_auto_detect
            run_auto_detect(args.target, args.scan_file)
        
        elif args.module == 'credentials':
            from modules.credentials import run_credential_harvest
            run_credential_harvest(args)
        
        elif args.module == 'api-intel':
            from modules.api_intel import run_api_lookup
            run_api_lookup(args)
        
        elif args.module == 'wifi':
            from modules.wifi import run_wifi_pentest
            run_wifi_pentest(args)
        
        elif args.module == 'ad':
            from modules.active_directory import run_ad_pentest
            run_ad_pentest(args)
        
        elif args.module == 'auto-audit':
            from modules.autoaudit import run_auto_audit
            run_auto_audit(args)
        
        elif args.module == 'advanced-report':
            from modules.advanced_report import run_advanced_report
            run_advanced_report(args)
        
        elif args.module == 'full-auto':
            from modules.automation_engine import run_full_automation
            run_full_automation(args)
            
        elif args.module == 'config':
            from config import show_config, check_tools, setup_config
            if args.show:
                show_config()
            elif args.check:
                check_tools()
            elif args.setup:
                setup_config()
            else:
                config_parser.print_help()
                
    except KeyboardInterrupt:
        print_warning("\n[!] Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print_error(f"[!] Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
