#!/usr/bin/env python3
"""
Módulo de Reconocimiento
Automatiza escaneos de Nmap
"""

import os
from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    run_command, run_command_realtime, save_output, validate_target,
    parse_nmap_output, log_action, print_table, get_timestamp
)
from config import Config


def run_nmap_quick(target, output_dir):
    """Escaneo rápido de Nmap (top 1000 puertos)"""
    print_info(f"Ejecutando scan rápido en {target}...")
    
    # Comando Nmap
    nmap_cmd = f"nmap -p- --min-rate {Config.NMAP_CONFIG['min_rate']} {target}"
    
    # Ejecutar
    exit_code, stdout, stderr = run_command(nmap_cmd, timeout=300)
    
    if exit_code == 0:
        # Guardar resultado
        filename = f"nmap_quick_{get_timestamp()}.txt"
        save_output(target, "recon", filename, stdout)
        
        # Parsear puertos
        ports = parse_nmap_output(stdout)
        print_success(f"Scan completado. Puertos encontrados: {len(ports)}")
        
        # Mostrar resultados
        if ports:
            display_ports(ports)
        
        return ports
    else:
        print_error(f"Error ejecutando Nmap: {stderr}")
        return []


def run_nmap_full(target, output_dir):
    """Escaneo completo de Nmap (todos los puertos)"""
    print_info(f"Ejecutando scan completo en {target} (puede tardar varios minutos)...")
    
    # Comando Nmap
    nmap_cmd = f"nmap -p{Config.NMAP_CONFIG['full_ports']} --min-rate {Config.NMAP_CONFIG['min_rate']} {target}"
    
    # Ejecutar
    exit_code, stdout, stderr = run_command(nmap_cmd, timeout=600)
    
    if exit_code == 0:
        # Guardar resultado
        filename = f"nmap_full_{get_timestamp()}.txt"
        save_output(target, "recon", filename, stdout)
        
        # Parsear puertos
        ports = parse_nmap_output(stdout)
        print_success(f"Scan completado. Puertos encontrados: {len(ports)}")
        
        # Mostrar resultados
        if ports:
            display_ports(ports)
        
        return ports
    else:
        print_error(f"Error ejecutando Nmap: {stderr}")
        return []


def run_nmap_service_version(target, ports, output_dir):
    """Escaneo de versiones y servicios en puertos específicos"""
    if not ports:
        print_warning("No hay puertos para escanear")
        return
    
    # Crear lista de puertos
    port_list = ','.join([str(p['port']) for p in ports if p['state'] == 'open'])
    
    if not port_list:
        print_warning("No hay puertos abiertos para escanear")
        return
    
    print_info(f"Detectando versiones en puertos: {port_list}...")
    
    # Comando Nmap
    nmap_cmd = f"nmap -sCV -p{port_list} {target}"
    
    # Ejecutar
    exit_code, stdout, stderr = run_command(nmap_cmd, timeout=300)
    
    if exit_code == 0:
        # Guardar resultado
        filename = f"nmap_services_{get_timestamp()}.txt"
        save_output(target, "recon", filename, stdout)
        print_success("Escaneo de servicios completado")
        
        # Mostrar output
        print(stdout)
    else:
        print_error(f"Error ejecutando Nmap: {stderr}")


def run_nmap_scripts(target, ports, output_dir):
    """Ejecuta scripts NSE de Nmap"""
    if not ports:
        print_warning("No hay puertos para escanear con scripts")
        return
    
    port_list = ','.join([str(p['port']) for p in ports if p['state'] == 'open'])
    
    if not port_list:
        return
    
    print_info(f"Ejecutando scripts NSE en puertos: {port_list}...")
    
    # Comando Nmap
    nmap_cmd = f"nmap -p{port_list} --script=default,vuln {target}"
    
    # Ejecutar
    exit_code, stdout, stderr = run_command(nmap_cmd, timeout=600)
    
    if exit_code == 0:
        # Guardar resultado
        filename = f"nmap_scripts_{get_timestamp()}.txt"
        save_output(target, "recon", filename, stdout)
        print_success("Scripts NSE completados")
        
        # Mostrar output
        print(stdout)
    else:
        print_error(f"Error ejecutando Nmap scripts: {stderr}")


def run_nmap_udp(target, output_dir):
    """Escaneo UDP de puertos comunes"""
    print_info(f"Ejecutando scan UDP en {target} (puede tardar)...")
    
    # Top UDP ports
    udp_ports = "53,67,68,69,123,135,137,138,139,161,162,445,500,514,520,631,1434,1900,4500,49152"
    
    # Comando Nmap (requiere root/admin)
    nmap_cmd = f"nmap -sU -p{udp_ports} {target}"
    
    # Ejecutar
    exit_code, stdout, stderr = run_command(nmap_cmd, timeout=300)
    
    if exit_code == 0:
        # Guardar resultado
        filename = f"nmap_udp_{get_timestamp()}.txt"
        save_output(target, "recon", filename, stdout)
        print_success("Scan UDP completado")
        
        # Parsear y mostrar
        ports = parse_nmap_output(stdout)
        if ports:
            display_ports(ports)
    else:
        print_warning("Scan UDP requiere privilegios de administrador")
        print_error(f"Error: {stderr}")


def display_ports(ports):
    """Muestra los puertos en formato de tabla"""
    if not ports:
        return
    
    headers = ["Puerto", "Protocolo", "Estado", "Servicio", "Versión"]
    rows = [
        [p['port'], p['protocol'], p['state'], p['service'], p['version']]
        for p in ports
    ]
    
    print_table(headers, rows)


def run_recon(args):
    """
    Función principal del módulo de reconocimiento
    
    Args:
        args: Argumentos parseados de argparse
    """
    print_banner(f"RECONOCIMIENTO: {args.target}")
    
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
    
    # Log
    log_action(args.target, "recon", "Iniciando reconocimiento")
    
    # Ejecutar scans según opciones
    ports = []
    
    if args.quick:
        ports = run_nmap_quick(args.target, output_dir)
    elif args.full:
        ports = run_nmap_full(args.target, output_dir)
    else:
        # Por defecto, scan rápido
        ports = run_nmap_quick(args.target, output_dir)
    
    # Escaneo de versiones si encontramos puertos
    if ports:
        run_nmap_service_version(args.target, ports, output_dir)
        
        # Scripts si se solicita
        if args.scripts:
            run_nmap_scripts(args.target, ports, output_dir)
    
    # Scan UDP si se solicita
    if args.udp:
        run_nmap_udp(args.target, output_dir)
    
    # Resumen final
    print_banner("RECONOCIMIENTO COMPLETADO")
    if ports:
        print_success(f"Total de puertos abiertos encontrados: {len([p for p in ports if p['state'] == 'open'])}")
        print_info(f"Revisa los resultados en: {output_dir}")
    else:
        print_warning("No se encontraron puertos abiertos")
    
    log_action(args.target, "recon", "Reconocimiento completado", f"{len(ports)} puertos")
