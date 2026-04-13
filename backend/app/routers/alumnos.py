from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models import Usuario
from app.schemas.alumnos import AlumnoCreate, AlumnoUpdate, AlumnoOut
from app.services.auth import get_current_user
from app.services import alumnos as svc
from app.services.auditoria import registrar_accion

router = APIRouter(prefix="/alumnos", tags=["alumnos"])


@router.get("", response_model=list[AlumnoOut])
async def listar_alumnos(
    incluir_inactivos: bool = Query(False),
    q: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return await svc.list_alumnos(db, incluir_inactivos, q)


@router.post("", response_model=AlumnoOut, status_code=201)
async def crear_alumno(
    data: AlumnoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    alumno = await svc.create_alumno(db, data, current_user.id)
    await registrar_accion(db, current_user.id, "CREATE", "alumnos", alumno.id)
    return alumno


@router.get("/{alumno_id}", response_model=AlumnoOut)
async def obtener_alumno(
    alumno_id: int,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return await svc.get_alumno(db, alumno_id)


@router.put("/{alumno_id}", response_model=AlumnoOut)
async def editar_alumno(
    alumno_id: int,
    data: AlumnoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    alumno = await svc.update_alumno(db, alumno_id, data, current_user.id)
    await registrar_accion(db, current_user.id, "UPDATE", "alumnos", alumno.id)
    return alumno


@router.patch("/{alumno_id}/desactivar", response_model=AlumnoOut)
async def desactivar_alumno(
    alumno_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    alumno = await svc.deactivate_alumno(db, alumno_id)
    await registrar_accion(db, current_user.id, "UPDATE", "alumnos", alumno.id, "desactivado")
    return alumno
