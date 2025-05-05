from pydantic import BaseModel
from typing import Optional

class Coordenadas(BaseModel):
    latitud: float
    longitud: float

class Zona(BaseModel):
    id: int
    nombre: str
    cultivo_principal: str
    hectareas: float
    coordenadas: Coordenadas

