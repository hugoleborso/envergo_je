import uvicorn

from fastapi import FastAPI
# from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware



from classes.responses import SurroundingsResponse
from classes.responses import SurroundingsSquareResponse
from classes.responses import SurroundingsCircleResponse
from classes.responses import SurroundingsTripleCircleResponse

from classes.responses import AltiResponse
from classes.coordinates import Point
from classes.altiQuery import altiQuery

from functions.stats import getStats



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
async def store_search(lat: str, long: str):
    point = Point(lat,long)
    pts = point.createDonutGridAround(100,300)
    altiQueryService = altiQuery("IGN")
    res = altiQueryService.QueryMultiplePoints(pts)
    return SurroundingsResponse(success=True,points=res,dataset=altiQueryService.dataSet)

@app.get("/surroundings/square", status_code=200)
async def store_search(lat: str, long: str,sidePointsNb:int=10,separationDistance:int=10):
    point = Point(lat,long)
    pts = point.createSquareGridAround(sidePointsNb,separationDistance)
    altiQueryService = altiQuery("IGN")
    res = altiQueryService.QueryMultiplePoints(pts)
    stats = getStats(point,res)
    return SurroundingsSquareResponse(
        success=True,
        center=point.gps.toJSON(),
        side=separationDistance*sidePointsNb,
        dataset=altiQueryService.dataSet,
        stats=stats)

@app.get("/surroundings/circle", status_code=200)
async def store_search(lat: str, long: str,radius:int=100):
    point = Point(lat,long)
    pts = point.createRoundGridAround(radius)
    altiQueryService = altiQuery("IGN")
    res = altiQueryService.QueryMultiplePoints(pts)
    stats = getStats(point,res)
    return SurroundingsCircleResponse(
        success=True,
        center=point.gps.toJSON(),
        radius=radius,
        dataset=altiQueryService.dataSet,
        stats=stats)

@app.get("/surroundings/triple-circle", status_code=200)
async def store_search(lat: str, long: str,radius:int=100):
    point = Point(lat,long)
    pts1 = point.createRoundGridAround(radius)
    pts3 = point.createDonutGridAround(radius,3*radius)
    pts5 = point.createDonutGridAround(3*radius,5*radius)
    altiQueryService = altiQuery("IGN")
    res1 = altiQueryService.QueryMultiplePoints(pts1)
    res3 = altiQueryService.QueryMultiplePoints(pts3)
    res5 = altiQueryService.QueryMultiplePoints(pts5)
    stats = getStats(point,res1+res3+res5)
    return SurroundingsTripleCircleResponse(
        success=True,
        center=point.gps.toJSON(),
        radii=[radius,3*radius,5*radius],
        dataset=altiQueryService.dataSet,
        stats=stats)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=80,
        host="0.0.0.0",
        log_config=None)
    

