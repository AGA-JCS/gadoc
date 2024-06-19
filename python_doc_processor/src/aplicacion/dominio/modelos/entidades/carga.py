from pydantic import BaseModel


class TipoCarga(BaseModel):
    pass


class Carga(BaseModel):
    pass


class TipoBulto(BaseModel):
    pass


class Bulto(BaseModel):
    id: int
    tipo_bulto: TipoBulto
