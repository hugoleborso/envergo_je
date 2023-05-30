import os
from utils.bassin_versant import localMultiCircleBassinVersant

from utils import carto
from utils import cartoOneTile
from tqdm import tqdm
import warnings
from time import time
warnings.filterwarnings("ignore")
#ignore when numpy is trying to do the mean of an empty slice

def main(points,cartoPrecision, innerRadius, radii, quadrantsNb,slope,inputFolder='local/alti_data/'):
    results = []
    times = [0,0,0,0]
    cartoMachine = carto.cartoQuerier(inputFolder)

    OriginLessInnerCirclePoints, OriginLessQuadrantsPoints,OriginLessAllPoints = carto.createQuadrants( cartoPrecision, innerRadius, radii, quadrantsNb)
    for point in tqdm(points, leave=False):
        innerCirclePoints = carto.updateOrigin(point,OriginLessInnerCirclePoints)
        allPoints = carto.updateOrigin(point,OriginLessAllPoints)
        t0=time()
        cartoMachine.loadNeededCartos(allPoints)
        t1=time()
        times[1]+=t1-t0
        
        quadrants = []
        for q in range(quadrantsNb):
            quadrants.append([])
            for i,_ in enumerate(radii):
                quadrants[q].append([])
                t0=time()
                quadrants[q][i]=cartoMachine.queryAlti(carto.updateOrigin(point,OriginLessQuadrantsPoints[q][i]))
                t1=time()
                times[2]+=t1-t0
        t0=time()
        innerCircleAlti = cartoMachine.queryAlti(innerCirclePoints)
        t1=time()
        times[2]+=t1-t0
        t0=time()
        results.append((point,localMultiCircleBassinVersant(innerCircleAlti,quadrants,radii,quadrantsNb,slope)))
        t1=time()
        times[3]+=t1-t0
    print("TIME SPENT")
    print('Creating Quadrants',times[0])
    print('Loading Cartos',times[1])
    print('Querying Alti',times[2])
    print('Calculating bassin versant',times[3])
    return results

def fasterMain(points,cartoPrecision, innerRadius, radii, quadrantsNb,slope,currentTile,inputFolder='local/alti_data/'):
    
    results = []
    times=[0,0,0,0]
    t0=time()
    cartoMachine = cartoOneTile.cartoQuerierOneTile(inputFolder,currentTile)
    t1=time()
    times[0]+=t1-t0
    OriginLessInnerCirclePoints, OriginLessQuadrantsPoints,_ = carto.createQuadrants( cartoPrecision, innerRadius, radii, quadrantsNb)
    for point in tqdm(points, leave=False):
        if cartoMachine.queryOnePoint(point) is not None:
            t0=time()
            innerCirclePoints=carto.updateOrigin(point,OriginLessInnerCirclePoints)
            t1=time()
            times[1]+=t1-t0
            quadrants = []
            for q in range(quadrantsNb):
                quadrants.append([])
                for i,_ in enumerate(radii):
                    quadrants[q].append([])
                    t0=time()
                    quadrants[q][i]=cartoMachine.queryAltis(carto.updateOrigin(point,OriginLessQuadrantsPoints[q][i]))
                    t1=time()
                    times[2]+=t1-t0

            innerCircleAlti = cartoMachine.queryAltis(innerCirclePoints)
            t0=time()
            results.append((point,localMultiCircleBassinVersant(innerCircleAlti,quadrants,radii,quadrantsNb,slope)))
            t1=time()
            times[3]+=t1-t0
        else:
            results.append((point,None))
    print("TIME SPENT")
    print('Creating CartoQuerier',times[0])
    print('Creating Quadrants',times[1])
    print('Querying Alti',times[2])
    print('Calculating bassin versant',times[3])
    return results

def cartoCreator(bottomLeft, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, innerRadius, radii, quadrantsNb, slope,inputFolder='local/alti_data/'):
    points = []
    for y in range(height):
        for x in range(width):
            points.append((round(bottomLeft[0]+x*outputCartoPrecision),round(bottomLeft[1]+y*outputCartoPrecision)))
    
    res = main(points, inputCartoPrecision, innerRadius, radii, quadrantsNb, slope, inputFolder)
    
    # saveListToCarto(res,ouptutFile,{"ncols": width,"nrows": height,"xllcorner": bottomLeft[0]-outputCartoPrecision/2, "yllcorner" : bottomLeft[1]+outputCartoPrecision/2,"cellsize"  :outputCartoPrecision,"NODATA_value":  -99999.00})
    carto.saveListToCarto(res,ouptutFile,{"ncols": width,"nrows": height,"xllcorner": bottomLeft[0], "yllcorner" : bottomLeft[1],"cellsize"  :outputCartoPrecision,"NODATA_value":  -99999.00})
    
def cartoCreatorFaster(bottomLeft,currentTile, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, innerRadius, radii, quadrantsNb, slope,inputFolder='local/alti_data/'):
    points = []
    for y in range(height):
        for x in range(width):
            points.append((round(bottomLeft[0]+x*outputCartoPrecision),round(bottomLeft[1]+y*outputCartoPrecision)))
    
    res = fasterMain(points, inputCartoPrecision, innerRadius, radii, quadrantsNb, slope, currentTile,inputFolder)
    
    # saveListToCarto(res,ouptutFile,{"ncols": width,"nrows": height,"xllcorner": bottomLeft[0]-outputCartoPrecision/2, "yllcorner" : bottomLeft[1]+outputCartoPrecision/2,"cellsize"  :outputCartoPrecision,"NODATA_value":  -99999.00})
    carto.saveListToCarto(res,ouptutFile,{"ncols": width,"nrows": height,"xllcorner": bottomLeft[0], "yllcorner" : bottomLeft[1],"cellsize"  :outputCartoPrecision,"NODATA_value":  -99999.00})
    
    
    
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
    
    print("Progression : first bar is the number of cartos, second is the current carto creation")
    for file in tqdm(os.listdir(inputFolder)):
        info = carto.getCartoInfo(inputFolder+'/'+file)
        bottomLeft=(info["xllcorner"],info["yllcorner"])
        ouptutFile = outputFolder+"/ENVERGO_BASSSIN_VERSANT_FXX_"+"{:04d}".format(round(bottomLeft[0]/1000))+"_"+"{:04d}".format(round(bottomLeft[1]/1000))+"_MNT_LAMB93.asc"
        # cartoCreator(bottomLeft, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, innerRadius, radii, quadrantsNb, slope,inputFolder)
        cartoCreatorFaster(bottomLeft,file, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, innerRadius, radii, quadrantsNb, slope,inputFolder)