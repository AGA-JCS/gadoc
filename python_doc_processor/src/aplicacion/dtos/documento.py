from pydantic import BaseModel


class ParametrosExtraccionDTO(BaseModel):
    numero_despacho: str
    tipo_documento: str
    full_path_doc: str
