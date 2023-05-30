from tests import testCartoCreator,compareCartosV2

PARAMS = [
    [5,[50,75,100,130,160],12],
    [5,[50,75,100,130,160],16],
    [20,[50,75,100,130,160],8],
    [20,[50,70,90,110,130,145,160],8],
    [5,[50,70,90,110,130,145,160],12],
    [5,[50,70,90,110,130,145,160],16],
]
PLACES = [
    ['44',(285000,6705000),'local/alti_data/RGEALTI_FXX_0285_6710_MNT_LAMB93_IGN69.asc','local/alti_data'],
    ['39',(890000,6630000),'local/alti_data_39/RGEALTI_FXX_0890_6625_MNT_LAMB93_IGN69.asc','local/alti_data_39'],
    ['29',(110000,6850000),'local/alti_data_29/RGEALTI_FXX_0110_6845_MNT_LAMB93_IGN69.asc','local/alti_data_29'],
    ['44',(315000,6700000),'local/alti_data/RGEALTI_FXX_0315_6705_MNT_LAMB93_IGN69.asc','local/alti_data'],
    ['39',(875000,6655000),'local/alti_data_39/RGEALTI_FXX_0875_6660_MNT_LAMB93_IGN69.asc','local/alti_data_39'],
    ['29',(215000,6840000),'local/alti_data_29/RGEALTI_FXX_0215_6845_MNT_LAMB93_IGN69.asc','local/alti_data_29'],
]

def getName(dep,params):
    return dep[0]+'_'+str(dep[1][0])+'_'+str(dep[1][1])+'_test_20_'+str(params[0])+'_'+str(params[2])+'_'+'-'.join([str(p) for p in params[1]])

generate=False
if generate:
    for place in PLACES:

        for params in PARAMS:
            print("Doing : ",place,params)
            name = getName(place,params)
            testCartoCreator(
                bottomLeft = place[1],
                currentTile = place[2],
                outputCartoPrecision = 20,
                inputCartoPrecision = params[0],
                width = 250,
                height = 250,
                ouptutFile = 'local/output/test/'+name+'.asc',
                ouptutScreenShot = 'local/output/test/'+name+'.png',
                innerRadius = 25,
                radii = params[1],
                quadrantsNb = params[2],
                slope = 0.05,
                inputFolder = place[3],
                show=False
                )

for place in PLACES:
    for params in PARAMS[1::]:
        print("Evaluating : ",place,params)
        testDir = 'local/output/test/'
        saveDir = 'local/output/decision/'+place[0]+'_'+str(place[1][0])+'_'+str(place[1][1])+'/'+str(params[0])+'v'+str(PARAMS[0][0])+'_'+'-'.join([str(p) for p in params[1]])+'v'+'-'.join([str(p) for p in PARAMS[0][1]])+'_'+str(params[2])+'v'+str(PARAMS[0][2])
        compareCartosV2(testDir+getName(place,PARAMS[0])+'.asc',testDir+getName(place,params)+'.asc',5000,8000,stretch=(1,1),saveDir=saveDir)