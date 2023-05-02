from utils.bassin_versant import localMultiCircleBassinVersant
from utils.carto import cartoQuerier,createQuadrants

def main(points,cartoPrecision, innerRadius, radii, quadrantsNb,slope):
    results = []
    cartoMachine = cartoQuerier('local/alti_data/')
    for point in points:
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

