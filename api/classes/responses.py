from pydantic import BaseModel

class Response(BaseModel):
    success:bool
    error:str|None

class AltiResponse(Response):
    lat:float
    long:float
    alti:float|None
    dataset:str
    
