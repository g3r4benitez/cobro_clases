# Implementation Plan: Sistema de Gestión de Cobro de Clases Kickboxing

**Branch**: `001-kickboxing-management` | **Date**: 2026-04-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-kickboxing-management/spec.md`

## Summary

Sistema web de gestión de cobro de clases de kickboxing. Permite registrar alumnos, clases,
asistencia y dos modalidades de pago (por clase individual o mensual). Incluye consultas de
clases impagas, historial de pagos y reportes por fecha. Monorepo con frontend React+Bootstrap,
backend FastAPI+Python y base de datos PostgreSQL, orquestado con Docker Compose.

## Technical Context

**Language/Version**: Python 3.11+ (backend), Node.js 20+ / React 18 (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLAlchemy 2.x, Alembic, pydantic v2, python-jose, passlib[bcrypt], uvicorn, asyncpg
- Frontend: React 18, Vite, Bootstrap 5, React Router v6, Axios
**Storage**: PostgreSQL 15+
**Testing**: pytest + httpx (backend), Vitest (frontend, opcional)
**Target Platform**: Web (desktop + móvil), Docker Compose (local/VPS)
**Project Type**: Web application (monorepo — backend API + frontend SPA)
**Performance Goals**: Respuesta < 3 segundos para cualquier consulta en uso normal
**Constraints**: Interfaz operable desde móvil; sin integración de pago electrónico en v1
**Scale/Scope**: Decenas de alumnos, cientos de clases/pagos; un administrador concurrente

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Estado | Verificación |
|-----------|--------|--------------|
| I. Registro Centralizado de Alumnos | ✅ PASS | Tabla `alumnos` con unicidad, datos editables solo por usuarios autenticados |
| II. Gestión de Pagos (clase/mensual) | ✅ PASS | Tablas `pagos_clase` y `pagos_mensual`; pagos se anulan, no se eliminan |
| III. Control de Asistencia | ✅ PASS | Tabla `asistencias` vinculada a alumno y clase; base para cálculo de impagas |
| IV. Interfaz Web Simple | ✅ PASS | Bootstrap 5 responsive; flujos de asistencia y pago diseñados para ≤3 clics |
| V. Simplicidad y Mantenibilidad | ✅ PASS | Lógica de impagas en capa de servicio; arquitectura routers→services→ORM |
| Data & Privacy | ✅ PASS | bcrypt para contraseñas; auth JWT; sin exposición de datos sin login |
| Development Workflow | ✅ PASS | Migraciones Alembic; spec antes de implementación; MVP incremental por US |

**Resultado**: Todas las gates pasan. Sin violaciones justificadas. Proceder.

## Project Structure

### Documentation (this feature)

```text
specs/001-kickboxing-management/
├── plan.md              # Este archivo
├── research.md          # Decisiones tecnológicas
├── data-model.md        # Esquema de base de datos
├── quickstart.md        # Guía de levantamiento
├── contracts/
│   └── api.md           # Contratos REST API
└── tasks.md             # (generado por /speckit-tasks)
```

### Source Code (repository root)

```text
cobro_clases/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── db/
│   │   │   ├── base.py          # Engine, SessionLocal, Base
│   │   │   └── models.py        # Modelos ORM SQLAlchemy
│   │   ├── schemas/             # Pydantic schemas (request/response)
│   │   │   ├── alumnos.py
│   │   │   ├── clases.py
│   │   │   ├── pagos.py
│   │   │   ├── asistencia.py
│   │   │   └── usuarios.py
│   │   ├── routers/             # Endpoints FastAPI
│   │   │   ├── auth.py
│   │   │   ├── usuarios.py
│   │   │   ├── alumnos.py
│   │   │   ├── clases.py
│   │   │   ├── asistencia.py
│   │   │   ├── pagos.py
│   │   │   └── auditoria.py
│   │   └── services/            # Lógica de negocio
│   │       ├── auth.py
│   │       ├── alumnos.py
│   │       ├── clases.py
│   │       ├── pagos.py
│   │       └── auditoria.py
│   ├── migrations/
│   │   └── versions/
│   ├── tests/
│   ├── alembic.ini
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── api/                 # Clientes Axios por dominio
│   │   │   ├── client.js        # Instancia Axios + interceptors JWT
│   │   │   ├── alumnos.js
│   │   │   ├── clases.js
│   │   │   └── pagos.js
│   │   ├── components/          # Componentes Bootstrap reutilizables
│   │   │   ├── Navbar.jsx
│   │   │   ├── AlertMessage.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   └── pages/
│   │       ├── Login/
│   │       │   └── LoginPage.jsx
│   │       ├── Alumnos/
│   │       │   ├── AlumnosPage.jsx
│   │       │   └── AlumnoForm.jsx
│   │       ├── Clases/
│   │       │   ├── ClasesPage.jsx
│   │       │   └── AsistenciaPage.jsx
│   │       ├── Pagos/
│   │       │   ├── PagoClasePage.jsx
│   │       │   └── PagoMensualPage.jsx
│   │       └── Reportes/
│   │           ├── ImpagarPage.jsx
│   │           └── ReportePage.jsx
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── .env.example
└── specs/
```

**Structure Decision**: Opción 2 (Web application). Backend en `backend/`, frontend en `frontend/`,
orquestados desde raíz con `docker-compose.yml`. Cada servicio tiene su propio Dockerfile.

## Complexity Tracking

> No hay violaciones al Constitution Check. Sin justificaciones requeridas.
