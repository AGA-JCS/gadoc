from pydantic import BaseModel
from datetime import datetime


class Observacion(BaseModel):
    id: int
    fuente: str
    fecha: datetime
    descripcion: str
    tipo: str
    flg_vigente: bool
