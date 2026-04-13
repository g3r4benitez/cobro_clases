# Quickstart: Sistema de Gestión de Cobro de Clases Kickboxing

**Feature**: 001-kickboxing-management
**Date**: 2026-04-08

## Prerequisitos

- Docker y Docker Compose v2 instalados.
- Git.
- Puerto 3000 (frontend), 8000 (backend) y 5432 (PostgreSQL) disponibles.

## Levantar el entorno con Docker Compose

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd cobro_clases

# 2. Copiar variables de entorno
cp .env.example .env
# Editar .env con los valores deseados (ver sección Variables de Entorno)

# 3. Levantar todos los servicios
docker compose up --build

# Backend disponible en: http://localhost:8000
# API docs (Swagger): http://localhost:8000/docs
# Frontend disponible en: http://localhost:3000
```

## Variables de Entorno (.env)

```env
# Base de datos
POSTGRES_DB=kickmanager
POSTGRES_USER=kickuser
POSTGRES_PASSWORD=kickpassword
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Backend
SECRET_KEY=cambiar_esto_en_produccion
ACCESS_TOKEN_EXPIRE_MINUTES=480

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
```

## Estructura de Carpetas

```text
cobro_clases/
├── backend/
│   ├── app/
│   │   ├── main.py              # Punto de entrada FastAPI
│   │   ├── db/
│   │   │   ├── base.py          # SQLAlchemy engine y session
│   │   │   └── models.py        # Modelos ORM
│   │   ├── schemas/             # Esquemas Pydantic (request/response)
│   │   ├── routers/             # Endpoints HTTP por dominio
│   │   │   ├── auth.py
│   │   │   ├── usuarios.py
│   │   │   ├── alumnos.py
│   │   │   ├── clases.py
│   │   │   ├── asistencia.py
│   │   │   ├── pagos.py
│   │   │   └── auditoria.py
│   │   └── services/            # Lógica de negocio
│   │       ├── alumnos.py
│   │       ├── clases.py
│   │       ├── pagos.py
│   │       └── auditoria.py
│   ├── migrations/              # Alembic migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── main.jsx             # Punto de entrada React
│   │   ├── App.jsx
│   │   ├── api/                 # Clientes de API (fetch/axios)
│   │   ├── components/          # Componentes reutilizables Bootstrap
│   │   └── pages/               # Páginas/vistas principales
│   │       ├── Alumnos/
│   │       ├── Clases/
│   │       ├── Pagos/
│   │       └── Reportes/
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── .env.example
└── specs/
```

## Crear el primer usuario administrador

```bash
# Una vez que el backend esté corriendo
curl -X POST http://localhost:8000/api/v1/usuarios \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "tu_contraseña"}'

# Nota: el primer usuario se crea sin autenticación.
# Los siguientes requieren token JWT.
```

## Validación Manual del Sistema

### Flujo completo de prueba

```bash
# 1. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d '{"username":"admin","password":"tu_contraseña"}'
# → Guardar access_token

TOKEN="<access_token_aquí>"

# 2. Crear alumno
curl -X POST http://localhost:8000/api/v1/alumnos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan","apellido":"Pérez","edad":25,"telefono":"11-1234-5678"}'

# 3. Crear clase para hoy
curl -X POST http://localhost:8000/api/v1/clases \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fecha":"2026-04-08"}'

# 4. Registrar asistencia (alumno_id=1, clase_id=1)
curl -X POST http://localhost:8000/api/v1/clases/1/asistencia \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"alumno_ids":[1]}'

# 5. Verificar clases impagas del alumno (debe aparecer clase_id=1)
curl http://localhost:8000/api/v1/pagos/alumno/1/impagas \
  -H "Authorization: Bearer $TOKEN"

# 6. Registrar pago por clase
curl -X POST http://localhost:8000/api/v1/pagos/clase \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"alumno_id":1,"clase_id":1,"monto":1500,"fecha_pago":"2026-04-08"}'

# 7. Verificar impagas de nuevo (debe estar vacío)
curl http://localhost:8000/api/v1/pagos/alumno/1/impagas \
  -H "Authorization: Bearer $TOKEN"
```

## Correr Migraciones Manualmente

```bash
# Dentro del contenedor backend
docker compose exec backend alembic upgrade head

# Crear nueva migración después de cambiar modelos
docker compose exec backend alembic revision --autogenerate -m "descripcion"
```

## Acceder a Swagger UI

Navegar a `http://localhost:8000/docs` para explorar y probar todos los endpoints con
autenticación integrada.
