from datetime import date, datetime
from pydantic import BaseModel


class ClaseCreate(BaseModel):
    fecha: date


class AsistenteOut(BaseModel):
    alumno_id: int
    nombre: str
    apellido: str

    model_config = {"from_attributes": True}


class ClaseOut(BaseModel):
    id: int
    fecha: date
    estado: str
    total_asistentes: int = 0

    model_config = {"from_attributes": True}


class ClaseDetailOut(BaseModel):
    id: int
    fecha: date
    estado: str
    asistentes: list[AsistenteOut] = []

    model_config = {"from_attributes": True}
