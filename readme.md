# KickManager

Sistema web para gestión de un gimnasio de kickboxing. Permite registrar alumnos, controlar asistencia a clases, y gestionar cobros por clase individual o mensualidad.

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.11 + FastAPI + SQLAlchemy + Alembic |
| Base de datos | PostgreSQL 15 |
| Frontend | React 18 + Vite + Bootstrap 5 |
| Infraestructura | Docker + Docker Compose |

## Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) y Docker Compose v2
- Git

## Inicio rápido

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd cobro_clases

# 2. Copiar variables de entorno
cp .env.example .env

# 3. Levantar todos los servicios
docker compose up --build
```

La primera vez Docker construirá las imágenes y ejecutará las migraciones automáticamente.

| Servicio | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Docs API (Swagger) | http://localhost:8000/docs |
| Base de datos | localhost:5432 |

## Crear el primer usuario

No se requiere autenticación para crear el primer usuario:

```bash
curl -X POST http://localhost:8000/api/v1/usuarios \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Luego ingresa con esas credenciales en http://localhost:3000.

## Variables de entorno

El archivo `.env.example` contiene todos los valores por defecto para desarrollo local. Para producción, genera una clave secreta segura:

```bash
openssl rand -hex 32
```

| Variable | Descripción | Default |
|----------|-------------|---------|
| `POSTGRES_DB` | Nombre de la base de datos | `kickmanager` |
| `POSTGRES_USER` | Usuario de PostgreSQL | `kickuser` |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL | `kickpassword` |
| `SECRET_KEY` | Clave secreta para JWT | *(cambiar en prod)* |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token de sesión | `480` |
| `VITE_API_URL` | URL del backend desde el frontend | `http://localhost:8000/api/v1` |

## Comandos útiles

```bash
# Ver logs de un servicio específico
docker compose logs -f backend
docker compose logs -f frontend

# Detener todos los servicios
docker compose down

# Detener y eliminar volúmenes (borra la base de datos)
docker compose down -v

# Reconstruir solo el backend
docker compose up --build backend
```

## Desarrollo sin Docker

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Requiere PostgreSQL corriendo localmente con los datos del .env
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Estructura del proyecto

```
cobro_clases/
├── backend/
│   ├── app/
│   │   ├── db/          # Configuración de base de datos y modelos
│   │   ├── routers/     # Endpoints: alumnos, clases, pagos, usuarios, auth
│   │   ├── schemas/     # Esquemas Pydantic
│   │   └── services/    # Lógica de negocio
│   ├── migrations/      # Migraciones Alembic
│   └── tests/
├── frontend/
│   └── src/
├── specs/               # Especificaciones de features
├── docker-compose.yml
└── .env.example
```

## Funcionalidades

- **Alumnos** — registro, edición y desactivación con historial conservado
- **Clases** — creación de sesiones y registro de asistencia
- **Pagos** — cobro por clase individual o mensualidad
- **Usuarios** — gestión de acceso con autenticación JWT
- **Auditoría** — log de operaciones del sistema
