from fastapi import APIRouter

import src.adaptadores.primarios.api.v1.router_bl as bl
import src.adaptadores.primarios.api.v1.router_documento_origen as rdo

api_router = APIRouter()
api_router.include_router(rdo.router, tags=["Documento de Origen"])
api_router.include_router(bl.router, tags=["Bill of Landing"])
