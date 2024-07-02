from pydantic import BaseModel


class Consignatario(BaseModel):
    nombre: str
    direccion: str
    pais: str


class Exportador(BaseModel):
    nombre: str
    direccion: str
    pais: str


class CiaNaviera(BaseModel):
    # id: int
    nombre: str
