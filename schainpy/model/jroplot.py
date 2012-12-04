import numpy
import time, datetime
from graphics.figure import  * 

class RTIPlot(Figure):
    
    __isConfig = None
    __nsubplots = None
    
    WIDTHPROF = None
    HEIGHTPROF = None
    
    def __init__(self):
        
        self.__timerange = 24*60*60
        self.__isConfig = False
        self.__nsubplots = 1
        
        self.WIDTH = 800
        self.HEIGHT = 300
        self.WIDTHPROF = 120
        self.HEIGHTPROF = 0
        
    def getSubplots(self):
        
        ncol = 1
        nrow = self.nplots
        
        return nrow, ncol
    
    def setup(self, idfigure, nplots, wintitle, showprofile=True):
               
        self.__showprofile = showprofile
        self.nplots = nplots
        
        ncolspan = 1
        colspan = 1
        if showprofile:
            ncolspan = 7
            colspan = 6
            self.__nsubplots = 2
            
        self.createFigure(idfigure = idfigure,
                          wintitle = wintitle,
                          widthplot = self.WIDTH + self.WIDTHPROF,
                          heightplot = self.HEIGHT + self.HEIGHTPROF)
        
        nrow, ncol = self.getSubplots()
        
        counter = 0
        for y in range(nrow):
            for x in range(ncol):
                
                if counter >= self.nplots:
                    break
                
                self.addAxes(nrow, ncol*ncolspan, y, x*ncolspan, colspan, 1)
                
                if showprofile:
                    self.addAxes(nrow, ncol*ncolspan, y, x*ncolspan+colspan, 1, 1)
                    
                counter += 1
    
    def __getTimeLim(self, x, xmin, xmax):
        
        thisdatetime = datetime.datetime.fromtimestamp(numpy.min(x))
        thisdate = datetime.datetime.combine(thisdatetime.date(), datetime.time(0,0,0))
        
        ####################################################
        #If the x is out of xrange
        if xmax < (thisdatetime - thisdate).seconds/(60*60.):
            xmin = None
            xmax = None
        
        if xmin == None:
            td = thisdatetime - thisdate
            xmin = td.seconds/(60*60.)
            
        if xmax == None:
            xmax = xmin + self.__timerange/(60*60.)
        
        mindt = thisdate + datetime.timedelta(0,0,0,0,0, xmin)
        tmin = time.mktime(mindt.timetuple())
        
        maxdt = thisdate + datetime.timedelta(0,0,0,0,0, xmax)
        tmax = time.mktime(maxdt.timetuple())
        
        self.__timerange = tmax - tmin
        
        return tmin, tmax
    
    def run(self, dataOut, idfigure, wintitle="", channelList=None, showprofile='True',
            xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None,
            timerange=None,
            save=False, filename=None):
        
        """
        
        Input:
            dataOut         :
            idfigure        :
            wintitle        :
            channelList     :
            showProfile     :
            xmin            :    None,
            xmax            :    None,
            ymin            :    None,
            ymax            :    None,
            zmin            :    None,
            zmax            :    None
        """
        
        if channelList == None:
            channelIndexList = dataOut.channelIndexList
        else:
            channelIndexList = []
            for channel in channelList:
                if channel not in dataOut.channelList:
                    raise ValueError, "Channel %d is not in dataOut.channelList"
                channelIndexList.append(channel)
        
        if timerange != None:
            self.__timerange = timerange
        
        tmin = None
        tmax = None
        x = dataOut.getDatatime()
        y = dataOut.getHeiRange()
        z = 10.*numpy.log10(dataOut.data_spc[channelIndexList,:,:])
        avg = numpy.average(z, axis=1)
        
        noise = dataOut.getNoise()
            
        if not self.__isConfig:
            
            nplots = len(channelIndexList)
            
            self.setup(idfigure=idfigure,
                       nplots=nplots,
                       wintitle=wintitle,
                       showprofile=showprofile)
            
            tmin, tmax = self.__getTimeLim(x, xmin, xmax)
            if ymin == None: ymin = numpy.nanmin(y)
            if ymax == None: ymax = numpy.nanmax(y)
            if zmin == None: zmin = numpy.nanmin(avg)*0.9
            if zmax == None: zmax = numpy.nanmax(avg)*0.9
            
            self.__isConfig = True
            
        thisDatetime = datetime.datetime.fromtimestamp(dataOut.utctime)
        title = "RTI: %s" %(thisDatetime.strftime("%d-%b-%Y"))
        xlabel = "Velocity (m/s)"
        ylabel = "Range (Km)"
        
        self.setWinTitle(title)
            
        for i in range(self.nplots):
            title = "Channel %d: %s" %(dataOut.channelList[i], thisDatetime.strftime("%d-%b-%Y %H:%M:%S"))
            axes = self.axesList[i*self.__nsubplots]
            z = avg[i].reshape((1,-1))
            axes.pcolor(x, y, z,
                        xmin=tmin, xmax=tmax, ymin=ymin, ymax=ymax, zmin=zmin, zmax=zmax,
                        xlabel=xlabel, ylabel=ylabel, title=title, rti=True, XAxisAsTime=True,
                        ticksize=9, cblabel='', cbsize="1%")
            
            if self.__showprofile:
                axes = self.axesList[i*self.__nsubplots +1]
                axes.pline(avg[i], y,
                        xmin=zmin, xmax=zmax, ymin=ymin, ymax=ymax,
                        xlabel='dB', ylabel='', title='',
                        ytick_visible=False,
                        grid='x')
            
        self.draw()
        
        if save:
            self.saveFigure(filename)
            
        if x[1] + (x[1]-x[0]) >= self.axesList[0].xmax:
            self.__isConfig = False
        
class SpectraPlot(Figure):
    
    __isConfig = None
    __nsubplots = None
    
    WIDTHPROF = None
    HEIGHTPROF = None
    
    def __init__(self):
        
        self.__isConfig = False
        self.__nsubplots = 1
        
        self.WIDTH = 300
        self.HEIGHT = 400
        self.WIDTHPROF = 120
        self.HEIGHTPROF = 0
        
    def getSubplots(self):
        
        ncol = int(numpy.sqrt(self.nplots)+0.9)
        nrow = int(self.nplots*1./ncol + 0.9)
        
        return nrow, ncol
    
    def setup(self, idfigure, nplots, wintitle, showprofile=True):
               
        self.__showprofile = showprofile
        self.nplots = nplots
        
        ncolspan = 1
        colspan = 1
        if showprofile:
            ncolspan = 3
            colspan = 2
            self.__nsubplots = 2
        
        self.createFigure(idfigure = idfigure,
                          wintitle = wintitle,
                          widthplot = self.WIDTH + self.WIDTHPROF,
                          heightplot = self.HEIGHT + self.HEIGHTPROF)
        
        nrow, ncol = self.getSubplots()
        
        counter = 0
        for y in range(nrow):
            for x in range(ncol):
                
                if counter >= self.nplots:
                    break
                
                self.addAxes(nrow, ncol*ncolspan, y, x*ncolspan, colspan, 1)
                
                if showprofile:
                    self.addAxes(nrow, ncol*ncolspan, y, x*ncolspan+colspan, 1, 1)
                    
                counter += 1
    
    def run(self, dataOut, idfigure, wintitle="", channelList=None, showprofile='True',
            xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None, save=False, filename=None):
        
        """
        
        Input:
            dataOut         :
            idfigure        :
            wintitle        :
            channelList     :
            showProfile     :
            xmin            :    None,
            xmax            :    None,
            ymin            :    None,
            ymax            :    None,
            zmin            :    None,
            zmax            :    None
        """
        
        if channelList == None:
            channelIndexList = dataOut.channelIndexList
        else:
            channelIndexList = []
            for channel in channelList:
                if channel not in dataOut.channelList:
                    raise ValueError, "Channel %d is not in dataOut.channelList"
                channelIndexList.append(channel)
        
        x = dataOut.getVelRange(1)
        y = dataOut.getHeiRange()
        z = 10.*numpy.log10(dataOut.data_spc[channelIndexList,:,:])
        avg = numpy.average(z, axis=1)
        
        noise = dataOut.getNoise()
        
        if not self.__isConfig:
            
            nplots = len(channelIndexList)
            
            self.setup(idfigure=idfigure,
                       nplots=nplots,
                       wintitle=wintitle,
                       showprofile=showprofile)
            
            if xmin == None: xmin = numpy.nanmin(x)
            if xmax == None: xmax = numpy.nanmax(x)
            if ymin == None: ymin = numpy.nanmin(y)
            if ymax == None: ymax = numpy.nanmax(y)
            if zmin == None: zmin = numpy.nanmin(avg)*0.9
            if zmax == None: zmax = numpy.nanmax(avg)*0.9
            
            self.__isConfig = True
            
        thisDatetime = datetime.datetime.fromtimestamp(dataOut.utctime)
        title = "Spectra: %s" %(thisDatetime.strftime("%d-%b-%Y %H:%M:%S"))
        xlabel = "Velocity (m/s)"
        ylabel = "Range (Km)"
        
        self.setWinTitle(title)
            
        for i in range(self.nplots):
            title = "Channel %d: %4.2fdB" %(dataOut.channelList[i], noise[i])
            axes = self.axesList[i*self.__nsubplots]
            axes.pcolor(x, y, z[i,:,:],
                        xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, zmin=zmin, zmax=zmax,
                        xlabel=xlabel, ylabel=ylabel, title=title,
                        ticksize=9, cblabel='')
            
            if self.__showprofile:
                axes = self.axesList[i*self.__nsubplots +1]
                axes.pline(avg[i], y,
                        xmin=zmin, xmax=zmax, ymin=ymin, ymax=ymax,
                        xlabel='dB', ylabel='', title='',
                        ytick_visible=False,
                        grid='x')
            
        self.draw()
        
        if save:
            self.saveFigure(filename)

class Scope(Figure):
    
    __isConfig = None
    
    def __init__(self):
        
        self.__isConfig = False
        self.WIDTH = 600
        self.HEIGHT = 200
    
    def getSubplots(self):
        
        nrow = self.nplots
        ncol = 3
        return nrow, ncol
    
    def setup(self, idfigure, nplots, wintitle):
        
        self.createFigure(idfigure, wintitle)
        
        nrow,ncol = self.getSubplots()
        colspan = 3
        rowspan = 1
        
        for i in range(nplots):
            self.addAxes(nrow, ncol, i, 0, colspan, rowspan)
            
        self.nplots = nplots
    
    def run(self, dataOut, idfigure, wintitle="", channelList=None,
            xmin=None, xmax=None, ymin=None, ymax=None, save=False, filename=None):
        
        """
        
        Input:
            dataOut         :
            idfigure        :
            wintitle        :
            channelList     :
            xmin            :    None,
            xmax            :    None,
            ymin            :    None,
            ymax            :    None,
        """
        
        if channelList == None:
            channelList = dataOut.channelList
        
        x = dataOut.heightList
        y = dataOut.data[channelList,:] * numpy.conjugate(dataOut.data[channelList,:])
        y = y.real
        
        noise = dataOut.getNoise()
        
        if not self.__isConfig:
            nplots = len(channelList)
            
            self.setup(idfigure=idfigure,
                       nplots=nplots,
                       wintitle=wintitle)
            
            if xmin == None: xmin = numpy.nanmin(x)
            if xmax == None: xmax = numpy.nanmax(x)
            if ymin == None: ymin = numpy.nanmin(y)
            if ymax == None: ymax = numpy.nanmax(y)
                
            self.__isConfig = True
        
        
        thisDatetime = datetime.datetime.fromtimestamp(dataOut.utctime)
        title = "Scope: %s" %(thisDatetime.strftime("%d-%b-%Y %H:%M:%S"))
        xlabel = "Range (Km)"
        ylabel = "Intensity"
        
        self.setWinTitle(title)
        
        for i in range(len(self.axesList)):
            title = "Channel %d: %4.2fdB" %(i, noise[i])
            axes = self.axesList[i]
            ychannel = y[i,:]
            axes.pline(x, ychannel,
                        xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
                        xlabel=xlabel, ylabel=ylabel, title=title)
        
        self.draw()
            
        if save:
            self.saveFigure(filename)
        