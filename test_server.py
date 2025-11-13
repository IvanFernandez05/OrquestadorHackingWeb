#!/usr/bin/env python3
"""
Servidor de prueba simple para demostrar el orquestador

SOLO PARA PRUEBAS - Contiene vulnerabilidades intencionales
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os


class TestHandler(SimpleHTTPRequestHandler):
    """Handler personalizado para servir archivos de prueba"""
    
    def do_GET(self):
        """Manejar peticiones GET"""
        if self.path == '/' or self.path == '/index.html':
            self.path = '/test_vulnerable_page.html'
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def log_message(self, format, *args):
        """Sobrescribir para mostrar logs más limpios"""
        print(f"[REQUEST] {self.client_address[0]} - {args[0]}")


def main():
    """Iniciar servidor de prueba"""
    port = 8080
    
    # Cambiar al directorio del script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("=" * 80)
    print("SERVIDOR DE PRUEBA PARA ORQUESTADOR DE VULNERABILIDADES".center(80))
    print("=" * 80)
    print()
    print(f"⚠️  Este servidor contiene vulnerabilidades intencionales para pruebas")
    print(f"⚠️  NO usar en producción o exponer a internet")
    print()
    print(f"Servidor corriendo en: http://localhost:{port}")
    print(f"Página de prueba: http://localhost:{port}/")
    print()
    print("Para probar el orquestador en otra terminal:")
    print(f"  python orchestrator.py -u http://localhost:{port}/")
    print()
    print("Presiona Ctrl+C para detener el servidor")
    print("=" * 80)
    print()
    
    server = HTTPServer(('localhost', port), TestHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServidor detenido")
        server.shutdown()


if __name__ == '__main__':
    main()
