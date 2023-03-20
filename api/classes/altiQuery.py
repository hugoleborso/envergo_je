import requests

class altiQueryResponse():
    def __init__(self,alti=None,error=None) -> None:
        self.alti=alti
        self.error=error
        
class elevationApiService():
    URL = "https://api.elevationapi.com/api/Elevation"
    dataSet = 'SRTM_GL3'
    
    def QueryOnePoint(self,lat,long):
        query = self.URL+f"?lat={lat}&lon={long}&dataSet={self.dataSet}"
        api_response = requests.get(query).json()
        if api_response["message"]=='OK':
            return altiQueryResponse(alti=api_response["geoPoints"][0]["elevation"])
        return altiQueryResponse(error=api_response["message"])

class ignApiService():
    URL = "https://wxs.ign.fr/calcul/alti/rest/elevation.json"
    
    def QueryOnePoint(self,lat,long):
        query = self.URL+f"?lat={lat}&lon={long}"
        api_response = requests.get(query).json()
        return altiQueryResponse(alti=api_response["elevations"][0]["z"])
    
    def QueryMultiplePoints(self,points):
        query = self.URL+f"?lat={'|'.join([str(pt.lat) for pt in points])}&lon={'|'.join([str(pt.long) for pt in points])}"
        api_response = requests.get(query).json()
        return api_response["elevations"]
    

class altiQuery():
    
    def __init__(self,serviceChoice):
        if serviceChoice == 'IGN':
            self.service = ignApiService()
            self.dataSet = "IGN"
        else :
            self.service = elevationApiService()
            self.dataSet = self.service.dataSet
    
    def QueryOnePoint(self,lat,long):
        return self.service.QueryOnePoint(lat,long)
    
    def QueryMultiplePoints(self,points):
        return self.service.QueryMultiplePoints(points)
    