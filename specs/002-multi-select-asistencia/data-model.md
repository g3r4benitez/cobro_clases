# Data Model: Multi-selección de alumnos en asistencia

**Feature**: 002-multi-select-asistencia  
**Date**: 2026-04-13

## Impacto en el modelo de datos

Esta feature **no modifica el modelo de datos**. No hay nuevas entidades, ni cambios en campos existentes, ni migraciones de base de datos requeridas.

## Entidades relevantes (sin cambios)

### Clase
- `id`: identificador único
- `fecha`: fecha de la clase
- `estado`: `activa` | `cancelada`
- `asistencias`: relación con registros de asistencia

### Alumno
- `id`: identificador único
- `nombre`: nombre del alumno
- `apellido`: apellido del alumno
- `activo`: estado de actividad

### Asistencia
- `clase_id`: referencia a la clase
- `alumno_id`: referencia al alumno
- Restricción de unicidad: un alumno no puede registrarse dos veces en la misma clase

## Estado de UI (cambio exclusivo en frontend)

El único cambio de "modelo" ocurre en el estado local del componente React:

| Antes | Después |
|-------|---------|
| `selectedId: string` (un solo ID como string) | `selectedIds: number[]` (array de IDs numéricos) |

Este cambio no persiste en ningún almacenamiento externo.
