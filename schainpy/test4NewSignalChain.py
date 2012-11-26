"""
$Author$
$Id$

"""
import datetime
from controller import *
from model import *


class Test():
    def __init__(self):
        self.createObjects()
        self.run()
        
    def createObjects(self):
        
        
        
        self.upConfig = controller.UPConf(id=1, name="voltageproc", type="voltage")
        
        opConf = self.upConfig.addOperation(name="init", priority=0)
        
        opConf1 = self.upConfig.addOperation(name="CohInt", priority=1, type="other")
        
        opConf1.addParameter(name="nCohInt", value=10)
        
        
        opConf = self.upConfig.addOperation(name="selectChannels", priority=2)
        
        opConf.addParameter(name="channelList", value=[0,1])
        
        
        #########################################
        self.objR = jrodataIO.VoltageReader()
        self.objP = jroprocessing.VoltageProc()
        
        self.objInt = jroprocessing.CohInt()
        
        self.objP.addOperation(self.objInt, opConf1.id)
        
        self.connect(self.objR, self.objP)
        
    def connect(self, obj1, obj2):
        obj2.dataIn = obj1.dataOut
        
    def run(self):
        
        while(True):
            self.objR.run(path="/Users/dsuarez/Remote/Meteors",
                    startDate=datetime.date(2012,1,1), 
                    endDate=datetime.date(2012,12,30), 
                    startTime=datetime.time(0,0,0), 
                    endTime=datetime.time(23,59,59), 
                    set=0, 
                    expLabel = "", 
                    ext = None, 
                    online = False)
            
            for opConf in self.upConfig.getOperationObjList():
                kwargs={}
                for parm in opConf.getParameterObjList():
                    kwargs[parm.name]=parm.value
                    
                self.objP.call(opConf,**kwargs)
            
            if self.objR.flagNoMoreFiles:
                break
            
            if self.objR.flagIsNewBlock:
                print 'Block No %04d, Time: %s' %(self.objR.nTotalBlocks, 
                                                  datetime.datetime.fromtimestamp(self.objR.basicHeaderObj.utc + self.objR.basicHeaderObj.miliSecond/1000.0),)

            
    

if __name__ == "__main__":
    Test()