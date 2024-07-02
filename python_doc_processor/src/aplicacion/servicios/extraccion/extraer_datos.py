from typing import Union

from src.aplicacion.dominio.servicios.respuestas import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)
from src.aplicacion.dtos.documento import ParametrosExtraccionDTO
from src.aplicacion.puertos.primarios.extractor_datos_doc import IExtractorDatosDoc

from .bl import ServicioExtraccionBL


class ExtraerDatosDocServicio(IExtractorDatosDoc):

    def __init__(self, servicio_extraccion_bl: ServicioExtraccionBL) -> None:
        self.servicio_extraccion_bl = servicio_extraccion_bl

    def _seleccionar_extractor(self, tipo_documento: str) -> IExtractorDatosDoc:
        match tipo_documento:
            case "BL":
                return self.servicio_extraccion_bl
            case _:
                raise NotImplementedError(f"Extractor para {tipo_documento} no implementado")

    def extraer_datos(self, parametros_extraccion: ParametrosExtraccionDTO) -> Union[ResponseSuccess, ResponseFailure]:
        # Seleccionar el extractor de datos
        try:
            extractor = self._seleccionar_extractor(parametros_extraccion.tipo_documento)
        except NotImplementedError as e:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, e)
        else:
            # extraer datos
            try:
                datos_extraidos = extractor.extraer_datos(parametros_extraccion)
            except Exception as e:
                return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)
            # devolver respuesta
            else:
                return ResponseSuccess(datos_extraidos)
