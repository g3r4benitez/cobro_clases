# Implementation Plan: Multi-selección de alumnos en asistencia

**Branch**: `002-multi-select-asistencia` | **Date**: 2026-04-13 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `/specs/002-multi-select-asistencia/spec.md`

## Summary

Reemplazar el control de selección simple (un alumno) en la página de asistencia por un control de selección múltiple que permita elegir uno o más alumnos y registrarlos en una única operación. El backend ya soporta este caso completamente; el cambio es exclusivamente en el componente `AsistenciaPage.jsx`.

## Technical Context

**Language/Version**: Python 3.11 (backend) / Node.js 20 + React 18 (frontend)  
**Primary Dependencies**: FastAPI, SQLAlchemy 2.0, Alembic (backend) · React 18, Vite, Bootstrap 5, Axios (frontend)  
**Storage**: PostgreSQL (sin cambios en este feature)  
**Testing**: pytest (backend); no hay suite de tests frontend configurada  
**Target Platform**: Web — mobile-first, navegador moderno  
**Project Type**: Web application (backend API + frontend SPA)  
**Performance Goals**: Respuesta perceptible inmediata al seleccionar/deseleccionar; registro de lote completado en < 2 s  
**Constraints**: Sin nuevas dependencias externas; interfaz responsive (Bootstrap 5)  
**Scale/Scope**: Listas de hasta ~100 alumnos disponibles; uso por un solo instructor concurrente

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Estado | Notas |
|-----------|--------|-------|
| I. Registro Centralizado de Alumnos | ✅ PASS | No se modifica el modelo de alumno. Solo cambia cómo se seleccionan desde la UI. |
| II. Gestión de Pagos | ✅ PASS | No aplica directamente. Sin impacto. |
| III. Control de Asistencia por Clase | ✅ PASS | La feature extiende el registro de asistencia. El vínculo alumno-clase sigue siendo la unidad mínima. |
| IV. Interfaz Web Simple y Operativa | ✅ PASS | El registro masivo reduce clics (≤3 para registrar N alumnos). Diseño mobile-first con Bootstrap 5 nativo. |
| V. Simplicidad y Mantenibilidad | ✅ PASS | Se usa `<select multiple>` nativo. Sin nuevas dependencias. Un solo archivo modificado. |
| Data & Privacy | ✅ PASS | No se exponen nuevos datos. Autenticación existente sin cambios. |

**Post-design re-check**: ✅ Todos los principios siguen pasando. Ninguna decisión de diseño introduce violaciones.

## Project Structure

### Documentation (this feature)

```text
specs/002-multi-select-asistencia/
├── plan.md              # Este archivo
├── research.md          # Decisiones técnicas y análisis de impacto
├── data-model.md        # Entidades relevantes (sin cambios en BD)
├── quickstart.md        # Instrucciones para levantar y probar
├── contracts/
│   └── asistencia-api.md  # Contrato del endpoint POST /asistencia
└── tasks.md             # (pendiente — generado por /speckit.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── routers/clases.py       # Sin cambios
│   ├── schemas/asistencia.py   # Sin cambios
│   └── services/clases.py      # Sin cambios (verificar)
└── tests/                      # Sin cambios

frontend/
├── src/
│   ├── api/clases.js            # Sin cambios (ya compatible)
│   └── pages/Clases/
│       └── AsistenciaPage.jsx   # ÚNICO ARCHIVO MODIFICADO
└── (no hay tests frontend)
```

**Structure Decision**: Web application (Option 2). Un único archivo de componente frontend es modificado. El backend no requiere cambios.

## Complexity Tracking

> No hay violaciones de constitución. Esta sección no aplica.
