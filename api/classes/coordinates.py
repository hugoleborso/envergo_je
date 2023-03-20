from pydantic import BaseModel
from pyproj import Proj, transform
from math import pi

class GPS() :
    r_earth = 6356752.3
    
    def __init__(self, lat : float, long : float):
        self.lat  = float(lat)
        self.long = float(long)
    
    def __repr__(self) -> str:
        return "GPS : ("+str(self.lat)+","+str(self.long)+")"
    
    def move(self,distanceLat:int,distanceLong:int):
        angleLat = distanceLat/ self.r_earth * (180 / pi)
        angleLong = distanceLong/ self.r_earth * (180 / pi)
        return GPS(self.lat+angleLat,self.long+angleLong)
    
    def toJSON(self):
        return {"lat":self.lat,"long":self.long}
        
class Lambert():
    
    def __init__(self, x : float, y : float) -> None:
        self.x = float(x)
        self.y = float(y)
    
    def __repr__(self) -> str:
        return "Lambert93 : ("+str(self.x)+","+str(self.y)+")"
    
    def toJSON(self):
        return {"x":self.x,"y":self.y}

class Point() : 
    lambertProj = Proj('epsg:2154')
    gpsProj = Proj('epsg:4326')
    
    def __init__(self,lat=None, long=None, x=None, y=None) -> None:
        if lat is not None and long is not None:
            self.gps = GPS(lat,long)
        
        if x is not None and y is not None:
            self.lambert = Lambert(x,y)
        
    def GPSToLambert(self):
        (x,y) = transform(self.gpsProj,self.lambertProj,self.gps.lat,self.gps.long)
        self.lambert = Lambert(x=x,y=y)
        return self.lambert
    
    def LambertToGPS(self):
        (lat,long) = transform(self.lambertProj,self.gpsProj,self.lambert.x,self.lambert.y)
        self.gps=GPS(lat=lat,long=long)
        return self.GPS
    
    def createSquareGridAround(self,sidePointsNb : int, separationDistance : int):
        pts=[]
        for x in range(0,sidePointsNb):
            for y in range(0,sidePointsNb):
                pts.append(self.gps.move(separationDistance*(x-sidePointsNb/2),separationDistance*(y-sidePointsNb/2)))
        return pts
    