from pydantic import BaseModel


class TipoCarga(BaseModel):
    nombre: str


class Carga(BaseModel):
    pass


class TipoBulto(BaseModel):
    nombre: str


class Bulto(BaseModel):
    id: int
    tipo_bulto: TipoBulto
