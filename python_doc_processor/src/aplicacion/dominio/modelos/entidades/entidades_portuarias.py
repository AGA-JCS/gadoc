from pydantic import BaseModel


class CiaNaviera(BaseModel):
    id: int
    nombre: str
