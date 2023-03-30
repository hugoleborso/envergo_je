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
        
        
class SurroundingsCircleResponse():
    def __init__(self,success,radius,center,dataset,stats,result,error=None):
        self.success=success
        self.error=error
        self.center=center
        self.radius=radius
        self.dataset=dataset
        self.stats=stats
        self.result=result
        
class SurroundingsTripleCircleResponse():
    def __init__(self,success,center,radii,dataset,stats,result,error=None):
        self.success=success
        self.error=error
        self.center=center
        self.radii=radii
        self.dataset=dataset
        self.stats=stats
        self.result=result

class SurroundingsSquareResponse():
    def __init__(self,success,center,side,dataset,stats,result,error=None):
        self.success=success
        self.center=center
        self.error=error
        self.side=side
        self.dataset=dataset
        self.stats=stats
        self.result=result
    
