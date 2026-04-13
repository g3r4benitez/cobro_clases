from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import AuditLog, Usuario


async def registrar_accion(
    db: AsyncSession,
    usuario_id: int,
    accion: str,
    entidad: str,
    entidad_id: int | None = None,
    detalle: str | None = None,
) -> None:
    log = AuditLog(
        usuario_id=usuario_id,
        accion=accion,
        entidad=entidad,
        entidad_id=entidad_id,
        detalle=detalle,
    )
    db.add(log)
    await db.flush()


async def get_log(
    db: AsyncSession,
    usuario_id: int | None = None,
    entidad: str | None = None,
    desde: date | None = None,
    hasta: date | None = None,
) -> list[dict]:
    stmt = select(AuditLog).options(selectinload(AuditLog.usuario)).order_by(AuditLog.created_at.desc())
    if usuario_id:
        stmt = stmt.where(AuditLog.usuario_id == usuario_id)
    if entidad:
        stmt = stmt.where(AuditLog.entidad == entidad)
    if desde:
        stmt = stmt.where(AuditLog.created_at >= desde)
    if hasta:
        stmt = stmt.where(AuditLog.created_at <= hasta)
    result = await db.execute(stmt)
    logs = result.scalars().all()
    return [
        {
            "id": log.id,
            "usuario": {"id": log.usuario.id, "username": log.usuario.username},
            "accion": log.accion,
            "entidad": log.entidad,
            "entidad_id": log.entidad_id,
            "detalle": log.detalle,
            "created_at": log.created_at,
        }
        for log in logs
    ]
