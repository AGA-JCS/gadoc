from abc import ABC, abstractmethod
from src.aplicacion.dominio.servicios.respuestas import ResponseFailure, ResponseSuccess
from src.aplicacion.dtos.documento import ParametrosExtraccionDTO
from typing import Union


class IServicioProcesadorDocumentos(ABC):

    @abstractmethod
    def extraer_datos(self, parametros_extraccion: ParametrosExtraccionDTO) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abstractmethod
    def cargar_documento(
        self, numero_despacho: int, tipo_documento: str, full_path_doc: str
    ) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError
