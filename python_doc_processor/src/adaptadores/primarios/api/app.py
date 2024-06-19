import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../..")

from fastapi import FastAPI

from src.configuracion.config import get_config
from src.configuracion.containers import Container

from .base import api_router

config = get_config()["PROCESS"]["API"]


def include_router(app_):
    app_.include_router(api_router)


def start_application():
    container = Container()
    app_ = FastAPI(title=config["NOMBRE"], version=config["VERSION"])
    app_.container = container
    include_router(app_)
    return app_


app = start_application()
