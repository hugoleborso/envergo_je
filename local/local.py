from utils.bassin_versant import localMultiCircleBassinVersant
from utils.carto import cartoQuerier,createQuadrants,saveListToCarto
from tqdm import tqdm

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
        results.append(localMultiCircleBassinVersant(innerCircleAlti,quadrants,radii,quadrantsNb,slope))
    
    return results


def cartoCreator(bottomLeft, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, innerRadius, radii, quadrantsNb, slope):
    points = []
    for y in range(height-1,-1,-1):
        for x in range(width):
            points.append((round(bottomLeft[0]+x*outputCartoPrecision),round(bottomLeft[1]+y*outputCartoPrecision)))
    
    print("====== starting carto creation ======\n")
    
    res = main(points, inputCartoPrecision, innerRadius, radii, quadrantsNb, slope)
    
    saveListToCarto(res,ouptutFile,{"ncols": width,"nrows": height,"xllcorner": bottomLeft[0]-outputCartoPrecision/2, "yllcorner" : bottomLeft[1]+outputCartoPrecision/2,"cellsize"  :outputCartoPrecision,"NODATA_value":  -99999.00})
    

            