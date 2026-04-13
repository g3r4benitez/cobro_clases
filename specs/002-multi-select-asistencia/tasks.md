# Tasks: Multi-selección de alumnos en asistencia

**Input**: Design documents from `/specs/002-multi-select-asistencia/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: No solicitados explícitamente. No se incluyen tareas de test.

**Scope summary**: Cambio de un único archivo frontend (`AsistenciaPage.jsx`). El backend ya es 100% compatible.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo (distintos archivos, sin dependencias)
- **[Story]**: A qué historia de usuario pertenece la tarea

---

## Phase 1: Setup

**Purpose**: Verificar que el entorno de desarrollo está disponible antes de realizar cambios.

- [X] T001 Levantar el entorno local (backend + frontend) y confirmar que `http://localhost:3000/clases/2/asistencia` carga correctamente (ver quickstart.md)

---

## Phase 2: Foundational (Prerequisitos bloqueantes)

**Purpose**: Confirmar compatibilidad del backend antes de tocar el frontend.

**⚠️ CRÍTICO**: T001 debe estar completo antes de continuar.

- [X] T002 Leer `backend/app/schemas/asistencia.py` y confirmar que `AsistenciaRegisterRequest` acepta `alumno_ids: list[int]` y que `AsistenciaResponse` incluye campos `registrados`, `ya_presentes` y `errores`
- [X] T003 Leer `frontend/src/api/clases.js` y confirmar que `registerAsistencia(claseId, alumnoIds)` envía `alumno_ids` como array (sin cambios necesarios)

**Checkpoint**: Backend y API client confirmados como compatibles — implementación frontend puede comenzar.

---

## Phase 3: User Story 1 — Seleccionar y registrar múltiples alumnos (Priority: P1) 🎯 MVP

**Goal**: Reemplazar el `<select>` simple por un `<select multiple>` que permita elegir uno o más alumnos y registrarlos en una única operación.

**Independent Test**: Abrir `/clases/2/asistencia`, seleccionar 3 alumnos con Ctrl+clic, hacer clic en "Agregar" y verificar que los 3 aparecen en la tabla de presentes con un solo clic.

### Implementación

- [X] T004 [US1] En `frontend/src/pages/Clases/AsistenciaPage.jsx`: reemplazar el estado `selectedId` (string) por `selectedIds` (array vacío `[]`) — actualizar `useState('')` a `useState([])`
- [X] T005 [US1] En `frontend/src/pages/Clases/AsistenciaPage.jsx`: agregar el atributo `multiple` al `<select>` y reemplazar el `onChange` actual por un handler que derive el array desde `Array.from(e.target.selectedOptions, o => Number(o.value))`
- [X] T006 [US1] En `frontend/src/pages/Clases/AsistenciaPage.jsx`: actualizar `handleAdd` para pasar `selectedIds` directamente a `registerAsistencia(id, selectedIds)` y resetear con `setSelectedIds([])` tras la operación (reemplazar las referencias a `selectedId`)
- [X] T007 [US1] En `frontend/src/pages/Clases/AsistenciaPage.jsx`: actualizar la condición `disabled` del botón "Agregar" a `selectedIds.length === 0 || saving`, y actualizar el texto del botón a `Agregar${selectedIds.length > 1 ? ` (${selectedIds.length})` : ''}`

**Checkpoint**: US1 completamente funcional — se pueden seleccionar y registrar varios alumnos en una sola operación.

---

## Phase 4: User Story 2 — Feedback de alumnos ya registrados (Priority: P2)

**Goal**: Cuando algún alumno seleccionado ya está presente, mostrar un aviso específico sin interrumpir el registro de los demás.

**Independent Test**: Forzar que uno de los alumnos seleccionados ya esté registrado; verificar que el sistema registra al resto y muestra el nombre del ya-presente en el mensaje de advertencia.

### Implementación

- [X] T008 [US2] En `frontend/src/pages/Clases/AsistenciaPage.jsx`: actualizar `handleAdd` para que, cuando `result.ya_presentes?.length > 0`, construya un mensaje específico listando los nombres de esos alumnos (cruzando `result.ya_presentes` con el array `alumnos`) y lo muestre como alerta de tipo `warning`

**Checkpoint**: US1 y US2 funcionan correctamente. El feedback es claro para registros parciales.

---

## Phase 5: Polish & Verificación final

**Purpose**: Validación manual del flujo completo según quickstart.md.

- [ ] T009 Ejecutar los escenarios de verificación manual descritos en `specs/002-multi-select-asistencia/quickstart.md`: selección múltiple, registro exitoso, intentar duplicado, clase sin alumnos disponibles
- [ ] T010 Verificar que el control de selección es usable en pantalla móvil (ancho ≤ 390px) con Bootstrap responsive

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sin dependencias — empezar aquí
- **Foundational (Phase 2)**: Depende de Phase 1
- **US1 (Phase 3)**: Depende de Phase 2 — BLOQUEADA hasta confirmar compatibilidad
- **US2 (Phase 4)**: Depende de Phase 3 — reutiliza la lógica de `handleAdd` modificada en T006
- **Polish (Phase 5)**: Depende de Phases 3 y 4

### Within Each User Story

- T004 → T005 → T006 → T007 (secuencial, mismo archivo)
- T008 depende de T006 (usa `result.ya_presentes` y array `alumnos`)

### Parallel Opportunities

Solo T002 y T003 (Phase 2) pueden ejecutarse en paralelo entre sí.  
El resto del trabajo es secuencial porque todas las tareas modifican el mismo archivo.

---

## Parallel Example: Phase 2

```text
# Ejecutar en paralelo:
Task T002: Leer backend/app/schemas/asistencia.py
Task T003: Leer frontend/src/api/clases.js
```

---

## Implementation Strategy

### MVP (User Story 1 solamente)

1. Completar Phase 1: Setup
2. Completar Phase 2: Foundational
3. Completar Phase 3: US1 (T004–T007)
4. **VALIDAR**: Probar selección múltiple manualmente en el navegador
5. Entregar — el flujo principal ya está resuelto

### Entrega incremental

1. Setup + Foundational → confirmación de compatibilidad
2. US1 completa → MVP funcional (multi-select operativo)
3. US2 → mejora de feedback para duplicados
4. Polish → validación final móvil

---

## Notes

- Todas las modificaciones de código ocurren en un único archivo: `frontend/src/pages/Clases/AsistenciaPage.jsx`
- El backend no requiere cambios
- No se crean nuevas dependencias npm
- Commit sugerido por historia: uno para US1 (T004–T007) y otro para US2 (T008)
