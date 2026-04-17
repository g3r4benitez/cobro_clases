# Tasks: Migrar base de datos a SQLite

**Input**: Design documents from `/specs/003-sqlite-migration/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, quickstart.md ✅

**Tests**: No se solicitaron tareas TDD — las validaciones son manuales (ejecutar alembic + iniciar server).

**Organization**: Tareas agrupadas por historia de usuario para implementación y prueba independiente.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo (archivos distintos, sin dependencias incompletas)
- **[Story]**: Historia de usuario a la que pertenece la tarea (US1, US2, US3)

---

## Phase 1: Setup (Infraestructura compartida)

**Purpose**: Agregar dependencia y actualizar control de versiones. Sin dependencias — pueden ejecutarse en paralelo.

- [x] T001 [P] Agregar `aiosqlite>=0.20.0` en `backend/requirements.txt` (línea después de `asyncpg`)
- [x] T002 [P] Agregar `*.db`, `*.db-shm` y `*.db-wal` al `.gitignore` en la raíz del repositorio

---

## Phase 2: Foundational (Prereq bloqueante)

**Purpose**: Corregir incompatibilidad de defaults booleanos en la migración antes de que cualquier historia pueda probarse.

**⚠️ CRITICAL**: Ninguna historia de usuario puede verificarse hasta completar esta fase.

- [x] T003 Corregir `server_default` booleanos en `backend/migrations/versions/0001_initial_schema.py`: reemplazar `sa.text("true")` → `sa.text("1")` en columnas `activo` de tablas `usuarios` y `alumnos`; reemplazar `sa.text("false")` → `sa.text("0")` en columnas `anulado` de tablas `pagos_clase` y `pagos_mensual`

**Checkpoint**: Migración compatible con SQLite. Las historias de usuario pueden iniciarse.

---

## Phase 3: User Story 1 — Aplicación funciona con SQLite sin configuración externa (Priority: P1) 🎯 MVP

**Goal**: El backend arranca y opera completamente usando SQLite como único requisito de base de datos.

**Independent Test**: Iniciar el backend sin variables `POSTGRES_*` definidas, ejecutar `alembic upgrade head` y verificar que `GET /health` responde `{"status": "ok"}` y que las operaciones CRUD funcionan.

### Implementation for User Story 1

- [x] T004 [US1] Reescribir `backend/app/db/base.py`: leer `DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./kickmanager.db")`; agregar `connect_args={"check_same_thread": False}` para SQLite; registrar listener `@event.listens_for(engine.sync_engine, "connect")` que ejecuta `PRAGMA foreign_keys=ON` cuando el dialecto es SQLite
- [x] T005 [US1] Actualizar `backend/migrations/env.py`: reemplazar la construcción de URL desde variables `POSTGRES_*` (líneas 17-25) por `DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./kickmanager.db")` y aplicarla con `config.set_main_option("sqlalchemy.url", DATABASE_URL)`
- [x] T006 [US1] Actualizar `backend/alembic.ini`: cambiar `sqlalchemy.url` en la sección `[alembic]` a `sqlite+aiosqlite:///./kickmanager.db` (valor placeholder — se sobreescribe en `env.py` en runtime)
- [x] T007 [US1] Validar manualmente: desde `backend/`, ejecutar `DATABASE_URL=sqlite+aiosqlite:///./kickmanager.db alembic upgrade head`; confirmar que se crea `kickmanager.db` y que `uvicorn app.main:app --port 8000` arranca sin errores

**Checkpoint**: US1 completa — backend funcional con SQLite, sin PostgreSQL ni Docker.

---

## Phase 4: User Story 2 — Esquema inicializado automáticamente (Priority: P2)

**Goal**: Al iniciar la aplicación, el esquema completo se crea sin intervención manual.

**Independent Test**: Eliminar `kickmanager.db`, ejecutar `sh backend/entrypoint.sh` y confirmar que todas las tablas existen y la API responde correctamente.

### Implementation for User Story 2

- [x] T008 [US2] Revisar `backend/entrypoint.sh`: confirmar que `alembic upgrade head` sigue siendo el primer comando (ya es correcto — sin modificación de código); documentar en un comentario inline que este comando crea el archivo `.db` si no existe cuando `DATABASE_URL` apunta a SQLite

**Checkpoint**: US2 completa — el arranque via `entrypoint.sh` inicializa el esquema automáticamente tanto con SQLite como con PostgreSQL.

---

## Phase 5: User Story 3 — Configuración seleccionable por entorno (Priority: P3)

**Goal**: El motor de base de datos se selecciona via `DATABASE_URL`; SQLite es el default; PostgreSQL sigue funcionando.

**Independent Test**: (a) Sin `DATABASE_URL` definida → SQLite funciona. (b) Con `DATABASE_URL=postgresql+asyncpg://...` → PostgreSQL funciona. Ambos escenarios verificados sin cambios de código.

### Implementation for User Story 3

- [x] T009 [P] [US3] Actualizar `.env.example` en la raíz del repositorio: reemplazar las variables `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` de base de datos por `DATABASE_URL=sqlite+aiosqlite:///./kickmanager.db`; agregar como comentario la URL PostgreSQL equivalente para referencia de producción
- [x] T010 [P] [US3] Actualizar `docker-compose.yml`: agregar `DATABASE_URL` como variable de entorno explícita en el servicio `backend` (con valor PostgreSQL por defecto para Docker); agregar comentario en el servicio `db` indicando que es opcional cuando se usa SQLite local
- [ ] T011 [US3] Validar compatibilidad PostgreSQL: definir `DATABASE_URL=postgresql+asyncpg://kickuser:kickpassword@localhost:5432/kickmanager` y confirmar que la aplicación conecta y opera correctamente (requiere PostgreSQL disponible o Docker)

**Checkpoint**: US3 completa — `DATABASE_URL` controla el motor; SQLite default; PostgreSQL producción preservado.

---

## Phase 6: Polish & Verificación final

**Purpose**: Ejecutar suite de tests y validar el escenario completo del quickstart.

- [x] T012 [P] Ejecutar `cd backend && pytest` y corregir cualquier falla relacionada con la migración de base de datos
- [ ] T013 Ejecutar el escenario completo de `specs/003-sqlite-migration/quickstart.md` desde cero (entorno limpio, sin `.db` previo) y confirmar que todos los pasos funcionan en menos de 2 minutos

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sin dependencias — iniciar inmediatamente; T001 y T002 en paralelo
- **Foundational (Phase 2)**: Depende de Phase 1 — **BLOQUEA** todas las historias
- **US1 (Phase 3)**: Depende de Phase 2 — T004, T005, T006 pueden ejecutarse en paralelo; T007 depende de T004+T005+T006
- **US2 (Phase 4)**: Depende de Phase 3 (US1 debe estar completa) — T008 es una verificación
- **US3 (Phase 5)**: Depende de Phase 3; T009 y T010 en paralelo; T011 depende de T009+T010
- **Polish (Phase 6)**: Depende de todas las historias completadas

### User Story Dependencies

- **US1 (P1)**: Inicia tras Phase 2 — sin dependencias de otras historias
- **US2 (P2)**: Inicia tras US1 — el entrypoint usa los mismos componentes modificados en US1
- **US3 (P3)**: Inicia tras US1 — la configuración de entorno depende de que `DATABASE_URL` esté implementado

### Parallel Opportunities

- T001 + T002 en paralelo (Phase 1)
- T004 + T005 + T006 en paralelo (Phase 3, archivos distintos)
- T009 + T010 en paralelo (Phase 5, archivos distintos)
- T012 en paralelo con T013 (Phase 6, independientes)

---

## Parallel Example: User Story 1

```bash
# Lanzar en paralelo (archivos distintos, sin dependencias entre sí):
Task T004: "Reescribir backend/app/db/base.py"
Task T005: "Actualizar backend/migrations/env.py"
Task T006: "Actualizar backend/alembic.ini"

# Solo después de T004+T005+T006:
Task T007: "Validación manual con alembic upgrade head"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Completar Phase 1: Setup (T001, T002)
2. Completar Phase 2: Foundational (T003) — CRÍTICO
3. Completar Phase 3: US1 (T004 → T005 → T006 → T007)
4. **STOP y VALIDAR**: Backend corre con SQLite sin Docker
5. Continuar con US2 y US3 si se requiere

### Incremental Delivery

1. Setup + Foundational → migración compatible
2. US1 → backend SQLite funcional (MVP deployable)
3. US2 → startup automático verificado
4. US3 → configuración por entorno documentada y validada
5. Polish → suite de tests y quickstart validado

---

## Notes

- [P] = archivos distintos, sin dependencias entre sí en esa fase
- T007 y T011 son validaciones manuales — no generan código nuevo
- T008 es revisión/confirmación, no modificación de código
- El archivo `kickmanager.db` se crea en `backend/` al ejecutar `alembic upgrade head`
- `asyncpg` se mantiene en `requirements.txt` para compatibilidad con PostgreSQL en producción
- Commit sugerido tras cada fase completada
