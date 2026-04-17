# Implementation Plan: Migrar base de datos a SQLite

**Branch**: `003-sqlite-migration` | **Date**: 2026-04-15 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `/specs/003-sqlite-migration/spec.md`

## Summary

Migrar el motor de base de datos de PostgreSQL (asyncpg) a SQLite (aiosqlite) para eliminar la dependencia de infraestructura externa en desarrollo local. La URL de conexión pasa a ser configurable via `DATABASE_URL`; el default es SQLite. PostgreSQL sigue siendo soportado para producción. Las migraciones Alembic se adaptan para compatibilidad con ambos motores. No hay cambios en el modelo de dominio ni en la API.

## Technical Context

**Language/Version**: Python 3.11 (backend) / Node.js 20 + React 18 (frontend)  
**Primary Dependencies**: FastAPI 0.109+, SQLAlchemy 2.0, Alembic 1.13, asyncpg (PostgreSQL), aiosqlite (SQLite — nuevo)  
**Storage**: SQLite (nuevo default) / PostgreSQL (producción, opcional)  
**Testing**: pytest  
**Target Platform**: Linux server / desarrollo local sin Docker  
**Project Type**: Web service (FastAPI + React SPA)  
**Performance Goals**: Sin cambios (uso personal de instructor de kickboxing)  
**Constraints**: Sin cambios al modelo de dominio ni a la API REST  
**Scale/Scope**: Usuario único / pequeño equipo; base de datos local

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Estado | Observaciones |
|-----------|--------|---------------|
| I. Registro Centralizado de Alumnos | ✅ PASS | Sin cambios en el modelo de alumnos |
| II. Gestión de Pagos | ✅ PASS | Sin cambios en el modelo de pagos |
| III. Control de Asistencia | ✅ PASS | Sin cambios en el modelo de asistencia |
| IV. Interfaz Web Simple y Operativa | ✅ PASS | Sin impacto en frontend |
| V. Simplicidad y Mantenibilidad | ✅ PASS | Reduce dependencias externas (elimina PostgreSQL+Docker para desarrollo) |
| Datos & Privacidad | ✅ PASS | Sin cambios en autenticación ni almacenamiento de contraseñas |
| Migraciones versionadas | ⚠️ ATENCIÓN | SQLite también usa Alembic (`alembic upgrade head`). Se adaptan las migraciones existentes para compatibilidad cruzada. No se bypass Alembic. |

**Veredicto**: PASS — sin violaciones. La adaptación de migraciones preserva el principio de versionado.

## Project Structure

### Documentation (this feature)

```text
specs/003-sqlite-migration/
├── plan.md              # Este archivo
├── research.md          # Decisiones técnicas y compatibilidad
├── data-model.md        # Cambios en capa de persistencia
├── quickstart.md        # Guía de inicio sin Docker
└── tasks.md             # Phase 2 output (/speckit.tasks — pendiente)
```

### Source Code (repository root)

```text
backend/
├── app/
│   └── db/
│       └── base.py          # MODIFICAR: DATABASE_URL env var + PRAGMA FK SQLite
├── migrations/
│   ├── env.py               # MODIFICAR: leer DATABASE_URL en lugar de POSTGRES_*
│   └── versions/
│       └── 0001_initial_schema.py  # MODIFICAR: boolean defaults true→1, false→0
├── alembic.ini              # MODIFICAR: url placeholder → sqlite default
├── requirements.txt         # MODIFICAR: agregar aiosqlite>=0.20.0
└── .env.example             # MODIFICAR: DATABASE_URL como variable principal

.env.example (raíz)          # MODIFICAR: agregar DATABASE_URL
.gitignore                   # MODIFICAR: agregar *.db
docker-compose.yml           # MODIFICAR: servicio db como opcional con comentario

frontend/                    # SIN CAMBIOS
```

**Structure Decision**: Aplicación web (backend/frontend separados). Cambios exclusivamente en `backend/` y archivos de configuración en la raíz.

## Phase 0: Research

**Completado** — ver [research.md](research.md)

Resoluciones clave:
- Driver async SQLite: `aiosqlite>=0.20.0` → URL `sqlite+aiosqlite:///./kickmanager.db`
- Variable única `DATABASE_URL` reemplaza variables `POSTGRES_*` individuales
- Boolean defaults en migración 0001: `"true"` → `"1"`, `"false"` → `"0"`
- Alembic async funciona con SQLite sin cambios estructurales en `env.py`
- `PRAGMA foreign_keys = ON` debe activarse por conexión en SQLite
- Tipos `Numeric`, `Date`, `DateTime`, `CheckConstraint` → todos compatibles con SQLite

## Phase 1: Design & Contracts

**Completado** — ver [data-model.md](data-model.md), [quickstart.md](quickstart.md)

- **data-model.md**: Documenta compatibilidad de tipos y cambios exactos en migration 0001
- **quickstart.md**: Guía de inicio en < 2 min sin Docker
- **contracts/**: No aplica — esta feature no modifica la API REST ni introduce nuevas interfaces
- **Agent context**: Actualizado via `update-agent-context.sh`

## Implementation Steps

Los siguientes pasos deben ejecutarse en orden para la implementación (serán detallados en `tasks.md` por `/speckit.tasks`):

### Paso 1 — Dependencias (`backend/requirements.txt`)
Agregar `aiosqlite>=0.20.0`. Mantener `asyncpg>=0.29.0` (usado en producción con PostgreSQL).

### Paso 2 — Configuración de base de datos (`backend/app/db/base.py`)
- Reemplazar construcción de URL PostgreSQL por lectura de `DATABASE_URL` con default SQLite
- Agregar `connect_args={"check_same_thread": False}` para SQLite
- Registrar listener `@event.listens_for(engine.sync_engine, "connect")` para activar `PRAGMA foreign_keys = ON` cuando el dialecto sea SQLite

### Paso 3 — Alembic env.py (`backend/migrations/env.py`)
- Reemplazar construcción de URL desde variables `POSTGRES_*` por lectura de `DATABASE_URL`
- Mantener el mismo default SQLite del paso 2

### Paso 4 — alembic.ini (`backend/alembic.ini`)
- Actualizar `sqlalchemy.url` al default SQLite (se overridea en `env.py` de todas formas)

### Paso 5 — Migración 0001 (`backend/migrations/versions/0001_initial_schema.py`)
- Reemplazar `sa.text("true")` → `sa.text("1")` en columnas `activo` (usuarios, alumnos)
- Reemplazar `sa.text("false")` → `sa.text("0")` en columnas `anulado` (pagos_clase, pagos_mensual)

### Paso 6 — Variables de entorno (`.env.example`)
- Reemplazar variables `POSTGRES_*` de BD por `DATABASE_URL=sqlite+aiosqlite:///./kickmanager.db`
- Mantener `SECRET_KEY` y `ACCESS_TOKEN_EXPIRE_MINUTES`
- Agregar comentario con la URL PostgreSQL para referencia de producción

### Paso 7 — Gitignore
- Agregar `*.db` y `*.db-shm`, `*.db-wal` a `.gitignore` (raíz del repositorio)

### Paso 8 — docker-compose.yml
- Agregar comentario indicando que el servicio `db` es opcional cuando se usa SQLite
- El servicio `backend` debe recibir `DATABASE_URL` como variable de entorno

### Paso 9 — Verificación
- Ejecutar `alembic upgrade head` con SQLite y confirmar que todas las tablas se crean
- Ejecutar tests del backend: `cd backend && pytest`
- Verificar que `asyncpg` sigue funcionando si `DATABASE_URL` apunta a PostgreSQL
