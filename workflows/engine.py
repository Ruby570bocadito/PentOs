#!/usr/bin/env python3
"""
Motor de Workflows para PentOps
Ejecuta workflows automatizados definidos en archivos YAML
"""

import yaml
import time
from pathlib import Path
from utils import (
    print_banner, print_success, print_error, print_info, print_warning,
    run_command, log_action, validate_target
)
from config import Config


class WorkflowEngine:
    """Motor de ejecución de workflows"""
    
    def __init__(self, target, workflow_file, dry_run=False):
        self.target = target
        self.workflow_file = Path(workflow_file)
        self.dry_run = dry_run
        self.workflow_data = None
        self.output_dir = Config.get_output_dir(target)
    
    def load_workflow(self):
        """Carga el workflow desde archivo YAML"""
        try:
            with open(self.workflow_file, 'r', encoding='utf-8') as f:
                self.workflow_data = yaml.safe_load(f)
            print_success(f"Workflow cargado: {self.workflow_data.get('name', 'Sin nombre')}")
            return True
        except FileNotFoundError:
            print_error(f"Archivo no encontrado: {self.workflow_file}")
            return False
        except yaml.YAMLError as e:
            print_error(f"Error parseando YAML: {str(e)}")
            return False
    
    def display_workflow(self):
        """Muestra la información del workflow"""
        if not self.workflow_data:
            return
        
        print_banner(f"WORKFLOW: {self.workflow_data.get('name', 'Sin nombre')}")
        print_info(f"Descripción: {self.workflow_data.get('description', 'N/A')}")
        print_info(f"Autor: {self.workflow_data.get('author', 'N/A')}")
        print_info(f"Versión: {self.workflow_data.get('version', '1.0')}\n")
        
        # Mostrar fases
        phases = self.workflow_data.get('phases', [])
        print_info(f"Fases totales: {len(phases)}\n")
        
        for i, phase in enumerate(phases, 1):
            print(f"  {i}. {phase.get('name', 'Sin nombre')}")
            tasks = phase.get('tasks', [])
            for j, task in enumerate(tasks, 1):
                print(f"     {i}.{j} {task.get('name', 'Sin nombre')}")
        print()
    
    def execute_task(self, task):
        """Ejecuta una tarea individual"""
        task_name = task.get('name', 'Tarea sin nombre')
        command = task.get('command', '')
        module = task.get('module', '')
        args = task.get('args', '')
        timeout = task.get('timeout', 300)
        
        print_info(f"Ejecutando: {task_name}")
        
        if self.dry_run:
            if module:
                print_warning(f"  [DRY-RUN] Módulo: {module} {args}")
            elif command:
                print_warning(f"  [DRY-RUN] Comando: {command}")
            return True
        
        # Ejecutar por módulo
        if module:
            # Construir comando para ejecutar módulo de PentOps
            pentops_cmd = f"python pentops.py {module} -t {self.target} {args}"
            print_verbose(f"Comando: {pentops_cmd}")
            
            exit_code, stdout, stderr = run_command(pentops_cmd, timeout=timeout)
            
            if exit_code == 0:
                print_success(f"✓ {task_name} completado")
                return True
            else:
                print_error(f"✗ {task_name} falló")
                if stderr:
                    print_error(f"  Error: {stderr[:200]}")
                return False
        
        # Ejecutar comando directo
        elif command:
            # Reemplazar placeholders
            cmd = command.replace('{target}', self.target)
            cmd = cmd.replace('{output_dir}', str(self.output_dir))
            
            exit_code, stdout, stderr = run_command(cmd, timeout=timeout)
            
            if exit_code == 0:
                print_success(f"✓ {task_name} completado")
                return True
            else:
                print_warning(f"⚠ {task_name} terminó con warnings")
                return True  # Continuar workflow
        
        return True
    
    def execute_phase(self, phase):
        """Ejecuta una fase completa"""
        phase_name = phase.get('name', 'Fase sin nombre')
        print_banner(f"FASE: {phase_name}")
        
        # Descripción de la fase
        if 'description' in phase:
            print_info(phase['description'])
        
        # Ejecutar tareas
        tasks = phase.get('tasks', [])
        successful = 0
        failed = 0
        
        for task in tasks:
            result = self.execute_task(task)
            if result:
                successful += 1
            else:
                failed += 1
                
                # Si critical, detener workflow
                if task.get('critical', False):
                    print_error("Tarea crítica falló. Deteniendo workflow.")
                    return False
            
            # Delay entre tareas
            delay = task.get('delay', 0)
            if delay > 0 and not self.dry_run:
                print_info(f"Esperando {delay} segundos...")
                time.sleep(delay)
        
        # Resumen de fase
        print_info(f"\nFase completada: {successful} exitosas, {failed} fallidas")
        return True
    
    def execute(self):
        """Ejecuta el workflow completo"""
        if not self.workflow_data:
            print_error("No hay workflow cargado")
            return False
        
        # Mostrar resumen
        self.display_workflow()
        
        if self.dry_run:
            print_warning("MODO DRY-RUN: No se ejecutarán comandos reales\n")
        else:
            print_info(f"Target: {self.target}")
            print_info(f"Resultados: {self.output_dir}\n")
        
        # Log inicio
        log_action(self.target, "workflow", f"Iniciando workflow: {self.workflow_data.get('name')}")
        
        # Ejecutar fases
        phases = self.workflow_data.get('phases', [])
        
        for i, phase in enumerate(phases, 1):
            print_info(f"\n{'='*60}")
            print_info(f"PROGRESO: Fase {i}/{len(phases)}")
            print_info(f"{'='*60}\n")
            
            result = self.execute_phase(phase)
            
            if not result:
                print_error("Workflow detenido por fallo crítico")
                log_action(self.target, "workflow", "Workflow detenido")
                return False
        
        # Workflow completado
        print_banner("✓ WORKFLOW COMPLETADO ✓")
        log_action(self.target, "workflow", "Workflow completado exitosamente")
        return True


def run_workflow(args):
    """
    Función principal del motor de workflows
    
    Args:
        args: Argumentos parseados de argparse
    """
    # Validar target
    if not validate_target(args.target):
        print_error(f"Target inválido: {args.target}")
        return
    
    # Determinar archivo de workflow
    if args.config:
        workflow_file = args.config
    else:
        # Workflows predefinidos
        workflow_file = Config.WORKFLOWS_DIR / f"{args.workflow}.yaml"
    
    if not Path(workflow_file).exists():
        print_error(f"Workflow no encontrado: {workflow_file}")
        print_info(f"Workflows disponibles en: {Config.WORKFLOWS_DIR}")
        return
    
    # Crear motor de workflow
    engine = WorkflowEngine(
        target=args.target,
        workflow_file=workflow_file,
        dry_run=args.dry_run
    )
    
    # Cargar y ejecutar
    if engine.load_workflow():
        engine.execute()
