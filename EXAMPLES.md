# 💡 Ejemplos de Uso de PentOps

## Ejemplo 1: Pentesting de Máquina CTF

```bash
# Objetivo: Máquina CTF 10.10.10.100

# Paso 1: Reconocimiento rápido
python pentops.py recon -t 10.10.10.100 --quick

# Paso 2: Enumeración automática
python pentops.py enum -t 10.10.10.100 --auto

# Paso 3: Análisis de vulnerabilidades web
python pentops.py vulnscan -t 10.10.10.100 --web -p 80

# Paso 4: Intentar brute force SSH (si aplica)
python pentops.py exploit -t 10.10.10.100 --bruteforce ssh

# Paso 5: Generar reporte
python pentops.py report -t 10.10.10.100 -o html
```

## Ejemplo 2: Workflow Automatizado

```bash
# Ejecutar workflow híbrido completo
python pentops.py workflow -w hybrid -t 192.168.1.50

# Primero en modo dry-run para ver qué hará
python pentops.py workflow -w hybrid -t 192.168.1.50 --dry-run

# Workflow rápido para CTF
python pentops.py workflow -w quick -t 10.10.10.100
```

## Ejemplo 3: Enumeración Web Detallada

```bash
# Target con servidor web en múltiples puertos
TARGET="example.com"

# Reconocimiento
python pentops.py recon -t $TARGET --quick

# Enumeración web en puerto 80
python pentops.py enum -t $TARGET -s http -p 80

# Enumeración web en puerto 8080
python pentops.py enum -t $TARGET -s http -p 8080

# Análisis de vulnerabilidades
python pentops.py vulnscan -t $TARGET --web -p 80,8080

# Reporte HTML
python pentops.py report -t $TARGET -o html
```

## Ejemplo 4: Enumeración SMB y Active Directory

```bash
# Target: Controlador de dominio
DC="192.168.1.10"

#  Reconocimiento
python pentops.py recon -t $DC --quick

# Enumeración SMB
python pentops.py enum -t $DC -s smb

# Vulnerabilidades SMB
python pentops.py vulnscan -t $DC -p 445

# Brute force SMB (con wordlists personalizadas)
python pentops.py exploit -t $DC --bruteforce smb \
  -u /path/to/users.txt \
  -p /path/to/passwords.txt
```

## Ejemplo 5: Workflow Personalizado

Crear archivo `mi_workflow.yaml`:

```yaml
name: "Pentesting Web Completo"
description: "Workflow especializado para aplicaciones web"
author: "Mi Equipo"
version: "1.0"

phases:
  - name: "Reconocimiento Web"
    tasks:
      - name: "Scan de puertos web"
        module: "recon"
        args: "--quick"
        timeout: 180
  
  - name: "Enumeración Web Profunda"
    tasks:
      - name: "Gobuster en puerto 80"
        module: "enum"
        args: "-s http -p 80"
        timeout: 600
      
      - name: "Nikto"
        module: "vulnscan"
        args: "--web -p 80"
        timeout: 300
  
  - name: "Reportes"
    tasks:
      - name: "Generar reporte"
        module: "report"
        args: "-o html"
        timeout: 60
```

Ejecutar:
```bash
python pentops.py workflow -w custom -t target.com -c mi_workflow.yaml
```

## Ejemplo 6: Docker Labs / Try Hack Me

```bash
# Máquina de DockerLabs
MACHINE_IP="172.17.0.2"

# Workflow rápido completo
python pentops.py workflow -w quick -t $MACHINE_IP

# O paso por paso:
# 1. Scan
python pentops.py recon -t $MACHINE_IP --quick --scripts

# 2. Enumeración
python pentops.py enum -t $MACHINE_IP --auto

# 3. Reporte para documentación
python pentops.py report -t $MACHINE_IP -o markdown
```

## Ejemplo 7: Configuración y Verificación

```bash
# Primera vez usando PentOps
python pentops.py config --setup

# Verificar herramientas instaladas
python pentops.py config --check

# Ver configuración actual
python pentops.py config --show

# Si falta alguna herramienta, instalarla:
# Ubuntu/Debian/Kali
sudo apt update
sudo apt install nmap gobuster nikto hydra sqlmap enum4linux

# Ver la ayuda de un módulo específico
python pentops.py recon --help
python pentops.py enum --help
```

## Ejemplo 8: SQL Injection

```bash
# Target con posible SQLi
TARGET="vulnerable-site.com"
URL="http://vulnerable-site.com/login.php?id=1"

# Reconocimiento
python pentops.py recon -t $TARGET --quick

# Probar SQL Injection con SQLMap
python pentops.py exploit -t $TARGET --sqli "$URL"

# Nota: SQLMap se ejecuta con opciones básicas
# Para opciones avanzadas, usar sqlmap directamente
```

## Ejemplo 9: Post-Explotación

```bash
# Una vez comprometido el sistema
TARGET="10.10.10.100"

# Obtener comandos de enumeración
python pentops.py postexploit -t $TARGET --enum

# Instrucciones para LinPEAS
python pentops.py postexploit -t $TARGET --linpeas

# Instrucciones para WinPEAS
python pentops.py postexploit -t $TARGET --winpeas

# Ver todas las guías
python pentops.py postexploit -t $TARGET
```

## Ejemplo 10: Modo Verbose

```bash
# Para debugging o ver más detalles
python pentops.py --verbose recon -t 192.168.1.100 --quick

# Sin banner (para automatización)
python pentops.py --no-banner recon -t 192.168.1.100 --quick
```

## Tips y Trucos

### 1. Organización de Resultados
Los resultados se guardan automáticamente en:
```
results/<target>/
├── recon/
├── enumeration/
├── vulnscan/
├── exploit/
├── postexploit/
└── pentops.log
```

### 2. Combinar con Otras Herramientas
PentOps es un orquestador. Complementa con:
- Burp Suite para testing web manual
- Metasploit para explotación avanzada
- BloodHound para Active Directory
- Wireshark para análisis de red

### 3. Aliases Útiles

Agregar a tu `.bashrc` o `.zshrc`:
```bash
alias pent='python /path/to/pentops.py'
alias pent-recon='python /path/to/pentops.py recon'
alias pent-enum='python /path/to/pentops.py enum'
alias pent-workflow='python /path/to/pentops.py workflow'
```

Uso:
```bash
pent-recon -t 10.10.10.100 --quick
pent-workflow -w hybrid -t 192.168.1.50
```

### 4. Integración con tmux/screen

```bash
# Terminal 1: Reconocimiento
python pentops.py recon -t 10.10.10.100 --full

# Terminal 2: Listener para reverse shell
nc -lvnp 4444

# Terminal 3: Enumeración mientras el scan corre
python pentops.py enum -t 10.10.10.100 --auto
```

## Solución de Problemas

### Error: Herramienta no encontrada
```bash
# Verificar instalación
python pentops.py config --check

# Instalar herramienta faltante
sudo apt install <tool-name>
```

### Timeout en scans
```bash
# Para redes lentas, editar config.py:
NMAP_CONFIG = {
    'timing': 'T3',  # Cambiar de T4 a T3
    'min_rate': '2000',  # Reducir rate
}
```

### Permissions issues (Nmap UDP)
```bash
# Scans UDP requieren sudo/admin
sudo python pentops.py recon -t 10.10.10.100 --udp
```
