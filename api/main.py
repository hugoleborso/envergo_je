import uvicorn

from fastapi import FastAPI
# from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


from classes.responses import SurroundingsResponse
from classes.responses import AltiResponse
from classes.coordinates import Point
from classes.altiQuery import altiQuery





app = FastAPI(title="EnvErgo Test API")
origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')

@app.get("/ping")
def ping():
    return {"ping": "pong"}

@app.get("/alti", status_code=200)
async def store_search(lat: float, long: float, api:str="IGN"):
    
    altiQueryService = altiQuery("IGN")
    res = AltiResponse(success=False,lat=lat,long=long,dataset=altiQueryService.dataSet,alti=None)
    altiServiceResponse = altiQueryService.QueryOnePoint(lat,long)
    
    if altiServiceResponse.error is None:
        res.success=True
        res.alti=altiServiceResponse.alti
    else:
        res.error=altiServiceResponse.error
    
    return res

@app.get("/surroundings", status_code=200)
async def store_search(lat: str, long: str,sidePointsNb:int=11,separationDistance:int=100):
    point = Point(lat,long)
    pts = point.createSquareGridAround(sidePointsNb,separationDistance)
    altiQueryService = altiQuery("IGN")
    res = altiQueryService.QueryMultiplePoints(pts)
    return SurroundingsResponse(success=True,points=res,dataset=altiQueryService.dataSet)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=80,
        host="0.0.0.0",
        log_config=None)
    

