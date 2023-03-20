from typing import List
from pydantic import BaseModel

class Response(BaseModel):
    success:bool
    error:str|None

class AltiResponse(Response):
    lat:float
    long:float
    alti:float|None
    dataset:str

class ignPoint():
    lon: float
    lat: float
    z: float
    acc: float

class SurroundingsResponse():
    def __init__(self,success,points,dataset,error=None):
        self.success=success
        self.error=error
        self.points=points
        self.dataset=dataset
    
