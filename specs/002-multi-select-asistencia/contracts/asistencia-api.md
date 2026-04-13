# API Contract: Registro de Asistencia

**Feature**: 002-multi-select-asistencia  
**Date**: 2026-04-13  
**Status**: Sin cambios — contrato existente ya compatible

## POST /clases/{clase_id}/asistencia

Registra uno o más alumnos como presentes en una clase.

**Request**

```json
{
  "alumno_ids": [1, 2, 3]
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `alumno_ids` | `integer[]` | Sí | Lista de uno o más IDs de alumnos a registrar. Mínimo 1 elemento. |

**Response 200**

```json
{
  "registrados": [1, 3],
  "ya_presentes": [2],
  "errores": []
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `registrados` | `integer[]` | IDs de alumnos registrados exitosamente en esta operación |
| `ya_presentes` | `integer[]` | IDs de alumnos que ya estaban registrados (no se duplicaron) |
| `errores` | `string[]` | Mensajes de error para casos no contemplados arriba |

**Notas**:
- Si un alumno ya está presente, se incluye en `ya_presentes` y NO se duplica en la base de datos.
- La operación es idempotente por alumno individual.
- Requiere autenticación (JWT en header `Authorization: Bearer <token>`).

---

## DELETE /clases/{clase_id}/asistencia/{alumno_id}

Quita un alumno de la lista de presentes. Sin cambios en este feature.
