import yaml
import os

base_dir = os.path.dirname(__file__)
full_path_config_file = os.path.join(base_dir, "config.yaml")


def get_config():
    with open(full_path_config_file) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def validate_config():
    dict_config = get_config()
    # TODO Validaciones de estructura de la configuración
    # TODO Validar tipos de puntos de conexión [DB|STORAGE|URL] (Hoy sólo soportamos DB)
    # TODO Validar cooncordancia de orígenes y destinos declarados en la sección CONNECTION_POINTS y los declarados en
    # cada artefacto en los atributos origen (ORIGIN) y destino (DESTINATION) respectivamente


if __name__ == "__main__":
    print(get_config())
