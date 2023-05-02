from math import pi,ceil,inf
import numpy as np
import matplotlib.pyplot as plt


def getCartoInfo(fileName):
    info = {}
    with open(fileName) as f:
        info["ncols"]= int(f.readline().split(' ')[-1])
        info["nrows"]= int(f.readline().split(' ')[-1])
        info["xllcorner"]= float(f.readline().split(' ')[-1])
        info["yllcorner"]= float(f.readline().split(' ')[-1])
        info["cellsize"]= float(f.readline().split(' ')[-1])
        info["NODATA_value"]= float(f.readline().split(' ')[-1])
    return info

def loadCarto(fileName):
    return np.loadtxt(fileName, skiprows=6)


def createQuadrants(x, y, cartoPrecision, innerRadius, radii, quadrantsNb,debugPrints=False):

    quarterPointsNb = ceil(radii[-1]/cartoPrecision)
    quadrantsBins = np.linspace(0,2*pi,quadrantsNb+1)
    quadrants = {q:{r:[] for r in range(len(radii))} for q in range(quadrantsNb)}
    innerAltiPoints = []

    origin = complex(x,y)
    
    # generate the points using the complex plane
    for i in range(-quarterPointsNb,quarterPointsNb+1):
        for j in range(-quarterPointsNb,quarterPointsNb+1):
            
            # create the displacement
            disp = complex(cartoPrecision*i,cartoPrecision*j)
            new_point = origin+disp
            # find the corresponding 'donut'
            radiusNb = next(i for i,r in enumerate([innerRadius]+ radii+[inf]) if abs(disp) <= r)
            
            # if we are in a 'donut' 
            if radiusNb !=0 and radiusNb<=len(radii):
                
                # find the right quadrant (only using the displacement, not the new point)
                quadNb = np.digitize(np.angle(complex(round(disp.real),round(disp.imag)))%(2*pi),quadrantsBins)-1
                
                if debugPrints:
                    print('displace',disp,'radius',radiusNb)
                    print('pt:',round(new_point.real),round(new_point.imag),'angle',np.angle(disp)%(2*pi),'quad',quadNb)
                    print(str(quadrants[quadNb][radiusNb-1]))
                
                # adding the coordinates of the new point (int format to prevent floating point errors)
                quadrants[quadNb][radiusNb-1].append((round(new_point.real),round(new_point.imag)))
            
            # if we are in the inner disk    
            if not radiusNb:
                innerAltiPoints.append((round(new_point.real),round(new_point.imag)))
            
    return innerAltiPoints,quadrants


def testPlot():
    qNb = 8
    radii = [50,75,100,130,160]
    colors=['blue','purple','red','pink','orange','yellow','lime','green']
    innerAtli,quads = createQuadrants(x=34,y=100,cartoPrecision= 5,innerRadius= 25,radii=radii,quadrantsNb= qNb)
    for i in range(4):
        print(i,quads[i])
    plt.scatter([p[0] for p in innerAtli],[p[1] for p in innerAtli],color='grey',s=0.1)
    for q in range(qNb):
        for i,_ in enumerate(radii):
            plt.scatter([p[0] for p in quads[q][i]],[p[1] for p in quads[q][i]],color=colors[q],s=(i+1)**2)
    plt.show()


def getMeanAltiFromCarto(carto,pointsList):
    return np.mean(carto[[coord[0] for coord in pointsList], [coord[1] for coord in pointsList]])


def localMultiCircleBassinVersant(point,innerRadius,cartoPrecision,radii,quadrantsNb,slope):
    surfaceCount=0
    carto= loadCarto('f')
    innerCircleAlti, quadrants = createQuadrants(point.x, point.yy, cartoPrecision, innerRadius, radii, quadrantsNb)
    innerCircleMeanAlti = getMeanAltiFromCarto(carto,innerCircleAlti)
    
    for quadrant in quadrants:
        surfaceCount += nextQuadrantCheck(carto,innerCircleMeanAlti,quadrant,radii,slope=slope)
    
    return surfaceCount/quadrantsNb


def nextQuadrantCheck(carto,currentAlti,quadrant,radii,index=0,surface=0,slope=0.05):
        
    if index==len(quadrant):
        return surface
    
    meanAlti = getMeanAltiFromCarto(carto,quadrant[index])
    if checkElevationDiff(meanAlti,currentAlti,index,radii,slope):
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


# carto = loadCarto('local/alti_data/RGEALTI_FXX_0285_6710_MNT_LAMB93_IGN69.asc')
# print(carto[[0,1,2,3,4,5],[0,1,2,3,4,5]])
print(getCartoInfo('local/alti_data/RGEALTI_FXX_0285_6710_MNT_LAMB93_IGN69.asc'))
# testPlot()





