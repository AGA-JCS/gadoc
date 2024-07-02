from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from src.aplicacion.dominio.modelos.entidades.actores import CiaNaviera
from src.aplicacion.dominio.modelos.entidades.carga import TipoBulto, TipoCarga
from src.aplicacion.dominio.modelos.value_objects.observacion import Observacion


class Cliente(BaseModel):
    id: int
    nombre: str
    idn: str
    direccion: str


class TipoDocumento(BaseModel):
    id: int
    nombre: str
    descripcion: str


class Documento(BaseModel):
    # tipo: TipoDocumento
    numero: str
    # checksum: str
    fecha_emision: datetime
    # id: Optional[int] = None
    emisor: Optional[str] = None
    # observaciones: Optional[List[Observacion]] = []

    def validar_consistencia_interna(self):
        # TODO: Definir validaciones internas generales a todo documento
        # Ejemplos:
        # 1. Validar que el checksum sea correcto
        # 2. Validar si el documento ya se encuentra procesado y asociado al despacho
        pass

    def validar_consistencia_externa(self):
        # TODO: Definir validaciones externas generales a todo documento
        # Ejemplos:
        # 1. Validar que el cliente si aparece mencionado sea el mismo que en el resto de los documentos asociados al despacho
        pass


class BillofLading(Documento):
    puerto_embarque: str
    puerto_desembarque: str
    tipo_carga: TipoCarga
    cia_transportadora: CiaNaviera
    tipo_bulto: TipoBulto
    cantidad: int
    peso_bruto: float
    flete: str
    identificacion_bultos: str


class PackingListDetail(BaseModel):
    pass


class PackingList(Documento):
    detalles: List[PackingListDetail]


class InvoiceDetail(BaseModel):
    pass


class Invoice(Documento):
    detalles: List[InvoiceDetail]


class OriginCertificate(Documento):
    pass
