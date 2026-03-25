#!/usr/bin/env python3
"""
Configuración centralizada de PentOps
"""

import os
import shutil
import json
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Configuración global de PentOps"""
    
    # Versión
    VERSION = "1.0.0"
    
    # Directorios
    BASE_DIR = Path(__file__).parent
    RESULTS_DIR = BASE_DIR / "results"
    WORKFLOWS_DIR = BASE_DIR / "workflows"
    WORDLISTS_DIR = BASE_DIR / "wordlists"
    
    # Configuración de comportamiento
    VERBOSE = False
    AUTO_SAVE = True
    
    # Colores ANSI
    class Colors:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    
    # Herramientas de pentesting (nombres, rutas se detectan automáticamente)
    TOOLS = [
        'nmap', 'gobuster', 'nikto', 'hydra', 'sqlmap', 'msfconsole',
        'searchsploit', 'enum4linux', 'smbclient', 'ftp', 'ssh', 'curl',
        'wget', 'nc', 'feroxbuster', 'ffuf', 'netcat', 'impacket',
        'responder', 'ldapsearch', 'bloodhound', 'rustscan', 'naabu',
    ]
    
    # Wordlists comunes (actualizar según tu sistema)
    WORDLISTS = {
        # Directorios web
        'web_common': '/usr/share/wordlists/dirb/common.txt',
        'web_big': '/usr/share/wordlists/dirb/big.txt',
        'web_dirbuster_medium': '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
        'web_seclists_common': '/usr/share/seclists/Discovery/Web-Content/common.txt',
        'web_seclists_raft': '/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt',
        
        # Usuarios
        'users_common': '/usr/share/seclists/Usernames/top-usernames-shortlist.txt',
        'users_names': '/usr/share/seclists/Usernames/Names/names.txt',
        
        # Contraseñas
        'pass_rockyou': '/usr/share/wordlists/rockyou.txt',
        'pass_common': '/usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-1000.txt',
        'pass_darkweb': '/usr/share/seclists/Passwords/darkweb2017-top10000.txt',
        
        # Fuzzing
        'fuzz_all': '/usr/share/seclists/Fuzzing/fuzz-Bo0oM.txt',
    }
    
    # Configuración de Nmap
    NMAP_CONFIG = {
        'quick_ports': '1-1000',
        'full_ports': '1-65535',
        'timing': 'T4',
        'min_rate': '5000',
        'scripts_dir': '/usr/share/nmap/scripts/',
    }
    
    # Configuración de Gobuster
    GOBUSTER_CONFIG = {
        'threads': 50,
        'timeout': '10s',
        'extensions': 'php,html,txt,js,zip,bak',
    }
    
    # Configuración de Hydra
    HYDRA_CONFIG = {
        'threads': 16,
        'timeout': 30,
    }
    
    # Puertos comunes por servicio
    COMMON_PORTS = {
        'http': [80, 8080, 8000, 8888, 3000, 5000],
        'https': [443, 8443],
        'ftp': [21],
        'ssh': [22],
        'telnet': [23],
        'smtp': [25, 587],
        'dns': [53],
        'pop3': [110, 995],
        'imap': [143, 993],
        'smb': [139, 445],
        'mysql': [3306],
        'rdp': [3389],
        'postgresql': [5432],
        'vnc': [5900],
        'nfs': [2049],
    }
    
    @classmethod
    def get_output_dir(cls, target: str) -> Path:
        """Obtiene el directorio de salida para un objetivo"""
        target_clean = target.replace('/', '_').replace(':', '_')
        output_dir = cls.RESULTS_DIR / target_clean
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    @classmethod
    def check_tool(cls, tool_name: str) -> bool:
        """Verifica si una herramienta está instalada"""
        return shutil.which(tool_name) is not None
    
    @classmethod
    def get_tool_path(cls, tool_name: str) -> Optional[str]:
        """Obtiene la ruta de una herramienta"""
        return shutil.which(tool_name)


def show_config() -> None:
    """Muestra la configuración actual"""
    from utils import print_info, print_success, print_error
    
    print_info("=== Configuración de PentOps ===\n")
    
    print_info(f"Directorio base: {Config.BASE_DIR}")
    print_info(f"Directorio de resultados: {Config.RESULTS_DIR}")
    print_info(f"Directorio de workflows: {Config.WORKFLOWS_DIR}")
    print_info(f"Directorio de wordlists: {Config.WORDLISTS_DIR}\n")
    
    print_info("=== Herramientas Instaladas ===")
    for tool in Config.TOOLS:
        if Config.check_tool(tool):
            print_success(f"✓ {tool}: {Config.get_tool_path(tool)}")
        else:
            print_error(f"✗ {tool}: No encontrado")


def check_tools() -> bool:
    """Verifica que las herramientas necesarias estén instaladas"""
    from utils import print_info, print_success, print_error, print_warning
    
    print_info("\n=== Verificando herramientas de pentesting ===\n")
    
    critical_tools = ['nmap', 'gobuster', 'hydra']
    optional_tools = ['nikto', 'sqlmap', 'enum4linux', 'feroxbuster', 'ffuf']
    
    all_ok = True
    
    print_info("Herramientas críticas:")
    for tool in critical_tools:
        if Config.check_tool(tool):
            print_success(f"  ✓ {tool}")
        else:
            print_error(f"  ✗ {tool} - NO ENCONTRADO")
            all_ok = False
    
    print_info("\nHerramientas opcionales:")
    for tool in optional_tools:
        if Config.check_tool(tool):
            print_success(f"  ✓ {tool}")
        else:
            print_warning(f"  ! {tool} - No encontrado (opcional)")
    
    if all_ok:
        print_success("\n✓ Todas las herramientas críticas están instaladas")
    else:
        print_error("\n✗ Faltan herramientas críticas. Instálalas antes de usar PentOps")
    
    return all_ok


def setup_config() -> None:
    """Configuración inicial de PentOps"""
    from utils import print_info, print_success
    
    print_info("\n=== Configuración inicial de PentOps ===\n")
    
    # Crear directorios necesarios
    Config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print_success(f"✓ Creado directorio de resultados: {Config.RESULTS_DIR}")
    
    Config.WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
    print_success(f"✓ Creado directorio de workflows: {Config.WORKFLOWS_DIR}")
    
    Config.WORDLISTS_DIR.mkdir(parents=True, exist_ok=True)
    print_success(f"✓ Creado directorio de wordlists: {Config.WORDLISTS_DIR}")
    
    # Verificar herramientas
    print_info("\nVerificando herramientas...")
    check_tools()
    
    print_success("\n✓ Configuración completada!")
