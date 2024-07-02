from dependency_injector import containers, providers

from src.adaptadores.secundarios.ia.gcp.extraccion.bl import VertexBLExtractor
from src.adaptadores.secundarios.ia.gcp.extraccion.extractor import VertexExtractor
from src.adaptadores.secundarios.ia.gcp.extraccion.lector import VertexLector
from src.adaptadores.secundarios.ia.gcp.extraccion.parametrizador import Parametrizador
from src.aplicacion.puertos.primarios.servicio_procesador_documento import (
    IServicioProcesadorDocumentos,
)
from src.aplicacion.puertos.secundarios.ia.extraccion.bl import IAIBLExtractor
from src.aplicacion.servicios.extraccion.bl import ServicioExtraccionBL
from src.aplicacion.servicios.servicio_procesador_documento import (
    ServicioProcesadorDocumentos,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.adaptadores.primarios.api.v1",
        ]
    )

    # repositorio_rol: IRepositorioRol = providers.Factory(RepositorioRol, DbManager().get_session())

    ####################################################################################################################
    # ADAPTADORES
    ####################################################################################################################
    # Secundarios
    vertex_parametrizador: Parametrizador = providers.Factory(Parametrizador)
    vertex_lector: VertexLector = providers.Factory(VertexLector)
    vertex_extractor: VertexExtractor = providers.Factory(
        VertexExtractor, parametrizador=vertex_parametrizador, lector=vertex_lector
    )
    vertex_extractor_datos_bl: IAIBLExtractor = providers.Factory(VertexBLExtractor, vertex_extractor=vertex_extractor)
    # Repositorios
    # UoW
    ####################################################################################################################
    # SERVICIOS
    ####################################################################################################################
    # Aplicacion
    servicio_procesador_documentos: IServicioProcesadorDocumentos = providers.Factory(ServicioProcesadorDocumentos)
    servicio_extraccion_bl: IServicioProcesadorDocumentos = providers.Factory(
        ServicioExtraccionBL, ia_extractor=vertex_extractor_datos_bl
    )
    # Dominio
