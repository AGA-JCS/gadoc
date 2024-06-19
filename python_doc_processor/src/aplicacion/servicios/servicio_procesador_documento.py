## Recibe como parametros:
#   - id_despacho
#   - tipo_documento
#   - ruta_nombre_documento
#   - folder_name cambiar a numero_despacho
#   - uri viene armada desde el uploader.

# Procesa y devuelve json
import json
import os

import structlog
import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import FinishReason, GenerativeModel, Part

from src.aplicacion.dominio.servicios.respuestas import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)
from src.aplicacion.dtos.documento import ParametrosExtraccionDTO
from src.aplicacion.puertos.primarios.servicio_procesador_documento import (
    IServicioProcesadorDocumentos,
)
from src.aplicacion.servicios.prompt import (
    promptBL,
    promptCarta,
    promptCertificadoOrigen,
    promptOrdenCompra,
    promptPolizaSeguro,
)
from src.configuracion.config import get_config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/appadmin/app/src/aplicacion/servicios/service-account.json"
logger = structlog.get_logger()
config = get_config()["PROCESS"]["CLOUD"]

# Definimos variales para VertexAI
project_id = config["PROJECT_ID"]
location_ai = config["LOCATION"]
llm = config["LLM"]


class ServicioProcesadorDocumentos(IServicioProcesadorDocumentos):

    def _obtener_prompt(self, tipo_documento) -> str:
        prompt_map = {
            "BL": promptBL,
            "Carta": promptCarta,
            "CO": promptCertificadoOrigen,
            "OC": promptOrdenCompra,
            "PS": promptPolizaSeguro,
        }
        # Obtenemos el prompt según el tipo de documento
        try:
            prompt = prompt_map.get(tipo_documento)
        except Exception as e:
            logger.exception("Prompt no encontrado para el tipo de documento", tipo_documento=tipo_documento)
            raise e
        else:
            return prompt

    def obtener_parametros_procesamiento(self, tipo_documento: str, full_path_doc: str) -> dict:
        try:
            prompt = self._obtener_prompt(tipo_documento)
        except Exception as e:
            logger.exception(
                "No se puede procesar el tipo de documento", tipo_documento=tipo_documento, full_path_doc=full_path_doc
            )
            raise e
        else:
            try:
                documento = Part.from_uri(mime_type="application/pdf", uri=full_path_doc)
            except Exception as e:
                logger.exception(
                    "No se puede procesar el documento", tipo_documento=tipo_documento, full_path_doc=full_path_doc
                )
                raise e
            else:
                return {
                    "prompt": prompt,
                    "document": documento,
                    "generation_config": {
                        "max_output_tokens": 8192,  # Limitar cuantos token el modelo puede dar como respuesta (la respuesta se corta en esa cantidad de tokens)
                        "temperature": 1,  # Va de 0 a 2, siendo 0 respuestas deterministicas, y 2 de alta variabilidad.
                        # "top_p": 0.95, # Similar a temperatura, permite indicar al modelo que solo elija
                    },
                    "safety_settings": {
                        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                    },
                }

    def procesar_documento(self, parametros: dict) -> json:
        prompt: str = parametros["prompt"]
        document: Part = parametros["document"]
        generation_config: dict = parametros["generation_config"]
        safety_settings: dict = parametros["safety_settings"]
        logger.debug("Iniciando VertexAI", project=project_id, location=location_ai)
        try:
            vertexai.init(project=project_id, location=location_ai)
        except Exception as e:
            logger.exception("No se puede iniciar VertexAI", project=project_id, location=location_ai)
            raise e
        else:
            logger.debug("Iniciando modelo", llm=llm)
            try:
                model = GenerativeModel(llm)
            except Exception as e:
                logger.exception("No se puede iniciar el modelo", llm=llm)
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
                    logger.debug("Documento procesado", respuesta=responses.text)
                    return responses.text

    ###########################################################################
    # Métodos de la interfaz
    ###########################################################################
    def extraer_datos(self, parametros_extraccion: ParametrosExtraccionDTO) -> ResponseSuccess | ResponseFailure:

        # 1. Obtener parametros de procesamiento
        try:
            parametros = self.obtener_parametros_procesamiento(
                parametros_extraccion.tipo_documento, parametros_extraccion.full_path_doc
            )
        except Exception as e:
            logger.exception(
                "No se puede obtener los parametros de procesamiento",
                tipo_documento=parametros_extraccion.tipo_documento,
                full_path_doc=parametros_extraccion.full_path_doc,
            )
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, e)
        else:
            # 2. Procesar documento
            try:
                respuesta = self.procesar_documento(parametros)
            except Exception as e:
                logger.exception(
                    "No se puede procesar el documento",
                    tipo_documento=parametros_extraccion.tipo_documento,
                    full_path_doc=parametros_extraccion.full_path_doc,
                )
                return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)
            else:
                return ResponseSuccess(value=respuesta)

    def cargar_documento(
        self, numero_despacho: int, tipo_documento: str, full_path_doc: str
    ) -> ResponseSuccess | ResponseFailure:
        return super().cargar_documento(numero_despacho, tipo_documento, full_path_doc)
