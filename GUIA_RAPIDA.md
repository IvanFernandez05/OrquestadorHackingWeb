# Guía Rápida de Uso

## Inicio Rápido

### 1. Instalación

```bash
# Clonar el repositorio
git clone https://github.com/IvanFernandez05/OrquestadorHackingWeb.git
cd OrquestadorHackingWeb

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Prueba Rápida

```bash
# Terminal 1: Iniciar servidor de prueba
python test_server.py

# Terminal 2: Ejecutar orquestador
python orchestrator.py -u http://localhost:8080/
```

## Escenarios de Uso

### Escanear un Objetivo Específico

```bash
# Escaneo completo
python orchestrator.py -u http://target.com

# Solo SQL Injection
python orchestrator.py -u http://target.com -s sql

# SQL Injection y XSS
python orchestrator.py -u http://target.com -s sql xss
```

### Escanear Múltiples Objetivos

Edita `config.json`:

```json
{
  "targets": [
    {
      "name": "App del Compañero 1",
      "url": "http://192.168.1.100:3000",
      "enabled": true
    },
    {
      "name": "App del Compañero 2",
      "url": "http://192.168.1.101:8080",
      "enabled": true
    }
  ],
  "timeout": 10,
  "max_retries": 3,
  "output_format": "console"
}
```

Luego ejecuta:

```bash
python orchestrator.py
```

### Usar Escáneres Individuales

```bash
# SQL Injection
python scanners/sql_injection.py http://target.com

# XSS
python scanners/xss_scanner.py http://target.com

# CSRF
python scanners/csrf_scanner.py http://target.com

# Bypass de Autenticación
python scanners/auth_bypass.py http://target.com

# Directory Traversal
python scanners/directory_traversal.py http://target.com
```

## Interpretación de Resultados

### Códigos de Color

- 🔵 **[INFO]** - Información general
- ✓ **[✓]** (Verde) - Operación exitosa o sin vulnerabilidades
- ⚠️ **[!]** (Amarillo) - Advertencia o vulnerabilidad encontrada
- ✗ **[✗]** (Rojo) - Error o vulnerabilidad crítica

### Tipos de Vulnerabilidades

1. **SQL Injection**
   - Busca errores SQL en respuestas
   - Prueba payloads comunes en formularios y parámetros GET

2. **XSS (Cross-Site Scripting)**
   - Verifica si el input se refleja sin sanitizar
   - Prueba scripts maliciosos en formularios

3. **CSRF (Cross-Site Request Forgery)**
   - Detecta formularios POST sin tokens CSRF
   - Busca campos hidden con tokens de protección

4. **Authentication Bypass**
   - Prueba credenciales por defecto comunes
   - Intenta bypass mediante SQL Injection

5. **Directory Traversal**
   - Busca parámetros que aceptan rutas de archivo
   - Intenta acceder a archivos del sistema

## Consejos para el Equipo

### Para el Hacker Ético (Tu Rol)

1. **Primero escanea individualmente**: Usa escáneres específicos para entender cada vulnerabilidad
2. **Documenta todo**: Guarda logs de los escaneos
3. **Comunica responsablemente**: Informa a tus compañeros de forma constructiva
4. **Verifica manualmente**: Los escáneres automáticos pueden tener falsos positivos

### Flujo de Trabajo Recomendado

```bash
# Paso 1: Verificar conectividad
python orchestrator.py -u http://target.com -s csrf

# Paso 2: Escaneo completo
python orchestrator.py -u http://target.com

# Paso 3: Revisar vulnerabilidades encontradas

# Paso 4: Verificar manualmente con navegador/herramientas

# Paso 5: Documentar y reportar al equipo
```

### Para los Compañeros del Equipo

1. **Crea vulnerabilidades obvias primero**: Facilita el aprendizaje
2. **Documenta qué vulnerabilidades incluiste**: Ayuda a validar los escáneres
3. **Itera**: Arregla las vulnerabilidades encontradas y vuelve a probar

## Personalización

### Añadir Nuevos Payloads

Edita los archivos en `scanners/`:

```python
# En scanners/sql_injection.py
SQL_PAYLOADS = [
    "'",
    "' OR '1'='1",
    # Añade tus payloads aquí
    "tu_payload_personalizado"
]
```

### Ajustar Timeouts

En `config.json`:

```json
{
  "timeout": 30,      // Tiempo de espera por petición
  "max_retries": 5    // Número de reintentos
}
```

## Solución de Problemas

### No se Detectan Vulnerabilidades

1. Verifica que el servidor objetivo esté corriendo
2. Revisa que la URL sea correcta (incluye http:// o https://)
3. Aumenta el timeout en `config.json`
4. Prueba manualmente que la vulnerabilidad existe

### Errores de Conexión

```bash
# Verifica conectividad básica
curl http://target.com

# Verifica que Python tenga acceso a red
python -c "import requests; print(requests.get('http://target.com').status_code)"
```

### El Escáner es Muy Lento

1. Reduce el número de payloads en cada escáner
2. Usa escáneres específicos en lugar del orquestador completo
3. Ajusta `timeout` y `max_retries` en config.json

## Recursos Adicionales

- **OWASP Top 10**: https://owasp.org/Top10/
- **PortSwigger Web Security Academy**: https://portswigger.net/web-security
- **HackTheBox**: https://www.hackthebox.com/

## Soporte

Para preguntas o problemas:
1. Revisa esta guía y el README.md
2. Consulta el código de ejemplo en `example_usage.py`
3. Contacta al equipo

---

**Recuerda**: Estas herramientas son para uso educativo en entornos controlados. Siempre obtén autorización antes de escanear cualquier sistema.
