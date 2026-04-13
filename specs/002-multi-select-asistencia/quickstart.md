# Quickstart: Multi-selección de alumnos en asistencia

**Feature**: 002-multi-select-asistencia  
**Date**: 2026-04-13

## Requisitos previos

- Docker Compose disponible (o backend/frontend corriendo localmente)
- Rama `002-multi-select-asistencia` activa

## Levantar el entorno

```bash
# Desde la raíz del proyecto
docker-compose up
```

O manualmente:

```bash
# Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend (en otra terminal)
cd frontend
npm run dev
```

## Verificar el feature

1. Abrir `http://localhost:3000` e iniciar sesión.
2. Navegar a **Clases** → seleccionar una clase activa → **Ver asistencia** (o ir directo a `/clases/{id}/asistencia`).
3. En el control de selección, mantener **Ctrl** (Windows/Linux) o **Cmd** (Mac) y hacer clic en 2-3 alumnos.
4. Hacer clic en **Agregar**.
5. Verificar que todos los alumnos seleccionados aparecen en la tabla de **Presentes**.
6. Intentar agregar un alumno ya presente junto con uno nuevo; verificar el mensaje de advertencia.

## Probar via API directamente

```bash
# Reemplazar TOKEN y los IDs según el entorno
curl -X POST http://localhost:8000/clases/2/asistencia \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"alumno_ids": [1, 2, 3]}'
```

Respuesta esperada:

```json
{
  "registrados": [1, 2, 3],
  "ya_presentes": [],
  "errores": []
}
```

## Ejecutar tests

```bash
cd backend
pytest
```
