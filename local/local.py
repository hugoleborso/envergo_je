import os
from utils import bassin_versant

from utils import carto
from utils import cartoOneTile
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")
#ignore when numpy is trying to do the mean of an empty slice

def main(points,cartoPrecision, innerRadius, radii, quadrantsNb,slope,currentTile,inputFolder='local/alti_data/'):
    
    results = []
    
    cartoMachine = cartoOneTile.cartoQuerierOneTile(inputFolder,currentTile)
    
    OriginLessInnerCirclePoints, OriginLessQuadrantsPoints,_ = carto.createQuadrants( cartoPrecision, innerRadius, radii, quadrantsNb)
    for point in tqdm(points, leave=False):
        if cartoMachine.queryOnePoint(point) is not None:
            
            innerCirclePoints=carto.updateOrigin(point,OriginLessInnerCirclePoints)
            
            quadrants = []
            for q in range(quadrantsNb):
                quadrants.append([])
                for i,_ in enumerate(radii):
                    quadrants[q].append([])
                    quadrants[q][i]=cartoMachine.queryAltis(carto.updateOrigin(point,OriginLessQuadrantsPoints[q][i]))
        
            innerCircleAlti = cartoMachine.queryAltis(innerCirclePoints)
            results.append((point,bassin_versant.calc(innerCircleAlti,quadrants,radii,quadrantsNb,slope)))

        else:
            results.append((point,None))

    return results

def cartoCreator(bottomLeft,currentTile, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, innerRadius, radii, quadrantsNb, slope,inputFolder='local/alti_data/'):
    points = []
    for y in range(height):
        for x in range(width):
            points.append((round(bottomLeft[0]+x*outputCartoPrecision),round(bottomLeft[1]+y*outputCartoPrecision)))
    
    res = main(points, inputCartoPrecision, innerRadius, radii, quadrantsNb, slope, currentTile,inputFolder)
    
    carto.saveListToCarto(res,ouptutFile,{"ncols": width,"nrows": height,"xllcorner": bottomLeft[0], "yllcorner" : bottomLeft[1],"cellsize"  :outputCartoPrecision,"NODATA_value":  -99999.00})
    
    
    
def bulkCartoCreator(inputFolder,outputFolder):
    print("\nRunning Bulk Carto Creator in "+inputFolder+' ...\n')
    
    #region parameters
    outputCartoPrecision = 20
    inputCartoPrecision = 5
    width = 250
    height = 250
    innerRadius = 25
    radii = [50,75,100,130,160]
    quadrantsNb = 12
    slope = 0.05
    #endregion
    
    print("Progression : first bar is the number of cartos, second is the current carto creation")
    for file in tqdm(os.listdir(inputFolder)):
        info = carto.getCartoInfo(inputFolder+'/'+file)
        bottomLeft=(info["xllcorner"],info["yllcorner"])
        ouptutFile = outputFolder+"/ENVERGO_BASSSIN_VERSANT_FXX_"+"{:04d}".format(round(bottomLeft[0]/1000))+"_"+"{:04d}".format(round(bottomLeft[1]/1000))+"_MNT_LAMB93.asc"
        cartoCreator(bottomLeft,inputFolder+'/'+file, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, innerRadius, radii, quadrantsNb, slope,inputFolder)