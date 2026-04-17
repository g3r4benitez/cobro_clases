# Data Model: Migrar base de datos a SQLite

**Feature**: 003-sqlite-migration  
**Date**: 2026-04-15

## Impacto en el modelo de datos

Esta feature **no modifica el modelo de dominio**. Las entidades (Usuario, Alumno, Clase, Asistencia, PagoClase, PagoMensual, AuditLog) y sus relaciones permanecen idénticas.

Los únicos cambios son en la **capa de persistencia** (driver, URL, compatibilidad de defaults SQL).

---

## Cambios en capa de configuración de BD

### `backend/app/db/base.py` — antes vs después

**Antes** (construye URL PostgreSQL desde variables individuales):
```
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=False)
```

**Después** (lee URL completa; default SQLite; activa FK pragma para SQLite):
```
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./kickmanager.db")

# Activar foreign keys para SQLite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_async_engine(DATABASE_URL, echo=False, connect_args=connect_args)
```

El evento `PRAGMA foreign_keys = ON` se registra por evento `connect` del engine cuando el dialecto es SQLite.

---

## Compatibilidad de tipos por columna

| Columna (tabla) | SQLAlchemy Type | PostgreSQL | SQLite | ¿Compatible? |
|-----------------|-----------------|------------|--------|--------------|
| `activo` (usuarios, alumnos) | `Boolean` | BOOLEAN | INTEGER (0/1) | ✅ con default `"1"`/`"0"` |
| `anulado` (pagos_clase, pagos_mensual) | `Boolean` | BOOLEAN | INTEGER (0/1) | ✅ con default `"1"`/`"0"` |
| `monto` (pagos_clase, pagos_mensual) | `Numeric(10,2)` | NUMERIC | REAL | ✅ (precisión float64 suficiente) |
| `created_at`, `updated_at` | `DateTime` | TIMESTAMP | TEXT/ISO8601 | ✅ SQLAlchemy maneja conversión |
| `fecha`, `fecha_pago` | `Date` | DATE | TEXT/ISO8601 | ✅ SQLAlchemy maneja conversión |
| `detalle` (audit_log) | `Text` | TEXT | TEXT | ✅ |
| Todos los `String(N)` | `String(N)` | VARCHAR(N) | TEXT | ✅ |

---

## Cambio en migración 0001

**Afecta**: columnas con `server_default=sa.text("true")` y `server_default=sa.text("false")`.

| Tabla | Columna | Antes | Después |
|-------|---------|-------|---------|
| `usuarios` | `activo` | `sa.text("true")` | `sa.text("1")` |
| `alumnos` | `activo` | `sa.text("true")` | `sa.text("1")` |
| `pagos_clase` | `anulado` | `sa.text("false")` | `sa.text("0")` |
| `pagos_mensual` | `anulado` | `sa.text("false")` | `sa.text("0")` |

**Nota**: `server_default="activa"` en `clases.estado` ya es un string literal — compatible sin cambios.
