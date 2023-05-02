
import matplotlib.pyplot as plt
import numpy as np
from utils.carto import fitToCarto

from utils.bassin_versant import localMultiCircleBassinVersant
from utils.carto import cartoQuerier,createQuadrants,loadCarto,getCartoInfo

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
            print('q',q,'i',i,'alti',np.mean(quadrants[q][i]))

    innerCircleAlti = cartoMachine.queryAlti(innerCirclePoints)
    
    return localMultiCircleBassinVersant(innerCircleAlti,quadrants,radii,quadrantsNb,slope)

#region test


def testPlot():
    qNb = 8
    radii = [50,75,100,130,160]
    innerAtli,quads,_ = createQuadrants(x=1155,y=1650,cartoPrecision= 5,innerRadius= 25,radii=radii,quadrantsNb= qNb)
    for i in range(4):
        print(i,quads[i])
    plotQuadrants(innerAtli,quads,radii,qNb)

def plotQuadrants(innerAtli,quads,radii,qNb):
    colors=['blue','purple','red','pink','orange','yellow','lime','green']
    fig, ax = plt.subplots()
    ax.set_xlim([0, 1000])
    ax.set_ylim([0, 1000])
    ax.scatter([p[0] for p in innerAtli],[p[1] for p in innerAtli],color='grey',s=0.1)
    for q in range(qNb):
        for i,_ in enumerate(radii):
            ax.scatter([1000-p[1]/5 for p in quads[q][i]],[p[0]/5 for p in quads[q][i]],color=colors[q],s=(i+1)**2)


    plt.show()

def testCarto():
    H = loadCarto('local/alti_data//RGEALTI_FXX_0330_6705_MNT_LAMB93_IGN69.asc')
    _,_,allPoints = createQuadrants(334155,6701650,5,25,[50,75,100,130,160],8)
    newAllPoints = [fitToCarto(p,getCartoInfo('local/alti_data//RGEALTI_FXX_0330_6705_MNT_LAMB93_IGN69.asc'))for p in allPoints]
    fig = plt.figure(figsize=(6, 3.2))
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    plt.imshow(H)
    plt.scatter([p[0] for p in newAllPoints],[p[1] for p in newAllPoints] ) # changer par l'affichage des quadrants si temps suffisant
    ax.set_aspect('equal')
    plt.colorbar(orientation='vertical')
    plt.show() 

# carto = loadCarto('local/alti_data/RGEALTI_FXX_0285_6710_MNT_LAMB93_IGN69.asc')
# print(carto[[0,1,2,3,4,5],[0,1,2,3,4,5]])
# print(getCartoInfo('local/alti_data/RGEALTI_FXX_0285_6710_MNT_LAMB93_IGN69.asc'))
# testPlot()
testCarto()
#endregion

# print(main(334155,6701650,5,25,[50,75,100,130,160],8,0.05))



