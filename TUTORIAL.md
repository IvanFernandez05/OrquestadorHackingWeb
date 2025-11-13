# Tutorial Completo - Orquestador de Hacking Web

## 📚 Índice

1. [Introducción](#introducción)
2. [Instalación Paso a Paso](#instalación-paso-a-paso)
3. [Primera Prueba - Tutorial Básico](#primera-prueba---tutorial-básico)
4. [Uso Avanzado](#uso-avanzado)
5. [Escenarios Prácticos](#escenarios-prácticos)
6. [Entendiendo los Resultados](#entendiendo-los-resultados)
7. [Consejos y Mejores Prácticas](#consejos-y-mejores-prácticas)

---

## Introducción

Este orquestador es una herramienta para realizar pruebas de seguridad en aplicaciones web. Te permite detectar vulnerabilidades comunes como:

- 🔓 **SQL Injection** - Inyección de código SQL
- 🚨 **XSS** - Cross-Site Scripting
- 🔐 **CSRF** - Cross-Site Request Forgery
- 👤 **Auth Bypass** - Bypass de autenticación
- 📁 **Directory Traversal** - Acceso no autorizado a archivos

---

## Instalación Paso a Paso

### Paso 1: Requisitos Previos

Necesitas tener instalado:
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

Verifica tu versión de Python:
```bash
python --version
# o
python3 --version
```

### Paso 2: Descargar el Proyecto

```bash
# Opción 1: Clonar con git
git clone https://github.com/IvanFernandez05/OrquestadorHackingWeb.git
cd OrquestadorHackingWeb

# Opción 2: Descargar como ZIP
# Ve a https://github.com/IvanFernandez05/OrquestadorHackingWeb
# Click en "Code" > "Download ZIP"
# Descomprime y navega a la carpeta
```

### Paso 3: Instalar Dependencias

```bash
# Instalar las librerías necesarias
pip install -r requirements.txt

# Si usas Python 3 específicamente:
pip3 install -r requirements.txt
```

### Paso 4: Verificar Instalación

```bash
# Verificar que el orquestador funciona
python orchestrator.py --help
```

Si ves el menú de ayuda, ¡todo está listo! 🎉

---

## Primera Prueba - Tutorial Básico

### Escenario: Probar el orquestador con el servidor de prueba

Esta es la forma más fácil de empezar y entender cómo funciona.

#### Paso 1: Abrir Dos Terminales

Necesitarás dos ventanas de terminal/consola:
- **Terminal 1**: Para el servidor de prueba
- **Terminal 2**: Para ejecutar el orquestador

#### Paso 2: Iniciar el Servidor de Prueba

En la **Terminal 1**:
```bash
cd OrquestadorHackingWeb
python test_server.py
```

Verás algo como:
```
================================================================================
            SERVIDOR DE PRUEBA PARA ORQUESTADOR DE VULNERABILIDADES             
================================================================================

⚠️  Este servidor contiene vulnerabilidades intencionales para pruebas
⚠️  NO usar en producción o exponer a internet

Servidor corriendo en: http://localhost:8080
Página de prueba: http://localhost:8080/
```

**¡No cierres esta terminal!** El servidor debe seguir ejecutándose.

#### Paso 3: Ejecutar tu Primer Escaneo

En la **Terminal 2**:
```bash
cd OrquestadorHackingWeb
python orchestrator.py -u http://localhost:8080/
```

#### Paso 4: Ver los Resultados

Verás una salida con colores mostrando:
- 🔵 **[INFO]** - Información sobre el escaneo
- ✅ **[✓]** - Conexión exitosa y escaneos sin problemas
- ⚠️ **[!]** - Vulnerabilidades encontradas
- ❌ **[✗]** - Errores

Ejemplo de salida:
```
================================================================================
                      ORQUESTADOR DE VULNERABILIDADES WEB                       
================================================================================

[INFO] URL: http://localhost:8080/
[✓] Conectado exitosamente (Status: 200)

[VULNERABILIDAD] CSRF
  → Formulario POST sin token CSRF en http://localhost:8080/login

Total de vulnerabilidades encontradas: 2
```

#### Paso 5: Detener el Servidor

Cuando termines, en la **Terminal 1** presiona `Ctrl+C` para detener el servidor.

---

## Uso Avanzado

### 1. Escanear Solo Vulnerabilidades Específicas

Si solo quieres buscar ciertos tipos de vulnerabilidades:

```bash
# Solo SQL Injection
python orchestrator.py -u http://localhost:8080/ -s sql

# Solo CSRF
python orchestrator.py -u http://localhost:8080/ -s csrf

# SQL Injection y XSS
python orchestrator.py -u http://localhost:8080/ -s sql xss

# Todos los escáneres (equivalente a no especificar -s)
python orchestrator.py -u http://localhost:8080/ -s all
```

### 2. Ver Escáneres Disponibles

```bash
python orchestrator.py --list-scanners
```

Salida:
```
Escáneres disponibles:
  sql       - SQL Injection
  xss       - Cross-Site Scripting (XSS)
  csrf      - Cross-Site Request Forgery (CSRF)
  auth      - Authentication Bypass
  traversal - Directory Traversal
  all       - Todos los escáneres
```

### 3. Configurar Múltiples Objetivos

Para escanear varios sitios automáticamente:

#### Paso 1: Editar `config.json`

```json
{
  "targets": [
    {
      "name": "Aplicación del Compañero 1",
      "url": "http://192.168.1.100:3000",
      "enabled": true
    },
    {
      "name": "Aplicación del Compañero 2",
      "url": "http://192.168.1.101:8080",
      "enabled": true
    },
    {
      "name": "Mi Aplicación Local",
      "url": "http://localhost:4000",
      "enabled": false
    }
  ],
  "timeout": 10,
  "max_retries": 3,
  "output_format": "console"
}
```

**Nota**: `"enabled": false` significa que ese objetivo se omitirá.

#### Paso 2: Ejecutar sin especificar URL

```bash
python orchestrator.py
```

El orquestador escaneará todos los objetivos que tengan `"enabled": true`.

### 4. Usar Escáneres Individuales

Puedes ejecutar cada escáner por separado:

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

Esto es útil cuando:
- Quieres enfocarte en un tipo específico de vulnerabilidad
- Necesitas resultados más rápidos
- Estás depurando un problema específico

---

## Escenarios Prácticos

### Escenario 1: Probar la Aplicación de un Compañero

Tu compañero Juan tiene una aplicación web en `http://192.168.1.50:3000`

#### Paso 1: Verificar Conectividad
```bash
# Primero verifica que puedes conectarte
curl http://192.168.1.50:3000
# o abre en tu navegador
```

#### Paso 2: Escaneo Rápido (Solo CSRF)
```bash
python orchestrator.py -u http://192.168.1.50:3000 -s csrf
```

#### Paso 3: Escaneo Completo
```bash
python orchestrator.py -u http://192.168.1.50:3000
```

#### Paso 4: Documentar Resultados
Guarda la salida en un archivo:
```bash
python orchestrator.py -u http://192.168.1.50:3000 > resultados_juan.txt 2>&1
```

### Escenario 2: Escanear Todas las Aplicaciones del Equipo

#### Paso 1: Crear Configuración del Equipo

Edita `config.json`:
```json
{
  "targets": [
    {
      "name": "App de Juan - Login",
      "url": "http://192.168.1.50:3000",
      "enabled": true
    },
    {
      "name": "App de María - E-commerce",
      "url": "http://192.168.1.51:8080",
      "enabled": true
    },
    {
      "name": "App de Pedro - Blog",
      "url": "http://192.168.1.52:5000",
      "enabled": true
    },
    {
      "name": "App de Ana - Admin Panel",
      "url": "http://192.168.1.53:4000",
      "enabled": true
    }
  ],
  "timeout": 15,
  "max_retries": 3
}
```

#### Paso 2: Ejecutar Escaneo Masivo
```bash
python orchestrator.py
```

Esto escaneará todas las aplicaciones una por una.

### Escenario 3: Investigar una Vulnerabilidad Específica

Encontraste que la app de Juan tiene una posible SQL Injection.

#### Paso 1: Escanear Solo SQL
```bash
python scanners/sql_injection.py http://192.168.1.50:3000
```

#### Paso 2: Verificar Manualmente
- Abre la aplicación en tu navegador
- Busca los formularios mencionados en el reporte
- Intenta los payloads reportados manualmente
- Documenta el comportamiento

### Escenario 4: Modo de Desarrollo Iterativo

Mientras tu compañero arregla vulnerabilidades:

```bash
# Ejecutar cada 30 segundos
while true; do
  clear
  echo "Escaneando... $(date)"
  python orchestrator.py -u http://192.168.1.50:3000 -s csrf
  sleep 30
done
```

Presiona `Ctrl+C` para detener el loop.

---

## Entendiendo los Resultados

### Tipos de Mensajes

#### 1. Mensajes Informativos [INFO]
```
[INFO] URL: http://localhost:8080/
[INFO] Probando parámetros GET...
[INFO] Analizando 5 formulario(s)...
```
**Qué significa**: El orquestador está informando qué está haciendo.

#### 2. Mensajes de Éxito [✓]
```
[✓] Conectado exitosamente (Status: 200)
[✓] No se detectaron vulnerabilidades SQL Injection evidentes
```
**Qué significa**: La operación fue exitosa o no se encontraron vulnerabilidades de ese tipo.

#### 3. Advertencias [!]
```
[!] Encontradas 2 posibles vulnerabilidades CSRF
```
**Qué significa**: Se encontraron vulnerabilidades que debes revisar.

#### 4. Vulnerabilidades [VULNERABILIDAD]
```
[VULNERABILIDAD] CSRF
  → Formulario POST sin token CSRF en http://localhost:8080/login
```
**Qué significa**: Detalles específicos de una vulnerabilidad encontrada.

#### 5. Errores [✗]
```
[✗] No se pudo conectar a http://target.com
```
**Qué significa**: Hubo un problema (conexión, timeout, etc.).

### Interpretación por Tipo de Vulnerabilidad

#### SQL Injection
```
[VULNERABILIDAD] SQL Injection (GET)
  → Parámetro vulnerable: id con payload: ' OR '1'='1
```
**Qué hacer**:
1. Ve a la URL reportada
2. El parámetro `id` acepta SQL sin validar
3. Prueba manualmente: `http://target.com/user?id=' OR '1'='1`
4. Si ves un error SQL o comportamiento extraño, la vulnerabilidad es real

#### XSS (Cross-Site Scripting)
```
[VULNERABILIDAD] XSS Reflejado (GET)
  → Parámetro vulnerable: search refleja contenido sin sanitizar
```
**Qué hacer**:
1. El parámetro `search` muestra tu input sin filtros
2. Intenta: `http://target.com/search?search=<script>alert('XSS')</script>`
3. Si aparece una alerta, hay XSS real

#### CSRF (Cross-Site Request Forgery)
```
[VULNERABILIDAD] CSRF
  → Formulario POST sin token CSRF en http://localhost:8080/login
```
**Qué hacer**:
1. Inspecciona el formulario de login
2. Busca campos `<input type="hidden" name="csrf_token">`
3. Si no hay token, el formulario es vulnerable a CSRF

#### Authentication Bypass
```
[VULNERABILIDAD] Credenciales por Defecto
  → Credenciales por defecto funcionan: admin/admin
```
**Qué hacer**:
1. Es una vulnerabilidad crítica
2. Las credenciales admin/admin funcionan
3. Reporta inmediatamente al compañero

#### Directory Traversal
```
[VULNERABILIDAD] Directory Traversal (GET)
  → Parámetro vulnerable: file permite lectura de archivos con: ../../etc/passwd
```
**Qué hacer**:
1. El parámetro `file` permite acceder a archivos del sistema
2. Prueba: `http://target.com/view?file=../../etc/passwd`
3. Si ves contenido del archivo, es vulnerable

### Resumen Final

Al final de cada escaneo verás:
```
================================================================================
                               RESUMEN DE ESCANEO                               
================================================================================

Total de vulnerabilidades encontradas: 3

SQL Injection: 1 vulnerabilidad(es)
  - SQL Injection: Parámetro vulnerable: id con payload: '

CSRF: 2 vulnerabilidad(es)
  - Missing CSRF Token: Formulario POST sin token CSRF en http://localhost:8080/login
  - Missing CSRF Token: Formulario POST sin token CSRF en http://localhost:8080/comment
```

**Interpreta esto como**:
- **Total encontradas**: Número de problemas detectados
- **Por tipo**: Desglose de cada tipo de vulnerabilidad
- **Detalles**: Información específica para investigar

---

## Consejos y Mejores Prácticas

### Para el Hacker Ético

#### 1. Workflow Recomendado
```
1. Conectividad → 2. Escaneo Rápido → 3. Escaneo Completo → 4. Verificación Manual → 5. Reporte
```

Ejemplo:
```bash
# 1. Verificar que funciona
curl http://target.com

# 2. Escaneo rápido (CSRF es rápido)
python orchestrator.py -u http://target.com -s csrf

# 3. Escaneo completo
python orchestrator.py -u http://target.com

# 4. Revisar vulnerabilidades manualmente en navegador

# 5. Crear reporte para el compañero
```

#### 2. Documentación

Crea un archivo de resultados:
```bash
# Guardar resultados con timestamp
python orchestrator.py -u http://target.com > "reporte_$(date +%Y%m%d_%H%M%S).txt" 2>&1
```

#### 3. No Seas Destructivo

- ❌ **NO** intentes explotar vulnerabilidades más allá de la detección
- ❌ **NO** modifiques datos en las bases de datos
- ❌ **NO** elimines archivos
- ✅ **SÍ** reporta todo lo que encuentres
- ✅ **SÍ** documenta los pasos para reproducir
- ✅ **SÍ** ayuda a tus compañeros a entender y arreglar

#### 4. Comunicación Efectiva

Cuando reportes a un compañero:
```
✅ BIEN:
"Hola Juan, encontré que tu formulario de login no tiene protección CSRF.
Está en http://192.168.1.50:3000/login
Para reproducir: [pasos]
Te sugiero añadir un token CSRF en el formulario."

❌ MAL:
"Tu app está llena de bugs."
```

### Para los Compañeros del Equipo

#### 1. Prepara tu Aplicación

Antes de que te escaneen:
```bash
# Asegúrate de que tu app esté corriendo
# Verifica que sea accesible desde otras máquinas
# Documenta qué vulnerabilidades incluiste intencionalmente
```

#### 2. Facilita el Escaneo

- Proporciona la URL completa: `http://192.168.1.50:3000`
- Indica páginas importantes: `/login`, `/admin`, `/search`
- Comparte credenciales de prueba si es necesario

#### 3. Responde a los Reportes

Cuando recibas un reporte:
1. Agradece al hacker ético
2. Verifica la vulnerabilidad
3. Arregla el problema
4. Pide un re-escaneo para confirmar

### Solución de Problemas Comunes

#### Problema: "No se pudo conectar"
```
[✗] No se pudo conectar a http://target.com
```

**Soluciones**:
```bash
# 1. Verifica que el servidor esté corriendo
curl http://target.com

# 2. Verifica la URL (incluye http:// o https://)
python orchestrator.py -u http://target.com  # ✅
python orchestrator.py -u target.com         # ❌

# 3. Verifica firewall/permisos de red

# 4. Aumenta el timeout en config.json
{
  "timeout": 30,  # Aumenta de 10 a 30
  "max_retries": 5
}
```

#### Problema: "No detecta vulnerabilidades que sé que existen"

**Soluciones**:
1. Los escáneres automáticos no son perfectos
2. Verifica manualmente
3. Prueba el escáner individual:
```bash
python scanners/sql_injection.py http://target.com
```
4. Revisa que la vulnerabilidad sea del tipo que estás escaneando

#### Problema: "Es muy lento"

**Soluciones**:
```bash
# 1. Escanea solo lo necesario
python orchestrator.py -u http://target.com -s csrf  # Más rápido

# 2. Reduce payloads (edita scanners/*.py)
# 3. Ajusta timeouts más bajos en config.json
{
  "timeout": 5,      # Reduce timeout
  "max_retries": 2   # Reduce reintentos
}
```

#### Problema: "Muchos falsos positivos"

**Solución**: Los escáneres automáticos pueden reportar falsos positivos. Siempre:
1. Verifica manualmente cada vulnerabilidad reportada
2. Usa tu criterio
3. Si no estás seguro, pregunta al equipo

### Personalización Avanzada

#### Añadir Tus Propios Payloads

Edita `scanners/sql_injection.py`:
```python
SQL_PAYLOADS = [
    "'",
    "' OR '1'='1",
    # Añade tus payloads personalizados aquí:
    "' UNION SELECT NULL, version()--",
    "admin'--",
    # etc.
]
```

#### Crear Tu Propio Escáner

Mira `scanners/csrf_scanner.py` como ejemplo y crea uno nuevo:
```python
# scanners/mi_escaner.py
class MiEscaner:
    def __init__(self, http_client, reporter):
        self.http_client = http_client
        self.reporter = reporter
    
    def scan(self, target_url):
        # Tu lógica aquí
        pass
```

---

## Recursos Adicionales

### Aprender Más Sobre Vulnerabilidades Web

- **OWASP Top 10**: https://owasp.org/Top10/
  - Lista de las 10 vulnerabilidades más críticas
  
- **PortSwigger Web Security Academy**: https://portswigger.net/web-security
  - Tutoriales interactivos gratuitos
  
- **HackTheBox**: https://www.hackthebox.com/
  - Máquinas virtuales para practicar

### Herramientas Complementarias

- **Burp Suite**: Proxy para interceptar peticiones HTTP
- **OWASP ZAP**: Escáner de vulnerabilidades open source
- **Postman**: Para probar APIs manualmente

### Documentación del Proyecto

- `README.md` - Documentación general
- `GUIA_RAPIDA.md` - Referencia rápida
- `example_usage.py` - Ejemplos de código

---

## Preguntas Frecuentes (FAQ)

### ¿Puedo usar esto en sitios web públicos?

**NO.** Solo usa estas herramientas en:
- Aplicaciones de tu equipo con permiso
- Tu propio servidor local
- Entornos de prueba autorizados

Usar herramientas de hacking sin autorización es **ilegal**.

### ¿Qué hago si encuentro una vulnerabilidad real?

1. No la explotes más allá de confirmar que existe
2. Documenta todo (URL, pasos, evidencia)
3. Reporta inmediatamente al responsable
4. Ayuda a arreglarla si puedes

### ¿Los resultados son 100% confiables?

No. Los escáneres automáticos pueden tener:
- **Falsos positivos**: Reporta vulnerabilidades que no existen
- **Falsos negativos**: No detecta vulnerabilidades que sí existen

Siempre verifica manualmente.

### ¿Puedo contribuir al proyecto?

¡Sí! Puedes:
- Añadir más escáneres
- Mejorar los existentes
- Reportar bugs
- Mejorar documentación

---

## Conclusión

Ahora estás listo para usar el Orquestador de Hacking Web. Recuerda:

✅ Usa las herramientas de forma ética
✅ Comunica tus hallazgos de forma constructiva
✅ Aprende de cada escaneo
✅ Ayuda a tu equipo a mejorar la seguridad

**¡Buena suerte en tu proyecto de equipo!** 🚀

---

## Soporte

¿Necesitas ayuda?
1. Revisa este tutorial y `GUIA_RAPIDA.md`
2. Consulta el código de ejemplo en `example_usage.py`
3. Pregunta a tu equipo
4. Abre un issue en GitHub

---

**Última actualización**: 2025
**Versión del tutorial**: 1.0
