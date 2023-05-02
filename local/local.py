
import matplotlib.pyplot as plt

from utils.bassin_versant import localMultiCircleBassinVersant
from utils.carto import cartoQuerier,createQuadrants

def main(x,y,cartoPrecision, innerRadius, radii, quadrantsNb,slope):
    innerCirclePoints, quadrantsPoints,allPoints = createQuadrants(x, y, cartoPrecision, innerRadius, radii, quadrantsNb)
    # plotQuadrants(innerCirclePoints,quadrantsPoints,radii,quadrantsNb)
    # print(allPoints)
    cartoMachine = cartoQuerier('local/alti_data/')
    cartoMachine.loadNeededCartos(allPoints)
    print(cartoMachine.loadedCartos)
    quadrants = []
    for q in range(quadrantsNb):
        quadrants.append([])
        for i,_ in enumerate(radii):
            quadrants[q].append([])
            quadrants[q][i]=cartoMachine.queryAlti(quadrantsPoints[q][i])
            print('q',q,'i',i,'alti',len(quadrants[q][i]))

    innerCircleAlti = cartoMachine.queryAlti(innerCirclePoints)
    
    return localMultiCircleBassinVersant(innerCircleAlti,quadrants,radii,quadrantsNb,slope)

#region test


def testPlot():
    qNb = 8
    radii = [50,75,100,130,160]
    innerAtli,quads = createQuadrants(x=34,y=100,cartoPrecision= 5,innerRadius= 25,radii=radii,quadrantsNb= qNb)
    for i in range(4):
        print(i,quads[i])
    plotQuadrants(innerAtli,quads,radii,qNb)

def plotQuadrants(innerAtli,quads,radii,qNb):
    colors=['blue','purple','red','pink','orange','yellow','lime','green']

    plt.scatter([p[0] for p in innerAtli],[p[1] for p in innerAtli],color='grey',s=0.1)
    for q in range(qNb):
        for i,_ in enumerate(radii):
            plt.scatter([p[0] for p in quads[q][i]],[p[1] for p in quads[q][i]],color=colors[q],s=(i+1)**2)
    plt.show()
    

# carto = loadCarto('local/alti_data/RGEALTI_FXX_0285_6710_MNT_LAMB93_IGN69.asc')
# print(carto[[0,1,2,3,4,5],[0,1,2,3,4,5]])
# print(getCartoInfo('local/alti_data/RGEALTI_FXX_0285_6710_MNT_LAMB93_IGN69.asc'))
# testPlot()

#endregion

print(main(285620,6707610,5,25,[50,75,100,130,160],8,0.05))



