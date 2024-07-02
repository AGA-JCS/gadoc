from abc import ABC, abstractmethod

from src.aplicacion.dominio.modelos.entidades.documento import BillofLading
from src.aplicacion.dtos.documento import ParametrosExtraccionDTO


class IAIBLExtractor(ABC):
    @abstractmethod
    def extraer_datos(self, parametros_extraccion: ParametrosExtraccionDTO) -> BillofLading:
        raise NotImplementedError
