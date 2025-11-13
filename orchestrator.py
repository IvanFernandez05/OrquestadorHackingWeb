#!/usr/bin/env python3
"""
Orquestador principal de escaneo de vulnerabilidades web
"""
import json
import sys
import argparse
from typing import List, Dict

from utils.http_client import HTTPClient
from utils.reporter import Reporter
from scanners.sql_injection import SQLInjectionScanner
from scanners.xss_scanner import XSSScanner
from scanners.csrf_scanner import CSRFScanner
from scanners.auth_bypass import AuthBypassScanner
from scanners.directory_traversal import DirectoryTraversalScanner


class VulnerabilityOrchestrator:
    """Orquestador de escáneres de vulnerabilidades"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config = self._load_config(config_file)
        self.reporter = Reporter()
        self.http_client = None
        self.all_vulnerabilities = []
    
    def _load_config(self, config_file: str) -> Dict:
        """Cargar configuración desde archivo JSON"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: No se encuentra el archivo {config_file}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: El archivo {config_file} no es un JSON válido")
            sys.exit(1)
    
    def run(self, target_url: str = None, scanners: List[str] = None):
        """Ejecutar escaneo de vulnerabilidades"""
        self.reporter.print_header("ORQUESTADOR DE VULNERABILIDADES WEB")
        
        # Inicializar cliente HTTP
        timeout = self.config.get('timeout', 10)
        max_retries = self.config.get('max_retries', 3)
        self.http_client = HTTPClient(timeout=timeout, max_retries=max_retries)
        
        # Determinar objetivos
        targets = []
        if target_url:
            targets = [{'name': 'Manual Target', 'url': target_url, 'enabled': True}]
        else:
            targets = [t for t in self.config.get('targets', []) if t.get('enabled', False)]
        
        if not targets:
            self.reporter.print_error("No hay objetivos configurados o habilitados")
            self.http_client.close()
            return
        
        # Escanear cada objetivo
        for target in targets:
            self._scan_target(target, scanners)
        
        # Mostrar resumen
        self.reporter.print_summary()
        
        # Cerrar cliente
        self.http_client.close()
        
        # Retornar código de salida basado en vulnerabilidades encontradas
        if self.all_vulnerabilities:
            return 1
        return 0
    
    def _scan_target(self, target: Dict, selected_scanners: List[str] = None):
        """Escanear un objetivo específico"""
        target_name = target.get('name', 'Unknown')
        target_url = target.get('url')
        
        if not target_url:
            self.reporter.print_error(f"Objetivo {target_name} no tiene URL configurada")
            return
        
        self.reporter.print_header(f"ESCANEANDO: {target_name}")
        self.reporter.print_info(f"URL: {target_url}")
        
        # Verificar conectividad
        response = self.http_client.get(target_url)
        if not response:
            self.reporter.print_error(f"No se pudo conectar a {target_url}")
            return
        
        self.reporter.print_success(f"Conectado exitosamente (Status: {response.status_code})")
        
        # Definir escáneres disponibles
        available_scanners = {
            'sql': ('SQL Injection', SQLInjectionScanner),
            'xss': ('XSS', XSSScanner),
            'csrf': ('CSRF', CSRFScanner),
            'auth': ('Auth Bypass', AuthBypassScanner),
            'traversal': ('Directory Traversal', DirectoryTraversalScanner)
        }
        
        # Si no se especifican escáneres, usar todos
        if not selected_scanners:
            selected_scanners = list(available_scanners.keys())
        
        # Ejecutar escáneres seleccionados
        for scanner_key in selected_scanners:
            if scanner_key not in available_scanners:
                self.reporter.print_warning(f"Escáner desconocido: {scanner_key}")
                continue
            
            scanner_name, scanner_class = available_scanners[scanner_key]
            try:
                scanner = scanner_class(self.http_client, self.reporter)
                vulnerabilities = scanner.scan(target_url)
                
                # Registrar vulnerabilidades encontradas
                for vuln in vulnerabilities:
                    self.reporter.add_vulnerability(scanner_name, target_url, vuln)
                    self.all_vulnerabilities.append(vuln)
                
            except Exception as e:
                self.reporter.print_error(f"Error en escáner {scanner_name}: {str(e)}")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Orquestador de escaneo de vulnerabilidades web',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos de uso:
  python orchestrator.py                           # Escanear objetivos en config.json
  python orchestrator.py -u http://target.com      # Escanear URL específica
  python orchestrator.py -u http://target.com -s sql xss  # Solo SQL Injection y XSS
  python orchestrator.py --list-scanners           # Listar escáneres disponibles
        '''
    )
    
    parser.add_argument('-u', '--url', 
                        help='URL objetivo (sobreescribe config.json)')
    parser.add_argument('-c', '--config', 
                        default='config.json',
                        help='Archivo de configuración (default: config.json)')
    parser.add_argument('-s', '--scanners', 
                        nargs='+',
                        choices=['sql', 'xss', 'csrf', 'auth', 'traversal', 'all'],
                        help='Escáneres a ejecutar (default: todos)')
    parser.add_argument('--list-scanners',
                        action='store_true',
                        help='Listar escáneres disponibles')
    
    args = parser.parse_args()
    
    # Listar escáneres
    if args.list_scanners:
        print("\nEscáneres disponibles:")
        print("  sql       - SQL Injection")
        print("  xss       - Cross-Site Scripting (XSS)")
        print("  csrf      - Cross-Site Request Forgery (CSRF)")
        print("  auth      - Authentication Bypass")
        print("  traversal - Directory Traversal")
        print("  all       - Todos los escáneres")
        sys.exit(0)
    
    # Procesar scanners
    scanners = args.scanners
    if scanners and 'all' in scanners:
        scanners = None
    
    # Ejecutar orquestador
    orchestrator = VulnerabilityOrchestrator(config_file=args.config)
    exit_code = orchestrator.run(target_url=args.url, scanners=scanners)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
