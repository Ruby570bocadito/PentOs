#!/usr/bin/env python3
"""
Sistema Avanzado de Reportes
Generación de informes profesionales con gráficos y estadísticas
"""

import json
from datetime import datetime
from pathlib import Path
from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    save_output, log_action, get_timestamp
)
from config import Config


class AdvancedReportGenerator:
    """Generador avanzado de reportes"""
    
    def __init__(self, target):
        self.target = target
        self.output_dir = Config.get_output_dir(target)
        self.data = {
            'metadata': {
                'target': target,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'pentester': 'PentOps Automated System',
                'version': Config.VERSION
            },
            'executive_summary': {},
            'technical_findings': [],
            'risk_assessment': {},
            'recommendations': []
        }
    
    def load_all_results(self):
        """Carga todos los resultados de módulos anteriores"""
        print_info("Recopilando resultados de todos los módulos...")
        
        modules = ['recon', 'enumeration', 'vulnscan', 'exploit', 'postexploit', 
                   'auto-detect', 'credentials', 'api-intel', 'auto-audit']
        
        all_results = {}
        
        for module in modules:
            module_dir = self.output_dir / module
            if module_dir.exists():
                # Buscar archivos JSON
                json_files = list(module_dir.glob('*.json'))
                if json_files:
                    try:
                        with open(json_files[-1], 'r') as f:  # El más reciente
                            all_results[module] = json.load(f)
                    except:
                        pass
        
        return all_results
    
    def generate_executive_summary(self, results):
        """Genera resumen ejecutivo"""
        print_info("Generando resumen ejecutivo...")
        
        summary = {
            'scope': f'Evaluación de seguridad de {self.target}',
            'duration': 'Auto-generado',
            'key_findings': [],
            'overall_risk': 'MEDIUM',
            'critical_count': 0,
            'high_count': 0
        }
        
        # Contar vulnerabilidades por severidad
        if 'auto-audit' in results:
            audit = results['auto-audit']
            if 'risk_assessment' in audit:
                risk = audit['risk_assessment']
                summary['critical_count'] = risk.get('severity_counts', {}).get('critical', 0)
                summary['high_count'] = risk.get('severity_counts', {}).get('high', 0)
                summary['overall_risk'] = risk.get('risk_level', 'MEDIUM')
            
            if 'findings' in audit:
                # Top 3 hallazgos críticos
                critical = [f for f in audit['findings'] if f['severity'] == 'critical'][:3]
                summary['key_findings'] = [f['title'] for f in critical]
        
        self.data['executive_summary'] = summary
        return summary
    
    def generate_technical_findings(self, results):
        """Genera sección de hallazgos técnicos"""
        print_info("Compilando hallazgos técnicos...")
        
        findings = []
        
        # Auto-audit findings
        if 'auto-audit' in results and 'findings' in results['auto-audit']:
            for finding in results['auto-audit']['findings']:
                findings.append({
                    'source': 'Auto-Audit',
                    'severity': finding.get('severity', 'info'),
                    'title': finding.get('title', 'Unknown'),
                    'description': finding.get('description', ''),
                    'recommendation': finding.get('recommendation', ''),
                    'cve': finding.get('cve', None)
                })
        
        # Auto-detect vulnerabilities
        if 'auto-detect' in results and 'vulnerabilities' in results['auto-detect']:
            for vuln in results['auto-detect']['vulnerabilities']:
                findings.append({
                    'source': 'Auto-Detection',
                    'severity': vuln.get('severity', 'high'),
                    'title': f"{vuln.get('service')} {vuln.get('version')} - {vuln.get('cve')}",
                    'description': vuln.get('cve', ''),
                    'recommendation': 'Actualizar software a la última versión',
                    'cve': vuln.get('cve')
                })
        
        self.data['technical_findings'] = findings
        return findings
    
    def generate_risk_matrix(self, findings):
        """Genera matriz de riesgo"""
        print_info("Construyendo matriz de riesgo...")
        
        matrix = {
            'critical': {'total': 0, 'items': []},
            'high': {'total': 0, 'items': []},
            'medium': {'total': 0, 'items': []},
            'low': {'total': 0, 'items': []},
            'info': {'total': 0, 'items': []}
        }
        
        for finding in findings:
            severity = finding.get('severity', 'info')
            if severity in matrix:
                matrix[severity]['total'] += 1
                matrix[severity]['items'].append(finding['title'])
        
        self.data['risk_matrix'] = matrix
        return matrix
    
    def generate_recommendations(self, findings):
        """Genera lista priorizada de recomendaciones"""
        print_info("Generando recomendaciones prioritarias...")
        
        recommendations = []
        
        # Ordenar por severidad
        sorted_findings = sorted(findings, 
                                key=lambda x: {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}.get(x.get('severity', 'info'), 4))
        
        for i, finding in enumerate(sorted_findings[:10], 1):  # Top 10
            recommendations.append({
                'priority': i,
                'severity': finding.get('severity', 'info'),
                'title': finding.get('title', 'Unknown'),
                'action': finding.get('recommendation', 'No specific recommendation'),
                'effort': 'Low' if finding.get('severity') in ['low', 'info'] else 'Medium' if finding.get('severity') == 'medium' else 'High'
            })
        
        self.data['recommendations'] = recommendations
        return recommendations
    
    def generate_markdown_report(self):
        """Genera reporte detallado en Markdown"""
        print_info("Generando reporte Markdown...")
        
        exec_summary = self.data['executive_summary']
        findings = self.data['technical_findings']
        matrix = self.data.get('risk_matrix', {})
        recommendations = self.data['recommendations']
        
        md = f"""# Informe de Auditoría de Seguridad

**Target:** {self.target}  
**Fecha:** {self.data['metadata']['date']}  
**Pentester:** {self.data['metadata']['pentester']}  
**Herramienta:** PentOps v{self.data['metadata']['version']}

---

## 📋 Resumen Ejecutivo

### Alcance
{exec_summary.get('scope', 'N/A')}

### Nivel de Riesgo Global
**{exec_summary.get('overall_risk', 'MEDIUM')}**

### Hallazgos Principales
"""
        
        # Key findings
        for finding in exec_summary.get('key_findings', []):
            md += f"- 🔴 {finding}\n"
        
        md += f"""

### Estadísticas de Vulnerabilidades

| Severidad | Cantidad |
|-----------|----------|
| 🔴 Críticas | {exec_summary.get('critical_count', 0)} |
| 🟠 Altas | {exec_summary.get('high_count', 0)} |
| 🟡 Medias | {matrix.get('medium', {}).get('total', 0)} |
| 🟢 Bajas | {matrix.get('low', {}).get('total', 0)} |

---

## 🔍 Hallazgos Técnicos Detallados

"""
        
        # Agrupar por severidad
        for severity in ['critical', 'high', 'medium', 'low', 'info']:
            severity_findings = [f for f in findings if f.get('severity') == severity]
            
            if severity_findings:
                icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢', 'info': 'ℹ️'}.get(severity, '')
                md += f"### {icon} {severity.upper()} ({len(severity_findings)})\n\n"
                
                for i, finding in enumerate(severity_findings, 1):
                    md += f"#### {i}. {finding.get('title', 'Unknown')}\n\n"
                    md += f"**Fuente:** {finding.get('source', 'Unknown')}\n\n"
                    
                    if finding.get('cve'):
                        md += f"**CVE:** {finding.get('cve')}\n\n"
                    
                    md += f"**Descripción:**  \n{finding.get('description', 'N/A')}\n\n"
                    md += f"**Recomendación:**  \n{finding.get('recommendation', 'N/A')}\n\n"
                    md += "---\n\n"
        
        md += """## 🎯 Recomendaciones Prioritarias

"""
        
        for rec in recommendations:
            priority_icon = {'critical': '🚨', 'high': '⚠️', 'medium': '📌', 'low': '💡', 'info': 'ℹ️'}.get(rec.get('severity', 'info'), '📌')
            md += f"### {rec['priority']}. {priority_icon} {rec['title']}\n\n"
            md += f"**Severidad:** {rec.get('severity', 'info').upper()}  \n"
            md += f"**Esfuerzo:** {rec.get('effort', 'Medium')}  \n\n"
            md += f"**Acción:**  \n{rec.get('action', 'No action specified')}\n\n"
            md += "---\n\n"
        
        md += """## 📊 Metodología

La evaluación se realizó usando la siguiente metodología:

1. **Reconocimiento** - Identificación de sistemas y servicios
2. **Enumeración** - Recopilación detallada de información
3. **Análisis de Vulnerabilidades** - Identificación de debilidades
4. **Auto-Auditoría** - Verificación automática de configuraciones
5. **Evaluación de Riesgo** - Scoring y priorización

## 🛠️ Herramientas Utilizadas

- **PentOps Automated Suite**
- Nmap - Escaneo de puertos
- Auto-detection engine
- Security compliance checks
- API intelligence sources

## ✅ Conclusiones

Se han identificado **{len(findings)}** hallazgos en total, de los cuales **{exec_summary.get('critical_count', 0)} son críticos** y **{exec_summary.get('high_count', 0)} son de severidad alta**.

Se recomienda priorizar la remediación de vulnerabilidades críticas y altas mediante:

1. Aplicación de parches de seguridad
2. Fortalecimiento de configuraciones
3. Implementación de controles de seguridad adicionales
4. Auditorías periódicas

---

## 📎 Anexos

### Archivos de Evidencia

Los archivos de evidencia técnica se encuentran en:
```
{self.output_dir}
```

### Referencias

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [MITRE ATT&CK](https://attack.mitre.org/)

---

**Reporte generado automáticamente por PentOps v{Config.VERSION}**  
*{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        # Guardar reporte
        report_file = self.output_dir / f"INFORME_COMPLETO_{get_timestamp()}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print_success(f"✓ Reporte Markdown generado: {report_file}")
        return report_file
    
    def generate_html_report(self):
        """Genera reporte HTML profesional"""
        print_info("Generando reporte HTML...")
        
        exec_summary = self.data['executive_summary']
        findings = self.data['technical_findings']
        matrix = self.data.get('risk_matrix', {})
        
        # HTML con CSS profesional
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Informe de Auditoría - {self.target}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 20px auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .meta {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #1e3c72;
            border-bottom: 3px solid #1e3c72;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        .risk-badge {{
            display: inline-block;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 1.5em;
            font-weight: bold;
            margin: 20px 0;
        }}
        
        .risk-critical {{ background: #dc3545; color: white; }}
        .risk-high {{ background: #fd7e14; color: white; }}
        .risk-medium {{ background: #ffc107; color: #333; }}
        .risk-low {{ background: #28a745; color: white; }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 30px 0;
        }}
        
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid;
        }}
        
        .stat-card.critical {{ border-color: #dc3545; }}
        .stat-card.high {{ border-color: #fd7e14; }}
        .stat-card.medium {{ border-color: #ffc107; }}
        .stat-card.low {{ border-color: #28a745; }}
        
        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            color: #1e3c72;
        }}
        
        .stat-label {{
            color: #666;
            text-transform: uppercase;
            font-size: 0.9em;
        }}
        
        .finding {{
            background: #f8f9fa;
            border-left: 4px solid;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        
        .finding.critical {{ border-color: #dc3545; }}
        .finding.high {{ border-color: #fd7e14; }}
        .finding.medium {{ border-color: #ffc107; }}
        .finding.low {{ border-color: #28a745; }}
        
        .finding-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #1e3c72;
        }}
        
        .finding-meta {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 15px;
        }}
        
        .recommendation {{
            background: #e7f3ff;
            border-left: 4px solid #0066cc;
            padding: 15px;
            margin-top: 10px;
            border-radius: 3px;
        }}
        
        .footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 30px;
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
            background: #1e3c72;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Informe de Auditoría de Seguridad</h1>
            <div class="meta">
                <p><strong>Target:</strong> {self.target}</p>
                <p><strong>Fecha:</strong> {self.data['metadata']['date']}</p>
                <p><strong>Generado por:</strong> PentOps v{Config.VERSION}</p>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📋 Resumen Ejecutivo</h2>
                <div class="risk-badge risk-{exec_summary.get('overall_risk', 'medium').lower()}">
                    Riesgo: { exec_summary.get('overall_risk', 'MEDIUM')}
                </div>
                
                <div class="stats">
                    <div class="stat-card critical">
                        <div class="stat-number">{exec_summary.get('critical_count', 0)}</div>
                        <div class="stat-label">Críticas</div>
                    </div>
                    <div class="stat-card high">
                        <div class="stat-number">{exec_summary.get('high_count', 0)}</div>
                        <div class="stat-label">Altas</div>
                    </div>
                    <div class="stat-card medium">
                        <div class="stat-number">{matrix.get('medium', {}).get('total', 0)}</div>
                        <div class="stat-label">Medias</div>
                    </div>
                    <div class="stat-card low">
                        <div class="stat-number">{matrix.get('low', {}).get('total', 0)}</div>
                        <div class="stat-label">Bajas</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🔍 Hallazgos Técnicos</h2>
"""
        
        # Findings por severidad
        for severity in ['critical', 'high', 'medium', 'low']:
            severity_findings = [f for f in findings if f.get('severity') == severity]
            if severity_findings:
                for finding in severity_findings:
                    html += f"""
                <div class="finding {severity}">
                    <div class="finding-title">{finding.get('title', 'Unknown')}</div>
                    <div class="finding-meta">
                        <strong>Severidad:</strong> {severity.upper()} | 
                        <strong>Fuente:</strong> {finding.get('source', 'Unknown')}
                    </div>
                    <div class="finding-description">
                        <p>{finding.get('description', 'N/A')}</p>
                    </div>
                    <div class="recommendation">
                        <strong>💡 Recomendación:</strong> {finding.get('recommendation', 'N/A')}
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
        
        <div class="footer">
            <p><strong>PentOps Automated Pentesting System</strong></p>
            <p>Este reporte es confidencial y solo para uso del cliente autorizado</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Guardar HTML
        html_file = self.output_dir / f"INFORME_COMPLETO_{get_timestamp()}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print_success(f"✓ Reporte HTML generado: {html_file}")
        return html_file
    
    def generate_complete_report(self):
        """Genera informe completo en todos los formatos"""
        print_banner("GENERANDO INFORME COMPLETO DE AUDITORÍA")
        
        # Cargar todos los resultados
        results = self.load_all_results()
        
        # Generar análisis
        self.generate_executive_summary(results)
        findings = self.generate_technical_findings(results)
        self.generate_risk_matrix(findings)
        self.generate_recommendations(findings)
        
        # Guardar data completa en JSON
        json_file = self.output_dir / f"INFORME_DATA_{get_timestamp()}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        # Generar reportes
        md_file = self.generate_markdown_report()
        html_file = self.generate_html_report()
        
        print_banner("✓ INFORME COMPLETO GENERADO")
        print_success(f"Markdown: {md_file}")
        print_success(f"HTML: {html_file}")
        print_success(f"JSON: {json_file}")
        
        return {
            'markdown': md_file,
            'html': html_file,
            'json': json_file
        }


def run_advanced_report(args):
    """
    Función principal para generar informe avanzado
    
    Args:
        args: Argumentos parseados
    """
    generator = AdvancedReportGenerator(args.target)
    
    log_action(args.target, "advanced-report", "Generando informe completo")
    
    reports = generator.generate_complete_report()
    
    print_info(f"\n📂 Todos los archivos en: {generator.output_dir}")
    
    log_action(args.target, "advanced-report", "Informe generado exitosamente")
    
    return reports
