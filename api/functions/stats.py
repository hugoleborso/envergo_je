def getStats(point,surroundingPoints):
    alts = [pt['z'] for pt in surroundingPoints]
    min 
    return {'mean':sum(alts)/len(alts),'max':max(alts),'min':min(alts)}


def tripleCircleBassinVersant(point,pointAlti,circles,radii,eightQuadrants):
    surfaceCount=0
    
    for quadrant in quadrantsGenerator(point,circles,eightQuadrants=eightQuadrants):
        surfaceCount += nextCircleCheck(pointAlti,quadrant)
    
    return surfaceCount/100 


def nextCircleCheck(alti,quadrant,index=0,score=0,addedScore={0:1,1:8,2:16},elevationPercentage={0:1.02,1:1.05,2:1.05}):
        
    if index==len(quadrant):
        return score
    
    meanAlti = sum([pt['z'] for pt in quadrant[index]])/len(quadrant[index])
    if meanAlti>elevationPercentage[index]*alti:
        score+=addedScore[index]
        return nextCircleCheck(meanAlti,quadrant,index=index+1,score=score)
    return score
    

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
        return abs(centerPoint.long-pt['long'])>=abs(centerPoint.lat-pt['lat'])
    return abs(centerPoint.long-pt['long'])>abs(centerPoint.lat-pt['lat'])

def hasMovedMoreLat(centerPoint,pt,includeEqual=False): # on crée la fonction antagoniste par lisibilité du code
    if includeEqual:
        return abs(centerPoint.lat-pt['lat'])>=abs(centerPoint.long-pt['long'])
    return abs(centerPoint.lat-pt['lat'])>abs(centerPoint.long-pt['long'])