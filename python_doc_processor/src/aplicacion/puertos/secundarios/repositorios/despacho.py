from abc import ABC, abstractmethod
from src.aplicacion.dominio.modelos.entidades.despacho import Despacho


class IRepositorioDespacho(ABC):
    @abstractmethod
    def obtener_despacho(self, numero_despacho: int) -> Despacho:
        raise NotImplementedError

    def guardar_despacho(self, despacho: Despacho) -> Despacho:
        raise NotImplementedError
