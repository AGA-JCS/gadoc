from datetime import datetime

from src.adaptadores.secundarios.ia.gcp.extraccion.extractor import VertexExtractor
from src.adaptadores.secundarios.ia.gcp.extraccion.utils import extract_json
from src.aplicacion.dominio.modelos.entidades.actores import CiaNaviera
from src.aplicacion.dominio.modelos.entidades.carga import TipoBulto
from src.aplicacion.dominio.modelos.entidades.documento import BillofLading, TipoCarga
from src.aplicacion.dtos.documento import ParametrosExtraccionDTO
from src.aplicacion.puertos.secundarios.ia.extraccion.bl import IAIBLExtractor


class VertexBLExtractor(IAIBLExtractor):
    def __init__(self, vertex_extractor: VertexExtractor) -> None:
        self.vertex_extractor = vertex_extractor

    def extraer_datos(self, parametros_extraccion: ParametrosExtraccionDTO) -> BillofLading:
        respuesta = self.vertex_extractor.extraer_datos(parametros_extraccion)
        bl = extract_json(respuesta.text)[0]

        bl["fecha_emision"] = datetime.strptime(bl["fecha_emision"], "%d-%m-%Y")
        bl["tipo_carga"] = TipoCarga(nombre=bl["tipo_carga"])
        bl["cia_transportadora"] = CiaNaviera(nombre=bl["cia_transportadora"])
        bl["tipo_bulto"] = TipoBulto(nombre=bl["tipo_bulto"])

        bl_salida = BillofLading(**bl)

        return bl_salida
