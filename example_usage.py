#!/usr/bin/env python3
"""
Ejemplo de uso del orquestador de vulnerabilidades web

Este script muestra cómo usar el orquestador programáticamente
"""
from utils.http_client import HTTPClient
from utils.reporter import Reporter
from scanners.sql_injection import SQLInjectionScanner
from scanners.xss_scanner import XSSScanner
from scanners.csrf_scanner import CSRFScanner


def ejemplo_basico():
    """Ejemplo básico de escaneo"""
    print("=" * 80)
    print("EJEMPLO 1: Escaneo básico de una URL".center(80))
    print("=" * 80 + "\n")
    
    # Configurar cliente y reporter
    client = HTTPClient(timeout=10, max_retries=3)
    reporter = Reporter()
    
    # URL de ejemplo (localhost)
    target_url = "http://localhost:8080"
    
    reporter.print_info(f"Escaneando: {target_url}")
    
    # Probar conectividad
    response = client.get(target_url)
    if not response:
        reporter.print_error("No se pudo conectar al objetivo")
        reporter.print_info("Asegúrate de que el servidor esté corriendo")
        client.close()
        return
    
    reporter.print_success(f"Conectado (Status: {response.status_code})")
    
    # Ejecutar escáneres
    print("\n1. Escaneando SQL Injection...")
    sql_scanner = SQLInjectionScanner(client, reporter)
    sql_vulns = sql_scanner.scan(target_url)
    
    print("\n2. Escaneando XSS...")
    xss_scanner = XSSScanner(client, reporter)
    xss_vulns = xss_scanner.scan(target_url)
    
    print("\n3. Escaneando CSRF...")
    csrf_scanner = CSRFScanner(client, reporter)
    csrf_vulns = csrf_scanner.scan(target_url)
    
    # Resumen
    total_vulns = len(sql_vulns) + len(xss_vulns) + len(csrf_vulns)
    print(f"\n{'=' * 80}")
    print(f"Total vulnerabilidades encontradas: {total_vulns}")
    print(f"  - SQL Injection: {len(sql_vulns)}")
    print(f"  - XSS: {len(xss_vulns)}")
    print(f"  - CSRF: {len(csrf_vulns)}")
    print(f"{'=' * 80}\n")
    
    client.close()


def ejemplo_personalizado():
    """Ejemplo de escaneo personalizado"""
    print("\n" + "=" * 80)
    print("EJEMPLO 2: Escaneo personalizado con configuración".center(80))
    print("=" * 80 + "\n")
    
    # Lista de objetivos
    objetivos = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://192.168.1.100"
    ]
    
    # Configurar
    client = HTTPClient(timeout=5, max_retries=2)
    reporter = Reporter()
    
    reporter.print_info("Escaneando múltiples objetivos...")
    
    for objetivo in objetivos:
        reporter.print_header(f"Objetivo: {objetivo}")
        
        # Verificar conectividad
        response = client.get(objetivo)
        if not response:
            reporter.print_warning(f"No se pudo conectar a {objetivo}")
            continue
        
        reporter.print_success("Conectado")
        
        # Escanear solo SQL Injection para este ejemplo
        scanner = SQLInjectionScanner(client, reporter)
        vulns = scanner.scan(objetivo)
        
        if vulns:
            reporter.print_warning(f"Encontradas {len(vulns)} vulnerabilidades")
        else:
            reporter.print_success("Sin vulnerabilidades evidentes")
    
    client.close()


def main():
    """Función principal"""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              EJEMPLOS DE USO - ORQUESTADOR HACKING WEB                    ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Este script contiene ejemplos de cómo usar el orquestador programáticamente.
Para ejecutar el orquestador desde línea de comandos, usa:

    python orchestrator.py -u http://target.com

Para más información:
    python orchestrator.py --help
    
""")
    
    print("NOTA: Los ejemplos a continuación requieren que tengas servidores")
    print("      web corriendo en las URLs especificadas.\n")
    
    respuesta = input("¿Deseas ejecutar los ejemplos? (s/n): ")
    
    if respuesta.lower() == 's':
        try:
            ejemplo_basico()
            ejemplo_personalizado()
        except KeyboardInterrupt:
            print("\n\nEjecución interrumpida por el usuario")
        except Exception as e:
            print(f"\n\nError: {e}")
    else:
        print("\nEjemplos cancelados. Revisa el código fuente para ver cómo funciona.")


if __name__ == '__main__':
    main()
