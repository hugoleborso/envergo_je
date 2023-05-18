from tests import bassinVersantPlot
from utils.bassin_versant import localMultiCircleBassinVersant
from utils.carto import cartoQuerier,createQuadrants,saveListToCarto
import multiprocessing
from tqdm import tqdm

def process_point(point, cartoMachine, cartoPrecision, innerRadius, radii, quadrantsNb,slope):
        innerCirclePoints, quadrantsPoints, _ = createQuadrants(point[0], point[1], cartoPrecision, innerRadius, radii, quadrantsNb)

        quadrants = []
        for q in range(quadrantsNb):
            quadrants.append([])
            for i, _ in enumerate(radii):
                quadrants[q].append([])
                quadrants[q][i] = cartoMachine.queryAlti(quadrantsPoints[q][i])

        innerCircleAlti = cartoMachine.queryAlti(innerCirclePoints)
        return (point, localMultiCircleBassinVersant(innerCircleAlti, quadrants, radii, quadrantsNb, slope))

if __name__=="__main__":
    name = 'test_20_10_12'
    bottomLeft = (285000,6705000),
    outputCartoPrecision = 20,
    inputCartoPrecision = 10,
    width = 500,
    height = 500,
    ouptutFile = 'local/output/'+name+'.asc',
    ouptutScreenShot = 'local/output/'+name+'.png',
    innerRadius = 25,
    radii = [50,75,100,130,160],
    quadrantsNb = 12,
    slope = 0.05
    
    points = []
    
    for y in range(height):
        for x in range(width):
            points.append((round(bottomLeft[0]+x*outputCartoPrecision),round(bottomLeft[1]+y*outputCartoPrecision)))

    results = []
    
    with multiprocessing.Pool() as pool:
        cartoMachine = cartoQuerier('local/alti_data/')  # Create a single cartoQuerier instance

        # Use pool.starmap to apply the process_point function to each point in parallel
        results = list(tqdm(pool.starmap(process_point, [(point, cartoMachine, inputCartoPrecision, innerRadius, radii, quadrantsNb,slope) for point in points]), total=len(points)))

    saveListToCarto(results,ouptutFile,{"ncols": width,"nrows": height,"xllcorner": bottomLeft[0], "yllcorner" : bottomLeft[1],"cellsize"  :outputCartoPrecision,"NODATA_value":  -99999.00})
    carte = 'local/alti_data/RGEALTI_FXX_0'+str(bottomLeft[0]//1000)+'_'+str(bottomLeft[1]//1000+5)+'_MNT_LAMB93_IGN69.asc'
    bassinVersantPlot(carte, ouptutFile, ouptutScreenShot)
