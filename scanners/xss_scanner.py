"""
Escáner de Cross-Site Scripting (XSS)
"""
import sys
from typing import List, Dict
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup
import html


class XSSScanner:
    """Escáner para detectar vulnerabilidades XSS"""
    
    # Payloads XSS comunes
    XSS_PAYLOADS = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
        "javascript:alert('XSS')",
        "<iframe src=javascript:alert('XSS')>",
        "<body onload=alert('XSS')>",
        "'\"><script>alert(String.fromCharCode(88,83,83))</script>",
        "<input onfocus=alert('XSS') autofocus>",
        "<select onfocus=alert('XSS') autofocus>",
        "<textarea onfocus=alert('XSS') autofocus>"
    ]
    
    def __init__(self, http_client, reporter):
        self.http_client = http_client
        self.reporter = reporter
        self.vulnerabilities = []
    
    def scan(self, target_url: str) -> List[Dict]:
        """Escanear objetivo en busca de XSS"""
        self.reporter.print_header(f"XSS SCAN - {target_url}")
        self.vulnerabilities = []
        
        # Escanear parámetros GET
        self._scan_get_params(target_url)
        
        # Escanear formularios
        self._scan_forms(target_url)
        
        if self.vulnerabilities:
            self.reporter.print_warning(f"Encontradas {len(self.vulnerabilities)} posibles vulnerabilidades XSS")
        else:
            self.reporter.print_success("No se detectaron vulnerabilidades XSS evidentes")
        
        return self.vulnerabilities
    
    def _scan_get_params(self, url: str):
        """Escanear parámetros GET"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if not params:
            return
        
        self.reporter.print_info("Probando parámetros GET...")
        
        for param_name in params:
            for payload in self.XSS_PAYLOADS:
                test_params = params.copy()
                test_params[param_name] = [payload]
                
                # Reconstruir URL con payload
                new_query = urlencode(test_params, doseq=True)
                test_url = urlunparse((
                    parsed.scheme, parsed.netloc, parsed.path,
                    parsed.params, new_query, parsed.fragment
                ))
                
                response = self.http_client.get(test_url)
                if response and self._check_xss_reflection(response.text, payload):
                    vuln = {
                        'type': 'Reflected XSS',
                        'method': 'GET',
                        'parameter': param_name,
                        'payload': payload,
                        'url': test_url,
                        'details': f'Parámetro vulnerable: {param_name} refleja contenido sin sanitizar'
                    }
                    self.vulnerabilities.append(vuln)
                    self.reporter.print_vulnerability('XSS Reflejado (GET)', vuln['details'])
    
    def _scan_forms(self, url: str):
        """Escanear formularios HTML"""
        response = self.http_client.get(url)
        if not response:
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        
        if not forms:
            return
        
        self.reporter.print_info(f"Analizando {len(forms)} formulario(s)...")
        
        for form in forms:
            action = form.get('action', '')
            method = form.get('method', 'get').upper()
            form_url = urljoin(url, action)
            
            inputs = form.find_all(['input', 'textarea'])
            for payload in self.XSS_PAYLOADS[:5]:  # Limitar payloads
                form_data = {}
                vulnerable_field = None
                
                for input_field in inputs:
                    input_name = input_field.get('name')
                    input_type = input_field.get('type', 'text')
                    
                    if not input_name:
                        continue
                    
                    if input_type == 'submit':
                        form_data[input_name] = input_field.get('value', 'submit')
                    else:
                        form_data[input_name] = payload
                        if not vulnerable_field:
                            vulnerable_field = input_name
                
                if method == 'POST':
                    response = self.http_client.post(form_url, data=form_data)
                else:
                    response = self.http_client.get(form_url, params=form_data)
                
                if response and self._check_xss_reflection(response.text, payload):
                    vuln = {
                        'type': 'Reflected XSS',
                        'method': method,
                        'form_action': form_url,
                        'field': vulnerable_field,
                        'payload': payload,
                        'details': f'Formulario vulnerable en {form_url} - campo: {vulnerable_field}'
                    }
                    self.vulnerabilities.append(vuln)
                    self.reporter.print_vulnerability('XSS (Formulario)', vuln['details'])
                    break
    
    def _check_xss_reflection(self, response_text: str, payload: str) -> bool:
        """Verificar si el payload se refleja sin sanitizar"""
        # Verificar si el payload aparece tal cual en la respuesta
        if payload in response_text:
            return True
        
        # Verificar si aparece sin codificar HTML
        unescaped_chars = ['<', '>', '"', "'"]
        for char in unescaped_chars:
            if char in payload and char in response_text:
                # El payload contiene caracteres especiales sin escapar
                return True
        
        return False


def main():
    """Función principal para ejecución standalone"""
    if len(sys.argv) < 2:
        print("Uso: python xss_scanner.py <url>")
        sys.exit(1)
    
    from utils.http_client import HTTPClient
    from utils.reporter import Reporter
    
    target = sys.argv[1]
    client = HTTPClient()
    reporter = Reporter()
    
    scanner = XSSScanner(client, reporter)
    vulnerabilities = scanner.scan(target)
    
    client.close()
    
    if vulnerabilities:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
