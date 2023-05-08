import numpy as np
from math import pi,ceil,inf
import os


def getCartoInfo(fileName):
    info = {}
    with open(fileName) as f:
        info["fileName"]= fileName
        info["ncols"]= int(f.readline().split(' ')[-1])
        info["nrows"]= int(f.readline().split(' ')[-1])
        info["xllcorner"]= float(f.readline().split(' ')[-1])
        info["yllcorner"]= float(f.readline().split(' ')[-1])
        info["cellsize"]= float(f.readline().split(' ')[-1])
        info["NODATA_value"]= float(f.readline().split(' ')[-1])
        info['x_range']=(round(info["xllcorner"]+info["cellsize"]/2),round(info["xllcorner"]+info["ncols"]*info["cellsize"]-info["cellsize"]/2))
        info['y_range']=(round(info["yllcorner"]-info["cellsize"]/2),round(info["yllcorner"]+info["nrows"]*info["cellsize"]-info["cellsize"]*3/2))
    return info

def loadCarto(fileName):
    return np.loadtxt(fileName, skiprows=6)

def saveListToCarto(list,fileName,info):
    saveArrayToCarto(np.reshape(list, (info["ncols"],info["nrows"])),fileName,info)

def saveArrayToCarto(array,fileName,info):
    header = "ncols     %s\n" % info["ncols"]
    header += "nrows    %s\n" % info["nrows"]
    header += "xllcorner %s\n" % info["xllcorner"]
    header += "yllcorner %s\n" % info["yllcorner"]
    header += "cellsize %s\n" % info["cellsize"]
    header += "NODATA_value %s\n" % info["NODATA_value"]
    
    np.savetxt(fileName, array, header=header, fmt="%1.2f")

def createQuadrants(x, y, cartoPrecision, innerRadius, radii, quadrantsNb,debugPrints=False):

    quarterPointsNb = ceil(radii[-1]/cartoPrecision)
    quadrantsBins = np.linspace(0,2*pi,quadrantsNb+1)
    quadrants = {q:{r:[] for r in range(len(radii))} for q in range(quadrantsNb)}
    innerAltiPoints = []
    allPoints = []

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
                allPoints.append((round(new_point.real),round(new_point.imag)))
            
            # if we are in the inner disk    
            if not radiusNb:
                innerAltiPoints.append((round(new_point.real),round(new_point.imag)))
            
    return innerAltiPoints,quadrants,allPoints

class cartoQuerier:
    def __init__(self,carto_dir) -> None:
        self.loadedCartos = []
        self.availableCartos=[]
        for file in os.listdir(carto_dir):
            self.availableCartos.append(getCartoInfo(carto_dir+'/'+file))
    
    def loadNeededCartos(self,allPoints):
        maxX,minX= max(allPoints, key=lambda x: x[0])[0],min(allPoints, key=lambda x: x[0])[0]
        maxY,minY= max(allPoints, key=lambda x: x[1])[1],min(allPoints, key=lambda x: x[1])[1]
        
        for c in self.availableCartos:
            # if one of the summits of the bounding square is in the carto, load it (might not be usefull, but not really slowing down, the point is to not laod all cartos at once)
            if isInCarto(maxX,maxY,c['x_range'],c['y_range']) or isInCarto(minX,maxY,c['x_range'],c['y_range']) or isInCarto(maxX,minY,c['x_range'],c['y_range']) or isInCarto(minX,minY,c['x_range'],c['y_range']):
                if not any(item[0] == c['fileName'] for item in self.loadedCartos ):
                    self.loadedCartos.append((c['fileName'],c,loadCarto(c['fileName'])))
            else : 
                if any(item[0] == c['fileName'] for item in self.loadedCartos ):
                    removeIndex = [c[0] for c in self.loadedCartos].index(c['fileName'])
                    del self.loadedCartos[removeIndex]
                    
    def queryAlti(self,points):
        altis = []
        for point in points:
            for (_,info,data) in self.loadedCartos:
                if isInCarto(point[0],point[1],info['x_range'],info['y_range']):
                    new_point=fitToCarto(point,info)
                    alti = data[new_point[1],new_point[0]]
                    
                    if alti == info['NODATA_value']:
                        alti=None
                    altis.append(alti)
        return altis

def fitToCarto(point,info):
    new_x=round((point[0]-info["x_range"][0])/info["cellsize"])
    new_y=round(info["nrows"]-(point[1]-info["y_range"][0])/info["cellsize"])-1
    
    return (new_x,new_y)

def isInCarto(x,y,x_range,y_range):
    return x>=x_range[0] and x<=x_range[1] and y>=y_range[0] and y<=y_range[1]
        
