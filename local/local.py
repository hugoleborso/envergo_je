import os
from utils.bassin_versant import localMultiCircleBassinVersant
from utils.carto import cartoQuerier,createQuadrants,saveListToCarto,getCartoInfo
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")
#ignore when numpy is trying to do the mean of an empty slice

def main(points,cartoPrecision, innerRadius, radii, quadrantsNb,slope,inputFolder='local/alti_data/'):
    results = []
    cartoMachine = cartoQuerier(inputFolder)
    for point in tqdm(points, leave=False):
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

def cartoCreator(bottomLeft, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, innerRadius, radii, quadrantsNb, slope,inputFolder='local/alti_data/'):
    points = []
    for y in range(height):
        for x in range(width):
            points.append((round(bottomLeft[0]+x*outputCartoPrecision),round(bottomLeft[1]+y*outputCartoPrecision)))
    
    res = main(points, inputCartoPrecision, innerRadius, radii, quadrantsNb, slope, inputFolder)
    
    # saveListToCarto(res,ouptutFile,{"ncols": width,"nrows": height,"xllcorner": bottomLeft[0]-outputCartoPrecision/2, "yllcorner" : bottomLeft[1]+outputCartoPrecision/2,"cellsize"  :outputCartoPrecision,"NODATA_value":  -99999.00})
    saveListToCarto(res,ouptutFile,{"ncols": width,"nrows": height,"xllcorner": bottomLeft[0], "yllcorner" : bottomLeft[1],"cellsize"  :outputCartoPrecision,"NODATA_value":  -99999.00})
    
def bulkCartoCreator(inputFolder,outputFolder):
    print("\nRunning Bulk Carto Creator in "+inputFolder+' ...\n')
    
    #region parameters
    outputCartoPrecision = 20
    inputCartoPrecision = 20
    width = 250
    height = 250
    innerRadius = 25
    radii = [50,75,100,130,160]
    quadrantsNb = 8
    slope = 0.05
    #endregion
    
    neededCartosCoordinates=[]
    for file in os.listdir(inputFolder):
        info = getCartoInfo(inputFolder+'/'+file)
        neededCartosCoordinates.append((info["xllcorner"],info["yllcorner"]))
    print("Progression : first bar is the number of cartos, second is the current carto creation")
    for bottomLeft in tqdm(neededCartosCoordinates):
        ouptutFile = outputFolder+"/ENVERGO_BASSSIN_VERSANT_FXX_"+"{:04d}".format(round(bottomLeft[0]/1000))+"_"+"{:04d}".format(round(bottomLeft[1]/1000))+"_MNT_LAMB93.asc"
        cartoCreator(bottomLeft, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, innerRadius, radii, quadrantsNb, slope,inputFolder)