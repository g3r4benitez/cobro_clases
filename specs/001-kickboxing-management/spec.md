# Feature Specification: Sistema de Gestión de Cobro de Clases Kickboxing

**Feature Branch**: `001-kickboxing-management`
**Created**: 2026-04-08
**Status**: Draft
**Input**: User description: sistema web para registrar alumnos, pagos por clase/mensual, asistencia y usuarios

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Gestión de Alumnos (Priority: P1)

El administrador puede registrar nuevos alumnos con sus datos personales y luego consultarlos,
editarlos o desactivarlos. Un alumno desactivado no puede recibir nuevas asistencias ni pagos,
pero su historial se conserva.

**Why this priority**: Sin alumnos registrados no es posible realizar ninguna otra operación del
sistema. Es el punto de entrada de todo flujo.

**Independent Test**: Crear un alumno con todos los campos requeridos, verificar que aparece en el
listado, editarlo y confirmar los cambios. Desactivarlo y confirmar que no aparece en listas operativas.

**Acceptance Scenarios**:

1. **Given** el administrador está en la pantalla de alumnos, **When** ingresa nombre, apellido, edad
   y teléfono y confirma, **Then** el alumno queda registrado y aparece en el listado.
2. **Given** el administrador intenta guardar un alumno sin nombre, apellido, edad o teléfono,
   **When** envía el formulario, **Then** el sistema muestra un mensaje indicando qué campos son
   requeridos y no guarda el registro.
3. **Given** existe un alumno registrado, **When** el administrador edita su teléfono o dirección y
   guarda, **Then** los datos actualizados se reflejan en el perfil del alumno.
4. **Given** existe un alumno registrado, **When** el administrador lo desactiva, **Then** el alumno
   no aparece en listas operativas pero su historial permanece accesible.

---

### User Story 2 - Registro de Clases y Asistencia (Priority: P1)

El administrador puede crear una clase (una fecha específica de actividad kickboxing), y luego
registrar qué alumnos estuvieron presentes en ella.

**Why this priority**: La clase es el evento central del sistema. Sin clases definidas no se puede
registrar asistencia ni cobros por clase.

**Independent Test**: Crear una clase para una fecha, agregar alumnos a la lista de presentes y
verificar que la asistencia queda registrada correctamente para esa fecha.

**Acceptance Scenarios**:

1. **Given** el administrador está en el módulo de clases, **When** crea una clase para una fecha
   específica, **Then** la clase queda registrada y disponible para registrar asistencia.
2. **Given** existe una clase creada, **When** el administrador marca como presente a un alumno
   registrado, **Then** la asistencia queda vinculada a ese alumno y esa clase.
3. **Given** existe una clase con alumnos presentes, **When** el administrador consulta la clase,
   **Then** puede ver la lista completa de alumnos que asistieron.
4. **Given** el administrador intenta registrar como presente a un alumno que no existe en el sistema,
   **Then** el sistema no permite la operación e indica que el alumno debe registrarse primero.

---

### User Story 3 - Pagos por Clase Individual (Priority: P1)

El administrador puede registrar el pago de un alumno por una clase específica. Un pago por clase
queda vinculado a un alumno y a una fecha de clase.

**Why this priority**: Es una de las dos modalidades de cobro del negocio.

**Independent Test**: Registrar el pago de un alumno por una clase específica y verificar que aparece
en el historial de pagos de ese alumno.

**Acceptance Scenarios**:

1. **Given** existe una clase y un alumno, **When** el administrador registra el pago por esa clase
   con un monto, **Then** el pago queda registrado con el alumno, la fecha de clase y el monto.
2. **Given** un alumno tiene un pago mensual vigente para el mes de una clase, **When** el
   administrador intenta registrar un pago por clase individual para ese mismo mes, **Then** el
   sistema advierte que el alumno ya tiene ese mes cubierto con pago mensual.
3. **Given** existe un pago por clase registrado, **When** el administrador consulta los pagos del
   alumno, **Then** el pago aparece en el historial con la fecha de clase y el monto.

---

### User Story 4 - Pagos Mensuales (Priority: P1)

El administrador puede registrar el pago mensual de un alumno. Un pago mensual cubre todas las
clases del mes indicado. Se registra la fecha en que se realizó el pago y el mes al que pertenece.

**Why this priority**: Es la segunda modalidad de cobro y afecta directamente el cálculo de clases
impagas.

**Independent Test**: Registrar un pago mensual para un alumno indicando la fecha de pago y el mes
de cobertura; verificar que el sistema reconoce todas las clases de ese mes como pagas para ese
alumno.

**Acceptance Scenarios**:

1. **Given** existe un alumno, **When** el administrador registra un pago mensual indicando la fecha
   del pago y el mes de cobertura (ej: abril 2026), **Then** el pago queda registrado con alumno,
   fecha de pago y mes cubierto.
2. **Given** un alumno tiene pago mensual para abril 2026, **When** el sistema evalúa si tiene
   clases impagas en abril, **Then** todas las clases de ese mes se consideran pagas para ese alumno.
3. **Given** existen pagos mensuales registrados, **When** el administrador consulta los pagos de un
   alumno, **Then** los pagos mensuales aparecen en el historial con la fecha de pago y el mes
   cubierto.
4. **Given** el administrador intenta registrar un pago mensual para un alumno y mes que ya tiene
   uno, **When** envía el formulario, **Then** el sistema advierte de la duplicación.

---

### User Story 5 - Consultas de Estado de Pagos (Priority: P2)

El administrador puede consultar: (a) clases impagas de un alumno, (b) historial completo de pagos
de un alumno, y (c) todos los pagos realizados en un rango de fechas.

**Why this priority**: Requiere que alumnos, clases y pagos (P1) estén implementados primero.
Es la funcionalidad de reporting core del negocio.

**Independent Test**: Con un alumno que asistió a 3 clases, pagó una por clase y tiene otro mes sin
cobertura mensual, verificar que el sistema lista correctamente las clases impagas. Verificar el
reporte de pagos para un rango de fechas.

**Acceptance Scenarios**:

1. **Given** un alumno asistió a clases sin pago registrado, **When** el administrador consulta las
   clases impagas del alumno, **Then** el sistema muestra la lista de clases a las que asistió sin
   cobertura de pago (individual ni mensual).
2. **Given** un alumno tiene pagos por clase y pagos mensuales, **When** el administrador consulta el
   historial, **Then** aparecen todos en orden cronológico indicando tipo, monto y fecha.
3. **Given** el administrador selecciona un rango de fechas, **When** solicita el reporte de pagos,
   **Then** el sistema muestra todos los pagos de cualquier alumno dentro de ese período.
4. **Given** un alumno tiene pago mensual para un mes y asistió a todas las clases de ese mes,
   **When** se consultan sus clases impagas, **Then** ninguna clase de ese mes aparece como impaga.

---

### User Story 6 - Gestión de Usuarios del Sistema y Auditoría (Priority: P3)

El administrador puede crear nuevos usuarios del sistema. Cada operación relevante queda asociada al
usuario que la realizó.

**Why this priority**: Funcionalidad importante pero el sistema puede operar con un solo usuario
hasta que esta esté implementada.

**Independent Test**: Crear un usuario nuevo, iniciar sesión con él, registrar un alumno y verificar
que el registro de auditoría indica que fue ese usuario quien realizó la acción.

**Acceptance Scenarios**:

1. **Given** el administrador está en la gestión de usuarios, **When** crea un nuevo usuario con
   nombre y contraseña, **Then** el usuario queda registrado y puede iniciar sesión.
2. **Given** un usuario autenticado realiza cualquier acción (crear alumno, registrar pago,
   marcar asistencia), **When** la acción se completa, **Then** el sistema registra quién la realizó
   con fecha y hora.
3. **Given** existe un registro de auditoría, **When** el administrador lo consulta, **Then** puede
   ver qué usuario realizó cada cambio y cuándo.

---

### Edge Cases

- ¿Qué sucede si se registra pago mensual dos veces para el mismo alumno y mes? El sistema advierte
  que ya existe un pago para ese mes y alumno.
- ¿Un alumno sin asistencias puede tener pago mensual? Sí, el pago mensual es independiente de la
  asistencia registrada.
- ¿Qué sucede si se intenta crear una clase para una fecha que ya existe? El sistema advierte la
  duplicación (una fecha = una clase).
- ¿Un alumno puede tener tanto pago mensual como pago por clase en el mismo mes? El sistema advierte
  pero no bloquea, ya que puede ser una corrección de datos.
- ¿Qué pasa con las clases de un alumno inactivo? Su historial de asistencia y pagos permanece;
  no se pueden agregar nuevas asistencias ni pagos.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE permitir crear alumnos con nombre (requerido), apellido (requerido),
  edad (requerido), teléfono (requerido) y dirección (opcional).
- **FR-002**: El sistema DEBE validar que los campos requeridos del alumno estén completos antes de
  guardar; DEBE mostrar mensajes descriptivos por campo faltante.
- **FR-003**: El sistema DEBE permitir editar los datos de un alumno existente.
- **FR-004**: El sistema DEBE permitir desactivar alumnos; los alumnos inactivos conservan su
  historial y no aceptan nuevas asistencias ni pagos.
- **FR-005**: El sistema DEBE permitir crear clases donde cada clase corresponde a una fecha específica
  del calendario; no DEBE existir más de una clase por fecha.
- **FR-006**: El sistema DEBE permitir registrar qué alumnos estuvieron presentes en una clase dada.
- **FR-007**: El sistema DEBE permitir registrar un pago por clase, vinculando alumno, clase y monto.
- **FR-008**: El sistema DEBE permitir registrar un pago mensual con: alumno, fecha en que se realizó
  el pago y mes/año de cobertura.
- **FR-009**: El sistema DEBE considerar como pagadas todas las clases de un mes para el que un alumno
  tenga pago mensual registrado (cobertura por mes calendario completo).
- **FR-010**: El sistema DEBE listar las clases impagas de un alumno: clases a las que asistió sin
  cobertura de pago individual ni mensual.
- **FR-011**: El sistema DEBE listar el historial completo de pagos de un alumno (ambas modalidades)
  en orden cronológico, indicando tipo, monto y fecha.
- **FR-012**: El sistema DEBE permitir filtrar todos los pagos del sistema por fecha específica o
  rango de fechas.
- **FR-013**: El sistema DEBE requerir autenticación para acceder a cualquier función.
- **FR-014**: El sistema DEBE permitir crear usuarios con nombre de usuario y contraseña.
- **FR-015**: El sistema DEBE registrar automáticamente qué usuario autenticado realizó cada
  operación relevante (crear/editar alumno, registrar pago, registrar asistencia), junto con fecha
  y hora exactas.
- **FR-016**: El sistema DEBE advertir al administrador si intenta registrar un pago mensual para un
  alumno y mes que ya tiene uno registrado.
- **FR-017**: El sistema DEBE advertir al administrador si intenta registrar un pago por clase para
  un alumno que ya tiene pago mensual vigente para ese mes.

### Key Entities

- **Alumno**: nombre, apellido, edad, teléfono, dirección (opcional), estado (activo/inactivo),
  fecha de alta.
- **Clase**: fecha (única en el sistema), estado (activa/cancelada).
- **Asistencia**: relación alumno–clase; registrado por (usuario), fecha de registro.
- **PagoClase**: alumno, clase, monto, fecha de registro, registrado por (usuario).
- **PagoMensual**: alumno, mes cubierto (mes+año), fecha de pago realizado, monto, registrado por
  (usuario).
- **Usuario**: nombre de usuario, contraseña (almacenada de forma segura), estado (activo/inactivo).
- **RegistroAuditoria**: usuario, acción, entidad afectada, fecha y hora.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El administrador puede registrar un nuevo alumno en menos de 2 minutos.
- **SC-002**: El administrador puede registrar la asistencia completa de una clase en menos de
  5 minutos, independientemente del número de alumnos.
- **SC-003**: El sistema calcula correctamente las clases impagas con 0% de errores en la evaluación
  de cobertura mensual vs. pago por clase.
- **SC-004**: El historial de pagos de un alumno muestra el 100% de los pagos registrados en orden
  cronológico sin omisiones.
- **SC-005**: El reporte de pagos por rango de fechas incluye el 100% de los pagos del período
  seleccionado sin omisiones.
- **SC-006**: El 100% de las operaciones relevantes quedan asociadas al usuario que las realizó.
- **SC-007**: El sistema responde a cualquier consulta o registro en menos de 3 segundos en
  condiciones normales de uso.
- **SC-008**: La interfaz es operable desde un dispositivo móvil sin pérdida de funcionalidad.

## Assumptions

- El sistema es de uso exclusivo del instructor/administrador; no hay portal para alumnos.
- Existe un único rol en esta versión: administrador. Todos los usuarios tienen el mismo nivel de
  acceso.
- El monto de cada pago (clase o mensual) se ingresa manualmente en cada registro; no hay tarifa
  predefinida en el sistema.
- El concepto "clase impaga" aplica solo a clases a las que el alumno efectivamente asistió y no
  tiene cobertura de pago (individual o mensual) para esa fecha.
- Un pago mensual cubre el mes calendario completo (del día 1 al último día del mes indicado).
- La interfaz debe ser accesible y operable desde dispositivos móviles (smartphone).
- No se requiere integración con medios de pago electrónico en esta versión; los pagos se registran
  manualmente como confirmación de pago ya cobrado.
- Las fechas se muestran en formato DD/MM/YYYY en la interfaz.
- Una fecha de calendario puede tener como máximo una clase; si no hubo clase en una fecha, no se
  registra.
