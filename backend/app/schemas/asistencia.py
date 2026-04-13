from pydantic import BaseModel


class AsistenciaRegisterRequest(BaseModel):
    alumno_ids: list[int]


class AsistenciaResponse(BaseModel):
    registrados: list[int]
    ya_presentes: list[int]
    errores: list[str]
