import matplotlib.pyplot as plt
import time
from local import main

from utils.carto import createQuadrants,loadCarto,getCartoInfo,fitToCarto


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

def testCarto(point):
    allColors=True
    qNb = 20
    radii = [50,75,100,130,160]
    innerRadius = 25
    slope = 0.05
    H = loadCarto('local/alti_data//RGEALTI_FXX_0330_6705_MNT_LAMB93_IGN69.asc')
    innerAlti,quads,allPoints = createQuadrants(point[0],point[1],5,innerRadius,radii,qNb)
    newAllPoints = [fitToCarto(p,getCartoInfo('local/alti_data//RGEALTI_FXX_0330_6705_MNT_LAMB93_IGN69.asc'))for p in allPoints]
    fig = plt.figure(figsize=(6, 3.2))
    ax = fig.add_subplot(111)
    res = main([point],5,innerRadius,radii,qNb,slope)
    ax.set_title('Alti and zones considered for the algo (1x = 5m)\nResult is '+str(res[0]))
    plt.imshow(H)
    
    if allColors:
        # not working but only for demo
        colors=['blue','purple','red','hotpink','pink','orange','yellow','lime','green','navy']
        newinnerAlti = [fitToCarto(p,getCartoInfo('local/alti_data//RGEALTI_FXX_0330_6705_MNT_LAMB93_IGN69.asc'))for p in innerAlti]
        ax.scatter([p[0] for p in newinnerAlti],[p[1] for p in newinnerAlti],color='grey',s=0.1)
        
        for q in range(qNb):
            for i,_ in enumerate(radii):
                newPoints = [fitToCarto(p,getCartoInfo('local/alti_data//RGEALTI_FXX_0330_6705_MNT_LAMB93_IGN69.asc'))for p in quads[q][i]]
                ax.scatter([p[0] for p in newPoints],[p[1] for p in newPoints],color=colors[q%len(colors)],edgecolor='none',s=(i+1)**2,alpha=0.5)
    else:
        newAllPoints = [fitToCarto(p,getCartoInfo('local/alti_data//RGEALTI_FXX_0330_6705_MNT_LAMB93_IGN69.asc'))for p in allPoints]
        ax.scatter([p[0] for p in newAllPoints],[p[1] for p in newAllPoints] ) # changer par l'affichage des quadrants si temps suffisant
    
    ax.set_aspect('equal')
    plt.colorbar(orientation='vertical')
    plt.show()

def stressTest():
    t0 = time.time()
    res = main([(334155,6701650)]*100,5,25,[50,75,100,130,160],8,0.05)
    t1 = time.time()

    total = t1-t0
    print('total time : ',total)

stressTest()
# testCarto((334155,6701650))
# print(main([(334155,6701650)],5,25,[50,75,100,130,160],8,0.05))



