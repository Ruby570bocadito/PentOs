#!/usr/bin/env python3
"""
Módulo de Generación de Reportes
"""

import os
from datetime import datetime
from pathlib import Path
from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    save_output, validate_target, log_action, get_timestamp
)
from config import Config


def generate_markdown_report(target, output_dir):
    """Genera un reporte en formato Markdown"""
    print_info("Generando reporte Markdown...")
    
    # Recopilar archivos de resultados
    results_dir = Config.get_output_dir(target)
    
    report_content = f"""# Reporte de Pentesting - {target}

**Fecha:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Target:** {target}  
**Herramienta:** PentOps v{Config.VERSION}

---

## 📋 Resumen Ejecutivo

[Descripción general del engagement]

---

## 🔍 Reconocimiento

### Escaneo de Puertos

[Resultados de Nmap]

```
[Pegar resultados aquí]
```

### Servicios Detectados

| Puerto | Servicio | Versión |
|--------|----------|---------|
| 22     | SSH      | OpenSSH 7.6 |
| 80     | HTTP     | Apache 2.4.29 |

---

## 🔎 Enumeración

### Enumeración Web (Puerto 80)

**Directorios encontrados:**
- /admin
- /backup
- /uploads

**Tecnologías detectadas:**
- PHP 7.2
- Apache 2.4.29
- MySQL

### Enumeración SMB

[Resultados de enum4linux]

---

## 🛡️ Vulnerabilidades Detectadas

### CVE-XXXX-XXXXX - [Nombre de la Vulnerabilidad]

**Severidad:** Alta  
**Descripción:**  
**Impacto:**  
**Remediación:**

---

## ⚔️ Explotación

### [Nombre de la Explotación]

**Vector de ataque:**  
**Pasos realizados:**

1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

**Resultado:**  
✓ Acceso obtenido como usuario `www-data`

---

## 🚀 Post-Explotación

### Escalación de Privilegios

**Técnica utilizada:**  
**Resultado:**  
✓ Obtenido acceso como `root`

### Flags Capturadas

- **User Flag:** `[hash]`
- **Root Flag:** `[hash]`

---

## 📊 Conclusiones

[Resumen de hallazgos y recomendaciones]

---

## 📎 Anexos

### Archivos de Resultados

Los siguientes archivos contienen información detallada:

- Escaneos Nmap: `{results_dir}/recon/`
- Enumeración: `{results_dir}/enumeration/`
- Vulnerabilidades: `{results_dir}/vulnscan/`

---

**Generado por PentOps**  
*Automated Pentesting Orchestration Tool*
"""
    
    # Guardar reporte
    report_file = results_dir / f"report_{target}_{get_timestamp()}.md"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print_success(f"Reporte generado: {report_file}")
        return report_file
    except Exception as e:
        print_error(f"Error generando reporte: {str(e)}")
        return None


def generate_html_report(target, output_dir):
    """Genera un reporte en formato HTML"""
    print_info("Generando reporte HTML...")
    
    results_dir = Config.get_output_dir(target)
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Pentesting - {target}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        .info-box {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 15px 0;
        }}
        
        .critical {{
            border-left-color: #dc3545;
        }}
        
        .warning {{
            border-left-color: #ffc107;
        }}
        
        .success {{
            border-left-color: #28a745;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background: #667eea;
            color: white;
        }}
        
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        
        pre {{
            background: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        
        .footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Reporte de Pentesting</h1>
            <p><strong>Target:</strong> {target}</p>
            <p><strong>Fecha:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📋 Resumen Ejecutivo</h2>
                <div class="info-box">
                    <p>Este reporte documenta los hallazgos del pentesting realizado en <code>{target}</code>.</p>
                </div>
            </div>
            
            <div class="section">
                <h2>🔍 Reconocimiento</h2>
                <h3>Puertos Detectados</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Puerto</th>
                            <th>Protocolo</th>
                            <th>Servicio</th>
                            <th>Versión</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>22</td>
                            <td>TCP</td>
                            <td>SSH</td>
                            <td>OpenSSH 7.6</td>
                        </tr>
                        <tr>
                            <td>80</td>
                            <td>TCP</td>
                            <td>HTTP</td>
                            <td>Apache 2.4.29</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>🛡️ Vulnerabilidades</h2>
                
                <div class="info-box critical">
                    <h4>🔴 CRÍTICO - [Vulnerabilidad]</h4>
                    <p><strong>Descripción:</strong> [Detalle de la vulnerabilidad]</p>
                    <p><strong>Impacto:</strong> Ejecución remota de código</p>
                    <p><strong>Remediación:</strong> Actualizar a la última versión</p>
                </div>
                
                <div class="info-box warning">
                    <h4>🟡 MEDIA - [Vulnerabilidad]</h4>
                    <p><strong>Descripción:</strong> [Detalle de la vulnerabilidad]</p>
                    <p><strong>Impacto:</strong> Divulgación de información</p>
                </div>
            </div>
            
            <div class="section">
                <h2>⚔️ Explotación</h2>
                <div class="info-box success">
                    <p><strong>Estado:</strong> ✓ Explotación exitosa</p>
                    <p><strong>Acceso obtenido:</strong> Usuario <code>www-data</code></p>
                </div>
            </div>
            
            <div class="section">
                <h2>📊 Conclusiones y Recomendaciones</h2>
                <ul>
                    <li>Actualizar todos los servicios a las últimas versiones</li>
                    <li>Implementar políticas de contraseñas robustas</li>
                    <li>Configurar firewall y segmentación de red</li>
                    <li>Realizar auditorías de seguridad periódicas</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>📎 Archivos Adjuntos</h2>
                <p>Los archivos de resultados se encuentran en:</p>
                <pre>{results_dir}</pre>
            </div>
        </div>
        
        <div class="footer">
            <p>Generado por <strong>PentOps v{Config.VERSION}</strong></p>
            <p>Automated Pentesting Orchestration Tool</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Guardar reporte
    report_file = results_dir / f"report_{target}_{get_timestamp()}.html"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print_success(f"Reporte HTML generado: {report_file}")
        print_info(f"Abre el reporte en tu navegador: file://{report_file.absolute()}")
        return report_file
    except Exception as e:
        print_error(f"Error generando reporte HTML: {str(e)}")
        return None


def generate_report(args):
    """
    Función principal del módulo de reportes
    
    Args:
        args: Argumentos parseados de argparse
    """
    print_info(f"Generación de reporte: {args.target}")
    
    # Validar target
    if not validate_target(args.target):
        print_error(f"Target inválido: {args.target}")
        return
    
    output_dir = Config.get_output_dir(args.target)
    
    # Verificar que existan resultados
    if not output_dir.exists():
        print_warning(f"No se encontraron resultados para {args.target}")
        print_info(f"Los resultados deberían estar en: {output_dir}")
        return
    
    log_action(args.target, "report", "Generando reporte")
    
    # Generar según formato
    output_format = args.output_format.lower()
    
    if output_format == 'html':
        generate_html_report(args.target, output_dir)
    elif output_format == 'markdown' or output_format == 'md':
        generate_markdown_report(args.target, output_dir)
    elif output_format == 'pdf':
        print_warning("Generación de PDF no implementada todavía")
        print_info("Genera primero en HTML o Markdown")
    else:
        print_error(f"Formato no soportado: {output_format}")
    
    print_success("Reporte generado")
    log_action(args.target, "report", f"Reporte {output_format} generado")
