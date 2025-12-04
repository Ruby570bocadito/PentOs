#!/usr/bin/env python3
"""
Módulo de Integración con APIs Externas
Integra Shodan, VirusTotal, ExploitDB, etc.
"""

import os
import json
import requests
from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    save_output, save_json, log_action, get_timestamp, print_table
)
from config import Config


class APIIntegrator:
    """Integrador de APIs de seguridad"""
    
    def __init__(self):
        self.shodan_key = os.getenv('SHODAN_API_KEY', '')
        self.vt_key = os.getenv('VT_API_KEY', '')
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'PentOps/1.0'})
    
    def shodan_lookup(self, ip):
        """Consulta información de IP en Shodan"""
        if not self.shodan_key:
            print_warning("Shodan API key no configurada. Exporta: export SHODAN_API_KEY=tu_key")
            return None
        
        print_info(f"Consultando Shodan para {ip}...")
        
        try:
            url = f"https://api.shodan.io/shodan/host/{ip}?key={self.shodan_key}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                print_success(f"\n✓ Información de Shodan para {ip}")
                print_info(f"  País: {data.get('country_name', 'N/A')}")
                print_info(f"  Ciudad: {data.get('city', 'N/A')}")
                print_info(f"  ISP: {data.get('isp', 'N/A')}")
                print_info(f"  Organización: {data.get('org', 'N/A')}")
                
                # Puertos abiertos
                if 'ports' in data:
                    print_info(f"\n  Puertos abiertos: {', '.join(map(str, data['ports']))}")
                
                # Vulnerabilidades
                if 'vulns' in data and data['vulns']:
                    print_warning(f"\n  ⚠️  Vulnerabilidades detectadas:")
                    for vuln in list(data['vulns'])[:5]:
                        print_warning(f"    • {vuln}")
                
                # Servicios
                if 'data' in data:
                    print_info(f"\n  Servicios detectados:")
                    for service in data['data'][:5]:
                        port = service.get('port', 'N/A')
                        product = service.get('product', '')
                        version = service.get('version', '')
                        print_info(f"    • Puerto {port}: {product} {version}".strip())
                
                return data
            
            elif response.status_code == 404:
                print_warning(f"IP {ip} no encontrada en Shodan")
            elif response.status_code == 401:
                print_error("API key de Shodan inválida")
            else:
                print_error(f"Error en Shodan API: {response.status_code}")
                
        except Exception as e:
            print_error(f"Error consultando Shodan: {str(e)}")
        
        return None
    
    def virustotal_lookup(self, target, target_type='ip'):
        """
        Consulta VirusTotal
        
        Args:
            target: IP, dominio o hash
            target_type: 'ip', 'domain', o 'file'
        """
        if not self.vt_key:
            print_warning("VirusTotal API key no configurada. Exporta: export VT_API_KEY=tu_key")
            return None
        
        print_info(f"Consultando VirusTotal para {target}...")
        
        try:
            headers = {'x-apikey': self.vt_key}
            
            if target_type == 'ip':
                url = f"https://www.virustotal.com/api/v3/ip_addresses/{target}"
            elif target_type == 'domain':
                url = f"https://www.virustotal.com/api/v3/domains/{target}"
            else:
                url = f"https://www.virustotal.com/api/v3/files/{target}"
            
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                attributes = data.get('data', {}).get('attributes', {})
                
                print_success(f"\n✓ Información de VirusTotal para {target}")
                
                # Estadísticas de detección
                if 'last_analysis_stats' in attributes:
                    stats = attributes['last_analysis_stats']
                    malicious = stats.get('malicious', 0)
                    suspicious = stats.get('suspicious', 0)
                    clean = stats.get('harmless', 0)
                    
                    if malicious > 0:
                        print_error(f"  ⚠️  Detectado como MALICIOSO por {malicious} motores")
                    elif suspicious > 0:
                        print_warning(f"  ⚠️  Detectado como SOSPECHOSO por {suspicious} motores")
                    else:
                        print_success(f"  ✓ Limpio según {clean} motores")
                
                # Reputación
                if 'reputation' in attributes:
                    rep = attributes['reputation']
                    if rep < 0:
                        print_error(f"  Reputación: {rep} (NEGATIVA)")
                    else:
                        print_success(f"  Reputación: {rep}")
                
                return data
            
            elif response.status_code == 404:
                print_warning(f"{target} no encontrado en VirusTotal")
            elif response.status_code == 401:
                print_error("API key de VirusTotal inválida")
            else:
                print_error(f"Error en VirusTotal API: {response.status_code}")
                
        except Exception as e:
            print_error(f"Error consultando VirusTotal: {str(e)}")
        
        return None
    
    def exploitdb_search(self, query):
        """Busca exploits en ExploitDB"""
        print_info(f"Buscando '{query}' en ExploitDB...")
        
        try:
            # Usar searchsploit si está disponible
            if Config.check_tool('searchsploit'):
                from utils import run_command
                exit_code, stdout, stderr = run_command(f"searchsploit {query}")
                
                if stdout:
                    print_success("\n✓ Exploits encontrados:")
                    print(stdout)
                    return stdout
                else:
                    print_warning("No se encontraron exploits")
            else:
                # API de ExploitDB (si existe)
                print_warning("searchsploit no disponible. Instala exploitdb")
                print_info("  sudo apt install exploitdb")
                
        except Exception as e:
            print_error(f"Error buscando en ExploitDB: {str(e)}")
        
        return None
    
    def cvedetails_lookup(self, cve_id):
        """Obtiene detalles de un CVE"""
        print_info(f"Buscando información de {cve_id}...")
        
        try:
            # API pública de NVD
            url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('resultsPerPage', 0) > 0:
                    cve = data['vulnerabilities'][0]['cve']
                    
                    print_success(f"\n✓ Detalles de {cve_id}")
                    print_info(f"  Publicado: {cve.get('published', 'N/A')}")
                    
                    # Descripción
                    desc = cve.get('descriptions', [{}])[0].get('value', 'N/A')
                    print_info(f"\n  Descripción: {desc[:200]}...")
                    
                    # CVSS Score
                    metrics = cve.get('metrics', {})
                    if 'cvssMetricV31' in metrics:
                        cvss = metrics['cvssMetricV31'][0]['cvssData']
                        score = cvss.get('baseScore', 'N/A')
                        severity = cvss.get('baseSeverity', 'N/A')
                        
                        color_func = print_error if float(score) >= 7 else print_warning
                        color_func(f"\n  CVSS Score: {score} ({severity})")
                    
                    return data
                else:
                    print_warning(f"CVE {cve_id} no encontrado")
                    
        except Exception as e:
            print_error(f"Error consultando CVE: {str(e)}")
        
        return None
    
    def haveibeenpwned_check(self, email):
        """Verifica si un email ha sido comprometido"""
        print_info(f"Verificando {email} en HaveIBeenPwned...")
        
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {'User-Agent': 'PentOps-Security-Tool'}
            
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                breaches = response.json()
                
                print_error(f"\n⚠️  {email} encontrado en {len(breaches)} brechas:")
                for breach in breaches[:5]:
                    name = breach.get('Name', 'N/A')
                    date = breach.get('BreachDate', 'N/A')
                    print_error(f"  • {name} ({date})")
                
                return breaches
            
            elif response.status_code == 404:
                print_success(f"✓ {email} NO encontrado en brechas conocidas")
            elif response.status_code == 429:
                print_warning("Rate limit alcanzado. Intenta más tarde")
            else:
                print_warning(f"Respuesta inesperada: {response.status_code}")
                
        except Exception as e:
            print_error(f"Error consultando HaveIBeenPwned: {str(e)}")
        
        return None


def run_api_lookup(args):
    """
    Función principal del módulo de APIs
    
    Args:
        args: Argumentos parseados
    """
    print_banner("BÚSQUEDA EN APIs DE SEGURIDAD")
    
    integrator = APIIntegrator()
    results = {}
    
    # Shodan
    if args.shodan or args.all:
        shodan_data = integrator.shodan_lookup(args.target)
        if shodan_data:
            results['shodan'] = shodan_data
    
    # VirusTotal
    if args.virustotal or args.all:
        vt_data = integrator.virustotal_lookup(args.target, args.type)
        if vt_data:
            results['virustotal'] = vt_data
    
    # ExploitDB
    if args.exploitdb:
        exploit_data = integrator.exploitdb_search(args.query)
        if exploit_data:
            results['exploitdb'] = exploit_data
    
    # CVE Details
    if args.cve:
        cve_data = integrator.cvedetails_lookup(args.cve)
        if cve_data:
            results['cve'] = cve_data
    
    # HaveIBeenPwned
    if args.hibp:
        hibp_data = integrator.haveibeenpwned_check(args.email)
        if hibp_data:
            results['haveibeenpwned'] = hibp_data
    
    # Guardar resultados
    if results:
        output_dir = Config.get_output_dir(args.target)
        save_json(args.target, "api-intel", f"api_results_{get_timestamp()}.json", results)
        print_success(f"\n✓ Resultados guardados en {output_dir}")
    
    print_banner("BÚSQUEDA COMPLETADA")
