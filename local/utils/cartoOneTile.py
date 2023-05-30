import numpy as np
import os
from carto import loadCarto,getCartoInfo

class cartoQuerierOneTile:
    
    def __init__(self,carto_dir,tile) -> None:
        self.centerTileInfo = getCartoInfo(tile)
        centerTile = loadCarto(self.centerTileInfo['fileName'])
        self.currentBigCarto = np.zeros_like(np.repeat(np.repeat(centerTile, 3, axis=0), 3, axis=1))

        #find the neigbor tiles and add them to the bigCarto
        for file in os.listdir(carto_dir):
            x_coord=-1
            y_coord=-1
            currentInfo = getCartoInfo(carto_dir+'/'+file)
            
            #checking if we are in the 3x3 neighborhood of the middle tile, and adding the carto to the big tile if so.
            
            if currentInfo['x_range'][1]+self.centerTileInfo['cellsize']==self.centerTileInfo['x_range'][0]:
                x_coord=0
            elif currentInfo['x_range'][0]==self.centerTileInfo['x_range'][0]:
                x_coord=1
            elif currentInfo['x_range'][0]==self.centerTileInfo['x_range'][1]+self.centerTileInfo['cellsize']:
                x_coord=2
            
            if currentInfo['y_range'][1]+self.centerTileInfo['cellsize']==self.centerTileInfo['y_range'][0]:
                y_coord=2
            elif currentInfo['y_range'][0]==self.centerTileInfo['y_range'][0]:
                y_coord=1
            elif currentInfo['y_range'][0]==self.centerTileInfo['y_range'][1]+self.centerTileInfo['cellsize']:
                y_coord=0
            
            if x_coord in [0,1,2] and y_coord in [0,1,2]:
                y_min=y_coord*self.centerTileInfo['nrows']
                y_max=(y_coord+1)*self.centerTileInfo['nrows']
                x_min=x_coord*self.centerTileInfo['ncols']
                x_max=(x_coord+1)*self.centerTileInfo['ncols']
                self.currentBigCarto[y_min:y_max,x_min:x_max]=loadCarto(carto_dir+'/'+file)
    
    
    def queryAltis(self, points):
        pointsCoordinates = self.fitToBigCarto(points)
        pointsCoordinates = pointsCoordinates.astype(int)
        return np.mean(self.currentBigCarto[pointsCoordinates[:, 0], pointsCoordinates[:, 1]])

    def fitToBigCarto(self, points):
        new_x = np.round((points[:, 0] - self.centerTileInfo["x_range"][0]) / self.centerTileInfo["cellsize"]) + self.centerTileInfo['ncols']
        new_y = np.round(self.centerTileInfo["nrows"] - (points[:, 1] - self.centerTileInfo["y_range"][0]) / self.centerTileInfo["cellsize"]) - 1 + self.centerTileInfo['nrows']
        return np.column_stack((new_y, new_x))
               

    def queryOnePoint(self,point):
        new_x=round((point[0]-self.centerTileInfo["x_range"][0])/self.centerTileInfo["cellsize"])+self.centerTileInfo['ncols']
        new_y=round(self.centerTileInfo["nrows"]-(point[1]-self.centerTileInfo["y_range"][0])/self.centerTileInfo["cellsize"])-1+self.centerTileInfo['nrows']
        return self.currentBigCarto[new_y,new_x]



        
