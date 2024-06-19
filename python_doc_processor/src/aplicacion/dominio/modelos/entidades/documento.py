from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from src.aplicacion.dominio.modelos.value_objects.observacion import Observacion
from src.aplicacion.dominio.modelos.entidades.carga import TipoCarga, TipoBulto
from src.aplicacion.dominio.modelos.entidades.entidades_portuarias import CiaNaviera


class TipoDocumento(BaseModel):
    id: int
    nombre: str
    descripcion: str


class Documento(BaseModel):
    id: int
    tipo: TipoDocumento
    numero: str
    checksum: str
    fecha_emision: datetime
    emisor: Optional[str] = None

    def validar_consistencia_interna(self):
        # TODO: Definir validaciones internas generales a todo documento
        # Ejemplos:
        # 1. Validar que el checksum sea correcto
        # 2. Validar si el documento ya se encuentra procesado y asociado al despacho
        pass


class BillofLading(Documento):
    puerto_embarque: str
    puerto_desembarque: str
    tipo_carga: TipoCarga
    cia_transportadora: CiaNaviera
    tipo_bulto: TipoBulto
    cantidad: int
    peso_bruto: int
    flete: str
    identificacion_bultos: str
    observaciones: Optional[List[Observacion]] = []


class PackingList(Documento):
    pass


class PackingListDetail(BaseModel):
    pass


class Invoice(Documento):
    pass


class InvoiceDetail(BaseModel):
    pass


class OriginCertificate(Documento):
    pass
