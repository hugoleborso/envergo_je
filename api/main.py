import uvicorn

from fastapi import FastAPI
from typing import List,Union
# from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware



from classes.responses import SurroundingsMultiCircleResponse

from classes.responses import AltiResponse
from classes.coordinates import Point
from classes.altiQuery import altiQuery

from functions.stats import getStats
from functions.stats import multiCircleBassinVersant



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
    
    altiQueryService = altiQuery(api)
    res = AltiResponse(success=False,lat=lat,long=long,dataset=altiQueryService.dataSet,alti=None)
    altiServiceResponse = altiQueryService.QueryOnePoint(lat,long)
    
    if altiServiceResponse.error is None:
        res.success=True
        res.alti=altiServiceResponse.alti
    else:
        res.error=altiServiceResponse.error
    
    return res

@app.get("/surroundings", status_code=200)
async def surroundings(lat: float, long: float,slope:float=0.05,innerCircleRadius:int=25,eightQuadrants:bool=True,strRadii:str="[50,75,100,125]" ):# -> SurroundingsTripleCircleResponse:
    point = Point(lat,long)
    altiQueryService = altiQuery("IGN")
    radii = [int(radius) for radius in strRadii[1:-1].split(',')]
    innerCircleAlti = altiQueryService.QueryMultiplePoints(point.createRoundGridAround(innerCircleRadius))
    pointsList = [point.createDonutGridAround(innerCircleRadius,radii[0])]+[point.createDonutGridAround(radii[i],radii[i+1]) for i in range(len(radii)-1)]
    circles = [altiQueryService.QueryMultiplePoints(pts) for pts in pointsList]
    stats = getStats(point,[pt for pts in circles for pt in pts])
    estimatedSurface = multiCircleBassinVersant(point.gps,innerCircleAlti,circles,radii,eightQuadrants,slope)
    
    return SurroundingsMultiCircleResponse(
        success = True,
        center  = point.gps.toJSON(),
        radii   = radii,
        slope   = slope,
        dataset = altiQueryService.dataSet,
        result  = estimatedSurface,
        stats   = stats
        )


if __name__ == "__main__":
    print('Starting')
    uvicorn.run(
        "main:app",
        port=80,
        host="0.0.0.0",
        log_config=None)
    

