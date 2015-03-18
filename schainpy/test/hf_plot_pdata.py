import os, sys
#import timeit
import datetime

path = os.path.split(os.getcwd())[0]
sys.path.append(path)

from controller import *

desc = "HF_EXAMPLE"
filename = "hf_test.xml"

controllerObj = Project()

controllerObj.setup(id = '191', name='test01', description=desc)


#path='/media/APOLLO/HF_rawdata/d2015026/0/cspec'
#path='/media/APOLLO/HF_rawdata/cspec'
#path='/media/APOLLO/bistatico'
#path='/home/alex/Downloads/pdata_hf/sousy'
path='/home/alex/Downloads/pdata_hf'
#path='/media/APOLLO/bistatico'



#path="/media/APOLLO/HF_rawdata/d2015059/sp01_f0" #f0=2.72e6
#path="/media/APOLLO/HF_rawdata/d2015059/sp01_f1" #f0=3.64e6
#path='/media/APOLLO/HF_rawdata/test'
#figpath='/home/alex/Pictures/hf2_16/last_data'
figpath='/home/alex/Pictures/pdata_plot'
pathFigure='/home/alex/Pictures/hf2_16/last_data'
#path='/home/alex/Downloads/ICA_LAST_TEST'

readUnitConfObj = controllerObj.addReadUnit(datatype='SpectraReader',
                                            path=path,
                                            startDate='2015/01/12',
                                            endDate='2015/05/13',
                                            startTime='00:00:00',
                                            endTime='23:59:59',
                                            online=0,
                                            #set=1426485881,
                                            delay=10,
                                            walk=1
                                            #timezone=-5*3600
                                            )

procUnitConfObj1 = controllerObj.addProcUnit(datatype='SpectraProc', inputId=readUnitConfObj.getId())

opObj11 = procUnitConfObj1.addOperation(name='SpectraPlot', optype='other')
opObj11.addParameter(name='id', value='1000', format='int')
opObj11.addParameter(name='wintitle', value='HF_Jicamarca_Spc', format='str')
#opObj11.addParameter(name='channelList', value='0', format='intlist') 
opObj11.addParameter(name='zmin', value='-120', format='float')
opObj11.addParameter(name='zmax', value='-70', format='float')
opObj11.addParameter(name='save', value='1', format='int')
opObj11.addParameter(name='figpath', value=figpath, format='str')
# opObj11.addParameter(name='figfile', value=figfile_spectra_name, format='str')
# opObj11.addParameter(name='wr_period', value='5', format='int')
#opObj11.addParameter(name='ftp_wei', value='0', format='int')
#opObj11.addParameter(name='exp_code', value='20', format='int')
#opObj11.addParameter(name='sub_exp_code', value='0', format='int')
#opObj11.addParameter(name='plot_pos', value='0', format='int')



# # figfile_power_name="jro_power_image"+freq2+date+ext_img
# # print figfile_power_name
opObj11 = procUnitConfObj1.addOperation(name='RTIPlot', optype='other')
opObj11.addParameter(name='id', value='2000', format='int')
opObj11.addParameter(name='wintitle', value='HF_Jicamarca', format='str')
opObj11.addParameter(name='showprofile', value='0', format='int')
#opObj11.addParameter(name='channelList', value='0', format='intlist') 
opObj11.addParameter(name='xmin', value='0', format='float')
opObj11.addParameter(name='xmax', value='24', format='float')
opObj11.addParameter(name='zmin', value='-110', format='float')
opObj11.addParameter(name='zmax', value='-50', format='float')
opObj11.addParameter(name='save', value='1', format='int')
opObj11.addParameter(name='figpath', value=figpath, format='str')
#opObj11.addParameter(name='figfile', value=figfile_power_name, format='str')
#opObj11.addParameter(name='wr_period', value='5', format='int')

#   
# opObj11 = procUnitConfObj1.addOperation(name='PowerProfile', optype='other')
# opObj11.addParameter(name='id', value='2004', format='int')
# opObj11.addParameter(name='wintitle', value='HF_Jicamarca', format='str')
# #opObj11.addParameter(name='channelList', value='0', format='intlist') 
# opObj11.addParameter(name='save', value='1', format='bool')
# opObj11.addParameter(name='figpath', value=figpath, format='str')
# #opObj11.addParameter(name='xmin', value='10', format='int')
# #opObj11.addParameter(name='xmax', value='40', format='int')
#   
# # figfile_phase_name="jro_phase_image"+freq1+date+ext_img
# # print figfile_phase_name
opObj11 = procUnitConfObj1.addOperation(name='CoherenceMap', optype='other')
opObj11.addParameter(name='id', value='3000', format='int')
opObj11.addParameter(name='wintitle', value='HF_Jicamarca', format='str')
opObj11.addParameter(name='showprofile', value='1', format='int')
opObj11.addParameter(name='xmin', value='0', format='float')
opObj11.addParameter(name='xmax', value='24', format='float')
#opObj11.addParameter(name='channelList', value='0', format='intlist') 
opObj11.addParameter(name='save', value='1', format='bool')
opObj11.addParameter(name='figpath', value=figpath, format='str')
 # opObj11.addParameter(name='figfile', value=figfile_phase_name, format='str')
 # opObj11.addParameter(name='wr_period', value='5', format='int')
   
# opObj11 = procUnitConfObj1.addOperation(name='CrossSpectraPlot', optype='other')
# opObj11.addParameter(name='id', value='6005', format='int')
# opObj11.addParameter(name='wintitle', value='HF_Jicamarca', format='str')
# opObj11.addParameter(name='zmin', value='-110', format='float')
# opObj11.addParameter(name='zmax', value='-50', format='float')
# #opObj11.addParameter(name='xmin', value='0', format='float')
# #opObj11.addParameter(name='xmax', value='24', format='float')
# #opObj11.addParameter(name='channelList', value='0,1,2,3', format='intlist') 
# opObj11.addParameter(name='save', value='1', format='bool')
# opObj11.addParameter(name='figpath', value=figpath, format='str')
#   
#   
#   
# xmin = 0
# xmax = 24
#  
procUnitConfObj2 = controllerObj.addProcUnit(datatype='ParametersProc', inputId=procUnitConfObj1.getId())
opObj20 = procUnitConfObj2.addOperation(name='GetMoments')
    
# opObj21 = procUnitConfObj2.addOperation(name='MomentsPlot', optype='other')
# opObj21.addParameter(name='id', value='3', format='int')
# opObj21.addParameter(name='wintitle', value='Moments Plot', format='str')
# opObj21.addParameter(name='save', value='1', format='bool')
# opObj21.addParameter(name='figpath', value=pathFigure, format='str')
# opObj21.addParameter(name='zmin', value='5', format='int')
# opObj21.addParameter(name='zmax', value='90', format='int')
#    
opObj21 = procUnitConfObj2.addOperation(name='ParametersPlot', optype='other')
opObj21.addParameter(name='id', value='4000', format='int')
opObj21.addParameter(name='wintitle', value='Radial Velocity Plot0', format='str')
opObj21.addParameter(name='channelList', value='0', format='intlist') 
opObj21.addParameter(name='save', value='1', format='bool')
opObj21.addParameter(name='figpath', value=figpath, format='str')
opObj21.addParameter(name='SNR', value='1', format='bool')
opObj21.addParameter(name='SNRmin', value='-10', format='int')
opObj21.addParameter(name='SNRmax', value='50', format='int')
opObj21.addParameter(name='SNRthresh', value='0', format='float')
opObj21.addParameter(name='xmin', value=0, format='float')
opObj21.addParameter(name='xmax', value=24, format='float')
#opObj21.addParameter(name='parameterIndex', value=, format='int')
    
#   
opObj21 = procUnitConfObj2.addOperation(name='ParametersPlot', optype='other')
opObj21.addParameter(name='id', value='5000', format='int')
opObj21.addParameter(name='wintitle', value='Radial Velocity Plot1', format='str')
opObj21.addParameter(name='channelList', value='1', format='intlist') 
opObj21.addParameter(name='save', value='1', format='bool')
opObj21.addParameter(name='figpath', value=figpath, format='str')
opObj21.addParameter(name='SNR', value='1', format='bool')
opObj21.addParameter(name='SNRmin', value='-20', format='int')
opObj21.addParameter(name='SNRmax', value='50', format='int')
opObj21.addParameter(name='SNRthresh', value='0', format='float')
opObj21.addParameter(name='xmin', value=0, format='float')
opObj21.addParameter(name='xmax', value=24, format='float')
   
#   
#   
# opObj23 = procUnitConfObj2.addOperation(name='EWDriftsPlot', optype='other')
# opObj23.addParameter(name='id', value='4', format='int')
# opObj23.addParameter(name='wintitle', value='EW Drifts', format='str')
# opObj23.addParameter(name='save', value='1', format='bool')
# opObj23.addParameter(name='figpath', value = pathFigure, format='str')
# opObj23.addParameter(name='zminZonal', value='-150', format='int')
# opObj23.addParameter(name='zmaxZonal', value='150', format='int')
# opObj23.addParameter(name='zminVertical', value='-30', format='float')
# opObj23.addParameter(name='zmaxVertical', value='30', format='float')
# opObj23.addParameter(name='SNR_1', value='1', format='bool')
# opObj23.addParameter(name='SNRmax', value='5', format='int')
# # opObj23.addParameter(name='SNRthresh', value='-50', format='float')
# opObj23.addParameter(name='xmin', value=xmin, format='float')
# opObj23.addParameter(name='xmax', value=xmax, format='float')
#   
#   
# # opObj11 = procUnitConf.Obj1.addOperation(name='SendByFTP', optype='other')
# # opObj11.addParameter(name='ext', value='*.jpeg', format='str')
# # opObj11.addParameter(name='localfolder', value='/home/alex/Pictures/ftp', format='str')
# # opObj11.addParameter(name='remotefolder', value='/home/wmaster/web2/data/JRO/HFT/2015/03/11/figures/', format='str')
# # opObj11.addParameter(name='server', value='181.177.232.125', format='str')
# # opObj11.addParameter(name='username', value='wmaster', format='str')
# # opObj11.addParameter(name='password', value='mst2010vhf', format='str')
print "Escribiendo el archivo XML"
controllerObj.writeXml(filename)
print "Leyendo el archivo XML"
controllerObj.readXml(filename)

controllerObj.createObjects()
controllerObj.connectObjects()

#timeit.timeit('controllerObj.run()', number=2)

controllerObj.run()