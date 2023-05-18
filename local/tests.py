import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import numpy as np


from local import main,cartoCreator
from utils.carto import createQuadrants,loadCarto,getCartoInfo,fitToCarto,saveArrayToCarto


def testPlot():
    qNb = 8
    radii = [50,75,100,130,160]
    innerAtli,quads,_ = createQuadrants(x=1155,y=1650,cartoPrecision= 5,innerRadius= 25,radii=radii,quadrantsNb= qNb)
    for i in range(4):
        print(i,quads[i])
    plotQuadrants(innerAtli,quads,radii,qNb)

def plotQuadrants(innerAtli, quads, radii, qNb):
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
    qNb = 10
    radii = [50,75,100,130,160]
    innerRadius = 25
    slope = 0.05
    innerAlti,quads,allPoints = createQuadrants(point[0],point[1],5,innerRadius,radii,qNb)
    newAllPoints = [fitToCarto(p,getCartoInfo('local/alti_data//RGEALTI_FXX_0330_6705_MNT_LAMB93_IGN69.asc'))for p in allPoints]
    fig = plt.figure(figsize=(6, 3.2))
    ax = fig.add_subplot(111)
    res = main([point],5,innerRadius,radii,qNb,slope)
    plotAltiCarto(
        'local/alti_data//RGEALTI_FXX_0330_6705_MNT_LAMB93_IGN69.asc',
        'Alti and zones considered for the algo (1x = 5m)\nResult is '+str(res[0]),
        ax)
    
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

def plotAltiCarto(altiCartoFile, title, alpha=1, stretch=1, givenAx=None, colormap=None,vmin=None,vmax=None):
    
    if givenAx is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else :
        ax = givenAx
        
    H = loadCarto(altiCartoFile)
    H = np.repeat(np.repeat(H,stretch, axis=0), stretch, axis=1)
    ax.set_title(title)
    
    if colormap=='bassinVersant':
        cmap = mpl.colors.ListedColormap(['white', 'orange','red'])
        my_cmap = cmap(np.arange(cmap.N))
        my_cmap[:,-1] = [0,1,0.7]
        my_cmap = mpl.colors.ListedColormap(my_cmap)
        bounds=[0,3000,8000,80000]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        plt.imshow(H,alpha=alpha,cmap=my_cmap,norm=norm)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('surface de bassin versant en m2', rotation=270)
        
    elif colormap=='alti':
        plt.imshow(H,alpha=alpha,cmap=mpl.colormaps['gist_earth'],vmin = -50,vmax = 100)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('altitude en m', rotation=270)
    
    elif colormap:
        plt.imshow(H,alpha=alpha,cmap=mpl.colormaps[colormap],vmin=vmin,vmax=vmax)
        plt.colorbar()
    
    else:
        plt.imshow(H,alpha=alpha)
        plt.colorbar()
        
    return ax 

def stressTest():
    t0 = time.time()
    res = main([(334155,6701650)]*100,5,25,[50,75,100,130,160],8,0.05)
    t1 = time.time()

    total = t1-t0
    print('total time : ',total)

def testCartoCreator(bottomLeft, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, ouptutScreenShot, innerRadius, radii, quadrantsNb, slope):
    cartoCreator(bottomLeft, outputCartoPrecision, inputCartoPrecision, width, height, ouptutFile, innerRadius, radii, quadrantsNb, slope)
    carte = 'local/alti_data/RGEALTI_FXX_0'+str(bottomLeft[0]//1000)+'_'+str(bottomLeft[1]//1000+5)+'_MNT_LAMB93_IGN69.asc'
    bassinVersantPlot(carte, ouptutFile, ouptutScreenShot)

def bassinVersantPlot(altiFile, bassinVersantFile, savePng, title='Bassin versant \n1 unité = 5m'):
    bassinVersantFileInfo = getCartoInfo(bassinVersantFile)
    altiFileInfo = getCartoInfo(altiFile)
    ax = plotAltiCarto(altiFile,title,colormap='alti')
    ax = plotAltiCarto(bassinVersantFile,title,alpha=0.5,stretch=round(altiFileInfo["nrows"]/bassinVersantFileInfo["nrows"]),colormap='bassinVersant',givenAx=ax)
    plt.savefig(savePng,dpi=500)

    plt.show()

def compareCartos(carto1,carto2,stretch=(1,1)):
    c1 = np.repeat(np.repeat(loadCarto(carto1),stretch[0], axis=0), stretch[0], axis=1)
    c2 = np.repeat(np.repeat(loadCarto(carto2),stretch[1], axis=0), stretch[1], axis=1)
    carName1 = carto1.split('/')[-1].split('.')[0]
    carName2 = carto2.split('/')[-1].split('.')[0]
    diff = c1-c2
    print('\n ====== Comparaison : '+carName1+' et  '+carName2+' ======')
    print("stats c1 : moyenne : ",np.mean(c1),"ecart type : ",np.std(c1))
    print("stats c2 : moyenne : ",np.mean(c2),"ecart type : ",np.std(c2))
    print('abs diff moyenne :',np.mean(np.abs(diff)),'\n')
    saveArrayToCarto(diff,'local/output/diff_'+carName1+'_'+carName2+'.asc',getCartoInfo(carto1))
    ax = plotAltiCarto('local/output/diff_'+carName1+'_'+carName2+'.asc',title='Pourcentage de différence : '+carName1+' et  '+carName2,alpha=1,colormap='cool',vmin = -10000,vmax = 10000)
    plt.savefig('local/output/diff_'+carName1+'_'+carName2+'.png',dpi=500)

    plt.show()
    

# stressTest()
# testCarto((334155,6701650))
# print(main([(334155,6701650)],5,25,[50,75,100,130,160],8,0.05))

generateCartos = False
if generateCartos:
    name = 'test_20_20_8'
    testCartoCreator(
        bottomLeft = (285000,6705000),
        outputCartoPrecision = 20,
        inputCartoPrecision = 20,
        width = 250,
        height = 250,
        ouptutFile = 'local/output/'+name+'.asc',
        ouptutScreenShot = 'local/output/'+name+'.png',
        innerRadius = 25,
        radii = [50,75,100,130,160],
        quadrantsNb = 8,
        slope = 0.05
        )
    name = 'test_20_20_12'
    testCartoCreator(
        bottomLeft = (285000,6705000),
        outputCartoPrecision = 20,
        inputCartoPrecision = 20,
        width = 250,
        height = 250,
        ouptutFile = 'local/output/'+name+'.asc',
        ouptutScreenShot = 'local/output/'+name+'.png',
        innerRadius = 25,
        radii = [50,75,100,130,160],
        quadrantsNb = 12,
        slope = 0.05
        )
    name = 'test_20_5_12'
    testCartoCreator(
        bottomLeft = (285000,6705000),
        outputCartoPrecision = 20,
        inputCartoPrecision = 5,
        width = 250,
        height = 250,
        ouptutFile = 'local/output/'+name+'.asc',
        ouptutScreenShot = 'local/output/'+name+'.png',
        innerRadius = 25,
        radii = [50,75,100,130,160],
        quadrantsNb = 12,
        slope = 0.05
        )

# compareCartos('local/output/test_20_20_8.asc','local/output/test_20_20_12.asc')
# compareCartos('local/output/test_20_20_12.asc','local/output/test_20_5_12.asc')

name = 'test_20_10_12'
testCartoCreator(
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
    )

# # bassinVersantPlot()







