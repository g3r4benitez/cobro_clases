from datetime import datetime
from pydantic import BaseModel, field_validator


class AlumnoCreate(BaseModel):
    nombre: str
    apellido: str
    edad: int
    telefono: str
    direccion: str | None = None

    @field_validator("nombre", "apellido", "telefono")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo es requerido y no puede estar vacío")
        return v.strip()

    @field_validator("edad")
    @classmethod
    def edad_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("La edad debe ser mayor que 0")
        return v


class AlumnoUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    edad: int | None = None
    telefono: str | None = None
    direccion: str | None = None

    @field_validator("nombre", "apellido", "telefono", mode="before")
    @classmethod
    def not_empty(cls, v):
        if v is not None and (not v or not str(v).strip()):
            raise ValueError("Este campo no puede estar vacío")
        return v.strip() if isinstance(v, str) else v

    @field_validator("edad", mode="before")
    @classmethod
    def edad_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("La edad debe ser mayor que 0")
        return v


class AlumnoOut(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: int
    telefono: str
    direccion: str | None
    activo: bool
    created_at: datetime

    model_config = {"from_attributes": True}
