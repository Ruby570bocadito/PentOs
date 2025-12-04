# 🚀 Guía de Características Avanzadas - PentOps v2.0

## Nuevas Características

### 1. Auto-Detección Inteligente 🧠

**Descripción**: Detecta automáticamente tecnologías, mapea CVEs y sugiere acciones.

```bash
# Auto-detección básica
python pentops.py autodetect -t 192.168.1.100

# Con archivo de scan previo
python pentops.py autodetect -t 192.168.1.100 -s results/scan.json
```

**Capacidades**:
- ✅ Detección de tecnologías desde headers HTTP
- ✅ Mapeo automático de CVEs conocidos
- ✅ Sugerencias de acciones priorizadas
- ✅ Generación automática de plan de ataque
- ✅ Identificación devulnerabilidades críticas

**Ejemplo de salida**:
```
🔍 Tecnologías Detectadas:
  • Apache 2.4.49 (Confianza: high)
  • PHP 7.4.3 (Confianza: high)

⚠️  Vulnerabilidades Conocidas:
  • [CRITICAL] Apache 2.4.49: CVE-2021-41773 - Path Traversal

💡 Acciones Sugeridas:
  ALTA PRIORIDAD:
    → [http:80] Buscar exploit para CVE-2021-41773
    → [http:80] Enumerar directorios con gobuster
```

---

### 2. Credential Harvesting 🔑

**Descripción**: Guías completas para extracción de credenciales en sistemas comprometidos.

```bash
# Guías de credential harvesting
python pentops.py credentials -t 192.168.1.100

# Búsqueda en directorio específico
python pentops.py credentials -t 192.168.1.100 -d /var/www/html
```

**Incluye guías para**:
- ✅ Navegadores (Chrome, Firefox)
- ✅ Claves SSH privadas
- ✅ Hashes de contraseñas (Linux/Windows)
- ✅ Bases de datos (MySQL, PostgreSQL, MongoDB, MSSQL)
- ✅ Archivos de configuración

**Ejemplo - Extracción de SSH**:
```bash
# Buscar claves privadas
find / -name id_rsa 2>/dev/null

# Crackear passphrase
ssh2john id_rsa > hash.txt
john --wordlist=rockyou.txt hash.txt
```

---

### 3. Integración con APIs de Seguridad 🌐

**Descripción**: Consulta automática de Shodan, VirusTotal, ExploitDB, CVE Details, HaveIBeenPwned.

#### Shodan
```bash
# Requiere API key
export SHODAN_API_KEY="tu_key_aqui"

python pentops.py api-intel -t 192.168.1.100 --shodan
```

**Información obtenida**:
- País, ciudad, ISP, organización
- Puertos abiertos históricos
- Vulnerabilidades conocidas
- Servicios y versiones detectadas

#### VirusTotal
```bash
# Requiere API key
export VT_API_KEY="tu_key_aqui"

# Para IPs
python pentops.py api-intel -t 192.168.1.100 --virustotal --type ip

# Para dominios
python pentops.py api-intel -t example.com --virustotal --type domain
```

#### ExploitDB
```bash
# Búsqueda de exploits
python pentops.py api-intel -t target.com --exploitdb --query "apache 2.4.49"
```

#### CVE Details
```bash
# Información de CVE específico
python pentops.py api-intel -t target.com --cve CVE-2021-41773
```

#### HaveIBeenPwned
```bash
# Verificar email comprometido
python pentops.py api-intel -t target.com --hibp --email user@example.com
```

#### Todas las búsquedas
```bash
python pentops.py api-intel -t 192.168.1.100 --all
```

---

### 4. Workflow Avanzado 🔄

**Descripción**: Workflow completo con auto-detección e inteligencia.

```bash
python pentops.py workflow -w advanced -t 192.168.1.100
```

**Fases del workflow**:
1. **Reconocimiento con Auto-Detección**
   - Scan rápido
   - Auto-detección inteligente
   - Búsqueda en Shodan

2. **Intelligence Gathering**
   - VirusTotal lookup
   - Búsqueda de exploits conocidos

3. **Enumeración Dirigida**
   - Based en servicios detectados
   - Enumeración web profunda

4. **Análisis Avanzado de Vulnerabilidades**
   - Escaneo web
   - Scripts NSE
   - Mapeo de CVEs

5. **Explotación Dirigida**
   - Basada en hallazgos
   - Preparación de listeners

6. **Post-Explotación Completa**
   - Credential harvesting
   - LinPEAS/WinPEAS

7. **Reporting Avanzado**
   - HTML interactivo
   - Markdown para documentación

---

### 5. Progress Indicators y Visualización 📊

**Descripción**: Barras de progreso, spinners, y visualización mejorada.

**Características**:
- ✅ Progress bars para scans largos
- ✅ Spinners animados
- ✅ Superficie de ataque visual
- ✅ Recomendaciones inteligentes
- ✅ Wordlists sugeridas por servicio

---

## Configuración de APIs

### Obtener API Keys

#### Shodan
1. Registrarse en https://account.shodan.io/register
2. Obtener API key de https://account.shodan.io/
3. Exportar: `export SHODAN_API_KEY="tu_key"`

#### VirusTotal
1. Registrarse en https://www.virustotal.com/gui/join-us
2. Obtener API key de tu perfil
3. Exportar: `export VT_API_KEY="tu_key"`

**Hacerlo permanente** (Linux):
```bash
echo 'export SHODAN_API_KEY="tu_key"' >> ~/.bashrc
echo 'export VT_API_KEY="tu_key"' >> ~/.bashrc
source ~/.bashrc
```

---

## Ejemplos Prácticos Avanzados

### Ejemplo 1: Pentesting con Auto-Detección
```bash
# 1. Reconnaissance con auto-detección
python pentops.py recon -t 10.10.10.100 --quick
python pentops.py autodetect -t 10.10.10.100

# 2. Seguir sugerencias del auto-detector
# (ejecutar comandos sugeridos)

# 3. API intelligence
python pentops.py api-intel -t 10.10.10.100 --all

# 4. Workflow completo
python pentops.py workflow -w advanced -t 10.10.10.100
```

### Ejemplo 2: Bug Bounty Workflow
```bash
# Target: example.com

# 1. Intelligence gathering
python pentops.py api-intel -t example.com --virustotal --type domain
python pentops.py api-intel -t example.com --shodan

# 2. Reconocimiento
python pentops.py recon -t example.com --quick

# 3. Auto-detección
python pentops.py autodetect -t example.com

# 4. Enumeración web
python pentops.py enum -t example.com -s http

# 5. Vulnerabilidades
python pentops.py vulnscan -t example.com --web

# 6. Reporte
python pentops.py report -t example.com -o html
```

### Ejemplo 3: Post-Explotación Completa
```bash
# Después de comprometer el sistema

# 1. Credential harvesting
python pentops.py credentials -t compromised-target

# 2. Ejecutar en el target:
#    - Comandos de enumeración sugeridos
#    - LinPEAS/WinPEAS
#    - Búsqueda de credenciales

# 3. Verificar credenciales encontradas
python pentops.py api-intel -t target --hibp --email found@email.com

# 4. Documentar hallazgos
python pentops.py report -t compromised-target -o html
```

---

## Mejoras en Reportes

### Reporte HTML Mejorado
- 📊 Gráficos de estadísticas
- 🎨 Diseño profesional con gradientes
- 📋 Timeline de actividades
- ⚠️  Categorización de vulnerabilidades
- 🔗 Links a CVEs y referencias

### Contenido Automático
- Resumen ejecutivo
- Servicios detectados (tabla)
- Vulnerabilidades con CVSS scores
- Evidencias de explotación
- Rutas de ataque visualizadas
- Recomendaciones priorizadas

---

## Tips Avanzados

### 1. Combinar Módulos
```bash
# Recon + AutoDetect + API Intel en secuencia
python pentops.py recon -t target --quick && \
python pentops.py autodetect -t target && \
python pentops.py api-intel -t target --all
```

### 2. Automation con Scripts
```bash
#!/bin/bash
TARGET=$1

echo "[+] Iniciando pentesting automatizado de $TARGET"

# Recon
python pentops.py recon -t $TARGET --quick

# Auto detect
python pentops.py autodetect -t $TARGET

# APIs
if [ ! -z "$SHODAN_API_KEY" ]; then
    python pentops.py api-intel -t $TARGET --shodan
fi

# Workflow
python pentops.py workflow -w advanced -t $TARGET

# Report
python pentops.py report -t $TARGET -o html

echo "[+] Pentesting completado. Revisa results/$TARGET/"
```

### 3. Integración con otras herramientas
```bash
# Exportar resultados para Metasploit
# results/<target>/recon/nmap_*.xml puede importarse a MSF

# Exportar para Burp Suite
# results/<target>/enumeration/http/ contiene URLs descubiertas
```

---

## Troubleshooting

### APIs no funcionan
```bash
# Verificar API keys
echo $SHODAN_API_KEY
echo $VT_API_KEY

# Probar conexión
curl "https://api.shodan.io/api-info?key=$SHODAN_API_KEY"
```

### Rate limiting
- Shodan: 1 query/second (plan gratuito)
- VirusTotal: 4 requests/minute (plan gratuito)
- HaveIBeenPwned: 1 request/1.5 seconds

### Dependencias faltantes
```bash
pip install -r requirements.txt --upgrade
```

---

## Roadmap Futuro

- [ ] Integración Metasploit RPC
- [ ] Dashboard web en tiempo real
- [ ] Sistema de plugins
- [ ] Base de datos SQLite para historial
- [ ] Generación de PDF real
- [ ] Modo colaborativo multi-usuario
- [ ] Integración con Burp Suite
- [ ] Módulo de WiFi pentesting
- [ ] Active Directory module
- [ ] Cloud pentesting (AWS, Azure, GCP)

---

**PentOps v2.0** - *Next-Gen Pentesting Automation* 🚀
