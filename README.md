# Sistema de Administración NAS con Django & uv

Este proyecto consiste en una plataforma de gestión y administración de almacenamiento en red (NAS) construida sobre una arquitectura robusta y moderna en Python. Permite la organización de archivos, gestión de almacenamiento y control de accesos mediante una interfaz web intuitiva, probada localmente sobre un ecosistema de contenedores.

---

## Tecnologías Principales

- **[Python 3.12](https://python.org):** Lenguaje base del proyecto, aprovechando las últimas mejoras de rendimiento y tipado estático.
- **[uv](https://astral.sh):** Administrador de paquetes de Python ultrarrápido escrito en Rust. Gestiona el entorno virtual, las herramientas y las dependencias a través de `pyproject.toml`.
- **[Django](https://djangoproject.com):** Framework web de alto nivel enfocado en la seguridad, escalabilidad y desarrollo limpio.
- **[django-filer](https://readthedocs.io):** Extensión especializada para Django que proporciona una estructura de archivos basada en carpetas, metadatos y control visual tipo NAS.
- **[django-storages](https://readthedocs.io):** Librería de abstracción para conectar el backend a diferentes sistemas de archivos, discos locales o protocolos de red (SMB, SFTP, AWS S3).
- **[Docker & Docker Compose](https://docker.com):** Infraestructura como código para empaquetar la aplicación Django y simular un servidor NAS Samba local en una red aislada.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado en tu sistema global:

- **[uv](https://astral.sh):** Gestor de paquetes de Python.
- **[Docker Desktop](https://docker.comproducts/docker-desktop/)** (incluye Docker Compose).

---

## Configuración del Proyecto (Entorno Local)

Si deseas realizar modificaciones o pruebas directamente en tu máquina sin Docker, `uv` autogestiona el entorno virtual:

### 1. Sincronizar Dependencias

```bash
uv sync
```

_Este comando leerá el archivo `pyproject.toml`, creará el entorno `.venv` y descargará los paquetes automáticamente._

### 2. Generar Archivo de Bloqueo

Antes de levantar el entorno Docker por primera vez, es obligatorio que exista el archivo de bloqueo de dependencias:

```bash
uv lock
```

---

## Infraestructura Docker (Entorno de Pruebas)

El proyecto cuenta con un archivo `docker-compose.yaml` que levanta dos servicios interconectados a través de una red bridge dedicada (`nas_network`):

1.  **`web` (Django):** Contenedor optimizado mediante compilación multi-etapa de `uv`.
2.  **`nas_server` (Samba):** Contenedor que simula un almacenamiento NAS en red local, persistido en la carpeta `./nas_storage` de tu máquina.

### 1. Construir y Levantar los Contenedores

Ejecuta el siguiente comando para compilar la imagen de Django y levantar el servidor NAS:

```bash
docker compose up --build
```

### 2. Aplicar Migraciones en el Contenedor

En una nueva terminal, crea las tablas necesarias en la base de datos interna de Django:

```bash
docker compose exec web python manage.py migrate
```

### 3. Crear Usuario Administrador

Genera tus credenciales de acceso para el panel de control web:

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Datos de Acceso y Redes

Una vez encendido el entorno, los servicios estarán disponibles en los siguientes puntos:

- **Interfaz Web Django:** [http://localhost:8000](http://localhost:8000)
- **Panel de Administración Django:** [http://localhost:8000/admin](http://localhost:8000/admin)

### Configuración de Red Interna (SMB / Samba NAS)

Para conectar Django con el servidor NAS simulado, debes utilizar las siguientes credenciales en tu configuración de almacenamiento:

- **Host del Servidor:** `nas_server` (gracias a la resolución de nombres en `nas_network`)
- **Puerto:** `445`
- **Usuario:** `nas_user`
- **Contraseña:** `nas_password`
- **Nombre del Recurso Compartido:** `shared_nas`

---

## Gestión de Dependencias (Para Desarrolladores)

Si necesitas agregar un nuevo paquete al proyecto, utiliza siempre el comando nativo de `uv` en tu terminal local. Esto mantendrá actualizado el archivo `pyproject.toml`:

```bash
uv add <nombre-del-paquete>
uv lock
```

_Recuerda reconstruir los contenedores con `docker compose up --build` después de agregar nuevas dependencias._
