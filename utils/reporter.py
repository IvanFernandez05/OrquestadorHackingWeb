"""
Sistema de reportes para vulnerabilidades encontradas
"""
from colorama import Fore, Style, init
from typing import List, Dict
from datetime import datetime

# Inicializar colorama
init(autoreset=True)


class Reporter:
    """Gestiona la generación de reportes de vulnerabilidades"""
    
    def __init__(self):
        self.vulnerabilities = []
    
    def add_vulnerability(self, scanner: str, target: str, vulnerability: Dict):
        """Añadir una vulnerabilidad encontrada"""
        self.vulnerabilities.append({
            'timestamp': datetime.now().isoformat(),
            'scanner': scanner,
            'target': target,
            'vulnerability': vulnerability
        })
    
    def print_header(self, title: str):
        """Imprimir cabecera de sección"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}{title.center(80)}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    def print_info(self, message: str):
        """Imprimir mensaje informativo"""
        print(f"{Fore.BLUE}[INFO] {message}{Style.RESET_ALL}")
    
    def print_success(self, message: str):
        """Imprimir mensaje de éxito"""
        print(f"{Fore.GREEN}[✓] {message}{Style.RESET_ALL}")
    
    def print_warning(self, message: str):
        """Imprimir mensaje de advertencia"""
        print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")
    
    def print_error(self, message: str):
        """Imprimir mensaje de error"""
        print(f"{Fore.RED}[✗] {message}{Style.RESET_ALL}")
    
    def print_vulnerability(self, vuln_type: str, details: str):
        """Imprimir vulnerabilidad encontrada"""
        print(f"{Fore.RED}[VULNERABILIDAD] {vuln_type}{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}→ {details}{Style.RESET_ALL}")
    
    def print_summary(self):
        """Imprimir resumen de vulnerabilidades encontradas"""
        self.print_header("RESUMEN DE ESCANEO")
        
        if not self.vulnerabilities:
            self.print_success("No se encontraron vulnerabilidades")
            return
        
        print(f"{Fore.RED}Total de vulnerabilidades encontradas: {len(self.vulnerabilities)}{Style.RESET_ALL}\n")
        
        # Agrupar por escáner
        by_scanner = {}
        for vuln in self.vulnerabilities:
            scanner = vuln['scanner']
            if scanner not in by_scanner:
                by_scanner[scanner] = []
            by_scanner[scanner].append(vuln)
        
        for scanner, vulns in by_scanner.items():
            print(f"{Fore.YELLOW}{scanner}: {len(vulns)} vulnerabilidad(es){Style.RESET_ALL}")
            for vuln in vulns:
                v = vuln['vulnerability']
                print(f"  - {v.get('type', 'Unknown')}: {v.get('details', 'No details')}")
