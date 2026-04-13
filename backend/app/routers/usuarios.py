from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioOut
from app.services.auth import create_usuario, SECRET_KEY, ALGORITHM
from app.services.auditoria import registrar_accion

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

oauth2_optional = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_optional_user(
    token: str | None = Depends(oauth2_optional),
    db: AsyncSession = Depends(get_db),
) -> Usuario | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            return None
        result = await db.execute(select(Usuario).where(Usuario.id == int(user_id)))
        return result.scalar_one_or_none()
    except JWTError:
        return None


@router.post("", response_model=UsuarioOut, status_code=201)
async def crear_usuario(
    data: UsuarioCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario | None = Depends(get_optional_user),
):
    # Count existing users
    count_result = await db.execute(select(func.count()).select_from(Usuario))
    user_count = count_result.scalar_one()

    # Require auth if users already exist
    if user_count > 0 and current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere autenticación para crear usuarios adicionales",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await create_usuario(db, data.username, data.password)

    if current_user:
        await registrar_accion(db, current_user.id, "CREATE", "usuarios", user.id)

    return user
