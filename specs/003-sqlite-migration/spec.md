# Feature Specification: Migrar base de datos a SQLite

**Feature Branch**: `003-sqlite-migration`  
**Created**: 2026-04-15  
**Status**: Draft  
**Input**: User description: "quiero migrar la base de datos del proyecto al motor sqlite, crear los archivos correspondientes"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Aplicación funciona con SQLite sin configuración externa (Priority: P1)

Un desarrollador puede clonar el proyecto, ejecutar un único comando de inicialización y tener la aplicación corriendo completamente funcional usando SQLite, sin necesidad de instalar o configurar PostgreSQL ni Docker.

**Why this priority**: Es el objetivo principal de la migración: eliminar la dependencia de infraestructura externa (PostgreSQL + Docker) para simplificar el desarrollo local y el despliegue.

**Independent Test**: Se puede verificar iniciando el backend sin variables de entorno de base de datos y confirmando que la API responde correctamente con datos persistidos en un archivo `.db` local.

**Acceptance Scenarios**:

1. **Given** el proyecto recién clonado sin ningún servicio de base de datos externo corriendo, **When** se ejecuta el backend, **Then** la aplicación inicia exitosamente y crea automáticamente el archivo de base de datos SQLite.
2. **Given** la aplicación corriendo con SQLite, **When** se realizan operaciones CRUD (crear alumno, registrar pago, marcar asistencia), **Then** los datos se persisten correctamente y sobreviven a un reinicio de la aplicación.
3. **Given** el archivo de base de datos SQLite existente, **When** se reinicia el backend, **Then** todos los datos previos siguen disponibles.

---

### User Story 2 - Esquema de base de datos inicializado automáticamente (Priority: P2)

Al iniciar la aplicación por primera vez con SQLite, el esquema completo de la base de datos (tablas de alumnos, pagos, asistencia) se crea automáticamente sin intervención manual.

**Why this priority**: Con PostgreSQL + Alembic el flujo requería ejecutar migraciones manualmente. Con SQLite el objetivo es que funcione "out of the box" sin pasos adicionales.

**Independent Test**: Se puede testear borrando el archivo `.db` y reiniciando el backend, verificando que todas las tablas se recrean y la API funciona normalmente.

**Acceptance Scenarios**:

1. **Given** no existe archivo de base de datos SQLite, **When** se inicia el backend por primera vez, **Then** se crea el archivo `.db` con todas las tablas del modelo de datos (alumnos, pagos, asistencia, usuarios).
2. **Given** el backend ya corriendo con SQLite, **When** se consulta cualquier endpoint de la API, **Then** no se producen errores relacionados con tablas o columnas faltantes.

---

### User Story 3 - Configuración de base de datos seleccionable por entorno (Priority: P3)

El sistema permite seleccionar entre SQLite (desarrollo/local) y PostgreSQL (producción) mediante una variable de entorno, sin modificar código fuente.

**Why this priority**: Preserva la posibilidad de usar PostgreSQL en producción mientras simplifica el desarrollo local con SQLite.

**Independent Test**: Se puede testear configurando la variable de entorno correspondiente con cada motor y verificando que la aplicación conecta al motor correcto.

**Acceptance Scenarios**:

1. **Given** la variable de entorno `DATABASE_URL` apunta a SQLite, **When** inicia el backend, **Then** usa SQLite como motor de almacenamiento.
2. **Given** la variable de entorno `DATABASE_URL` apunta a PostgreSQL, **When** inicia el backend, **Then** usa PostgreSQL como motor de almacenamiento (comportamiento actual preservado).
3. **Given** no se define `DATABASE_URL`, **When** inicia el backend, **Then** usa SQLite con una ruta predeterminada como valor por defecto.

---

### Edge Cases

- ¿Qué ocurre si el directorio donde se crea el archivo `.db` no tiene permisos de escritura?
- ¿Cómo se comportan las migraciones Alembic existentes (escritas para PostgreSQL) al ejecutarse contra SQLite?
- ¿Qué sucede con las rutas de archivo `.db` en sistemas operativos distintos (Windows vs Linux)?
- ¿Qué ocurre si el archivo `.db` está corrupto o bloqueado por otro proceso?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE soportar SQLite como motor de base de datos válido para todas las operaciones del dominio (alumnos, pagos, asistencia).
- **FR-002**: El sistema DEBE crear el archivo de base de datos SQLite y su esquema automáticamente al iniciar si no existen.
- **FR-003**: El sistema DEBE permitir configurar la ruta del archivo SQLite mediante una variable de entorno o archivo de configuración.
- **FR-004**: El sistema DEBE incluir un valor predeterminado para la base de datos SQLite que funcione sin configuración adicional.
- **FR-005**: El sistema DEBE actualizar las dependencias del backend para incluir el driver asíncrono de SQLite y mantener compatibilidad con el driver de PostgreSQL.
- **FR-006**: El sistema DEBE actualizar la configuración de base de datos para construir la URL de conexión según el motor seleccionado.
- **FR-007**: Las migraciones o la inicialización del esquema DEBEN ser compatibles con SQLite.
- **FR-008**: El archivo de base de datos SQLite DEBE ser excluido del control de versiones (`.gitignore`).
- **FR-009**: La documentación de inicio rápido (README o equivalente) DEBE reflejar los nuevos pasos para correr el proyecto con SQLite.

### Key Entities

- **Archivo de base de datos SQLite**: Archivo binario (`.db`) generado localmente que reemplaza al servidor PostgreSQL; persiste todos los modelos existentes del dominio.
- **Configuración de base de datos**: Variable de entorno o configuración que determina qué motor usar y con qué parámetros de conexión.
- **Driver de base de datos**: Librería que implementa la comunicación asíncrona con SQLite en lugar de la librería equivalente para PostgreSQL.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un desarrollador puede tener el backend funcional en menos de 2 minutos desde cero, sin instalar servicios externos de base de datos.
- **SC-002**: El 100% de los endpoints de la API funciona correctamente con SQLite (mismos resultados que con PostgreSQL para las operaciones del dominio).
- **SC-003**: El inicio del backend sin configuración de base de datos no produce errores; la aplicación crea y usa automáticamente la base de datos predeterminada.
- **SC-004**: Los datos persisten entre reinicios de la aplicación: tras crear un registro y reiniciar el backend, el dato sigue disponible en la API.

## Assumptions

- El proyecto usa SQLAlchemy con soporte asíncrono; SQLite es compatible a través de un driver asíncrono equivalente.
- Las características específicas de PostgreSQL en uso (si existen) son compatibles con SQLite o serán adaptadas durante la implementación.
- El entorno de producción puede seguir usando PostgreSQL; la migración a SQLite está orientada principalmente al desarrollo local y simplificación de despliegue.
- No se requiere migración de datos existentes de PostgreSQL a SQLite; se asume una base de datos nueva para el entorno SQLite.
- Las migraciones Alembic existentes pueden requerir ajustes de compatibilidad o ser reemplazadas por creación automática de esquema para SQLite.
- El archivo `.db` de SQLite se almacenará en el directorio del backend o en una ruta configurable, no en memoria.
