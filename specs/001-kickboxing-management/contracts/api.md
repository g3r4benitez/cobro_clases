# API Contracts: Sistema de Gestión de Cobro de Clases Kickboxing

**Base URL**: `http://localhost:8000/api/v1`
**Autenticación**: Bearer JWT en header `Authorization: Bearer <token>`
**Formato**: JSON (Content-Type: application/json)
**Errores estándar**: 400 Bad Request, 401 Unauthorized, 404 Not Found, 409 Conflict, 422 Unprocessable Entity

---

## Auth

### POST /auth/login

Autenticar usuario y obtener token JWT.

**Request**:
```json
{
  "username": "admin",
  "password": "secreto"
}
```

**Response 200**:
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

**Response 401**: Credenciales inválidas.

---

## Usuarios

### POST /usuarios

Crear un nuevo usuario del sistema.

**Auth**: Requerida.

**Request**:
```json
{
  "username": "instructor2",
  "password": "contraseña_segura"
}
```

**Response 201**:
```json
{
  "id": 2,
  "username": "instructor2",
  "activo": true,
  "created_at": "2026-04-08T10:00:00"
}
```

**Response 409**: Username ya existe.

---

## Alumnos

### GET /alumnos

Listar alumnos activos.

**Query params**:
- `incluir_inactivos` (bool, default false): incluir alumnos inactivos.
- `q` (string): filtro por nombre o apellido (búsqueda parcial).

**Response 200**:
```json
[
  {
    "id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "edad": 25,
    "telefono": "11-1234-5678",
    "direccion": "Av. Corrientes 1234",
    "activo": true,
    "created_at": "2026-04-01T09:00:00"
  }
]
```

### POST /alumnos

Crear un nuevo alumno.

**Request**:
```json
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "edad": 25,
  "telefono": "11-1234-5678",
  "direccion": "Av. Corrientes 1234"
}
```

**Response 201**: Objeto alumno creado (mismo esquema que GET).

**Response 422**: Campos requeridos faltantes.

### GET /alumnos/{id}

Obtener detalle de un alumno.

**Response 200**: Objeto alumno.

**Response 404**: Alumno no encontrado.

### PUT /alumnos/{id}

Editar datos de un alumno.

**Request**: mismos campos que POST (todos opcionales en PUT).

**Response 200**: Objeto alumno actualizado.

### PATCH /alumnos/{id}/desactivar

Desactivar un alumno (soft delete).

**Response 200**:
```json
{ "id": 1, "activo": false }
```

---

## Clases

### GET /clases

Listar clases.

**Query params**:
- `desde` (date YYYY-MM-DD): filtro desde fecha.
- `hasta` (date YYYY-MM-DD): filtro hasta fecha.

**Response 200**:
```json
[
  {
    "id": 1,
    "fecha": "2026-04-07",
    "estado": "activa",
    "total_asistentes": 5
  }
]
```

### POST /clases

Crear una clase para una fecha específica.

**Request**:
```json
{
  "fecha": "2026-04-08"
}
```

**Response 201**:
```json
{
  "id": 2,
  "fecha": "2026-04-08",
  "estado": "activa",
  "total_asistentes": 0
}
```

**Response 409**: Ya existe una clase para esa fecha.

### GET /clases/{id}

Obtener detalle de una clase con lista de asistentes.

**Response 200**:
```json
{
  "id": 1,
  "fecha": "2026-04-07",
  "estado": "activa",
  "asistentes": [
    { "alumno_id": 1, "nombre": "Juan", "apellido": "Pérez" }
  ]
}
```

### PATCH /clases/{id}/cancelar

Marcar una clase como cancelada.

**Response 200**:
```json
{ "id": 1, "estado": "cancelada" }
```

---

## Asistencia

### POST /clases/{clase_id}/asistencia

Registrar asistencia de uno o varios alumnos a una clase.

**Request**:
```json
{
  "alumno_ids": [1, 2, 3]
}
```

**Response 200**:
```json
{
  "registrados": [1, 2, 3],
  "ya_presentes": [],
  "errores": []
}
```

**Response 404**: Clase o algún alumno no encontrado.

### DELETE /clases/{clase_id}/asistencia/{alumno_id}

Quitar asistencia de un alumno de una clase.

**Response 200**: Confirmación de eliminación.

---

## Pagos

### POST /pagos/clase

Registrar pago por clase individual.

**Request**:
```json
{
  "alumno_id": 1,
  "clase_id": 1,
  "monto": 1500.00,
  "fecha_pago": "2026-04-08"
}
```

**Response 201**:
```json
{
  "id": 1,
  "alumno_id": 1,
  "clase_id": 1,
  "monto": 1500.00,
  "fecha_pago": "2026-04-08",
  "warning": null,
  "created_at": "2026-04-08T10:30:00"
}
```

**Nota**: Si el alumno ya tiene pago mensual para ese mes, `warning` contiene el mensaje de
advertencia pero el pago se registra igualmente.

**Response 409**: Pago duplicado para ese alumno y clase.

### POST /pagos/mensual

Registrar pago mensual.

**Request**:
```json
{
  "alumno_id": 1,
  "mes_cubierto": 4,
  "anio_cubierto": 2026,
  "fecha_pago": "2026-04-01",
  "monto": 8000.00
}
```

**Response 201**:
```json
{
  "id": 1,
  "alumno_id": 1,
  "mes_cubierto": 4,
  "anio_cubierto": 2026,
  "fecha_pago": "2026-04-01",
  "monto": 8000.00,
  "created_at": "2026-04-08T10:00:00"
}
```

**Response 409**: Ya existe pago mensual activo para ese alumno/mes/año.

### GET /pagos/alumno/{alumno_id}

Listar todo el historial de pagos de un alumno (clase + mensuales).

**Response 200**:
```json
{
  "alumno_id": 1,
  "pagos": [
    {
      "tipo": "mensual",
      "id": 1,
      "mes_cubierto": 3,
      "anio_cubierto": 2026,
      "fecha_pago": "2026-03-01",
      "monto": 8000.00,
      "anulado": false
    },
    {
      "tipo": "clase",
      "id": 2,
      "clase_id": 5,
      "fecha_clase": "2026-04-07",
      "fecha_pago": "2026-04-07",
      "monto": 1500.00,
      "anulado": false
    }
  ]
}
```

### GET /pagos/alumno/{alumno_id}/impagas

Listar clases a las que el alumno asistió y no tiene cobertura de pago.

**Response 200**:
```json
{
  "alumno_id": 1,
  "clases_impagas": [
    {
      "clase_id": 3,
      "fecha": "2026-04-03"
    }
  ]
}
```

### GET /pagos/reporte

Reporte de pagos por fecha o rango de fechas.

**Query params**:
- `desde` (date YYYY-MM-DD, requerido): fecha inicio.
- `hasta` (date YYYY-MM-DD, opcional, default=desde): fecha fin.

**Response 200**:
```json
{
  "desde": "2026-04-01",
  "hasta": "2026-04-08",
  "total_recaudado": 11000.00,
  "pagos": [
    {
      "tipo": "mensual",
      "alumno_id": 1,
      "alumno_nombre": "Juan Pérez",
      "fecha_pago": "2026-04-01",
      "monto": 8000.00
    },
    {
      "tipo": "clase",
      "alumno_id": 2,
      "alumno_nombre": "María López",
      "fecha_pago": "2026-04-07",
      "clase_fecha": "2026-04-07",
      "monto": 1500.00
    }
  ]
}
```

### PATCH /pagos/clase/{id}/anular

Anular un pago por clase.

**Request**:
```json
{ "motivo": "Pago duplicado por error" }
```

**Response 200**:
```json
{ "id": 1, "anulado": true, "motivo_anulacion": "Pago duplicado por error" }
```

### PATCH /pagos/mensual/{id}/anular

Anular un pago mensual.

**Request**:
```json
{ "motivo": "Pago registrado en mes incorrecto" }
```

**Response 200**:
```json
{ "id": 1, "anulado": true, "motivo_anulacion": "Pago registrado en mes incorrecto" }
```

---

## Auditoría

### GET /auditoria

Consultar el log de auditoría.

**Query params**:
- `usuario_id` (int): filtrar por usuario.
- `entidad` (string): filtrar por entidad (alumnos, clases, pagos_clase, etc.).
- `desde` (date): filtrar desde fecha.
- `hasta` (date): filtrar hasta fecha.

**Response 200**:
```json
[
  {
    "id": 1,
    "usuario": { "id": 1, "username": "admin" },
    "accion": "CREATE",
    "entidad": "alumnos",
    "entidad_id": 5,
    "created_at": "2026-04-08T10:00:00"
  }
]
```
