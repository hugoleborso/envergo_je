from pydantic import BaseModel

class GPS(BaseModel) :
    lat : float
    long : float
    
    def __init__(self, lat : float, long : float):
        self.lat  = lat
        self.long = long
        
class Lambert(BaseModel):
    lambert1:float
    lambert2:float
    lambert3:float
    
    def __init__(self, lambert1 : float, lambert2 : float, lambert3 : float) -> None:
        self.lambert1 = lambert1
        self.lambert2 = lambert2
        self.lambert3 = lambert3

class Point(BaseModel) : 
    gps : type[GPS]
    lambert : type[Lambert]
    
    def __init__(self,lat=None, long=None, lambert1=None, lambert2=None,lambert3 = None) -> None:
        if lat is not None and long is not None:
            self.gps = GPS(lat,long)
        
        if lambert1 is not None and lambert2 is not None and lambert3 is not None:
            self.lambert = Lambert(lambert1,lambert2,lambert3)
        
    def GPSToLambert(self):
        lamb1=self.gps.lat+self.gps.long
        lamb2=self.gps.lat+self.gps.long
        lamb3=self.gps.lat+self.gps.long
        self.lambert = Lambert(lambert1=lamb1,lambert2=lamb2,lambert3=lamb3)
        return self.lambert
    
    def LambertToGPS(self):
        lat=self.lambert.lambert1
        long=self.lambert.lambert2
        self.gps=GPS(lat=lat,long=long)
        return self.GPS
    