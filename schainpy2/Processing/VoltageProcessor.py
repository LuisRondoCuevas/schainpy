'''

$Author$
$Id$
'''

import os 
import sys
import numpy

path = os.path.split(os.getcwd())[0]
sys.path.append(path)

from Data.Voltage import Voltage
from IO.VoltageIO import VoltageWriter
from Graphics.schainPlotTypes import ScopeFigure

class VoltageProcessor:
    dataInObj = None
    dataOutObj = None
    integratorObjIndex = None
    writerObjIndex = None
    integratorObjList = None
    writerObjList = None

    def __init__(self):
        self.integratorObjIndex = None
        self.writerObjIndex = None
        self.plotObjIndex = None
        self.integratorObjList = []
        self.writerObjList = []
        self.plotObjList = []

    def setup(self,dataInObj=None,dataOutObj=None):
        self.dataInObj = dataInObj

        if self.dataOutObj == None:
            dataOutObj = Voltage()

        self.dataOutObj = dataOutObj

        return self.dataOutObj

    def init(self):
        self.integratorObjIndex = 0
        self.writerObjIndex = 0
        self.plotObjIndex = 0
        
        if not(self.dataInObj.flagNoData):
            self.dataOutObj.copy(self.dataInObj)
        # No necesita copiar en cada init() los atributos de dataInObj
        # la copia deberia hacerse por cada nuevo bloque de datos
    
    def addScope(self, idfigure, nframes, wintitle, driver):
        if idfigure==None:
            idfigure = self.plotObjIndex
            
        scopeObj = ScopeFigure(idfigure, nframes, wintitle, driver)
        self.plotObjList.append(scopeObj)
    
    def plotScope(self,
                    idfigure=None,
                    minvalue=None,
                    maxvalue=None,
                    xmin=None,
                    xmax=None,
                    wintitle='',
                    driver='plplot',
                    save=False,
                    gpath=None,
                    titleList=None,
                    xlabelList=None,
                    ylabelList=None,
                    type="power"):
        
        if self.dataOutObj.flagNoData:
            return 0
        
        nframes = len(self.dataOutObj.channelList)
        
        if len(self.plotObjList) <= self.plotObjIndex:
            self.addScope(idfigure, nframes, wintitle, driver)
        
        self.plotObjList[self.plotObjIndex].plot1DArray(data1D=self.dataOutObj.data, 
                                             x=self.dataOutObj.heightList, 
                                             channelList=self.dataOutObj.channelList, 
                                             xmin=xmin, 
                                             xmax=xmax, 
                                             minvalue=minvalue, 
                                             maxvlaue=maxvalue, 
                                             save=save, 
                                             gpath=gpath)
        
        self.plotObjIndex += 1
    

    def addIntegrator(self,N,timeInterval):
        objCohInt = CoherentIntegrator(N,timeInterval)
        self.integratorObjList.append(objCohInt)

    def addWriter(self, wrpath, blocksPerFile, profilesPerBlock):
        writerObj = VoltageWriter(self.dataOutObj)
        writerObj.setup(wrpath,blocksPerFile,profilesPerBlock)
        self.writerObjList.append(writerObj)
        
    def writeData(self, wrpath, blocksPerFile, profilesPerBlock):
        
        if self.dataOutObj.flagNoData:
            return 0
            
        if len(self.writerObjList) <= self.writerObjIndex:
            self.addWriter(wrpath, blocksPerFile, profilesPerBlock)
        
        self.writerObjList[self.writerObjIndex].putData()
        
        self.writerObjIndex += 1
        
    def integrator(self, N=None, timeInterval=None):
        if self.dataOutObj.flagNoData:
            return 0
        if len(self.integratorObjList) <= self.integratorObjIndex:
            self.addIntegrator(N,timeInterval)

        myCohIntObj = self.integratorObjList[self.integratorObjIndex]
        myCohIntObj.exe(data=self.dataOutObj.data,timeOfData=None)
        


class CoherentIntegrator:
    
    integ_counter = None
    data = None
    navg = None
    buffer = None
    nCohInt = None
    
    def __init__(self, N=None,timeInterval=None):
        
        self.data = None
        self.navg = None
        self.buffer = None
        self.timeOut = None
        self.exitCondition = False
        self.isReady = False
        self.nCohInt = N
        self.integ_counter = 0
        if timeInterval!=None:
            self.timeIntervalInSeconds = timeInterval * 60. #if (type(timeInterval)!=integer) -> change this line
        
        if ((timeInterval==None) and (N==None)):
            raise ValueError, "N = None ; timeInterval = None"
        
        if timeInterval == None:
            self.timeFlag = False
        else:
            self.timeFlag = True
        
    def exe(self, data, timeOfData):
        
        if self.timeFlag:
            if self.timeOut == None:
                self.timeOut = timeOfData + self.timeIntervalInSeconds
            
            if timeOfData < self.timeOut:
                if self.buffer == None:
                    self.buffer = data
                else:
                    self.buffer = self.buffer + data
                self.integ_counter += 1
            else:
                self.exitCondition = True
                
        else:
            if self.integ_counter < self.nCohInt:
                if self.buffer == None:
                    self.buffer = data
                else:
                    self.buffer = self.buffer + data
            
                self.integ_counter += 1

            if self.integ_counter == self.nCohInt:
                self.exitCondition = True
                
        if self.exitCondition:
            self.data = self.buffer
            self.navg = self.integ_counter
            self.isReady = True
            self.buffer = None
            self.timeOut = None
            self.integ_counter = 0
            self.exitCondition = False
            
            if self.timeFlag:
                self.buffer = data
                self.timeOut = timeOfData + self.timeIntervalInSeconds
        else:
            self.isReady = False

    
