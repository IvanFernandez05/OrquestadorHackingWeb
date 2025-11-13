# OrquestadorHackingWeb

Herramientas de orquestación y scripts para pruebas de seguridad web (Ethical Hacking).

## Descripción

Este proyecto contiene un conjunto de herramientas y scripts diseñados para facilitar las pruebas de seguridad en aplicaciones web. Está pensado para el rol de hacker ético en un equipo de 5 personas donde cada miembro desarrolla páginas web con diferentes vulnerabilidades.

## Características

- **Escáneres de Vulnerabilidades**:
  - Inyección SQL
  - Cross-Site Scripting (XSS)
  - Cross-Site Request Forgery (CSRF)
  - Bypass de Autenticación
  - Directory Traversal
  
- **Orquestador Principal**: Coordina y ejecuta múltiples escáneres de forma automática
- **Sistema de Configuración**: Gestión centralizada de objetivos y parámetros
- **Reportes Detallados**: Salida en consola con código de colores

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/IvanFernandez05/OrquestadorHackingWeb.git
cd OrquestadorHackingWeb
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Configuración

Edita el archivo `config.json` para añadir tus objetivos:

```json
{
  "targets": [
    {
      "name": "Aplicación de Prueba",
      "url": "http://localhost:3000",
      "enabled": true
    }
  ],
  "timeout": 10,
  "max_retries": 3,
  "output_format": "console"
}
```

### Ejecutar el Orquestador

Para escanear todos los objetivos configurados:

```bash
python orchestrator.py
```

### Ejecutar Escáneres Individuales

Cada escáner puede ejecutarse de forma independiente:

```bash
# Escaneo de SQL Injection
python scanners/sql_injection.py http://target.com

# Escaneo de XSS
python scanners/xss_scanner.py http://target.com

# Escaneo de CSRF
python scanners/csrf_scanner.py http://target.com

# Prueba de bypass de autenticación
python scanners/auth_bypass.py http://target.com

# Escaneo de directory traversal
python scanners/directory_traversal.py http://target.com
```

## Estructura del Proyecto

```
OrquestadorHackingWeb/
├── orchestrator.py          # Orquestador principal
├── config.json              # Configuración de objetivos
├── requirements.txt         # Dependencias Python
├── scanners/                # Módulos de escaneo
│   ├── __init__.py
│   ├── sql_injection.py
│   ├── xss_scanner.py
│   ├── csrf_scanner.py
│   ├── auth_bypass.py
│   └── directory_traversal.py
└── utils/                   # Utilidades comunes
    ├── __init__.py
    ├── http_client.py       # Cliente HTTP con reintentos
    └── reporter.py          # Sistema de reportes
```

## Advertencias

⚠️ **USO ÉTICO SOLAMENTE**: Estas herramientas están diseñadas exclusivamente para pruebas de seguridad autorizadas en entornos controlados. El uso no autorizado de estas herramientas contra sistemas que no te pertenecen es ilegal.

## Licencia

Este proyecto es para fines educativos y de práctica en un entorno controlado.