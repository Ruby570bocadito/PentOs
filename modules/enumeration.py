#!/usr/bin/env python3
"""
Módulo de Enumeración
Enumeración de servicios específicos
"""

from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    run_command, run_command_realtime, save_output, validate_target,
    log_action, get_timestamp, get_wordlist, detect_service_from_port
)
from config import Config


def enumerate_http(target, port, output_dir):
    """Enumeración de servicios HTTP/HTTPS"""
    print_info(f"Enumerando HTTP en puerto {port}...")
    
    protocol = 'https' if port == 443 or port == 8443 else 'http'
    url = f"{protocol}://{target}:{port}"
    
    # Gobuster
    wordlist = get_wordlist('web_common')
    if wordlist and Config.check_tool('gobuster'):
        print_info("Ejecutando Gobuster...")
        gobuster_cmd = (
            f"gobuster dir -u {url} -w {wordlist} "
            f"-t {Config.GOBUSTER_CONFIG['threads']} "
            f"-x {Config.GOBUSTER_CONFIG['extensions']} "
            f"--timeout {Config.GOBUSTER_CONFIG['timeout']} "
            f"--no-error"
        )
        
        exit_code, stdout, stderr = run_command(gobuster_cmd, timeout=600)
        if exit_code == 0:
            filename = f"gobuster_{port}_{get_timestamp()}.txt"
            save_output(target, "enumeration/http", filename, stdout)
            print_success("Gobuster completado")
            print(stdout)
    
    # Nikto (si está disponible)
    if Config.check_tool('nikto'):
        print_info("Ejecutando Nikto...")
        nikto_cmd = f"nikto -h {url}"
        exit_code, stdout, stderr = run_command(nikto_cmd, timeout=300)
        if exit_code == 0:
            filename = f"nikto_{port}_{get_timestamp()}.txt"
            save_output(target, "enumeration/http", filename, stdout)
            print_success("Nikto completado")
    
    # Curl para headers
    if Config.check_tool('curl'):
        print_info("Obteniendo headers HTTP...")
        curl_cmd = f"curl -I {url}"
        exit_code, stdout, stderr = run_command(curl_cmd)
        if exit_code == 0:
            filename = f"http_headers_{port}_{get_timestamp()}.txt"
            save_output(target, "enumeration/http", filename, stdout)
            print(stdout)


def enumerate_smb(target, output_dir):
    """Enumeración de SMB"""
    print_info("Enumerando SMB...")
    
    # enum4linux
    if Config.check_tool('enum4linux'):
        print_info("Ejecutando enum4linux...")
        enum4_cmd = f"enum4linux -a {target}"
        exit_code, stdout, stderr = run_command(enum4_cmd, timeout=300)
        if exit_code == 0:
            filename = f"enum4linux_{get_timestamp()}.txt"
            save_output(target, "enumeration/smb", filename, stdout)
            print_success("enum4linux completado")
            print(stdout)
    
    # smbclient - listar shares
    if Config.check_tool('smbclient'):
        print_info("Listando recursos compartidos SMB...")
        smb_cmd = f"smbclient -L //{target} -N"
        exit_code, stdout, stderr = run_command(smb_cmd)
        if exit_code == 0:
            filename = f"smbclient_shares_{get_timestamp()}.txt"
            save_output(target, "enumeration/smb", filename, stdout)
            print(stdout)
    
    # Nmap SMB scripts
    print_info("Ejecutando scripts SMB de Nmap...")
    nmap_cmd = f"nmap -p445 --script=smb-enum-*,smb-vuln-* {target}"
    exit_code, stdout, stderr = run_command(nmap_cmd, timeout=300)
    if exit_code == 0:
        filename = f"nmap_smb_scripts_{get_timestamp()}.txt"
        save_output(target, "enumeration/smb", filename, stdout)
        print_success("Scripts SMB completados")


def enumerate_ftp(target, port, output_dir):
    """Enumeración de FTP"""
    print_info(f"Enumerando FTP en puerto {port}...")
    
    # Nmap FTP scripts
    nmap_cmd = f"nmap -p{port} --script=ftp-* {target}"
    exit_code, stdout, stderr = run_command(nmap_cmd, timeout=180)
    if exit_code == 0:
        filename = f"nmap_ftp_{port}_{get_timestamp()}.txt"
        save_output(target, "enumeration/ftp", filename, stdout)
        print_success("Enumeración FTP completada")
        print(stdout)
    
    # Intentar conexión anónima
    print_info("Probando acceso FTP anónimo...")
    # Note: En Windows, el comando ftp puede variar
    ftp_cmd = f'echo "user anonymous\npass anonymous\nls\nquit" | ftp {target} {port}'
    exit_code, stdout, stderr = run_command(ftp_cmd)
    if stdout:
        print(stdout)


def enumerate_ssh(target, port, output_dir):
    """Enumeración de SSH"""
    print_info(f"Enumerando SSH en puerto {port}...")
    
    # Nmap SSH scripts
    nmap_cmd = f"nmap -p{port} --script=ssh-* {target}"
    exit_code, stdout, stderr = run_command(nmap_cmd, timeout=180)
    if exit_code == 0:
        filename = f"nmap_ssh_{port}_{get_timestamp()}.txt"
        save_output(target, "enumeration/ssh", filename, stdout)
        print_success("Enumeración SSH completada")
        print(stdout)


def enumerate_smtp(target, port, output_dir):
    """Enumeración de SMTP"""
    print_info(f"Enumerando SMTP en puerto {port}...")
    
    # Nmap SMTP scripts
    nmap_cmd = f"nmap -p{port} --script=smtp-* {target}"
    exit_code, stdout, stderr = run_command(nmap_cmd, timeout=180)
    if exit_code == 0:
        filename = f"nmap_smtp_{port}_{get_timestamp()}.txt"
        save_output(target, "enumeration/smtp", filename, stdout)
        print_success("Enumeración SMTP completada")
        print(stdout)


def enumerate_mysql(target, port, output_dir):
    """Enumeración de MySQL"""
    print_info(f"Enumerando MySQL en puerto {port}...")
    
    # Nmap MySQL scripts
    nmap_cmd = f"nmap -p{port} --script=mysql-* {target}"
    exit_code, stdout, stderr = run_command(nmap_cmd, timeout=180)
    if exit_code == 0:
        filename = f"nmap_mysql_{port}_{get_timestamp()}.txt"
        save_output(target, "enumeration/mysql", filename, stdout)
        print_success("Enumeración MySQL completada")
        print(stdout)


def auto_enumerate(target, output_dir):
    """Auto-detecta servicios y enumera automáticamente"""
    print_info("Auto-detectando servicios...")
    
    # Primero hacer un scan rápido para detectar puertos
    from modules.recon import run_nmap_quick
    ports = run_nmap_quick(target, output_dir)
    
    if not ports:
        print_warning("No se detectaron puertos abiertos")
        return
    
    # Enumerar cada servicio detectado
    for port_info in ports:
        if port_info['state'] != 'open':
            continue
        
        port = port_info['port']
        service = port_info['service'].lower() if port_info['service'] else detect_service_from_port(port)
        
        print_info(f"\nEnumerando servicio detectado: {service} en puerto {port}")
        
        # Enumeraciones específicas
        if 'http' in service or port in [80, 443, 8080, 8443, 8000, 3000, 5000]:
            enumerate_http(target, port, output_dir)
        elif 'smb' in service or port in [139, 445]:
            enumerate_smb(target, output_dir)
        elif 'ftp' in service or port == 21:
            enumerate_ftp(target, port, output_dir)
        elif 'ssh' in service or port == 22:
            enumerate_ssh(target, port, output_dir)
        elif 'smtp' in service or port in [25, 587]:
            enumerate_smtp(target, port, output_dir)
        elif 'mysql' in service or port == 3306:
            enumerate_mysql(target, port, output_dir)
        else:
            print_warning(f"No hay enumeración específica para: {service}")


def run_enumeration(args):
    """
    Función principal del módulo de enumeración
    
    Args:
        args: Argumentos parseados de argparse
    """
    print_banner(f"ENUMERACIÓN: {args.target}")
    
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
    log_action(args.target, "enumeration", "Iniciando enumeración")
    
    # Modo auto
    if args.auto:
        auto_enumerate(args.target, output_dir)
    
    # Servicio específico
    elif args.service:
        service = args.service.lower()
        port = None
        
        if args.ports:
            port = int(args.ports.split(',')[0])
        
        if service == 'http' or service == 'https':
            port = port or 80
            enumerate_http(args.target, port, output_dir)
        elif service == 'smb':
            enumerate_smb(args.target, output_dir)
        elif service == 'ftp':
            port = port or 21
            enumerate_ftp(args.target, port, output_dir)
        elif service == 'ssh':
            port = port or 22
            enumerate_ssh(args.target, port, output_dir)
        elif service == 'smtp':
            port = port or 25
            enumerate_smtp(args.target, port, output_dir)
        elif service == 'mysql':
            port = port or 3306
            enumerate_mysql(args.target, port, output_dir)
        else:
            print_error(f"Servicio no soportado: {service}")
    
    # Puertos específicos
    elif args.ports:
        ports_list = [int(p.strip()) for p in args.ports.split(',')]
        for port in ports_list:
            service = detect_service_from_port(port)
            print_info(f"\nEnumerando puerto {port} (servicio probable: {service})")
            
            if port in [80, 443, 8080, 8443, 8000, 3000, 5000]:
                enumerate_http(args.target, port, output_dir)
            elif port in [139, 445]:
                enumerate_smb(args.target, output_dir)
            elif port == 21:
                enumerate_ftp(args.target, port, output_dir)
            elif port == 22:
                enumerate_ssh(args.target, port, output_dir)
    
    else:
        print_warning("Especifica --auto, -s/--service, o -p/--ports")
        print_info("Ejemplo: pentops.py enum -t 192.168.1.100 --auto")
    
    print_banner("ENUMERACIÓN COMPLETADA")
    log_action(args.target, "enumeration", "Enumeración completada")
