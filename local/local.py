from utils.bassin_versant import localMultiCircleBassinVersant
from utils.carto import cartoQuerier,createQuadrants,saveListToCarto
from tqdm import tqdm
import concurrent.futures
from tqdm import tqdm

class bassinVersantCalculator:
    def __init__(self,cartoMachine,params):
        self.cartoMachine=cartoMachine
        self.params=params
    
    def populateParams(self,cartoPrecision, innerRadius, radii, quadrantsNb,slope):
        self.params = {
            "cartoPrecision":cartoPrecision,
            "innerRadius":innerRadius,
            "radii":radii,
            "quadrantsNb":quadrantsNb,
            "slope":slope
        }
    
    def localMultiCircleBassinVersant(self,innerCircleAlti, quadrants):
        return localMultiCircleBassinVersant(innerCircleAlti,
                                             quadrants,
                                             self.params["radii"],
                                             self.params["quadrantsNb"],
                                             self.params["slope"])
        
    def process_point(self,point):
        innerCirclePoints, quadrantsPoints, allPoints = createQuadrants(point[0], 
                                                                        point[1], 
                                                                        self.params["cartoPrecision"], 
                                                                        self.params["innerRadius"], 
                                                                        self.params["radii"], 
                                                                        self.params["quadrantsNb"])
        self.cartoMachine.loadNeededCartos(allPoints)
        
        quadrants = []
        for q in range(self.params["quadrantsNb"]):
            quadrants.append([])
            for i, _ in enumerate(self.params["radii"]):
                quadrants[q].append([])
                quadrants[q][i] = self.cartoMachine.queryAlti(quadrantsPoints[q][i])

        innerCircleAlti = self.cartoMachine.queryAlti(innerCirclePoints)
        return (point, self.localMultiCircleBassinVersant(innerCircleAlti, quadrants))


def main(points,cartoPrecision, innerRadius, radii, quadrantsNb,slope):
    results = []
    cartoMachine = cartoQuerier('local/alti_data/')
    for point in tqdm(points):
        innerCirclePoints, quadrantsPoints,allPoints = createQuadrants(point[0],point[1], cartoPrecision, innerRadius, radii, quadrantsNb)
        cartoMachine.loadNeededCartos(allPoints)
        
        quadrants = []
        for q in range(quadrantsNb):
            quadrants.append([])
            for i,_ in enumerate(radii):
                quadrants[q].append([])
                quadrants[q][i]=cartoMachine.queryAlti(quadrantsPoints[q][i])

        innerCircleAlti = cartoMachine.queryAlti(innerCirclePoints)
        results.append((point,localMultiCircleBassinVersant(innerCircleAlti,quadrants,radii,quadrantsNb,slope)))
    
    return results

def mainThreading(points,cartoPrecision, innerRadius, radii, quadrantsNb,slope):
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(2) as executor:
        
        BvMachine = bassinVersantCalculator(cartoQuerier('local/alti_data/'),None)
        BvMachine.populateParams(cartoPrecision, innerRadius, radii, quadrantsNb,slope)
        
        futures = [executor.submit(BvMachine.process_point, point) for point in points]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            results.append(future.result())

    return results

def cartoCreator(bottomLeft, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, innerRadius, radii, quadrantsNb, slope):
    points = []
    for y in range(height):
        for x in range(width):
            points.append((round(bottomLeft[0]+x*outputCartoPrecision),round(bottomLeft[1]+y*outputCartoPrecision)))
    
    print("====== starting carto creation ======\n")
    
    res = mainThreading(points, inputCartoPrecision, innerRadius, radii, quadrantsNb, slope)
    
    # saveListToCarto(res,ouptutFile,{"ncols": width,"nrows": height,"xllcorner": bottomLeft[0]-outputCartoPrecision/2, "yllcorner" : bottomLeft[1]+outputCartoPrecision/2,"cellsize"  :outputCartoPrecision,"NODATA_value":  -99999.00})
    saveListToCarto(res,ouptutFile,{"ncols": width,"nrows": height,"xllcorner": bottomLeft[0], "yllcorner" : bottomLeft[1],"cellsize"  :outputCartoPrecision,"NODATA_value":  -99999.00})
    

            