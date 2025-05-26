# Back - Mantainer Web Hook

## Descripción

Un backend encargado de leer y actualizar un archivo JSON que almacena la configuración y el estado de los hooks de mantenimiento.

## Configuración

El archivo `config.json` debe tener la siguiente estructura y campos:

```jsonc
{
  "apiKey"         : "TU_API_KEY",     // Clave para autenticar solicitudes al API
  "hooksFilePath"  : "./alerted-users.json",   // Ruta al archivo JSON que contiene los hooks
  "schemaFilePath" : "./schema.json",  // Ruta al esquema JSON para validación
  "logFilePath"    : "./logs/app.log", // Ruta al archivo de log principal
  "logMaxSizeMB"   : 50,                // Tamaño máximo (en MB) del archivo de log antes de rotación
  "dev"            : false,             // Flag para habilitar /docs de FastAPI solo en entorno de desarrollo
  "cors"           : ["valores", "de", "los", "cors"] // Lista de orígenes permitidos para CORS (solo en modo producción)
}
```

### Esquema JSON por Defecto

El archivo referenciado por `schema.json` debe definir la estructura y las reglas de validación de los hooks. Por defecto, debe existir siempre la siguiente sección inmutable:

```json
{
  "list": [
    { "name": "Matias Araya", "phone": "+56950997093" }
  ]
}
```

Además, puede contener otras secciones (por ejemplo, `gerencia`, `lideresdev`, `syt`, etc.), cada una de ellas como un array de objetos con la forma:

```json
"seccion": [
  { "name": "Nombre Apellido", "phone": "+569XXXXXXXX" }
]
```

* La sección `list` es **inmutable** (no podrá modificarse ni eliminarse).
* Las demás secciones son **mutables**, pueden no existir o tener cero, uno o varios objetos.
* Cada objeto dentro de cualquier sección siempre debe disponer de las propiedades `name` y `phone`.

## Requisitos Funcionales

* **RF-0 (Carga de Configuración)**: Al iniciar, el sistema debe leer el archivo `config.json`, validar su estructura y cargar todos los parámetros de configuración necesarios para el funcionamiento.
* **RF-1 (Lectura de Usuarios Alertados)**: El sistema debe exponer un endpoint `GET /alerted-users` que devuelva el contenido actual del archivo `alerted-users.json`.
* **RF-2 (Actualización de Usuarios Alertados)**: El sistema debe exponer un endpoint `POST /alerted-users` que reciba un payload JSON y actualice el archivo `alerted-users.json` con los nuevos datos.
* **RF-3 (Validación de Esquema)**: Antes de aplicar cambios, el sistema debe validar la estructura y los tipos de datos del JSON conforme a un esquema predefinido, rechazando solicitudes inválidas.
* **RF-4 (Control de Concurrencia)**: El sistema debe asegurar acceso exclusivo al archivo JSON durante operaciones de escritura para evitar condiciones de carrera.
* **RF-5 (Registro de Operaciones)**: Todas las operaciones de lectura y escritura deben registrarse en un log con nivel de detalle suficiente (usuario, timestamp, acción realizada).
* **RF-6 (Backup del JSON en Log)**: El sistema debe crear un respaldo del contenido completo del archivo JSON y registrar esa copia en el log en una sola línea por operación.
* **RF-7 (Documentación de API en Dev)**: El sistema debe exponer la documentación interactiva de FastAPI (`/docs` y `/redoc`) únicamente cuando el flag `dev` esté configurado en `true` en `config.json`. Si `dev` es `false`, estas rutas deben estar deshabilitadas.

* **RF-8 (Manejo de CORS)**: El sistema debe gestionar el CORS según el entorno:
  - En modo desarrollo (`dev = true`), deshabilitar cualquier política de CORS.
  - En modo producción (`dev = false`), habilitar CORS usando los orígenes definidos en la propiedad `"cors"` del `config.json`.

## Requisitos No Funcionales

* **RNF-1 (Operatividad)**: El sistema debe ejecutarse continuamente, priorizando la disponibilidad y el manejo de errores sobre la velocidad de respuesta. En caso de conflicto, se debe garantizar que la aplicación no falle incluso si implica sacrificar rendimiento temporal.
* **RNF-2 (Seguridad)**: Todos los endpoints deben requerir autenticación y autorización adecuadas. El archivo JSON de configuración debe cifrarse en reposo y validarse para prevenir inyecciones o manipulación no autorizada.
* **RNF-3 (Monitorización)**: Debe exponer un endpoint de health check (`GET /health`) para verificar el estado del servicio. Los logs serán estructurados en JSON, detallando nivel, timestamp y metadatos de contexto.
* **RNF-4 (Portabilidad)**: Debe poder ejecutarse en entornos Linux y Windows mediante Docker, sin modificaciones en el código.

## Tecnologías

* **Lenguajes**: Python
* **Frameworks/Librerías**: FastAPI&#x20;
* **Base de Datos**: Archivo JSON local
* **Contenedores**: Docker, Docker Compose
* **Herramientas de Logging**:

  * **Loguru**: librería para Python que ofrece una API sencilla, soporta logging estructurado (JSON), rotación de archivos y configuración mínima.
* **Control de Versiones**: Git. El proyecto forma parte de un repositorio más grande, por lo que solo contiene el archivo `.gitignore`. La gestión de versiones se realiza en el monorepo global.

## Flujos de Trabajo / Arquitectura

### Flujo Principal de Usuarios Alertados

1. Cliente envía `GET /alerted-users`.
2. El servidor lee el archivo `alerted-users.json` y retorna su contenido.
3. Cliente envía `POST /alerted-users` con nuevo payload.
4. El servidor valida el JSON contra el esquema (`schema.json`).
5. El servidor crea backup en log y actualiza `alerted-users.json`.
6. Se retorna confirmación de éxito o error.

### Flujo de Health Check

1. Cliente envía `GET /health` al servicio.
2. El servidor verifica:

   * La configuración (`config.json`) se haya cargado correctamente.
   * El archivo de usuarios alertados (`alerted-users.json`) sea accesible y no esté bloqueado.
3. El servidor recopila métricas internas: estado de la aplicación, uptime y timestamp.
4. El servidor crea una respuesta JSON con campos:

   ```jsonc
   {
     "status": "ok",       // o "error" si falla alguna verificación
     "uptime": 12345,        // tiempo en segundos desde el arranque
     "timestamp": "2025-05-24T23:59:59Z"
   }
   ```
5. Se retorna HTTP 200 para `status: ok`, o HTTP 500 si `status: error`.

### Control de Concurrencia

* Uso de un mutex (o lock de archivo) para operaciones de escritura.
* Lecturas pueden hacerse en paralelo.

## Instalación

## Estructura de Archivos del Proyecto

```plaintext
app/
├── logs/
│   └── app.log
├── routers/
│   ├── __init__.py
│   └── alerted_users.py
├── alerted-users.json
├── config.json
├── config.py
├── main.py
├── models.py
├── schema.json
├── schema.json.example
├── services.py
├── __init__.py
.gitignore
alerted-user.json.example
config.json.example
Dockerfile
Dockerfile.dev
ia.md
README.md
requirements.txt
```

- **app/**: Carpeta principal del backend.
  - **logs/app.log**: Archivo de logs principal.
  - **routers/**: Módulos de rutas/endpoints.
    - **alerted_users.py**: Endpoints para usuarios alertados.
    - **__init__.py**: Inicialización del módulo de rutas.
  - **alerted-users.json**: Archivo con los datos de usuarios alertados.
  - **config.json**: Configuración principal de la app.
  - **config.py**: Lógica para cargar y validar la configuración.
  - **main.py**: Punto de entrada de la aplicación FastAPI.
  - **models.py**: Modelos de datos internos.
  - **schema.json**: Esquema de validación para los datos.
  - **services.py**: Lógica de negocio y servicios principales.
  - **__init__.py**: Inicialización del módulo principal.
- **.gitignore**: Exclusiones de git.
- **alerted-user.json.example**: Ejemplo de archivo de usuarios alertados.
- **config.json.example**: Ejemplo de archivo de configuración.  
  Ejemplo:
  ```jsonc
  {
    "apiKey": "TU_API_KEY",
    "hooksFilePath": "./alerted-users.json",
    "schemaFilePath": "./schema.json",
    "logFilePath": "./logs/app.log",
    "logMaxSizeMB": 50,
    "dev": false,
    "cors": ["https://frontend.com", "https://otro-origen.com"]
  }
  ```
- **Dockerfile**: Docker para producción.
- **Dockerfile.dev**: Docker para desarrollo.
- **ia.md**: Instrucciones para el LLM.
- **README.md**: Documentación general.
- **requirements.txt**: Dependencias del proyecto.
