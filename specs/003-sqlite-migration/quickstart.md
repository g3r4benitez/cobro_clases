# Quickstart: Backend con SQLite (sin Docker)

**Feature**: 003-sqlite-migration  
**Date**: 2026-04-15

## Requisitos previos

- Python 3.11+
- No se necesita PostgreSQL ni Docker

## Inicio rápido (SQLite — desarrollo local)

```bash
# 1. Crear entorno virtual e instalar dependencias
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Configurar variables de entorno mínimas
export DATABASE_URL="sqlite+aiosqlite:///./kickmanager.db"
export SECRET_KEY="dev-secret-key-cambiar-en-produccion"
export ACCESS_TOKEN_EXPIRE_MINUTES=480

# 3. Ejecutar migraciones (crea el archivo kickmanager.db automáticamente)
alembic upgrade head

# 4. Iniciar el servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El archivo `kickmanager.db` se crea en el directorio `backend/`.

## Usando un archivo .env

Crear `backend/.env`:

```
DATABASE_URL=sqlite+aiosqlite:///./kickmanager.db
SECRET_KEY=dev-secret-key-cambiar-en-produccion
ACCESS_TOKEN_EXPIRE_MINUTES=480
```

## Producción con PostgreSQL

Para usar PostgreSQL en lugar de SQLite, cambiar la variable:

```
DATABASE_URL=postgresql+asyncpg://usuario:password@host:5432/kickmanager
```

El resto de la aplicación no requiere cambios.

## Con Docker (opcional)

El `docker-compose.yml` incluye el servicio `db` (PostgreSQL) como servicio opcional. Para usarlo:

```bash
docker-compose up
```

Para correr sin PostgreSQL usando SQLite en el contenedor:

```bash
DATABASE_URL=sqlite+aiosqlite:///./kickmanager.db docker-compose up backend frontend
```
