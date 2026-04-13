<!--
SYNC IMPACT REPORT
==================
Version change: N/A (initial) → 1.0.0
Modified principles: None (initial fill)
Added sections:
  - Core Principles (5 principles)
  - Data & Privacy Standards
  - Development Workflow
  - Governance
Templates reviewed:
  - .specify/templates/plan-template.md ✅ compatible
  - .specify/templates/spec-template.md ✅ compatible
  - .specify/templates/tasks-template.md ✅ compatible
Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Confirm exact project start date; set to 2026-04-08 (today)
-->

# KickManager Constitution

## Core Principles

### I. Registro Centralizado de Alumnos

El sistema DEBE mantener un registro único y completo de cada alumno.
Cada alumno DEBE tener: nombre completo, datos de contacto, fecha de alta y estado activo/inactivo.
No se permiten duplicados: la unicidad se valida por DNI/documento o correo electrónico.
Los datos personales DEBEN ser editables solo por usuarios autorizados.

**Rationale**: Un registro confiable es el fundamento de todas las operaciones de cobro y asistencia.
Sin datos de alumno consistentes, los pagos y la asistencia no pueden trazarse correctamente.

### II. Gestión de Pagos (por Clase y Mensual)

El sistema DEBE soportar dos modalidades de pago: pago por clase individual y pago mensual.
Cada pago DEBE registrarse con: alumno, monto, fecha, modalidad y estado (pendiente/confirmado).
Un alumno con pago mensual vigente NO DEBE ser cobrado por clase individual en ese período.
Los pagos DEBEN ser auditables: no se eliminan, se anulan con justificación.

**Rationale**: El modelo de negocio requiere flexibilidad en la modalidad de cobro.
La integridad del historial de pagos es crítica para la confianza del instructor y del alumno.

### III. Control de Asistencia por Clase

El sistema DEBE permitir registrar qué alumnos estuvieron presentes en cada clase.
Cada clase DEBE tener: fecha, horario y lista de asistentes.
El registro de asistencia DEBE poder vincularse al cobro por clase cuando aplique.
Un alumno SOLO puede ser registrado como asistente si existe en el sistema.

**Rationale**: La asistencia es el evento que activa el cobro por clase y permite medir la participación.
Sin este control no es posible calcular correctamente lo que debe cada alumno.

### IV. Interfaz Web Simple y Operativa

La interfaz DEBE ser usable en dispositivos móviles (responsive).
Las operaciones más frecuentes (registrar asistencia, confirmar pago) DEBEN completarse en ≤3 clics.
El sistema DEBE funcionar sin conexión degradada — las operaciones críticas DEBEN indicar claramente
si requieren conectividad.
No se construyen funcionalidades que no estén en los requisitos actuales (YAGNI).

**Rationale**: El sistema será usado principalmente por el instructor en el lugar de entrenamiento,
posiblemente desde un teléfono. La usabilidad directa es no negociable.

### V. Simplicidad y Mantenibilidad

La solución DEBE usar la menor cantidad de dependencias externas que resuelvan el problema.
Cada capa de la aplicación (modelo, servicio, vista) DEBE tener una responsabilidad única y clara.
La lógica de negocio DEBE vivir en servicios, no en vistas ni en modelos de base de datos.
El código DEBE ser legible sin necesidad de documentación exhaustiva.

**Rationale**: Un sistema sobrediseñado para un negocio pequeño genera deuda técnica sin valor.
La mantenibilidad a largo plazo depende de que el instructor o un desarrollador pueda entenderlo
rápidamente.

## Data & Privacy Standards

Los datos personales de los alumnos (nombre, contacto) DEBEN almacenarse de forma segura.
No se almacenan contraseñas en texto plano; se usa hashing con sal (bcrypt o equivalente).
El acceso al sistema DEBE requerir autenticación. Solo el instructor (o admin designado) puede
gestionar alumnos, pagos y clases.
Los datos NO se comparten con terceros ni se exponen en URLs públicas sin autorización.
El historial de pagos y asistencia DEBE conservarse; no se permite borrado permanente de registros
financieros.

## Development Workflow

1. Toda nueva funcionalidad parte de una especificación en `/specs/`.
2. El modelo de datos se define antes de implementar servicios o vistas.
3. Los cambios al esquema de base de datos se realizan SIEMPRE mediante migraciones versionadas.
4. Cada funcionalidad entregada DEBE poder demostrarse de forma independiente (MVP incremental).
5. Se valida contra los principios del Constitution Check antes de iniciar cualquier plan de implementación.
6. Los commits DEBEN referenciar la tarea o historia de usuario que implementan.

## Governance

Esta constitución es el documento rector del proyecto KickManager. Ninguna decisión de diseño o
implementación puede contradecirla sin un proceso de enmienda formal.

**Proceso de enmienda**:
1. Proponer el cambio con justificación explícita y principio afectado.
2. Evaluar el impacto en templates y artefactos dependientes.
3. Actualizar la versión según reglas de versionado semántico.
4. Actualizar `LAST_AMENDED_DATE` y propagar cambios a templates afectados.

**Política de versionado**:
- MAJOR: eliminación o redefinición incompatible de un principio.
- MINOR: nuevo principio o sección con guía material.
- PATCH: aclaraciones, correcciones de redacción, sin cambio semántico.

**Cumplimiento**: Todo plan (`plan.md`) DEBE incluir un "Constitution Check" que verifique
explícitamente cada principio antes de avanzar a implementación.

**Version**: 1.0.0 | **Ratified**: 2026-04-08 | **Last Amended**: 2026-04-08
