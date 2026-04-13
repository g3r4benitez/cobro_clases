# Research: Sistema de Gestión de Cobro de Clases Kickboxing

**Feature**: 001-kickboxing-management
**Date**: 2026-04-08

## Technology Stack Decisions

### Frontend

**Decision**: React.js + Bootstrap 5 + CSS personalizado
**Rationale**: El usuario especificó explícitamente React.js, HTML, CSS y Bootstrap. Bootstrap 5
proporciona componentes responsive listos para uso móvil, alineado con el requisito mobile-first
de la constitución. React permite gestión de estado eficiente para formularios y listas dinámicas.
**Alternatives considered**: Vue.js, Angular — descartados por preferencia explícita del usuario.

### Backend

**Decision**: Python 3.11+ con FastAPI
**Rationale**: El usuario especificó Python y FastAPI. FastAPI ofrece validación automática de
datos via Pydantic, documentación OpenAPI generada automáticamente (Swagger UI), y soporte nativo
para async/await. Ideal para APIs REST.
**Alternatives considered**: Django REST Framework — descartado por preferencia explícita.

### Base de Datos

**Decision**: PostgreSQL 15+
**Rationale**: El usuario especificó PostgreSQL. Soporta integridad referencial (foreign keys),
transacciones ACID críticas para registros de pagos, y tipos de dato DATE/TIMESTAMP necesarios
para el modelo de clases y pagos mensuales.
**Alternatives considered**: MySQL, SQLite — descartados por preferencia explícita.

### ORM / Migrations

**Decision**: SQLAlchemy 2.x (ORM) + Alembic (migraciones)
**Rationale**: Stack estándar en el ecosistema FastAPI+PostgreSQL. SQLAlchemy 2.x con soporte async
mejora el rendimiento. Alembic gestiona migraciones versionadas tal como exige el workflow de la
constitución.
**Alternatives considered**: Tortoise ORM — compatible pero menor adopción y documentación.

### Autenticación

**Decision**: JWT (JSON Web Tokens) con python-jose + passlib (bcrypt)
**Rationale**: FastAPI tiene soporte nativo para OAuth2 con JWT. bcrypt para hashing de contraseñas
tal como exige la constitución (Principio V — Data & Privacy Standards). Tokens en header
Authorization: Bearer, sin cookies de sesión (más simple para API REST).
**Alternatives considered**: Sesiones con Redis — mayor infraestructura sin beneficio para este
caso de uso.

### Contenedores

**Decision**: Docker + Docker Compose v2
**Rationale**: El usuario especificó Docker. Docker Compose permite orquestar los tres servicios
(frontend, backend, db) con un único `docker-compose up`. Configuración con variables de entorno
(.env) para separar configuración de código.
**Services**: `db` (PostgreSQL), `backend` (FastAPI + uvicorn), `frontend` (Node dev server o
nginx para producción).

### Estructura del Monorepo

**Decision**: Raíz del repo con carpetas `frontend/` y `backend/` separadas
**Rationale**: El usuario especificó monorepo con frontend y backend en carpetas separadas. Cada
servicio tiene su propio Dockerfile. `docker-compose.yml` en la raíz orquesta ambos.

```
cobro_clases/
├── backend/
├── frontend/
├── docker-compose.yml
├── .env.example
└── specs/
```

### Manejo de Pagos Mensuales vs. Impagas

**Decision**: Lógica en capa de servicio (backend)
**Rationale**: La evaluación de "clase impaga" requiere cruzar asistencias con pagos por clase y
pagos mensuales. Esta lógica DEBE residir en un servicio (Principio V de la constitución), no en
la base de datos ni en el frontend. Query: clases con asistencia del alumno donde NO existe pago
por clase NI pago mensual que cubra ese mes.

### Auditoría

**Decision**: Campo `created_by` (FK a usuarios) en cada entidad mutable + tabla audit_log
**Rationale**: FR-015 requiere registrar qué usuario realizó cada operación. Se usa una tabla
`audit_log` con acción, entidad, usuario y timestamp para trazabilidad completa.

### Comunicación Frontend-Backend

**Decision**: REST API sobre HTTP, CORS configurado para desarrollo local
**Rationale**: FastAPI genera automáticamente documentación OpenAPI. El frontend React consume la
API via fetch/axios. CORS habilitado en desarrollo para permitir puerto separado (3000 → 8000).

## Best Practices Aplicadas

- Variables de entorno para credenciales de base de datos (nunca hardcodeadas).
- Migraciones versionadas con Alembic; nunca modificar schema directamente.
- Validación de datos en schemas Pydantic (backend) y validación client-side en formularios React.
- Separación clara: routers (HTTP) → services (lógica de negocio) → repositories/ORM (datos).
- Respuestas de error HTTP estándar (400, 401, 404, 409, 422) con mensajes descriptivos.
- Paginación en listados que pueden crecer (historial de pagos, listado de alumnos).
