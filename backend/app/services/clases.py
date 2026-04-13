from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Asistencia, Clase
from app.services.alumnos import get_alumno, assert_alumno_activo


async def list_clases(
    db: AsyncSession, desde: date | None = None, hasta: date | None = None
) -> list[dict]:
    stmt = select(Clase).options(selectinload(Clase.asistencias)).order_by(Clase.fecha.desc())
    if desde:
        stmt = stmt.where(Clase.fecha >= desde)
    if hasta:
        stmt = stmt.where(Clase.fecha <= hasta)
    result = await db.execute(stmt)
    clases = result.scalars().all()
    return [
        {
            "id": c.id,
            "fecha": c.fecha,
            "estado": c.estado,
            "total_asistentes": len(c.asistencias),
        }
        for c in clases
    ]


async def get_clase(db: AsyncSession, clase_id: int) -> Clase:
    result = await db.execute(
        select(Clase)
        .options(selectinload(Clase.asistencias).selectinload(Asistencia.alumno))
        .where(Clase.id == clase_id)
    )
    clase = result.scalar_one_or_none()
    if not clase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clase no encontrada")
    return clase


async def create_clase(db: AsyncSession, fecha: date, created_by: int) -> Clase:
    existing = await db.execute(select(Clase).where(Clase.fecha == fecha))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una clase para la fecha {fecha}",
        )
    clase = Clase(fecha=fecha, created_by=created_by)
    db.add(clase)
    await db.flush()
    await db.refresh(clase)
    return clase


async def cancel_clase(db: AsyncSession, clase_id: int) -> Clase:
    clase = await get_clase(db, clase_id)
    clase.estado = "cancelada"
    await db.flush()
    await db.refresh(clase)
    return clase


async def register_asistencia(
    db: AsyncSession, clase_id: int, alumno_ids: list[int], created_by: int
) -> dict:
    clase = await get_clase(db, clase_id)
    registrados = []
    ya_presentes = []
    errores = []

    for alumno_id in alumno_ids:
        try:
            alumno = await get_alumno(db, alumno_id)
            assert_alumno_activo(alumno)
        except HTTPException as e:
            errores.append(f"Alumno {alumno_id}: {e.detail}")
            continue

        existing = await db.execute(
            select(Asistencia).where(
                Asistencia.alumno_id == alumno_id, Asistencia.clase_id == clase_id
            )
        )
        if existing.scalar_one_or_none():
            ya_presentes.append(alumno_id)
            continue

        asistencia = Asistencia(alumno_id=alumno_id, clase_id=clase_id, created_by=created_by)
        db.add(asistencia)
        registrados.append(alumno_id)

    await db.flush()
    return {"registrados": registrados, "ya_presentes": ya_presentes, "errores": errores}


async def remove_asistencia(db: AsyncSession, clase_id: int, alumno_id: int) -> dict:
    result = await db.execute(
        select(Asistencia).where(
            Asistencia.alumno_id == alumno_id, Asistencia.clase_id == clase_id
        )
    )
    asistencia = result.scalar_one_or_none()
    if not asistencia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistencia no encontrada")
    await db.delete(asistencia)
    await db.flush()
    return {"message": "Asistencia eliminada"}
