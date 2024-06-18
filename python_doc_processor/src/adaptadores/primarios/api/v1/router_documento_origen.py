import json

# from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from src.aplicacion.servicios.servicio_procesador_documento import (
    ServicioProcesadorDocumentos,
)

# from src.configuracion.containers import Container

router = APIRouter()


@router.post("/doc-origen/procesar", tags=["Documento de Origen"])  # , response_model=PropiedadDto)
# @inject
async def procesar_documento_origen(servicio_procesador_documentos: ServicioProcesadorDocumentos):
    respuesta = servicio_dom_propiedades.obtener_propiedades()
    data = jsonable_encoder(respuesta.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[respuesta.type],
    )
