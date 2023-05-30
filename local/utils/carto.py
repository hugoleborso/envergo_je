import numpy as np
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
    info = getCartoInfo(fileName)
    carto = np.loadtxt(fileName, skiprows=6)
    carto[carto==info["NODATA_value"]]=np.nan
    return carto

def saveListToCarto(data_list,fileName,info):
    # Extract coordinates and altitudes separately
    coordinates = [element[0] for element in data_list]
    altitudes = [element[1] for element in data_list]

    # Convert coordinates and altitudes to numpy arrays
    coordinates_array = np.array(coordinates)
    altitudes_array = np.array(altitudes)

    # Create the 2D numpy array with coordinates as indices and altitudes as values
    x_coords, y_coords = coordinates_array.T
    num_x = len(np.unique(x_coords))
    num_y = len(np.unique(y_coords))
    result_array = np.zeros((num_y,num_x ))
    x_indices = np.searchsorted(np.unique(x_coords), x_coords)
    y_indices = num_y - 1 - np.searchsorted(np.unique(y_coords), y_coords) 
    result_array[y_indices, x_indices] = altitudes_array  

    saveArrayToCarto(np.reshape(result_array, (info["ncols"],info["nrows"])),fileName,info)

def saveArrayToCarto(array,fileName,info):
    header = "ncols     %s\n" % info["ncols"]
    header += "nrows    %s\n" % info["nrows"]
    header += "xllcorner %s\n" % info["xllcorner"]
    header += "yllcorner %s\n" % info["yllcorner"]
    header += "cellsize %s\n" % info["cellsize"]
    header += "NODATA_value %s\n" % info["NODATA_value"]
    array[np.isnan(array) | (array == None)]=float(info["NODATA_value"])
    
    np.savetxt(fileName, array, header=header, fmt="%1.2f")

def createQuadrants(cartoPrecision, innerRadius, radii, quadrantsNb, debugPrints=False):
    quarterPointsNb = int(np.ceil(radii[-1] / cartoPrecision))
    quadrantsBins = np.linspace(0, 2 * np.pi, quadrantsNb + 1)
    quadrants = [[[] for _ in range(len(radii))] for _ in range(quadrantsNb)]
    innerAltiPoints = []
    allPoints = []

    points = np.mgrid[-quarterPointsNb:quarterPointsNb + 1, -quarterPointsNb:quarterPointsNb + 1]
    displacements = cartoPrecision * points
    # new_points = origin + displacements[0] + 1j * displacements[1]
    new_points = displacements[0] + 1j * displacements[1]
    
    # find the corresponding 'donut' for each point
    distances = np.abs(new_points)
    radiusNbs = np.searchsorted(np.concatenate(([innerRadius], radii, [np.inf])), distances)
    
    # find the quadrant for each point
    angles = np.angle(new_points) % (2 * np.pi)
    quadNbs = np.digitize(angles, quadrantsBins) - 1
    
    # process the points based on their quadrant and radius using the masks
    for quadNb in range(quadrantsNb):
        for radiusNb in range(len(radii)):
            mask = np.logical_and(quadNbs == quadNb, radiusNbs == radiusNb + 1)
            quad_points = new_points[mask]
            quadrants[quadNb][radiusNb].extend(zip(np.round(quad_points.real).astype(int), np.round(quad_points.imag).astype(int)))
            # Convert the extended points to a NumPy array
            quadrants[quadNb][radiusNb] = np.array(quadrants[quadNb][radiusNb], dtype=np.int32)
            allPoints.extend(zip(np.round(quad_points.real).astype(int), np.round(quad_points.imag).astype(int)))
    
    allPoints=np.array(allPoints)
    inner_points = np.array(new_points[radiusNbs == 0])
    innerAltiPoints.extend(zip(np.round(inner_points.real).astype(int), np.round(inner_points.imag).astype(int)))
    
    
    #idea : send points without origin, add origin afterwards
    return innerAltiPoints, quadrants, allPoints

def updateOrigin(origin,points):
    return np.add(points, origin)

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

                    
    def queryAlti(self,points):
        altis = []
        for point in points:
            for (_,info,data) in self.loadedCartos:
                if isInCarto(point[0],point[1],info['x_range'],info['y_range']):
                    new_point=fitToCarto(point,info)
                    altis.append(data[new_point[1],new_point[0]])

        return np.mean(altis)

def fitToCarto(point,info):
    new_x=round((point[0]-info["x_range"][0])/info["cellsize"])
    new_y=round(info["nrows"]-(point[1]-info["y_range"][0])/info["cellsize"])-1
    
    return (new_x,new_y)

def isInCarto(x,y,x_range,y_range):
    return x>=x_range[0] and x<=x_range[1] and y>=y_range[0] and y<=y_range[1]
        
