from abc import ABC, abstractmethod

from src.aplicacion.dominio.modelos.entidades.documento import OriginCertificate
from src.aplicacion.dtos.documento import ParametrosExtraccionDTO


class IServicioExtraccionBL(ABC):
    @abstractmethod
    def extraer_datos(self, parametros_extraccion: ParametrosExtraccionDTO) -> OriginCertificate:
        raise NotImplementedError
