# Research: Multi-selección de alumnos en asistencia

**Feature**: 002-multi-select-asistencia  
**Date**: 2026-04-13

## Findings

### Decision 1: Compatibilidad del backend

**Decision**: No se requieren cambios en el backend.  
**Rationale**: El endpoint `POST /clases/{clase_id}/asistencia` ya acepta `alumno_ids: list[int]` (schema `AsistenciaRegisterRequest`). La función `registerAsistencia(claseId, alumnoIds)` en el cliente API del frontend ya envía un array. El router, servicio y schema de respuesta (`registrados`, `ya_presentes`, `errores`) ya soportan operaciones en lote.  
**Alternatives considered**: Agregar un endpoint nuevo solo para batch — rechazado, el existente ya resuelve el caso.

---

### Decision 2: Control de selección múltiple en frontend

**Decision**: Reemplazar el `<select>` simple (HTML nativo) por un `<select multiple>` con atributo `multiple`, usando Bootstrap para el estilo (`form-select`).  
**Rationale**: Es el cambio mínimo posible. Bootstrap 5 ya incluye estilos para `<select multiple>`. No requiere dependencias adicionales. El usuario puede seleccionar/deseleccionar con Ctrl/Cmd+clic o Shift+clic, comportamiento nativo bien conocido.  
**Alternatives considered**:
- Librería de terceros (react-select, downshift): rechazada, viola el principio de mínimas dependencias externas (Constitución V).
- Checkboxes inline: más espacio en pantalla, peor usabilidad en listas largas, mayor complejidad de estado.

---

### Decision 3: Gestión del estado de selección

**Decision**: Reemplazar `selectedId: string` por `selectedIds: number[]` en el estado del componente. Derivar los IDs seleccionados desde `event.target.selectedOptions`.  
**Rationale**: Es el cambio de estado más directo que corresponde al cambio del control. No requiere librerías de formulario adicionales.  
**Alternatives considered**: Usar un Set en lugar de array — rechazado, un array simple es suficiente y más simple de serializar al enviar al backend.

---

### Decision 4: UX del botón "Agregar"

**Decision**: El botón "Agregar" se deshabilita cuando `selectedIds.length === 0`, igual que la lógica actual con `!selectedId`.  
**Rationale**: Consistencia con el comportamiento existente. El texto del botón puede cambiar a "Agregar (N)" para dar feedback sobre cuántos alumnos están seleccionados cuando N > 1.  
**Alternatives considered**: Texto fijo sin contador — aceptable, pero el contador mejora la usabilidad sin coste adicional.

---

### Decision 5: Archivos a modificar

Solo un archivo de frontend requiere cambios:

- `frontend/src/pages/Clases/AsistenciaPage.jsx`

No se modifican:
- Backend (ningún archivo)
- API client (`frontend/src/api/clases.js`) — ya compatible
- Otros componentes frontend

---

### Resumen de impacto

| Capa | Cambio requerido | Archivos |
|------|-----------------|----------|
| Backend router | Ninguno | — |
| Backend service | Ninguno | — |
| Backend schema | Ninguno | — |
| Frontend API client | Ninguno | — |
| Frontend componente | Sí | `AsistenciaPage.jsx` |
