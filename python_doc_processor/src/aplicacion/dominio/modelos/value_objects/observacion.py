from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Observacion(BaseModel):
    id: int
    fuente: str
    fecha: datetime
    contenido: str
    tipo: str
    flg_vigente: bool = True
