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
    
        
class SurroundingsMultiCircleResponse():
    def __init__(self,success,center,radii,slope,dataset,stats,result,error=None):
        self.success=success
        self.error=error
        self.center=center
        self.radii=radii
        self.slope=slope,
        self.dataset=dataset
        self.stats=stats
        self.result=result
