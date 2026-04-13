from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models import Usuario
from app.schemas.clases import ClaseCreate, ClaseOut, ClaseDetailOut, AsistenteOut
from app.schemas.asistencia import AsistenciaRegisterRequest, AsistenciaResponse
from app.services.auth import get_current_user
from app.services import clases as svc
from app.services.auditoria import registrar_accion

router = APIRouter(prefix="/clases", tags=["clases"])


@router.get("", response_model=list[ClaseOut])
async def listar_clases(
    desde: date | None = Query(None),
    hasta: date | None = Query(None),
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return await svc.list_clases(db, desde, hasta)


@router.post("", response_model=ClaseOut, status_code=201)
async def crear_clase(
    data: ClaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    clase = await svc.create_clase(db, data.fecha, current_user.id)
    await registrar_accion(db, current_user.id, "CREATE", "clases", clase.id)
    return {"id": clase.id, "fecha": clase.fecha, "estado": clase.estado, "total_asistentes": 0}


@router.get("/{clase_id}", response_model=ClaseDetailOut)
async def obtener_clase(
    clase_id: int,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    clase = await svc.get_clase(db, clase_id)
    asistentes = [
        {"alumno_id": a.alumno_id, "nombre": a.alumno.nombre, "apellido": a.alumno.apellido}
        for a in clase.asistencias
    ]
    return {"id": clase.id, "fecha": clase.fecha, "estado": clase.estado, "asistentes": asistentes}


@router.patch("/{clase_id}/cancelar")
async def cancelar_clase(
    clase_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    clase = await svc.cancel_clase(db, clase_id)
    await registrar_accion(db, current_user.id, "UPDATE", "clases", clase.id, "cancelada")
    return {"id": clase.id, "estado": clase.estado}


@router.post("/{clase_id}/asistencia", response_model=AsistenciaResponse)
async def registrar_asistencia(
    clase_id: int,
    data: AsistenciaRegisterRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    result = await svc.register_asistencia(db, clase_id, data.alumno_ids, current_user.id)
    if result["registrados"]:
        await registrar_accion(db, current_user.id, "CREATE", "asistencias", clase_id)
    return result


@router.delete("/{clase_id}/asistencia/{alumno_id}")
async def quitar_asistencia(
    clase_id: int,
    alumno_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    result = await svc.remove_asistencia(db, clase_id, alumno_id)
    await registrar_accion(db, current_user.id, "DELETE", "asistencias", clase_id)
    return result
