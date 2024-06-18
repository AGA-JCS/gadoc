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


class ServicioProcesadorDocumentos:

    def obtener_prompt(self, tipo_documento) -> str:
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
        except:
            logger.exception("Prompt no encontrado para el tipo de documento", tipo_documento=tipo_documento)
        else:
            return prompt

    def query_llm(self, full_path, tipo_documento):
        prompt = self.obtener_prompt(tipo_documento)
        document = Part.from_uri(mime_type="application/pdf", uri=full_path)

        generation_config = {
            "max_output_tokens": 8192,  # Limitar cuantos token el modelo puede dar como respuesta (la respuesta se corta en esa cantidad de tokens)
            "temperature": 1,  # Va de 0 a 2, siendo 0 respuestas deterministicas, y 2 de alta variabilidad.
            # "top_p": 0.95, # Similar a temperatura, permite indicar al modelo que solo elija
        }
        safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }

        return self.procesar_documento(document, prompt, generation_config, safety_settings)

    def procesar_documento(self, document, prompt, generation_config, safety_settings) -> json:
        vertexai.init(project=project_id, location=location_ai)
        print(f"Project : {project_id}")
        print(f"Location : {location_ai}")
        print(f"Llm : {llm}")
        print(f"Promt: {prompt}")
        print(f"Document: {document}")
        model = GenerativeModel(llm)
        responses = model.generate_content(
            [
                document,
                prompt,
            ],  # Se entrega los adjuntos (pdfs, imagenes, videos, etc), junto con la instrucción de texto en un listado
            generation_config=generation_config,  # Setting de parametros como top-p, top-k, temperatura, etc.
            safety_settings=safety_settings,  # Settings de seguridad
            stream=False,
        )
        print(responses.text)
        return responses.text

    # def obtener_propiedades(self, id_despacho: int, full_path: str, tipo_documento: str):
    #     prompt = self.obtener_prompt(tipo_documento = tipo_documento)
