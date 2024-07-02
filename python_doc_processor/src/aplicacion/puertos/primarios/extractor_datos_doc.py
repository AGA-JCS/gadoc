from abc import ABC, abstractmethod
from typing import Union

from src.aplicacion.dominio.servicios.respuestas import ResponseFailure, ResponseSuccess
from src.aplicacion.dtos.documento import ParametrosExtraccionDTO


class IExtractorDatosDoc(ABC):

    @abstractmethod
    def extraer_datos(self, parametros_extraccion: ParametrosExtraccionDTO) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError
