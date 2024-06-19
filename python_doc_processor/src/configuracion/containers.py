from dependency_injector import containers, providers
from src.aplicacion.puertos.primarios.servicio_procesador_documento import IServicioProcesadorDocumentos
from src.aplicacion.servicios.servicio_procesador_documento import ServicioProcesadorDocumentos


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
    # Repositorios
    # UoW
    ####################################################################################################################
    # SERVICIOS
    ####################################################################################################################
    # Aplicacion
    servicio_procesador_documentos: IServicioProcesadorDocumentos = providers.Factory(ServicioProcesadorDocumentos)
    # Dominio
