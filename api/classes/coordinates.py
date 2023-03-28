from pyproj import Proj, transform
from haversine import inverse_haversine,haversine,Direction,Unit


class GPS() :
    r_earth = 6372800
    
    def __init__(self, lat : float, long : float):
        self.lat  = float(lat)
        self.long = float(long)
    
    def __repr__(self) -> str:
        return "GPS : ("+str(self.lat)+","+str(self.long)+")"
    
    def toTuple(self):
        return (self.lat,self.long)
    
    def move(self,distanceNorth:int,distanceWest:int):
        newPt = inverse_haversine(inverse_haversine(self.toTuple(),distanceNorth,direction=Direction.NORTH,unit=Unit.METERS),distanceWest,Direction.WEST,unit=Unit.METERS)
        return GPS(newPt[0],newPt[1])
    
    def toJSON(self):
        return {"lat":self.lat,"long":self.long}

    def distanceToPoint(self,point):
        return haversine(self.toTuple(),point.toTuple(),unit=Unit.METERS)
        
        
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
                dx,dy=separationDistance*(x-sidePointsNb/2+0.5),separationDistance*(y-sidePointsNb/2+0.5)
                pts.append(self.gps.move(dx,dy))
        return pts
    
    def createRoundGridAround(self, radius : int):
        pts=[]
        for new_pt in self.createSquareGridAround(separationDistance = 2*radius/12,sidePointsNb = 12):
            if self.gps.distanceToPoint(new_pt)<=radius:
                pts.append(new_pt)
        return pts
    
    def createDonutGridAround(self, innerRadius : int, outerRadius:int):
        pts=[]
        for new_pt in self.createSquareGridAround(separationDistance = 2*outerRadius/12,sidePointsNb = 12):
            d = self.gps.distanceToPoint(new_pt)
            if d<=outerRadius and d>innerRadius:
                pts.append(new_pt)
        return pts
    