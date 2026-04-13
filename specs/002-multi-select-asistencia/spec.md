# Feature Specification: Multi-selección de alumnos en registro de asistencia

**Feature Branch**: `002-multi-select-asistencia`  
**Created**: 2026-04-13  
**Status**: Draft  
**Input**: User description: "en la url que resuelve http://localhost:3000/clases/2/asistencia, me gustaria que el select de alumnos tenga otro comportamiento, en lugar de solo permitir seleccionar 1 solo alumno, deberia poder seleccionarse uno o más, para asi facilitar el proceso de registro de asistencia a clases, realizar los cambios necesarios en front end y backend"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Seleccionar y registrar múltiples alumnos a la vez (Priority: P1)

El usuario (instructor/administrador) ingresa a la página de asistencia de una clase. En lugar de agregar alumnos uno por uno, puede seleccionar varios alumnos a la vez desde la lista desplegable y registrarlos todos con un solo clic en "Agregar".

**Why this priority**: Es el cambio central solicitado. Reduce drásticamente el tiempo y los clics necesarios para registrar asistencia en grupos grandes.

**Independent Test**: Se puede probar seleccionando 3 alumnos distintos, haciendo clic en "Agregar" y verificando que los 3 aparecen en la tabla de presentes.

**Acceptance Scenarios**:

1. **Given** una clase activa con alumnos disponibles, **When** el usuario selecciona 3 alumnos en el control de selección, **Then** los 3 alumnos quedan seleccionados visualmente antes de confirmar.
2. **Given** 3 alumnos seleccionados, **When** el usuario hace clic en "Agregar", **Then** los 3 alumnos son registrados como presentes y aparecen en la tabla de asistentes.
3. **Given** que se completó el registro de múltiples alumnos, **When** la operación finaliza, **Then** el control de selección queda vacío/limpio y listo para una nueva selección.

---

### User Story 2 - Feedback claro sobre alumnos ya registrados en selección masiva (Priority: P2)

Al registrar múltiples alumnos a la vez, si alguno ya figura como presente, el sistema informa cuáles no pudieron registrarse sin afectar a los demás.

**Why this priority**: Garantiza que los errores parciales no bloqueen el flujo ni causen confusión. Complementa la historia P1.

**Independent Test**: Se puede probar intentando agregar un alumno ya presente junto con uno nuevo; el nuevo debe registrarse y aparecer un aviso sobre el duplicado.

**Acceptance Scenarios**:

1. **Given** una selección que incluye un alumno ya registrado y uno nuevo, **When** el usuario hace clic en "Agregar", **Then** el alumno nuevo es registrado y se muestra un mensaje indicando cuál no pudo agregarse.
2. **Given** que todos los alumnos seleccionados ya están presentes, **When** el usuario hace clic en "Agregar", **Then** se muestra un mensaje de advertencia y no se crean registros duplicados.

---

### Edge Cases

- ¿Qué ocurre si el usuario intenta hacer clic en "Agregar" sin haber seleccionado ningún alumno? → El botón permanece deshabilitado.
- ¿Qué ocurre si todos los alumnos disponibles ya están presentes? → El control de selección aparece vacío; no hay opciones para seleccionar.
- ¿Qué ocurre si la clase está cancelada? → El comportamiento existente de solo lectura no cambia; el multi-select aplica únicamente a clases activas.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El control de selección de alumnos DEBE permitir seleccionar uno o más alumnos simultáneamente.
- **FR-002**: El botón "Agregar" DEBE permanecer deshabilitado mientras no haya al menos un alumno seleccionado.
- **FR-003**: Al confirmar, el sistema DEBE registrar como presentes todos los alumnos seleccionados en una única operación hacia el servidor.
- **FR-004**: Tras un registro exitoso, la selección DEBE limpiarse automáticamente y la tabla de presentes DEBE actualizarse.
- **FR-005**: El sistema DEBE mostrar un mensaje de advertencia por cada alumno que no pudo registrarse (por ejemplo, ya estaba presente), sin cancelar el registro de los demás alumnos válidos de la misma operación.
- **FR-006**: Los alumnos que ya figuran como presentes DEBEN estar excluidos de las opciones disponibles en el control de selección.

### Key Entities

- **Clase**: Sesión de kickboxing con fecha, estado y lista de asistentes.
- **Alumno**: Persona inscripta con nombre, apellido e identificador único.
- **Asistencia**: Vínculo entre un alumno y una clase que indica que el alumno estuvo presente en esa sesión.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El tiempo para registrar la asistencia de 10 alumnos se reduce al menos un 60% respecto al flujo anterior de selección uno por uno.
- **SC-002**: El 100% de los alumnos seleccionados en una operación masiva son registrados correctamente cuando ninguno está duplicado.
- **SC-003**: Los registros parciales (cuando algún alumno ya está presente) no generan pérdida de datos: el resto de los alumnos seleccionados son guardados exitosamente.
- **SC-004**: El control de selección responde sin demora perceptible al seleccionar o deseleccionar alumnos con listas de hasta 100 alumnos.

## Assumptions

- El backend ya expone un endpoint que acepta una lista de identificadores de alumnos en una sola llamada; el cambio en backend es mínimo o nulo a nivel de lógica de negocio.
- El control de selección múltiple reemplaza completamente al control de selección simple actual; no coexisten ambos.
- La funcionalidad de quitar asistentes individualmente (botón "Quitar" en la tabla de presentes) no cambia.
- El diseño debe ser mobile-first y coherente con el estilo visual existente en la aplicación.
- Solo usuarios autenticados pueden registrar asistencia; el control de acceso existente no se modifica.
