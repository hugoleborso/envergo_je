from scipy import stats

def getStats(point,surroundingPoints):
    st = stats.describe([pt['z'] for pt in surroundingPoints])
    return {'mean':st.mean,'max':st.minmax[1],'min':st.minmax[0],'var':st.variance}

def tripleCircleBassinVersant(point,pointAlti,circle1,circle2,circle3):
    surfaceCount=0
    NW = [[pt for pt in circle if pt['lat']>=point.lat and pt['lon']<point.long] for circle in [circle1,circle2,circle3]]
    NE = [[pt for pt in circle if pt['lat']>=point.lat and pt['lon']>=point.long] for circle in [circle1,circle2,circle3]]
    SE = [[pt for pt in circle if pt['lat']<point.lat and pt['lon']<point.long] for circle in [circle1,circle2,circle3]]
    SW = [[pt for pt in circle if pt['lat']<point.lat and pt['lon']>=point.long] for circle in [circle1,circle2,circle3]]
    
    for quadrant in [NW,NE,SE,SW]:
        meanAlti1 = sum([pt['z'] for pt in quadrant[0]])/len(quadrant[0])
        if meanAlti1>1.02*pointAlti:
            surfaceCount+=1
            meanAlti3 = sum([pt['z'] for pt in quadrant[1]])/len(quadrant[1])
            if meanAlti3>1.05*meanAlti1:
                surfaceCount+=8
                meanAlti5 = sum([pt['z'] for pt in quadrant[2]])/len(quadrant[2])
                if meanAlti5>1.05*meanAlti3:
                    surfaceCount+=16
    
    return surfaceCount/100
    