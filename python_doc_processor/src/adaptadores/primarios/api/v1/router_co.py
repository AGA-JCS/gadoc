import json

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from src.adaptadores.primarios.api import STATUS_CODES
from src.aplicacion.dominio.modelos.entidades.documento import BillofLading
from src.aplicacion.dtos.documento import ParametrosExtraccionDTO
from src.aplicacion.puertos.primarios.servicio_procesador_documento import (
    IServicioProcesadorDocumentos,
)
from src.configuracion.containers import Container

router = APIRouter()


@router.post(
    "/doc-origen/extraer/bl", tags=["Bill of Landing"], response_model=BillofLading
)  # , response_model=PropiedadDto)
@inject
def procesar_documento_origen(
    parametros: ParametrosExtraccionDTO,
    servicio_extraccion_bl: IServicioProcesadorDocumentos = Depends(Provide[Container.servicio_extraccion_bl]),
):
    respuesta = servicio_extraccion_bl.extraer_datos(parametros_extraccion=parametros)
    data = jsonable_encoder(respuesta.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[respuesta.type],
    )
