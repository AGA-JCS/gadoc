import json

import structlog
import vertexai
from vertexai.generative_models import GenerativeModel, Part

from src.configuracion.config import get_config

config = get_config()["PROCESS"]["CLOUD"]
logger = structlog.get_logger()


class VertexLector:

    def __init__(self) -> None:
        self.project_id = config["PROJECT_ID"]
        self.location_ai = config["LOCATION"]
        self.llm = config["LLM"]

    def extraer_contenido(self, parametros_procesamiento: dict) -> json:
        prompt: str = parametros_procesamiento["prompt"]
        document: Part = parametros_procesamiento["document"]
        generation_config: dict = parametros_procesamiento["generation_config"]
        safety_settings: dict = parametros_procesamiento["safety_settings"]
        logger.debug("Iniciando VertexAI", project=self.project_id, location=self.location_ai)
        try:
            vertexai.init(project=self.project_id, location=self.location_ai)
        except Exception as e:
            logger.exception("No se puede iniciar VertexAI", project=self.project_id, location=self.location_ai)
            raise e
        else:
            logger.debug("Iniciando modelo", llm=self.llm)
            try:
                model = GenerativeModel(self.llm)
            except Exception as e:
                logger.exception("No se puede iniciar el modelo", llm=self.llm)
                raise e
            else:
                logger.debug(f"Extrayendo informacion", prompt=prompt, document=document)
                try:
                    responses = model.generate_content(
                        [
                            document,
                            prompt,
                        ],  # Se entrega los adjuntos (pdfs, imagenes, videos, etc), junto con la instrucción de texto en un listado
                        generation_config=generation_config,  # Setting de parametros como top-p, top-k, temperatura, etc.
                        safety_settings=safety_settings,  # Settings de seguridad
                        stream=False,
                    )
                except Exception as e:
                    logger.exception("No se puede procesar el documento", prompt=prompt, document=document)
                    raise e
                else:
                    logger.debug("Documento procesado", respuesta=responses)
                    return responses
