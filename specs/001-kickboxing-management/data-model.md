# Data Model: Sistema de Gestión de Cobro de Clases Kickboxing

**Feature**: 001-kickboxing-management
**Date**: 2026-04-08

## Entidades y Esquema

### usuarios

| Campo          | Tipo         | Restricciones                      | Descripción                      |
|----------------|--------------|------------------------------------|----------------------------------|
| id             | INTEGER      | PK, AUTO_INCREMENT                 | Identificador único              |
| username       | VARCHAR(50)  | NOT NULL, UNIQUE                   | Nombre de usuario para login     |
| password_hash  | VARCHAR(255) | NOT NULL                           | Hash bcrypt de la contraseña     |
| activo         | BOOLEAN      | NOT NULL, DEFAULT TRUE             | Estado del usuario               |
| created_at     | TIMESTAMP    | NOT NULL, DEFAULT NOW()            | Fecha de creación                |

**Validaciones**:
- `username`: mínimo 3 caracteres, sin espacios.
- `password_hash`: nunca se almacena la contraseña en texto plano.

---

### alumnos

| Campo      | Tipo         | Restricciones                   | Descripción                        |
|------------|--------------|---------------------------------|------------------------------------|
| id         | INTEGER      | PK, AUTO_INCREMENT              | Identificador único                |
| nombre     | VARCHAR(100) | NOT NULL                        | Nombre del alumno                  |
| apellido   | VARCHAR(100) | NOT NULL                        | Apellido del alumno                |
| edad       | INTEGER      | NOT NULL, CHECK (edad > 0)      | Edad en años                       |
| telefono   | VARCHAR(20)  | NOT NULL                        | Teléfono de contacto               |
| direccion  | VARCHAR(255) | NULL                            | Dirección (opcional)               |
| activo     | BOOLEAN      | NOT NULL, DEFAULT TRUE          | Estado: activo / inactivo          |
| created_at | TIMESTAMP    | NOT NULL, DEFAULT NOW()         | Fecha de alta                      |
| created_by | INTEGER      | NOT NULL, FK → usuarios(id)     | Usuario que registró el alumno     |
| updated_at | TIMESTAMP    | NULL                            | Última fecha de actualización      |
| updated_by | INTEGER      | NULL, FK → usuarios(id)         | Último usuario que editó           |

**Validaciones**:
- `nombre`, `apellido`: campos requeridos, no vacíos.
- `edad`: entero positivo mayor que 0.
- `telefono`: requerido, no vacío.
- Un alumno inactivo no acepta nuevas asistencias ni pagos.

---

### clases

| Campo      | Tipo      | Restricciones                   | Descripción                                  |
|------------|-----------|---------------------------------|----------------------------------------------|
| id         | INTEGER   | PK, AUTO_INCREMENT              | Identificador único                          |
| fecha      | DATE      | NOT NULL, UNIQUE                | Fecha de la clase (una por día)              |
| estado     | VARCHAR(20)| NOT NULL, DEFAULT 'activa'     | 'activa' o 'cancelada'                       |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW()         | Fecha de creación del registro               |
| created_by | INTEGER   | NOT NULL, FK → usuarios(id)     | Usuario que creó la clase                    |

**Validaciones**:
- `fecha`: UNIQUE — no puede existir más de una clase por fecha.
- Una clase cancelada conserva asistencias y pagos registrados.

---

### asistencias

| Campo       | Tipo      | Restricciones                              | Descripción                              |
|-------------|-----------|--------------------------------------------|------------------------------------------|
| id          | INTEGER   | PK, AUTO_INCREMENT                         | Identificador único                      |
| alumno_id   | INTEGER   | NOT NULL, FK → alumnos(id)                 | Alumno presente                          |
| clase_id    | INTEGER   | NOT NULL, FK → clases(id)                  | Clase a la que asistió                   |
| created_at  | TIMESTAMP | NOT NULL, DEFAULT NOW()                    | Fecha/hora de registro                   |
| created_by  | INTEGER   | NOT NULL, FK → usuarios(id)                | Usuario que registró la asistencia       |

**Restricciones adicionales**:
- UNIQUE (alumno_id, clase_id) — un alumno no puede tener dos asistencias a la misma clase.
- Solo se puede registrar asistencia de alumnos con `activo = TRUE`.

---

### pagos_clase

| Campo       | Tipo      | Restricciones                              | Descripción                              |
|-------------|-----------|--------------------------------------------|------------------------------------------|
| id          | INTEGER   | PK, AUTO_INCREMENT                         | Identificador único                      |
| alumno_id   | INTEGER   | NOT NULL, FK → alumnos(id)                 | Alumno que pagó                          |
| clase_id    | INTEGER   | NOT NULL, FK → clases(id)                  | Clase pagada                             |
| monto       | NUMERIC(10,2) | NOT NULL, CHECK (monto > 0)            | Monto abonado                            |
| fecha_pago  | DATE      | NOT NULL                                   | Fecha en que se realizó el pago          |
| created_at  | TIMESTAMP | NOT NULL, DEFAULT NOW()                    | Fecha/hora de registro en el sistema     |
| created_by  | INTEGER   | NOT NULL, FK → usuarios(id)                | Usuario que registró el pago             |
| anulado     | BOOLEAN   | NOT NULL, DEFAULT FALSE                    | Si el pago fue anulado                   |
| motivo_anulacion | VARCHAR(255) | NULL                              | Justificación de anulación               |

**Validaciones**:
- `monto`: mayor que 0.
- `anulado`: los pagos no se eliminan, solo se anulan (integridad del historial).
- Solo se puede registrar para alumnos `activo = TRUE`.

---

### pagos_mensual

| Campo        | Tipo      | Restricciones                             | Descripción                              |
|--------------|-----------|-------------------------------------------|------------------------------------------|
| id           | INTEGER   | PK, AUTO_INCREMENT                        | Identificador único                      |
| alumno_id    | INTEGER   | NOT NULL, FK → alumnos(id)                | Alumno que pagó                          |
| mes_cubierto | INTEGER   | NOT NULL, CHECK (mes BETWEEN 1 AND 12)    | Mes de cobertura (1–12)                  |
| anio_cubierto| INTEGER   | NOT NULL, CHECK (anio > 2000)             | Año de cobertura                         |
| fecha_pago   | DATE      | NOT NULL                                  | Fecha en que se realizó el pago          |
| monto        | NUMERIC(10,2) | NOT NULL, CHECK (monto > 0)           | Monto abonado                            |
| created_at   | TIMESTAMP | NOT NULL, DEFAULT NOW()                   | Fecha/hora de registro en el sistema     |
| created_by   | INTEGER   | NOT NULL, FK → usuarios(id)               | Usuario que registró el pago             |
| anulado      | BOOLEAN   | NOT NULL, DEFAULT FALSE                   | Si el pago fue anulado                   |
| motivo_anulacion | VARCHAR(255) | NULL                             | Justificación de anulación               |

**Restricciones adicionales**:
- UNIQUE (alumno_id, mes_cubierto, anio_cubierto, anulado=FALSE) — previene duplicados activos.
- Un pago mensual cubre el mes calendario completo (día 1 al último día del mes).

---

### audit_log

| Campo       | Tipo         | Restricciones                    | Descripción                              |
|-------------|--------------|----------------------------------|------------------------------------------|
| id          | INTEGER      | PK, AUTO_INCREMENT               | Identificador único                      |
| usuario_id  | INTEGER      | NOT NULL, FK → usuarios(id)      | Usuario que realizó la acción            |
| accion      | VARCHAR(50)  | NOT NULL                         | Tipo de acción (CREATE, UPDATE, DELETE)  |
| entidad     | VARCHAR(50)  | NOT NULL                         | Tabla/entidad afectada                   |
| entidad_id  | INTEGER      | NULL                             | ID del registro afectado                 |
| detalle     | TEXT         | NULL                             | JSON con datos anteriores/nuevos         |
| created_at  | TIMESTAMP    | NOT NULL, DEFAULT NOW()          | Fecha/hora de la acción                  |

---

## Relaciones

```
usuarios ──< alumnos           (created_by, updated_by)
usuarios ──< clases            (created_by)
usuarios ──< asistencias       (created_by)
usuarios ──< pagos_clase       (created_by)
usuarios ──< pagos_mensual     (created_by)
usuarios ──< audit_log         (usuario_id)
alumnos  ──< asistencias       (alumno_id)
alumnos  ──< pagos_clase       (alumno_id)
alumnos  ──< pagos_mensual     (alumno_id)
clases   ──< asistencias       (clase_id)
clases   ──< pagos_clase       (clase_id)
```

## Lógica de Negocio Clave

### Evaluación de Clase Impaga

Una clase es "impaga" para un alumno cuando:
1. El alumno tiene `asistencias` registrada para esa clase, Y
2. NO existe `pagos_clase` activo (anulado=FALSE) para ese alumno y esa clase, Y
3. NO existe `pagos_mensual` activo (anulado=FALSE) para ese alumno donde
   `mes_cubierto = MONTH(clase.fecha)` Y `anio_cubierto = YEAR(clase.fecha)`.

Esta lógica se implementa en la capa de servicio del backend.

### Cobertura Mensual

Un pago mensual con `mes_cubierto=4, anio_cubierto=2026` cubre todas las clases
con `fecha` entre `2026-04-01` y `2026-04-30` inclusive.

### Advertencias (sin bloqueo)

- Si se intenta registrar `pagos_clase` para un alumno que ya tiene `pagos_mensual` activo
  para ese mes: el backend retorna HTTP 200 con `warning: "El alumno ya tiene pago mensual
  para este mes"` junto con el pago registrado.
- Si se intenta registrar `pagos_mensual` para un alumno/mes que ya tiene uno activo:
  el backend retorna HTTP 409 con error descriptivo.
