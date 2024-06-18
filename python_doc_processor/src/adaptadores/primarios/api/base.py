from fastapi import APIRouter

from src.adapadores.primarios.api.v1 import route_documento_origen

api_router = APIRouter()
api_router.include_router(route_documento_origen.router, tags=["Documento de Origen"])
