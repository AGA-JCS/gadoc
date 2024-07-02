import structlog
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import Part

import src.adaptadores.secundarios.ia.gcp.extraccion.prompts as prompts

logger = structlog.get_logger()


class Parametrizador:

    def _obtener_prompt(self, tipo_documento) -> str:
        prompt_map = {
            "BL": prompts.promptBL,
            "Carta": prompts.promptCarta,
            "CO": prompts.promptCertificadoOrigen,
            "OC": prompts.promptOrdenCompra,
            "PS": prompts.promptPolizaSeguro,
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
