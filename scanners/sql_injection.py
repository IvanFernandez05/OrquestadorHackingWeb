"""
Escáner de inyección SQL
"""
import sys
from typing import List, Dict
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup
import re


class SQLInjectionScanner:
    """Escáner para detectar vulnerabilidades de inyección SQL"""
    
    # Payloads comunes de SQL Injection
    SQL_PAYLOADS = [
        "'",
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' /*",
        "admin' --",
        "admin' #",
        "' UNION SELECT NULL--",
        "1' AND '1'='1",
        "1' AND '1'='2"
    ]
    
    # Patrones de error SQL
    SQL_ERROR_PATTERNS = [
        r"SQL syntax.*MySQL",
        r"Warning.*mysql_.*",
        r"MySQLSyntaxErrorException",
        r"valid MySQL result",
        r"PostgreSQL.*ERROR",
        r"Warning.*pg_.*",
        r"valid PostgreSQL result",
        r"Npgsql\.",
        r"Driver.*SQL.*Server",
        r"OLE DB.*SQL Server",
        r"SQLServer JDBC Driver",
        r"SqlException",
        r"Oracle error",
        r"Oracle.*Driver",
        r"SQLite.*exception",
        r"SQLite3::SQLException"
    ]
    
    def __init__(self, http_client, reporter):
        self.http_client = http_client
        self.reporter = reporter
        self.vulnerabilities = []
    
    def scan(self, target_url: str) -> List[Dict]:
        """Escanear objetivo en busca de SQL Injection"""
        self.reporter.print_header(f"SQL INJECTION SCAN - {target_url}")
        self.vulnerabilities = []
        
        # Escanear parámetros GET
        self._scan_get_params(target_url)
        
        # Escanear formularios
        self._scan_forms(target_url)
        
        if self.vulnerabilities:
            self.reporter.print_warning(f"Encontradas {len(self.vulnerabilities)} posibles vulnerabilidades SQL Injection")
        else:
            self.reporter.print_success("No se detectaron vulnerabilidades SQL Injection evidentes")
        
        return self.vulnerabilities
    
    def _scan_get_params(self, url: str):
        """Escanear parámetros GET"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if not params:
            return
        
        self.reporter.print_info("Probando parámetros GET...")
        
        for param_name in params:
            for payload in self.SQL_PAYLOADS:
                test_params = params.copy()
                test_params[param_name] = [payload]
                
                # Reconstruir URL con payload
                new_query = urlencode(test_params, doseq=True)
                test_url = urlunparse((
                    parsed.scheme, parsed.netloc, parsed.path,
                    parsed.params, new_query, parsed.fragment
                ))
                
                response = self.http_client.get(test_url)
                if response and self._check_sql_error(response.text):
                    vuln = {
                        'type': 'SQL Injection',
                        'method': 'GET',
                        'parameter': param_name,
                        'payload': payload,
                        'url': test_url,
                        'details': f'Parámetro vulnerable: {param_name} con payload: {payload}'
                    }
                    self.vulnerabilities.append(vuln)
                    self.reporter.print_vulnerability('SQL Injection (GET)', vuln['details'])
    
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
            
            inputs = form.find_all('input')
            for payload in self.SQL_PAYLOADS[:3]:  # Limitar payloads en formularios
                form_data = {}
                for input_field in inputs:
                    input_name = input_field.get('name')
                    input_type = input_field.get('type', 'text')
                    
                    if not input_name:
                        continue
                    
                    if input_type == 'submit':
                        form_data[input_name] = input_field.get('value', 'submit')
                    else:
                        form_data[input_name] = payload
                
                if method == 'POST':
                    response = self.http_client.post(form_url, data=form_data)
                else:
                    response = self.http_client.get(form_url, params=form_data)
                
                if response and self._check_sql_error(response.text):
                    vuln = {
                        'type': 'SQL Injection',
                        'method': method,
                        'form_action': form_url,
                        'payload': payload,
                        'details': f'Formulario vulnerable en {form_url} con payload: {payload}'
                    }
                    self.vulnerabilities.append(vuln)
                    self.reporter.print_vulnerability('SQL Injection (Formulario)', vuln['details'])
                    break
    
    def _check_sql_error(self, response_text: str) -> bool:
        """Verificar si hay errores SQL en la respuesta"""
        for pattern in self.SQL_ERROR_PATTERNS:
            if re.search(pattern, response_text, re.IGNORECASE):
                return True
        return False


def main():
    """Función principal para ejecución standalone"""
    if len(sys.argv) < 2:
        print("Uso: python sql_injection.py <url>")
        sys.exit(1)
    
    from utils.http_client import HTTPClient
    from utils.reporter import Reporter
    
    target = sys.argv[1]
    client = HTTPClient()
    reporter = Reporter()
    
    scanner = SQLInjectionScanner(client, reporter)
    vulnerabilities = scanner.scan(target)
    
    client.close()
    
    if vulnerabilities:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
