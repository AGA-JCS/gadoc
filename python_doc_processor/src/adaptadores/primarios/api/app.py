import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../..")

from fastapi import FastAPI
from pydantic import BaseModel

from src.aplicacion.servicios.servicio_procesador_documento import (
    ServicioProcesadorDocumentos,
)

# from src.configuracion.config import get_config

# from .base import api_router

# from src.configuracion.containers import Container


# Define el modelo Pydantic para recibir los datos
class Datos(BaseModel):
    numero_despacho: str
    option_key: str
    full_path: str


# correr: fastapi dev app.py
#         uvicorn app:app --reload

# config = get_config()["PROCESS"]["CLOUD"]

# app = FastAPI(title=config["NOMBRE"], version=config["VERSION"])
app = FastAPI()


# Define el endpoint para recibir los datos
@app.post("/endpoint")
async def datos_recibidos(data: Datos):
    # Puedes procesar los datos aquí
    # Por ejemplo, imprimir los datos recibidos
    print(f"Numero Despacho: {data.numero_despacho}")
    print(f"Option Key: {data.option_key}")
    print(f"full_path: {data.full_path}")

    procesador = ServicioProcesadorDocumentos()

    result = procesador.query_llm(full_path=data.full_path, tipo_documento=data.option_key)

    # Retornar una respuesta
    return {"message": "Datos recibidos correctamente", "result": result}


# def include_router(app_):
#     app_.include_router(api_router)


# def start_application():
#     # container = Container()
#     app_ = FastAPI(title=config["NOMBRE"], version=config["VERSION"])
#     # app_.container = container
#     include_router(app_)
#     return app_


# app = start_application()
