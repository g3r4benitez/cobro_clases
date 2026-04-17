# Research: Migrar base de datos a SQLite

**Feature**: 003-sqlite-migration  
**Date**: 2026-04-15

## Decision 1: Driver asíncrono para SQLite

**Decision**: Usar `aiosqlite` como driver asíncrono de SQLite.  
**Rationale**: SQLAlchemy 2.0 soporta SQLite de forma asíncrona mediante el dialecto `sqlite+aiosqlite://`. Es el único driver oficial async para SQLite en el ecosistema Python. No requiere cambios en la capa de sesión ni en el ORM; solo cambia la URL de conexión.  
**Alternatives considered**: `sqlalchemy[asyncio]` con `aiosqlite` (misma opción), modo sync con `sqlite://` (descartado por incompatibilidad con la arquitectura async actual).

---

## Decision 2: URL de conexión configurable via DATABASE_URL

**Decision**: Reemplazar la construcción de URL desde variables `POSTGRES_*` por una única variable `DATABASE_URL`. Si no está definida, el default es `sqlite+aiosqlite:///./kickmanager.db`.  
**Rationale**: Simplifica la configuración. Para SQLite solo se necesita la ruta al archivo; para PostgreSQL se puede seguir usando la URL completa. Un solo punto de configuración es más mantenible.  
**Alternatives considered**: Mantener variables `POSTGRES_*` y agregar `SQLITE_PATH` separado (más variables, más complejidad), usar variable `DB_DRIVER` para seleccionar (indirección innecesaria).

---

## Decision 3: Boolean server_defaults — incompatibilidad SQLite

**Problem identified**: La migración `0001_initial_schema.py` usa `server_default=sa.text("true")` y `server_default=sa.text("false")` para columnas Boolean. SQLite no acepta los literales `true`/`false` como texto SQL válido en versiones < 3.23.0 (2018).  
**Decision**: Actualizar la migración `0001` para usar `sa.text("1")` y `sa.text("0")` en lugar de `sa.text("true")` y `sa.text("false")`. Los enteros `1`/`0` son válidos tanto en PostgreSQL como en SQLite para columnas Boolean mapeadas por SQLAlchemy.  
**Alternatives considered**: Usar valores booleanos nativos de SQLAlchemy `sa.true()` / `sa.false()` (también válido, pero `1`/`0` es más universal y explícito).

---

## Decision 4: Alembic con SQLite (modo async)

**Decision**: Alembic en modo async (`env.py` con `async_engine_from_config`) funciona con `sqlite+aiosqlite://` sin cambios estructurales. Solo se requiere actualizar la URL en `env.py` para leer `DATABASE_URL` en lugar de construir la URL PostgreSQL.  
**Rationale**: Mantiene el flujo de migraciones versionadas (requerido por la Constitución). `entrypoint.sh` puede seguir ejecutando `alembic upgrade head` tanto para SQLite como para PostgreSQL.  
**Alternatives considered**: `Base.metadata.create_all()` al inicio de la app para SQLite (descartado: viola el principio de migraciones versionadas de la Constitución), Alembic modo offline para SQLite (innecesario).

---

## Decision 5: Ruta del archivo SQLite

**Decision**: Default `sqlite+aiosqlite:///./kickmanager.db`, lo que ubica el archivo en el directorio de trabajo del proceso (directorio `backend/` cuando se ejecuta localmente o `/app` en Docker).  
**Rationale**: Ruta relativa simple, configurable via `DATABASE_URL`. El archivo es creado automáticamente por SQLite si no existe.  
**Alternatives considered**: Ruta absoluta `/data/kickmanager.db` (requiere crear el directorio), memoria `sqlite+aiosqlite:///:memory:` (no persiste entre reinicios).

---

## Decision 6: Compatibilidad de tipos SQLite

- **Numeric(10, 2)**: SQLite lo mapea a REAL (float64). Precisión suficiente para los montos del sistema.
- **Date / DateTime**: SQLite los almacena como TEXT (ISO 8601) o INTEGER. SQLAlchemy maneja la conversión transparentemente.
- **CheckConstraint**: SQLite ≥ 3.25.0 (septiembre 2018) las enforce. Compatible con sistemas modernos.
- **UniqueConstraint**: Totalmente compatible.
- **ForeignKeyConstraint**: SQLite las soporta pero NO las activa por defecto. Se debe ejecutar `PRAGMA foreign_keys = ON` por conexión.

**Decision adicional**: Activar `PRAGMA foreign_keys = ON` en el evento `connect` del engine para SQLite, para mantener la integridad referencial que PostgreSQL ya garantiza.

---

## Archivos a modificar

| Archivo | Cambio |
|---------|--------|
| `backend/requirements.txt` | Agregar `aiosqlite>=0.20.0`; `asyncpg` puede mantenerse (usado en prod con PostgreSQL) |
| `backend/app/db/base.py` | Leer `DATABASE_URL` env var; default SQLite; activar PRAGMA FK para SQLite |
| `backend/migrations/env.py` | Leer `DATABASE_URL` en lugar de construir URL PostgreSQL |
| `backend/alembic.ini` | Actualizar `sqlalchemy.url` a SQLite como placeholder (se overridea en env.py) |
| `backend/migrations/versions/0001_initial_schema.py` | Reemplazar `sa.text("true")`→`sa.text("1")`, `sa.text("false")`→`sa.text("0")` |
| `.env.example` | Reemplazar variables `POSTGRES_*` por `DATABASE_URL=sqlite+aiosqlite:///./kickmanager.db` (o hacer ambos opcionales) |
| `.gitignore` (raíz y/o `backend/`) | Agregar `*.db` |
| `docker-compose.yml` | Hacer servicio `db` (PostgreSQL) opcional; agregar comentario |
