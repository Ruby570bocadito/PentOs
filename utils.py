#!/usr/bin/env python3
"""
Utilidades compartidas para PentOps
"""

import subprocess
import os
import sys
import re
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any
from config import Config

logging.basicConfig(
    level=logging.DEBUG if Config.VERBOSE else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pentops.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('pentops')


# ==========================================
# FUNCIONES DE OUTPUT COLORIZADO
# ==========================================

def print_banner(text: str) -> None:
    """Imprime un banner"""
    print(f"\n{Config.Colors.CYAN}{Config.Colors.BOLD}{'='*60}{Config.Colors.RESET}")
    print(f"\n{Config.Colors.CYAN}{Config.Colors.BOLD}{text}{Config.Colors.RESET}")
    print(f"\n{Config.Colors.CYAN}{Config.Colors.BOLD}{'='*60}{Config.Colors.RESET}\n")


def print_success(text: str) -> None:
    """Imprime mensaje de éxito"""
    print(f"{Config.Colors.GREEN}[+] {text}{Config.Colors.RESET}")


def print_error(text: str) -> None:
    """Imprime mensaje de error"""
    print(f"{Config.Colors.RED}[!] {text}{Config.Colors.RESET}", file=sys.stderr)


def print_warning(text: str) -> None:
    """Imprime mensaje de advertencia"""
    print(f"{Config.Colors.YELLOW}[*] {text}{Config.Colors.RESET}")


def print_info(text: str) -> None:
    """Imprime mensaje informativo"""
    print(f"{Config.Colors.BLUE}[i] {text}{Config.Colors.RESET}")


def print_verbose(text: str) -> None:
    """Imprime solo en modo verbose"""
    if Config.VERBOSE:
        print(f"{Config.Colors.MAGENTA}[v] {text}{Config.Colors.RESET}")


# ==========================================
# ASCII ARTCOLLECTION - Simplified and properly escaped
ASCII_ART_COLLECTION = {
    'scan': [
        "    SCANNING TARGET...\n    [>] Detecting services\n    [>] Identifying versions",
        "    RECONNAISSANCE MODE\n    Gathering intelligence...\n    Mapping attack surface...",
        "    PORT SCAN INITIATED\n    Probing network..."
    ],
    'enum': [
        "    ENUMERATING SERVICES\n    [+] Extracting data\n    [+] Listing resources",
        "    DEEP ENUMERATION\n    Analyzing services...\n    Building attack vectors...",
        "    DATA EXTRACTION\n    Gathering credentials...\n    Mapping shares..."
    ],
    'exploit': [
        "    EXPLOITATION PHASE\n    [!] Launching payload\n    [!] Executing exploit",
        "    EXPLOIT DEPLOYED!\n    Gaining access...\n    Establishing shell...",
        "    ATTACK EXECUTION\n    [*] Payload sent\n    [*] Waiting for callback..."
    ],
    'wifi': [
        "    WiFi ATTACK MODE\n    [~] Monitoring airwaves\n    [~] Capturing handshakes",
        "    WiFi PENETRATION\n    Deauth attack active...\n    Cracking WPA/WPA2...",
        "    WIRELESS AUDIT\n    [!] Evil Twin deployed\n    [!] Harvesting creds"
    ],
    'success': [
        "    SUCCESS!\n    Target compromised!\n    All objectives achieved",
        "    SUCCESS\n    [OK] Exploitation successful\n    [OK] Flags captured\n    [OK] Root access obtained",
        "    VICTORY!\n    100% COMPROMISED\n    System owned!"
    ]
}





def get_random_ascii_art(action_type: Optional[str] = None) -> str:
    """Retorna ASCII art aleatorio de la colección"""
    import random
    
    if action_type and action_type in ASCII_ART_COLLECTION:
        arts = ASCII_ART_COLLECTION[action_type]
    else:
        all_arts = []
        for arts_list in ASCII_ART_COLLECTION.values():
            all_arts.extend(arts_list)
        arts = all_arts
    
    return random.choice(arts) if arts else ""


def display_action_art(action_type: str = 'scan') -> None:
    """Muestra ASCII art con colorización según el tipo"""
    art = get_random_ascii_art(action_type)
    
    # Colorización según tipo
    color_map = {
        'scan': Config.Colors.CYAN,
        'enum': Config.Colors.BLUE,
        'exploit': Config.Colors.RED,
        'wifi': Config.Colors.MAGENTA,
        'success': Config.Colors.GREEN
    }
    
    color = color_map.get(action_type, Config.Colors.CYAN)
    print(f"{color}{art}{Config.Colors.RESET}")


# ==========================================
# PROGRESS BAR
# ==========================================

def print_progress_bar(current: int, total: int, prefix: str = '', suffix: str = '', length: int = 50, fill: str = '█') -> None:
    """Muestra una barra de progreso ASCII"""
    percent = 100 * (current / float(total))
    filled_length = int(length * current // total)
    bar = fill * filled_length + '░' * (length - filled_length)
    
    # Formato con colores
    print(f'\r{Config.Colors.CYAN}{prefix}{Config.Colors.RESET} '
          f'{Config.Colors.GREEN}|{bar}|{Config.Colors.RESET} '
          f'{Config.Colors.YELLOW}{percent:.1f}%{Config.Colors.RESET} '
          f'{Config.Colors.CYAN}{suffix}{Config.Colors.RESET}', end='')
    
    # Nueva línea al completar
    if current == total:
        print()


# ==========================================
# EJECUCIÓN DE COMANDOS
# ==========================================

def run_command(command: str, shell: bool = True, capture_output: bool = True, timeout: Optional[int] = None) -> Tuple[int, str, str]:
    """
    Ejecuta un comando del sistema.
    
    NOTE: shell=True es necesario para herramientas de pentesting (nmap, hydra, etc.)
    que usan argumentos complejos en formato string. Para seguridad adicional,
    los inputs deben ser validados en los módulos que llaman esta función.
    
    Args:
        command: Comando a ejecutar
        shell: Ejecutar en shell (default True para compatibilidad con herramientas de pentesting)
        capture_output: Capturar salida
        timeout: Timeout en segundos
    
    Returns:
        tuple: (exit_code, stdout, stderr)
    """
    print_verbose(f"Ejecutando: {command}")
    logger.debug(f"Executing command: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=capture_output,
            text=True,
            timeout=timeout
        )
        
        return result.returncode, result.stdout, result.stderr
        
    except FileNotFoundError:
        cmd_name = command.split()[0] if shell else command
        print_error(f"Comando no encontrado: {cmd_name}")
        print_info(f"Instala la herramienta o verifica que esté en tu PATH")
        logger.error(f"Command not found: {cmd_name}")
        return -1, "", f"Command not found: {cmd_name}"
    except subprocess.TimeoutExpired:
        print_error(f"Timeout ejecutando: {command}")
        logger.error(f"Command timeout: {command}")
        return -1, "", "Timeout"
    except PermissionError:
        print_error(f"Permiso denegado: {command}")
        logger.error(f"Permission denied: {command}")
        return -1, "", "Permission denied"
    except Exception as e:
        print_error(f"Error ejecutando comando: {str(e)}")
        logger.error(f"Command error: {str(e)}")
        return -1, "", str(e)


def run_command_realtime(command: str) -> int:
    """Ejecuta un comando y muestra la salida en tiempo real"""
    print_verbose(f"Ejecutando (realtime): {command}")
    
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                print(line.rstrip())
        
        return process.returncode
        
    except FileNotFoundError:
        cmd_name = command.split()[0] if ' ' in command else command
        print_error(f"Comando no encontrado: {cmd_name}")
        return -1
    except Exception as e:
        print_error(f"Error ejecutando comando: {str(e)}")
        return -1


# ==========================================
# VALIDACIÓN
# ==========================================

def validate_ip(ip: str) -> bool:
    """Valida una dirección IP"""
    pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if pattern.match(ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False


def validate_domain(domain: str) -> bool:
    """Valida un nombre de dominio"""
    pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    )
    return bool(pattern.match(domain))


def validate_target(target: str) -> bool:
    """Valida que el target sea una IP o dominio válido"""
    return validate_ip(target) or validate_domain(target)


def validate_port(port: Any) -> bool:
    """Valida un número de puerto"""
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except (ValueError, TypeError):
        return False


def validate_port_range(port_range: str) -> bool:
    """Valida un rango de puertos (ej: 1-1000 o 80,443,8080)"""
    # Rango con guión
    if '-' in port_range:
        parts = port_range.split('-')
        if len(parts) == 2:
            return validate_port(parts[0]) and validate_port(parts[1])
    
    # Lista separada por comas
    elif ',' in port_range:
        ports = port_range.split(',')
        return all(validate_port(p.strip()) for p in ports)
    
    # Puerto único
    else:
        return validate_port(port_range)
    
    return False


# ==========================================
# PARSEO DE RESULTADOS
# ==========================================

def parse_nmap_output(output: str) -> List[Dict[str, Any]]:
    """Parsea la salida de nmap y extrae puertos abiertos"""
    ports = []
    
    for line in output.split('\n'):
        match = re.match(r'(\d+)/(tcp|udp)\s+(open|filtered|closed)\s+(\S+)\s*(.*)?', line)
        if match:
            port_info = {
                'port': int(match.group(1)),
                'protocol': match.group(2),
                'state': match.group(3),
                'service': match.group(4),
                'version': match.group(5).strip() if match.group(5) else ''
            }
            ports.append(port_info)
    
    return ports


def detect_service_from_port(port: int) -> str:
    """Detecta el servicio probable basado en el puerto"""
    for service, ports in Config.COMMON_PORTS.items():
        if port in ports:
            return service
    return 'unknown'


# ==========================================
# FILESYST EM Y GUARDADO
# ==========================================

def save_output(target: str, module: str, filename: str, content: str) -> Optional[Path]:
    """Guarda la salida de un módulo"""
    output_dir = Config.get_output_dir(target)
    module_dir = output_dir / module
    module_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = module_dir / filename
    
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        print_success(f"Guardado: {filepath}")
        return filepath
    except Exception as e:
        print_error(f"Error guardando archivo: {str(e)}")
        return None


def save_json(target: str, module: str, filename: str, data: Any) -> Optional[Path]:
    """Guarda datos en formato JSON"""
    content = json.dumps(data, indent=2, ensure_ascii=False)
    return save_output(target, module, filename, content)


def load_json(filepath: str) -> Optional[Any]:
    """Carga datos desde un archivo JSON"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print_error(f"Error cargando JSON: {str(e)}")
        return None


# ==========================================
# WORDLISTS
# ==========================================

def get_wordlist(wordlist_name: str) -> Optional[str]:
    """Obtiene la ruta de una wordlist con fallback"""
    search_paths = []
    
    if wordlist_name in Config.WORDLISTS:
        search_paths.append(Config.WORDLISTS[wordlist_name])
    
    search_paths.extend([
        Config.WORDLISTS_DIR / wordlist_name,
        Config.WORDLISTS_DIR / f"{wordlist_name}.txt",
        Path(f"/usr/share/wordlists/{wordlist_name}"),
        Path(f"/usr/share/wordlists/{wordlist_name}.txt"),
        Path(f"/usr/share/seclists/{wordlist_name}"),
        Path(f"/usr/share/seclists/{wordlist_name}.txt"),
    ])
    
    for path in search_paths:
        if path.exists():
            return str(path)
    
    print_warning(f"Wordlist no encontrada: {wordlist_name}")
    print_info("Puedes descargar wordlists con:")
    print("  sudo apt install wordlists")
    print("  git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists")
    
    return None


def get_timestamp() -> str:
    """Obtiene timestamp actual"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def log_action(target: str, module: str, action: str, details: str = "") -> None:
    """Registra una acción en el log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{module}] {action}"
    if details:
        log_entry += f" - {details}"
    
    output_dir = Config.get_output_dir(target)
    log_file = output_dir / "pentops.log"
    
    try:
        with open(log_file, 'a') as f:
            f.write(log_entry + '\n')
    except Exception:
        pass
    
    if Config.VERBOSE:
        print_verbose(log_entry)


# ==========================================
# FORMATEO DE TABLAS
# ==========================================

def print_table(headers: List[str], rows: List[List[Any]]) -> None:
    """Imprime una tabla formateada"""
    if not rows:
        return
    
    # Calcular anchos de columna
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Imprimir encabezados
    header_row = " | ".join(
        f"{h:<{col_widths[i]}}" for i, h in enumerate(headers)
    )
    print(f"\n{Config.Colors.CYAN}{header_row}{Config.Colors.RESET}")
    print(f"{Config.Colors.CYAN}{'-' * len(header_row)}{Config.Colors.RESET}")
    
    # Imprimir filas
    for row in rows:
        row_str = " | ".join(
            f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row)
        )
        print(row_str)
    
    print()  # Línea en blanco al final
