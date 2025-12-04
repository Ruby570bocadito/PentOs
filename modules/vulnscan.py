#!/usr/bin/env python3
"""
Módulo de Escaneo de Vulnerabilidades
"""

from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    run_command, save_output, validate_target, log_action, get_timestamp
)
from config import Config


def run_nikto(target, port, output_dir):
    """Ejecuta Nikto en un servidor web"""
    if not Config.check_tool('nikto'):
        print_warning("Nikto no está instalado")
        return
    
    protocol = 'https' if port in [443, 8443] else 'http'
    url = f"{protocol}://{target}:{port}"
    
    print_info(f"Ejecutando Nikto en {url}...")
    
    nikto_cmd = f"nikto -h {url} -Format txt -output -"
    exit_code, stdout, stderr = run_command(nikto_cmd, timeout=600)
    
    if exit_code == 0 or stdout:  # Nikto puede devolver exit code != 0 con resultados
        filename = f"nikto_{port}_{get_timestamp()}.txt"
        save_output(target, "vulnscan", filename, stdout)
        print_success("Nikto completado")
        print(stdout)
    else:
        print_error(f"Error ejecutando Nikto: {stderr}")


def run_nmap_vuln_scripts(target, ports, output_dir):
    """Ejecuta scripts de vulnerabilidades de Nmap"""
    if not ports:
        print_warning("No hay puertos para escanear")
        return
    
    port_list = ports
    print_info(f"Ejecutando scripts de vulnerabilidades en puertos: {port_list}...")
    
    nmap_cmd = f"nmap -p{port_list} --script=vuln {target}"
    exit_code, stdout, stderr = run_command(nmap_cmd, timeout=600)
    
    if exit_code == 0:
        filename = f"nmap_vuln_{get_timestamp()}.txt"
        save_output(target, "vulnscan", filename, stdout)
        print_success("Scripts de vulnerabilidades completados")
        print(stdout)
    else:
        print_error(f"Error ejecutando Nmap scripts: {stderr}")


def searchsploit_lookup(target, services_info, output_dir):
    """Busca exploits con searchsploit basado en servicios detectados"""
    if not Config.check_tool('searchsploit'):
        print_warning("Searchsploit no está instalado")
        return
    
    print_info("Buscando exploits con searchsploit...")
    
    # Simular búsqueda por servicios comunes
    # En producción, parsearías la info de servicios del scan previo
    services = services_info.split(',') if services_info else []
    
    all_results = []
    for service in services:
        print_info(f"Buscando exploits para: {service}")
        search_cmd = f"searchsploit {service}"
        exit_code, stdout, stderr = run_command(search_cmd)
        
        if stdout:
            all_results.append(f"\n=== {service} ===\n{stdout}")
    
    if all_results:
        filename = f"searchsploit_{get_timestamp()}.txt"
        save_output(target, "vulnscan", filename, '\n'.join(all_results))
        print_success("Búsqueda de exploits completada")


def run_vulnscan(args):
    """
    Función principal del módulo de vulnerabilidades
    
    Args:
        args: Argumentos parseados de argparse
    """
    print_banner(f"ANÁLISIS DE VULNERABILIDADES: {args.target}")
    
    # Validar target
    if not validate_target(args.target):
        print_error(f"Target inválido: {args.target}")
        return
    
    # Obtener directorio de salida
    if args.output:
        output_dir = args.output
    else:
        output_dir = Config.get_output_dir(args.target)
    
    print_info(f"Resultados se guardarán en: {output_dir}")
    log_action(args.target, "vulnscan", "Iniciando análisis de vulnerabilidades")
    
    # Determinar puertos
    ports = args.ports if args.ports else "80,443,8080"
    
    # Scan web con Nikto
    if args.web:
        for port in ports.split(','):
            run_nikto(args.target, int(port), output_dir)
    
    # Scripts de vulnerabilidades de Nmap
    run_nmap_vuln_scripts(args.target, ports, output_dir)
    
    # Searchsploit
    if args.searchsploit:
        # Aquí deberías obtener info de servicios de scans previos
        services_info = "openssh,apache,mysql"  # Ejemplo
        searchsploit_lookup(args.target, services_info, output_dir)
    
    print_banner("ANÁLISIS DE VULNERABILIDADES COMPLETADO")
    log_action(args.target, "vulnscan", "Análisis completado")
