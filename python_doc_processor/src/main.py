import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


# Define el modelo Pydantic para recibir los datos
class Datos(BaseModel):
    numero_despacho: str
    option_key: str
    concatenado: str


# Inicializa la aplicación FastAPI
app = FastAPI()


# Define el endpoint para recibir los datos
@app.post("/endpoint")
async def datos_recibidos(data: Datos):
    # Puedes procesar los datos aquí
    # Por ejemplo, imprimir los datos recibidos
    print(f"Numero Despacho: {data.numero_despacho}")
    print(f"Option Key: {data.option_key}")
    print(f"Concatenado: {data.concatenado}")

    # Retornar una respuesta
    return {"message": "Datos recibidos correctamente"}


# uvicorn src.main:app --reload
