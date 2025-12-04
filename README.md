# 🛡️ PentOps - Pentesting Operations CLI

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

**PentOps** es una herramienta de línea de comandos profesional para automatizar y orquestar procesos de pentesting. Integra múltiples herramientas de ciberseguridad en un flujo de trabajo unificado y eficiente.

```
    ____             __  ____            
   / __ \___  ____  / /_/ __ \____  _____
  / /_/ / _ \/ __ \/ __/ / / / __ \/ ___/
 / ____/  __/ / / / /_/ /_/ / /_/ (__  ) 
/_/    \___/_/ /_/\__/\____/ .___/____/  
                          /_/            
        ⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        [SKULL ASCII ART]
```

## ✨ Características

- 🎯 **Banner Profesional**: Calavera ASCII estilo Metasploit
- 🔧 **Módulos Especializados**: Recon, Enum, VulnScan, Exploit,PostExploit, Report
- 🧠 **Auto-Detección Inteligente**: Detección de tecnologías, CVEs y sugerencias automáticas
- 🔑 **Credential Harvesting**: Guías completas para extracción de credenciales
- 🌐 **Integración APIs**: Shodan, VirusTotal, ExploitDB, CVE Details, HaveIBeenPwned
- ⚙️ **Motor de Workflows**: Automatización completa con archivos YAML
- 🛠️ **Integración de Herramientas**: Nmap, Metasploit, Hydra, SQLMap, Gobuster, Nikto
- 📊 **Reportes Profesionales**: Generación automática en HTML y Markdown
- 🎨 **Output Colorizado**: Terminal visualmente informativa
- 💡 **Recomendaciones Inteligentes**: Sistema de sugerencias basado en hallazgos

## 📋 Requisitos

### Herramientas Críticas
- `nmap` - Escaneo de puertos
- `gobuster` - Enumeración web
- `hydra` - Brute force

### Herramientas Opcionales
- `nikto` - Escaneo web de vulnerabilidades
- `sqlmap` - SQL Injection
- `enum4linux` - Enumeración SMB
- `feroxbuster` - Enumeración web avanzada
- `searchsploit` - Búsqueda de exploits

### Python 3.8+
```bash
python --version
```

## 🚀 Instalación

### 1. Clonar o Descargar
```bash
cd c:\Users\rafag\Downloads\CLI
```

### 2. Instalar Dependencias Python
```bash
pip install -r requirements.txt
```

### 3. Verificar Herramientas
```bash
python pentops.py config --check
```

### 4. Configuración Inicial
```bash
python pentops.py config --setup
```

## 📖 Uso

### Banner y Ayuda
```bash
python pentops.py --help
```

### Módulo de Reconocimiento
```bash
# Scan rápido
python pentops.py recon -t 192.168.1.100 --quick

# Scan completo
python pentops.py recon -t 192.168.1.100 --full

# Con scripts NSE
python pentops.py recon -t 192.168.1.100 --quick --scripts
```

### Módulo de Enumeración
```bash
# Auto-detección y enumeración
python pentops.py enum -t 192.168.1.100 --auto

# Servicio específico
python pentops.py enum -t 192.168.1.100 -s http
python pentops.py enum -t 192.168.1.100 -s smb

# Puertos específicos
python pentops.py enum -t 192.168.1.100 -p 80,443,445
```

### Módulo de Vulnerabilidades
```bash
# Escaneo web + scripts
python pentops.py vulnscan -t 192.168.1.100 --web

# Buscar exploits
python pentops.py vulnscan -t 192.168.1.100 --searchsploit
```

### Módulo de Explotación
```bash
# Brute force SSH
python pentops.py exploit -t 192.168.1.100 --bruteforce ssh

# SQL Injection
python pentops.py exploit -t 192.168.1.100 --sqli "http://target.com/page.php?id=1"
```

### Módulo de Post-Explotación
```bash
# Guías de enumeración
python pentops.py postexploit -t 192.168.1.100 --enum

# Instrucciones LinPEAS
python pentops.py postexploit -t 192.168.1.100 --linpeas

# Instrucciones WinPEAS
python pentops.py postexploit -t 192.168.1.100 --winpeas
```

### Workflows Automatizados
```bash
# Workflow híbrido completo
python pentops.py workflow -w hybrid -t 192.168.1.100

# Workflow rápido para CTF
python pentops.py workflow -w quick -t 192.168.1.100

# Dry-run (sin ejecutar)
python pentops.py workflow -w hybrid -t 192.168.1.100 --dry-run

# Workflow personalizado
python pentops.py workflow -w custom -t 192.168.1.100 -c mi_workflow.yaml
```

### Generación de Reportes
```bash
# Reporte HTML
python pentops.py report -t 192.168.1.100 -o html

# Reporte Markdown
python pentops.py report -t 192.168.1.100 -o markdown
```

### Auto-Detección Inteligente (NUEVO!)
```bash
# Auto-detección de tecnologías y vulnerabilidades
python pentops.py autodetect -t 192.168.1.100

# Con archivo de scan previo
python pentops.py autodetect -t 192.168.1.100 -s results/scan.json
```

### Credential Harvesting (NUEVO!)
```bash
# Guías de extracción de credenciales
python pentops.py credentials -t 192.168.1.100

# Búsqueda en directorio específico
python pentops.py credentials -t 192.168.1.100 -d /var/www/html
```

### Integración con APIs (NUEVO!)
```bash
# Shodan lookup (requiere API key)
export SHODAN_API_KEY="tu_key"
python pentops.py api-intel -t 192.168.1.100 --shodan

# VirusTotal
export VT_API_KEY="tu_key"
python pentops.py api-intel -t 192.168.1.100 --virustotal

# Búsqueda de CVE
python pentops.py api-intel -t target.com --cve CVE-2021-41773

# HaveIBeenPwned
python pentops.py api-intel -t target.com --hibp --email user@example.com

# Todas las APIs
python pentops.py api-intel -t 192.168.1.100 --all
```

## 📁 Estructura del Proyecto

```
CLI/
├── pentops.py              # Script principal
├── config.py               # Configuración
├── utils.py                # Utilidades
├── requirements.txt        # Dependencias Python
├── README.md               # Documentación principal
├── EXAMPLES.md             # Ejemplos prácticos
├── ADVANCED.md             # Características avanzadas (NUEVO!)
│
├── modules/                # Módulos de pentesting
│   ├── __init__.py
│   ├── recon.py           # Reconocimiento
│   ├── enumeration.py     # Enumeración
│   ├── vulnscan.py        # Análisis de vulnerabilidades
│   ├── exploit.py         # Explotación
│   ├── postexploit.py     # Post-explotación
│   ├── report.py          # Generación de reportes
│   ├── autodetect.py      # Auto-detección inteligente (NUEVO!)
│   ├── credentials.py     # Credential harvesting (NUEVO!)
│   ├── api_intel.py       # Integración APIs (NUEVO!)
│   └── helpers.py         # Helpers avanzados (NUEVO!)
│
├── workflows/              # Motor de workflows
│   ├── __init__.py
│   ├── engine.py          # Motor de ejecución
│   ├── hybrid.yaml        # Workflow híbrido
│   ├── quick.yaml         # Workflow rápido
│   └── advanced.yaml      # Workflow avanzado (NUEVO!)
│
└── results/                # Resultados (auto-generado)
    └── <target>/
        ├── recon/
        ├── enumeration/
        ├── vulnscan/
        ├── exploit/
        ├── postexploit/
        └── pentops.log
```

## 🎯 Workflows Disponibles

### Hybrid - Workflow Híbrido Práctico-Teórico
Workflow completo de 6 fases:
1. Reconocimiento y Descubrimiento
2. Enumeración de Servicios
3. Análisis de Vulnerabilidades
4. Explotación
5. Post-Explotación
6. Documentación y Reporte

### Quick - Workflow Rápido CTF
Workflow optimizado para CTFs:
1. Reconocimiento Rápido
2. Enumeración Automática
3. Vulnerabilidades Comunes
4. Documentación Rápida

### Custom - Workflow Personalizado
Define tus propios workflows en formato YAML.

## 🔧 Crear Workflows Personalizados

Ejemplo de workflow YAML:

```yaml
name: "Mi Workflow Personalizado"
description: "Descripción del workflow"
author: "Tu Nombre"
version: "1.0"

phases:
  - name: "Fase 1"
    description: "Descripción de la fase"
    tasks:
      - name: "Tarea 1"
        module: "recon"
        args: "--quick"
        timeout: 300
        critical: true
      
      - name: "Tarea 2"
        command: "nmap -sV {target}"
        timeout: 180
        critical: false
```

## ⚠️ Advertencia Legal

**USO ÉTICO ÚNICAMENTE**

Esta herramienta debe usarse SOLO en:
- Entornos de laboratorio propios
- Sistemas con autorización explícita por escrito
- Evaluaciones de seguridad legítimas
- CTFs y máquinas de práctica autorizadas

❌ **NO USAR** para:
- Acceder a sistemas sin autorización
- Actividades ilegales
- Pruebas no autorizadas

El autor no se hace responsable del mal uso de esta herramienta.

## 📊 Ejemplo de Flujo Completo

```bash
# 1. Configurar PentOps
python pentops.py config --setup
python pentops.py config --check

# 2. Ejecutar workflow completo
python pentops.py workflow -w hybrid -t 10.10.10.100

# 3. O paso por paso
python pentops.py recon -t 10.10.10.100 --quick
python pentops.py enum -t 10.10.10.100 --auto
python pentops.py vulnscan -t 10.10.10.100 --web
python pentops.py exploit -t 10.10.10.100 --bruteforce ssh
python pentops.py postexploit -t 10.10.10.100 --linpeas

# 4. Generar reporte
python pentops.py report -t 10.10.10.100 -o html
```

## 🤝 Contribuir

Las contribuciones son bienvenidas:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📝 Changelog

### v1.0.0 (2025-12-04)
- ✨ Release inicial
- 🎯 Banner ASCII con calavera
- 🔧 6 módulos principales
- ⚙️ Motor de workflows con YAML
- 📊 Reportes HTML y Markdown

## 👨‍💻 Autor

Desarrollado para automatizar y optimizar procesos de pentesting.

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles

---

**PentOps** - *Automated Pentesting Orchestration Tool*

Para soporte o preguntas, abre un issue en GitHub.
