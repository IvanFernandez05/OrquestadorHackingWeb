"""
Escáner de Cross-Site Request Forgery (CSRF)
"""
import sys
from typing import List, Dict
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class CSRFScanner:
    """Escáner para detectar vulnerabilidades CSRF"""
    
    # Nombres comunes de tokens CSRF
    CSRF_TOKEN_NAMES = [
        'csrf_token',
        'csrf',
        'csrftoken',
        '_csrf',
        '_token',
        'token',
        'authenticity_token',
        '__RequestVerificationToken',
        'anti-csrf-token'
    ]
    
    def __init__(self, http_client, reporter):
        self.http_client = http_client
        self.reporter = reporter
        self.vulnerabilities = []
    
    def scan(self, target_url: str) -> List[Dict]:
        """Escanear objetivo en busca de CSRF"""
        self.reporter.print_header(f"CSRF SCAN - {target_url}")
        self.vulnerabilities = []
        
        response = self.http_client.get(target_url)
        if not response:
            self.reporter.print_error("No se pudo conectar al objetivo")
            return self.vulnerabilities
        
        # Analizar formularios
        self._scan_forms(target_url, response.text)
        
        if self.vulnerabilities:
            self.reporter.print_warning(f"Encontradas {len(self.vulnerabilities)} posibles vulnerabilidades CSRF")
        else:
            self.reporter.print_success("Todos los formularios parecen tener protección CSRF")
        
        return self.vulnerabilities
    
    def _scan_forms(self, url: str, html_content: str):
        """Escanear formularios en busca de tokens CSRF"""
        soup = BeautifulSoup(html_content, 'html.parser')
        forms = soup.find_all('form')
        
        if not forms:
            self.reporter.print_info("No se encontraron formularios en la página")
            return
        
        self.reporter.print_info(f"Analizando {len(forms)} formulario(s)...")
        
        for idx, form in enumerate(forms):
            action = form.get('action', '')
            method = form.get('method', 'get').upper()
            form_url = urljoin(url, action)
            
            # Solo verificar formularios POST (los GET no necesitan CSRF normalmente)
            if method != 'POST':
                continue
            
            # Buscar tokens CSRF en el formulario
            has_csrf_token = self._has_csrf_token(form)
            
            if not has_csrf_token:
                vuln = {
                    'type': 'Missing CSRF Token',
                    'method': method,
                    'form_action': form_url,
                    'form_id': form.get('id', f'form-{idx}'),
                    'details': f'Formulario POST sin token CSRF en {form_url}'
                }
                self.vulnerabilities.append(vuln)
                self.reporter.print_vulnerability('CSRF', vuln['details'])
            else:
                self.reporter.print_success(f"Formulario en {form_url} tiene protección CSRF")
    
    def _has_csrf_token(self, form) -> bool:
        """Verificar si un formulario tiene token CSRF"""
        inputs = form.find_all('input')
        
        for input_field in inputs:
            input_name = input_field.get('name', '').lower()
            input_id = input_field.get('id', '').lower()
            input_type = input_field.get('type', '').lower()
            
            # Verificar por nombre
            for csrf_name in self.CSRF_TOKEN_NAMES:
                if csrf_name.lower() in input_name or csrf_name.lower() in input_id:
                    return True
            
            # Verificar inputs hidden con valores largos (posibles tokens)
            if input_type == 'hidden':
                value = input_field.get('value', '')
                if len(value) > 20:  # Tokens suelen ser largos
                    return True
        
        return False


def main():
    """Función principal para ejecución standalone"""
    if len(sys.argv) < 2:
        print("Uso: python csrf_scanner.py <url>")
        sys.exit(1)
    
    from utils.http_client import HTTPClient
    from utils.reporter import Reporter
    
    target = sys.argv[1]
    client = HTTPClient()
    reporter = Reporter()
    
    scanner = CSRFScanner(client, reporter)
    vulnerabilities = scanner.scan(target)
    
    client.close()
    
    if vulnerabilities:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
