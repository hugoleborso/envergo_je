from math import pi

def getStats(point,surroundingPoints):
    alts = [pt['z'] for pt in surroundingPoints]
    min 
    return {'mean':sum(alts)/len(alts),'max':max(alts),'min':min(alts)}


def multiCircleBassinVersant(point,innerCircleAlti,circles,radii,eightQuadrants,slope):
    surfaceCount=0
    innerCircleMeanAlti = sum([pt['z'] for pt in innerCircleAlti])/len(innerCircleAlti)
    
    for quadrant in quadrantsGenerator(point,circles,eightQuadrants=eightQuadrants):
        surfaceCount += nextQuadrantCheck(innerCircleMeanAlti,quadrant,radii,slope=slope)
    
    return surfaceCount/8 if eightQuadrants else surfaceCount/4


def nextQuadrantCheck(alti,quadrant,radii,index=0,surface=0,slope=0.05):
        
    if index==len(quadrant):
        return surface
    
    meanAlti = sum([pt['z'] for pt in quadrant[index]])/len(quadrant[index])
    if checkElevationDiff(meanAlti,alti,index,radii,slope):
        surface+=getSurface(index,radii)
        return nextQuadrantCheck(meanAlti,quadrant,radii,index=index+1,surface=surface,slope=slope)
    return surface


def checkElevationDiff(meanAlti,altiToCheck,index,radii,slope):
    if index == 0:
        return (meanAlti-altiToCheck)/(radii[0]/2)>slope
    else :
        return (meanAlti-altiToCheck)/((radii[index]-radii[index-1])/2)>slope
    
    
def getSurface(index,radii):
    if index == 0:
        return pi*radii[index]**2
    else:
        return pi*radii[index]**2-pi*radii[index-1]**2


def quadrantsGenerator(centerPoint,circles,eightQuadrants=False):
    quadrants=[]
    if not eightQuadrants:
        for q in ['NW','NE','SE','SW']:
            quadrants.append([[pt for pt in circle if isQuadrant(q,centerPoint,pt)] for circle in circles])
    else:
        for i,q in enumerate(['NW','NE','SE','SW']):
            quadrants.append([[pt for pt in circle if isQuadrant(q,centerPoint,pt) and hasMovedMoreLat(centerPoint,pt,includeEqual=i%2)] for circle in circles])
            quadrants.append([[pt for pt in circle if isQuadrant(q,centerPoint,pt) and hasMovedMoreLong(centerPoint,pt,includeEqual=(i-1)%2)] for circle in circles])
        # resultat : NNW,NWW,NNE,NEE,SSE,SEE,SSW,SWW, avec une chacun frontière avec condition de type '>=' et une de type '>'
    return quadrants


def isQuadrant(quadrant,centerPoint,pt):
    match quadrant:
        case 'NW':
            return pt['lat']>=centerPoint.lat and pt['lon']<centerPoint.long
        case 'NE':
            return pt['lat']>centerPoint.lat and pt['lon']>=centerPoint.long
        case 'SE':
            return pt['lat']<=centerPoint.lat and pt['lon']>centerPoint.long
        case 'SW':
            return pt['lat']<centerPoint.lat and pt['lon']>=centerPoint.long


def hasMovedMoreLong(centerPoint,pt,includeEqual=False):
    if includeEqual:
        return abs(centerPoint.long-pt['lon'])>=abs(centerPoint.lat-pt['lat'])
    return abs(centerPoint.long-pt['lon'])>abs(centerPoint.lat-pt['lat'])

def hasMovedMoreLat(centerPoint,pt,includeEqual=False): # on crée la fonction antagoniste par lisibilité du code
    if includeEqual:
        return abs(centerPoint.lat-pt['lat'])>=abs(centerPoint.long-pt['lon'])
    return abs(centerPoint.lat-pt['lat'])>abs(centerPoint.long-pt['lon'])