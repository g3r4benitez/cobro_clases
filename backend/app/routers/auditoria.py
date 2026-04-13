from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models import Usuario
from app.services.auth import get_current_user
from app.services.auditoria import get_log

router = APIRouter(prefix="/auditoria", tags=["auditoria"])


@router.get("")
async def obtener_auditoria(
    usuario_id: int | None = Query(None),
    entidad: str | None = Query(None),
    desde: date | None = Query(None),
    hasta: date | None = Query(None),
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return await get_log(db, usuario_id, entidad, desde, hasta)
