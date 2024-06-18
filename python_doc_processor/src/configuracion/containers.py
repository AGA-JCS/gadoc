from dependency_injector import containers, providers


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
    # Dominio
