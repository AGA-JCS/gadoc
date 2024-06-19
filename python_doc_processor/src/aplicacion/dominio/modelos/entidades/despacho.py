from pydantic import BaseModel
from datetime import datetime
from typing import List
from src.aplicacion.dominio.modelos.entidades.documento import Documento


class TipoOperacion(BaseModel):
    id: int
    nombre: str
    descripcion: str


class Despacho(BaseModel):
    id: int
    fecha_creacion: datetime
    tipo_operacion: TipoOperacion
    documentos: List[Documento]

    def validar_consistencia(self):
        pass
