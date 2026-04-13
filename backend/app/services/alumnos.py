from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Alumno
from app.schemas.alumnos import AlumnoCreate, AlumnoUpdate


async def list_alumnos(db: AsyncSession, incluir_inactivos: bool = False, q: str | None = None) -> list[Alumno]:
    stmt = select(Alumno)
    if not incluir_inactivos:
        stmt = stmt.where(Alumno.activo == True)
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(or_(Alumno.nombre.ilike(pattern), Alumno.apellido.ilike(pattern)))
    stmt = stmt.order_by(Alumno.apellido, Alumno.nombre)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_alumno(db: AsyncSession, alumno_id: int) -> Alumno:
    result = await db.execute(select(Alumno).where(Alumno.id == alumno_id))
    alumno = result.scalar_one_or_none()
    if not alumno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
    return alumno


async def create_alumno(db: AsyncSession, data: AlumnoCreate, created_by: int) -> Alumno:
    alumno = Alumno(**data.model_dump(), created_by=created_by)
    db.add(alumno)
    await db.flush()
    await db.refresh(alumno)
    return alumno


async def update_alumno(db: AsyncSession, alumno_id: int, data: AlumnoUpdate, updated_by: int) -> Alumno:
    alumno = await get_alumno(db, alumno_id)
    if not alumno.activo:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No se puede editar un alumno inactivo")
    update_data = data.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(alumno, field, value)
    # alumno.updated_at = datetime.now(timezone.utc)
    alumno.updated_at = datetime.now()
    alumno.updated_by = updated_by
    await db.flush()
    await db.refresh(alumno)
    return alumno


async def deactivate_alumno(db: AsyncSession, alumno_id: int) -> Alumno:
    alumno = await get_alumno(db, alumno_id)
    alumno.activo = False
    alumno.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(alumno)
    return alumno


def assert_alumno_activo(alumno: Alumno) -> None:
    if not alumno.activo:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El alumno está inactivo y no puede recibir nuevas asistencias ni pagos",
        )
