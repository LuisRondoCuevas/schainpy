import os, sys
import time
import datetime

path = os.path.dirname(os.getcwd())
path = os.path.dirname(path)
sys.path.insert(0, path)

from schainpy.controller import Project

desc = "AMISR Experiment"

filename = "amisr_reader.xml"

controllerObj = Project()

controllerObj.setup(id = '191', name='esf_proc', description=desc)


path = os.path.join(os.environ['HOME'],'amisr')
# path = '/media/signalchain/HD-PXU2/AMISR_JULIA_MODE'
# path = '/media/soporte/E9F4-F053/AMISR/Data/NoiseTest/EEJ'
# path = '/media/soporte/E9F4-F053/AMISR/Data/ESF'
path = '/mnt/data_amisr'

#path = '/media/soporte/AMISR_104'
#figpath = os.path.join(os.environ['HOME'],'Pictures/amisr/test/proc/esf')
#figpath = '/media/soporte/E9F4-F053/AMISR/Data/JULIA/ESF'
figpath = '/home/soporte/Data/ESF'
remotefolder = "/home/wmaster/graficos" 

xmin = '18'
xmax = '31'
dbmin = '60' #'60'#'55' #'40' #noise  esf  eej
dbmax = '75' #'70' #'55'
show = '1'

code = '1,-1,-1,-1,1,1,1,1,-1,-1,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1,-1,1,-1,1,1,-1,1'
nCode = '1'
nBaud = '28'
nosamp = '2' # oversample

str = datetime.date.today()
str1 = str + datetime.timedelta(days=1)
today = str.strftime("%Y/%m/%d")
tomorrow = str1.strftime("%Y/%m/%d")

readUnitConfObj = controllerObj.addReadUnit(datatype='AMISRReader',
                                            path=path,
                                            startDate=today, #'2014/10/07',
                                            endDate=tomorrow, #'2014/10/07',
                                            startTime='18:01:30',#'07:00:00',
                                            endTime='07:00:00',#'15:00:00',
                                            walk=0,
                                            code = code,
                                            nCode = nCode,
                                            nBaud = nBaud,
                                            timezone='lt',
                                            online=1)

#AMISR Processing Unit

#Voltage Processing Unit
procUnitConfObjBeam0 = controllerObj.addProcUnit(datatype='VoltageProc', inputId=readUnitConfObj.getId())
opObj10 = procUnitConfObjBeam0.addOperation(name='setRadarFrequency')
opObj10.addParameter(name='frequency', value='445e6', format='float') #changed on Dec 3, 15:40h
#opObj10.addParameter(name='frequency', value='435e6', format='float')

# opObj12 = procUnitConfObjBeam0.addOperation(name='selectHeights')
# opObj12.addParameter(name='minHei', value='0', format='float')

# code = '1,1,-1,1,1,-1,1,-1,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1,-1,-1,1,1,1,1,-1,-1,-1'
# code = '1,1,0,1,1,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,0,0,0'
#Noise--> no code

opObj11 = procUnitConfObjBeam0.addOperation(name='Decoder', optype='other')
opObj11.addParameter(name='code', value=code, format='floatlist')
opObj11.addParameter(name='nCode', value=nCode, format='int')
opObj11.addParameter(name='nBaud', value=nBaud, format='int')
opObj11.addParameter(name='osamp', value=nosamp, format='int')


# opObj12 = procUnitConfObjBeam0.addOperation(name='selectHeights')
# opObj12.addParameter(name='minHei', value='50', format='float')
# opObj12.addParameter(name='maxHei', value='150', format='float')
#Coherent Integration
# opObj11 = procUnitConfObjBeam0.addOperation(name='CohInt', optype='other')
# opObj11.addParameter(name='n', value='2', format='int')

# opObj11 = procUnitConfObjBeam0.addOperation(name='Scope', optype='other')
# opObj11.addParameter(name='id', value='121', format='int')

#Spectra Unit Processing, getting spectras with nProfiles and nFFTPoints
procUnitConfObjSpectraBeam0 = controllerObj.addProcUnit(datatype='SpectraProc', inputId=procUnitConfObjBeam0.getId())
procUnitConfObjSpectraBeam0.addParameter(name='nFFTPoints', value=32, format='int')
# 
opObj11 =  procUnitConfObjSpectraBeam0.addOperation(name='IncohInt', optype='other')
opObj11.addParameter(name='n', value='60', format='int')
#opObj11.addParameter(name='timeInterval', value='30', format='float')

   
# # #RemoveDc
# # opObj11 = procUnitConfObjSpectraBeam0.addOperation(name='removeDC')

#Noise Estimation    
opObj11 = procUnitConfObjSpectraBeam0.addOperation(name='getNoise')
opObj11.addParameter(name='minHei', value='100', format='float')
opObj11.addParameter(name='maxHei', value='280', format='float')
#opObj11.addParameter(name='minHei', value='15', format='float')
#opObj11.addParameter(name='maxHei', value='20', format='float')

#SpectraPlot    
opObj11 = procUnitConfObjSpectraBeam0.addOperation(name='SpectraPlot', optype='other')
opObj11.addParameter(name='id', value='1', format='int')
opObj11.addParameter(name='wintitle', value='ESF AMISR', format='str')
#opObj11.addParameter(name='zmin', value='38', format='int')
opObj11.addParameter(name='zmin', value=dbmin, format='int')
opObj11.addParameter(name='zmax', value=dbmax, format='int')
opObj11.addParameter(name='save', value='0', format='bool')
opObj11.addParameter(name='figpath', value = figpath, format='str')
opObj11.addParameter(name='ftp', value='1', format='int')
opObj11.addParameter(name='wr_period', value='2', format='int')
opObj11.addParameter(name='exp_code', value='21', format='int')
opObj11.addParameter(name='sub_exp_code', value='4', format='int')
opObj11.addParameter(name='ftp_wei', value='0', format='int')
opObj11.addParameter(name='plot_pos', value='0', format='int')

 

# #RTIPlot
# #title0 = 'RTI AMISR Beam 0'
opObj11 = procUnitConfObjSpectraBeam0.addOperation(name='RTIPlot', optype='other')
opObj11.addParameter(name='id', value='2', format='int')
opObj11.addParameter(name='wintitle', value='ESF AMISR', format='str')
opObj11.addParameter(name='showprofile', value='0', format='int')
opObj11.addParameter(name='xmin', value=xmin, format='float')
opObj11.addParameter(name='xmax', value=xmax, format='float')
opObj11.addParameter(name='zmin', value=dbmin, format='int')
opObj11.addParameter(name='zmax', value=dbmax, format='int')
opObj11.addParameter(name='save', value='1', format='bool')
opObj11.addParameter(name='figpath', value = figpath, format='str')
opObj11.addParameter(name='show', value = show, format='bool')
opObj11.addParameter(name='ftp', value='1', format='int')
opObj11.addParameter(name='wr_period', value='2', format='int')
opObj11.addParameter(name='exp_code', value='21', format='int')
opObj11.addParameter(name='sub_exp_code', value='4', format='int')
opObj11.addParameter(name='ftp_wei', value='0', format='int')
opObj11.addParameter(name='plot_pos', value='0', format='int')


# #send to server
procUnitConfObj2 = controllerObj.addProcUnit(name='SendToServer')
#procUnitConfObj2.addParameter(name='server', value='jro-app.igp.gob.pe', format='str')
procUnitConfObj2.addParameter(name='server', value='10.10.120.125', format='str')
procUnitConfObj2.addParameter(name='username', value='wmaster', format='str')
procUnitConfObj2.addParameter(name='password', value='mst2010vhf', format='str')
procUnitConfObj2.addParameter(name='localfolder', value=figpath, format='str')
procUnitConfObj2.addParameter(name='remotefolder', value=remotefolder, format='str')
procUnitConfObj2.addParameter(name='ext', value='.png', format='str')
procUnitConfObj2.addParameter(name='period', value='300', format='int')
procUnitConfObj2.addParameter(name='protocol', value='ssh', format='str')

# # # 
# #Noise
#title0 = 'RTI AMISR Beam 0'
# opObj11 = procUnitConfObjSpectraBeam0.addOperation(name='Noise', optype='other')
# opObj11.addParameter(name='id', value='3', format='int')
# opObj11.addParameter(name='wintitle', value='ESF AMISR', format='str')
# opObj11.addParameter(name='showprofile', value='0', format='int')
# opObj11.addParameter(name='xmin', value=xmin, format='float')
# opObj11.addParameter(name='xmax', value=xmax, format='float')
# opObj11.addParameter(name='ymin', value=dbmin, format='int')
# opObj11.addParameter(name='ymax', value=dbmax, format='int')
# opObj11.addParameter(name='save', value='1', format='bool')
# opObj11.addParameter(name='figpath', value = figpath, format='str')
# opObj11.addParameter(name='show', value = show, format='bool')


#Generate *.pdata from AMISR data
# opObj11 = procUnitConfObjSpectraBeam0.addOperation(name='SpectraWriter', optype='other')
# opObj11.addParameter(name='path', value=figpath)
# opObj11.addParameter(name='blocksPerFile', value='10', format='int')
# opObj11.addParameter(name='datatype', value="4", format="int") #size of data to be saved
# 
# #generate moments 
# procUnitConfObj2 = controllerObj.addProcUnit(datatype='ParametersProc', inputId=procUnitConfObjSpectraBeam0.getId())
# opObj20 = procUnitConfObj2.addOperation(name='GetMoments')
# 
# opObj12 = procUnitConfObj2.addOperation(name='HDF5Writer', optype='other')
# opObj12.addParameter(name='path', value=figpath+'/plots')
# opObj12.addParameter(name='blocksPerFile', value='10', format='int')
# opObj12.addParameter(name='metadataList',value='type,inputUnit,heightList',format='list')
# opObj12.addParameter(name='dataList',value='data_param,data_SNR,utctime',format='list')
# opObj12.addParameter(name='mode',value='1',format='int')


# procUnitConfObj2 = controllerObj.addProcUnit(name='SendToServer')
# procUnitConfObj2.addParameter(name='server', value='jro-app.igp.gob.pe', format='str')
# procUnitConfObj2.addParameter(name='username', value='wmaster', format='str')
# procUnitConfObj2.addParameter(name='password', value='mst2010vhf', format='str')
# procUnitConfObj2.addParameter(name='localfolder', value=pathFigure, format='str')
# procUnitConfObj2.addParameter(name='remotefolder', value=remotefolder, format='str')
# procUnitConfObj2.addParameter(name='ext', value='.png', format='str')
# procUnitConfObj2.addParameter(name='period', value=5, format='int')
# procUnitConfObj2.addParameter(name='protocol', value='ftp', format='str')
#-----------------------------------------------------------------------------------------------


print "Escribiendo el archivo XML"
controllerObj.writeXml(filename)
print "Leyendo el archivo XML"
controllerObj.readXml(filename)

controllerObj.createObjects()
controllerObj.connectObjects()
controllerObj.run()

#21 3 pm


