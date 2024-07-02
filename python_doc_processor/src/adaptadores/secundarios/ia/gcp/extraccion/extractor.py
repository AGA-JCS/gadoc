from typing import Iterable, Union

import structlog
from vertexai.generative_models import GenerationResponse

from src.aplicacion.dominio.modelos.entidades.documento import BillofLading
from src.aplicacion.dtos.documento import ParametrosExtraccionDTO

logger = structlog.get_logger()
from src.configuracion.config import get_config

config = get_config()["PROCESS"]["CLOUD"]

from src.adaptadores.secundarios.ia.gcp.extraccion.lector import VertexLector
from src.adaptadores.secundarios.ia.gcp.extraccion.parametrizador import Parametrizador


class VertexExtractor:
    def __init__(self, parametrizador: Parametrizador, lector: VertexLector) -> None:
        self.parametrizador = parametrizador
        self.lector = lector

    def extraer_datos(
        self, parametros_extraccion: ParametrosExtraccionDTO
    ) -> Union[GenerationResponse, Iterable[GenerationResponse]]:
        # 1. Obtener parametros de procesamiento
        try:
            parametros_procesamiento = self.parametrizador.obtener_parametros_procesamiento(
                parametros_extraccion.tipo_documento, parametros_extraccion.full_path_doc
            )
        except Exception as e:
            logger.exception(
                "No se puede obtener los parametros de procesamiento",
                tipo_documento=parametros_extraccion.tipo_documento,
                full_path_doc=parametros_extraccion.full_path_doc,
            )
            raise e
        else:
            # 2. Procesar documento
            try:
                respuesta = self.lector.extraer_contenido(parametros_procesamiento)
            except Exception as e:
                logger.exception(
                    "No se puede procesar el documento",
                    tipo_documento=parametros_extraccion.tipo_documento,
                    full_path_doc=parametros_extraccion.full_path_doc,
                )
                raise e
            else:
                return respuesta
