# Cheatsheet - Orquestador de Hacking Web

## 🚀 Comandos Rápidos

### Instalación
```bash
pip install -r requirements.txt
```

### Uso Básico
```bash
# Escaneo completo de una URL
python orchestrator.py -u http://target.com

# Ver escáneres disponibles
python orchestrator.py --list-scanners

# Ver ayuda
python orchestrator.py --help
```

### Escáneres Específicos
```bash
# Solo SQL Injection
python orchestrator.py -u http://target.com -s sql

# Solo XSS
python orchestrator.py -u http://target.com -s xss

# Solo CSRF
python orchestrator.py -u http://target.com -s csrf

# Solo Auth Bypass
python orchestrator.py -u http://target.com -s auth

# Solo Directory Traversal
python orchestrator.py -u http://target.com -s traversal

# Múltiples escáneres
python orchestrator.py -u http://target.com -s sql xss csrf

# Todos los escáneres
python orchestrator.py -u http://target.com -s all
```

### Múltiples Objetivos
```bash
# Usar configuración de config.json
python orchestrator.py

# Con archivo de configuración personalizado
python orchestrator.py -c mi_config.json
```

### Escáneres Individuales
```bash
# SQL Injection
python scanners/sql_injection.py http://target.com

# XSS
python scanners/xss_scanner.py http://target.com

# CSRF
python scanners/csrf_scanner.py http://target.com

# Auth Bypass
python scanners/auth_bypass.py http://target.com

# Directory Traversal
python scanners/directory_traversal.py http://target.com
```

### Servidor de Prueba
```bash
# Iniciar servidor (Terminal 1)
python test_server.py

# Escanear servidor local (Terminal 2)
python orchestrator.py -u http://localhost:8080/
```

## 📝 Configuración (config.json)

```json
{
  "targets": [
    {
      "name": "Nombre Descriptivo",
      "url": "http://192.168.1.100:3000",
      "enabled": true
    }
  ],
  "timeout": 10,
  "max_retries": 3,
  "output_format": "console"
}
```

## 🎯 Tipos de Vulnerabilidades

| Escáner | Código | Descripción |
|---------|--------|-------------|
| SQL Injection | `sql` | Inyección de código SQL |
| XSS | `xss` | Cross-Site Scripting |
| CSRF | `csrf` | Cross-Site Request Forgery |
| Auth Bypass | `auth` | Bypass de autenticación |
| Directory Traversal | `traversal` | Acceso no autorizado a archivos |

## 📊 Interpretación de Resultados

| Símbolo | Significado |
|---------|-------------|
| 🔵 `[INFO]` | Información general |
| ✅ `[✓]` | Éxito / Sin vulnerabilidades |
| ⚠️ `[!]` | Vulnerabilidad encontrada |
| ❌ `[✗]` | Error |

## 💡 Tips Rápidos

### Guardar Resultados
```bash
# Guardar en archivo
python orchestrator.py -u http://target.com > resultados.txt 2>&1

# Con timestamp
python orchestrator.py -u http://target.com > "scan_$(date +%Y%m%d_%H%M%S).txt" 2>&1
```

### Verificar Conectividad
```bash
# Con curl
curl http://target.com

# Con Python
python -c "import requests; print(requests.get('http://target.com').status_code)"
```

### Escaneo Rápido vs Completo
```bash
# Rápido (solo CSRF, ~10 segundos)
python orchestrator.py -u http://target.com -s csrf

# Completo (todos los escáneres, ~2-5 minutos)
python orchestrator.py -u http://target.com
```

## 🔧 Solución de Problemas

### Error: "No module named 'bs4'"
```bash
pip install beautifulsoup4
```

### Error: "No se pudo conectar"
1. Verifica que el servidor esté corriendo
2. Verifica la URL (incluye `http://` o `https://`)
3. Verifica firewall/red
4. Aumenta timeout en `config.json`

### Escaneo Muy Lento
```bash
# Usar escáneres específicos
python orchestrator.py -u http://target.com -s csrf

# Reducir timeout en config.json
{
  "timeout": 5,
  "max_retries": 2
}
```

## 📚 Archivos de Documentación

| Archivo | Propósito |
|---------|-----------|
| `README.md` | Documentación general |
| `TUTORIAL.md` | Tutorial completo paso a paso |
| `GUIA_RAPIDA.md` | Guía de referencia rápida |
| `CHEATSHEET.md` | Este archivo - referencia de comandos |
| `example_usage.py` | Ejemplos de código |

## 🔗 Flujo de Trabajo Típico

```bash
# 1. Verificar conectividad
curl http://target.com

# 2. Escaneo rápido inicial
python orchestrator.py -u http://target.com -s csrf

# 3. Escaneo completo
python orchestrator.py -u http://target.com

# 4. Guardar resultados
python orchestrator.py -u http://target.com > reporte.txt 2>&1

# 5. Verificar manualmente en navegador
```

## ⚠️ Recordatorios Importantes

- ✅ **SÍ**: Usar en aplicaciones con permiso
- ✅ **SÍ**: Reportar vulnerabilidades encontradas
- ✅ **SÍ**: Verificar manualmente los resultados
- ❌ **NO**: Usar en sitios públicos sin autorización
- ❌ **NO**: Explotar vulnerabilidades más allá de la detección
- ❌ **NO**: Modificar/eliminar datos

## 📞 Ayuda

Para más información, consulta:
- `TUTORIAL.md` - Tutorial completo
- `python orchestrator.py --help` - Ayuda de comandos
- `python orchestrator.py --list-scanners` - Lista de escáneres

---

**Versión**: 1.0 | **Última actualización**: 2025
