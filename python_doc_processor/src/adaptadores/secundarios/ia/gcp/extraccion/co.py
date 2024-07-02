from datetime import datetime

from src.adaptadores.secundarios.ia.gcp.extraccion.extractor import VertexExtractor
from src.adaptadores.secundarios.ia.gcp.extraccion.utils import extract_json
from src.aplicacion.dominio.modelos.entidades.actores import CiaNaviera
from src.aplicacion.dominio.modelos.entidades.carga import TipoBulto
from src.aplicacion.dominio.modelos.entidades.documento import OriginCertificate
from src.aplicacion.dtos.documento import ParametrosExtraccionDTO
from src.aplicacion.puertos.secundarios.ia.extraccion.co import IAICOExtractor


class VertexCOExtractor(IAICOExtractor):
    def __init__(self, vertex_extractor: VertexExtractor) -> None:
        self.vertex_extractor = vertex_extractor

    def extraer_datos(self, parametros_extraccion: ParametrosExtraccionDTO) -> OriginCertificate:
        respuesta = self.vertex_extractor.extraer_datos(parametros_extraccion)
        co = extract_json(respuesta.text)[0]

        co_salida = OriginCertificate(**co)

        return co_salida
