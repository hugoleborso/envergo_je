import uvicorn
import requests

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from classes.coordinates import Point
from classes.responses import AltiResponse





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

@app.get("/alti")
async def store_search(lat: float, long: float):
    # point = Point(lat=lat,long=long)
    dataSet = 'SRTM_GL3'
    
    query = f"https://api.elevationapi.com/api/Elevation?lat={lat}&lon={long}&dataSet={dataSet}"
    api_response = requests.get(query).json()
    res = AltiResponse(success=False,lat=lat,long=long,dataset=dataSet,alti=None)
    
    if api_response["message"]=='OK':
        res.success=True
        res.lat=api_response["geoPoints"][0]["latitude"]
        res.long=api_response["geoPoints"][0]["longitude"]
        res.alti=api_response["geoPoints"][0]["elevation"]
        res.dataset=api_response["dataSet"]["name"]
    
    return res

@app.get("/surroundings")
async def store_search(lat: str, long: str):
    print("Querying the IGN api")
    return {"coordinates":"str(found)"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=80,
        host="0.0.0.0",
        log_config=None)
    

