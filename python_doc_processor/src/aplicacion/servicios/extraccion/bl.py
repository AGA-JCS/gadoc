import structlog

from src.aplicacion.dominio.modelos.entidades.documento import BillofLading
from src.aplicacion.dominio.servicios.respuestas import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)
from src.aplicacion.dtos.documento import ParametrosExtraccionDTO
from src.aplicacion.puertos.primarios.servicio_procesador_documento import (
    IServicioProcesadorDocumentos,
)
from src.aplicacion.puertos.secundarios.ia.extraccion.bl import IAIBLExtractor

logger = structlog.get_logger(__name__)


class ServicioExtraccionBL(IServicioProcesadorDocumentos):

    def __init__(self, ia_extractor: IAIBLExtractor) -> None:
        self.ia_extractor = ia_extractor

    def extraer_datos(self, parametros_extraccion: ParametrosExtraccionDTO) -> ResponseSuccess | ResponseFailure:
        # 1. Obtener parametros de procesamiento
        try:
            datos_extraidos = self.ia_extractor.extraer_datos(parametros_extraccion)
        except Exception as e:
            logger.exception(
                "No se pueden extraer los datos del documento",
                tipo_documento=parametros_extraccion.tipo_documento,
                full_path_doc=parametros_extraccion.full_path_doc,
            )
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)
        else:
            return ResponseSuccess(value=datos_extraidos)
