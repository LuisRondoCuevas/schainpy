import sys
import time
import numpy,math
from scipy import interpolate
from schainpy.model.proc.jroproc_base import ProcessingUnit, Operation, MPDecorator
from schainpy.model.data.jrodata import Voltage
from schainpy.utils import log
from time import time


@MPDecorator
class VoltageProc(ProcessingUnit):

    def __init__(self):

        ProcessingUnit.__init__(self)

        self.dataOut = Voltage()
        self.flip = 1
        self.setupReq = False

    def run(self):

        if self.dataIn.type == 'AMISR':
            self.__updateObjFromAmisrInput()

        if self.dataIn.type == 'Voltage':
            self.dataOut.copy(self.dataIn)

    #         self.dataOut.copy(self.dataIn)

    def __updateObjFromAmisrInput(self):

        self.dataOut.timeZone = self.dataIn.timeZone
        self.dataOut.dstFlag = self.dataIn.dstFlag
        self.dataOut.errorCount = self.dataIn.errorCount
        self.dataOut.useLocalTime = self.dataIn.useLocalTime

        self.dataOut.flagNoData = self.dataIn.flagNoData
        self.dataOut.data = self.dataIn.data
        self.dataOut.utctime = self.dataIn.utctime
        self.dataOut.channelList = self.dataIn.channelList
        #self.dataOut.timeInterval = self.dataIn.timeInterval
        self.dataOut.heightList = self.dataIn.heightList
        self.dataOut.nProfiles = self.dataIn.nProfiles

        self.dataOut.nCohInt = self.dataIn.nCohInt
        self.dataOut.ippSeconds = self.dataIn.ippSeconds
        self.dataOut.frequency = self.dataIn.frequency

        self.dataOut.azimuth = self.dataIn.azimuth
        self.dataOut.zenith = self.dataIn.zenith

        self.dataOut.beam.codeList = self.dataIn.beam.codeList
        self.dataOut.beam.azimuthList = self.dataIn.beam.azimuthList
        self.dataOut.beam.zenithList = self.dataIn.beam.zenithList
    #
    #        pass#
    #
    #    def init(self):
    #
    #
    #        if self.dataIn.type == 'AMISR':
    #            self.__updateObjFromAmisrInput()
    #
    #        if self.dataIn.type == 'Voltage':
    #            self.dataOut.copy(self.dataIn)
    #        # No necesita copiar en cada init() los atributos de dataIn
    #        # la copia deberia hacerse por cada nuevo bloque de datos

    def selectChannels(self, channelList):

        channelIndexList = []

        for channel in channelList:
            if channel not in self.dataOut.channelList:
                raise ValueError("Channel %d is not in %s" %(channel, str(self.dataOut.channelList)))

            index = self.dataOut.channelList.index(channel)
            channelIndexList.append(index)

        self.selectChannelsByIndex(channelIndexList)

    def selectChannelsByIndex(self, channelIndexList):
        """
        Selecciona un bloque de datos en base a canales segun el channelIndexList

        Input:
            channelIndexList    :    lista sencilla de canales a seleccionar por ej. [2,3,7]

        Affected:
            self.dataOut.data
            self.dataOut.channelIndexList
            self.dataOut.nChannels
            self.dataOut.m_ProcessingHeader.totalSpectra
            self.dataOut.systemHeaderObj.numChannels
            self.dataOut.m_ProcessingHeader.blockSize

        Return:
            None
        """

        for channelIndex in channelIndexList:
            if channelIndex not in self.dataOut.channelIndexList:
                print(channelIndexList)
                raise ValueError("The value %d in channelIndexList is not valid" %channelIndex)

        if self.dataOut.flagDataAsBlock:
            """
            Si la data es obtenida por bloques, dimension = [nChannels, nProfiles, nHeis]
            """
            data = self.dataOut.data[channelIndexList,:,:]
        else:
            data = self.dataOut.data[channelIndexList,:]

        self.dataOut.data = data
        # self.dataOut.channelList = [self.dataOut.channelList[i] for i in channelIndexList]
        self.dataOut.channelList = range(len(channelIndexList))

        return 1

    def selectHeights(self, minHei=None, maxHei=None):
        """
        Selecciona un bloque de datos en base a un grupo de valores de alturas segun el rango
        minHei <= height <= maxHei

        Input:
            minHei    :    valor minimo de altura a considerar
            maxHei    :    valor maximo de altura a considerar

        Affected:
            Indirectamente son cambiados varios valores a travez del metodo selectHeightsByIndex

        Return:
            1 si el metodo se ejecuto con exito caso contrario devuelve 0
        """

        if minHei == None:
            minHei = self.dataOut.heightList[0]

        if maxHei == None:
            maxHei = self.dataOut.heightList[-1]

        if (minHei < self.dataOut.heightList[0]):
            minHei = self.dataOut.heightList[0]

        if (maxHei > self.dataOut.heightList[-1]):
            maxHei = self.dataOut.heightList[-1]

        minIndex = 0
        maxIndex = 0
        heights = self.dataOut.heightList

        inda = numpy.where(heights >= minHei)
        indb = numpy.where(heights <= maxHei)

        try:
            minIndex = inda[0][0]
        except:
            minIndex = 0

        try:
            maxIndex = indb[0][-1]
        except:
            maxIndex = len(heights)

        self.selectHeightsByIndex(minIndex, maxIndex)

        return 1


    def selectHeightsByIndex(self, minIndex, maxIndex):
        """
        Selecciona un bloque de datos en base a un grupo indices de alturas segun el rango
        minIndex <= index <= maxIndex

        Input:
            minIndex    :    valor de indice minimo de altura a considerar
            maxIndex    :    valor de indice maximo de altura a considerar

        Affected:
            self.dataOut.data
            self.dataOut.heightList

        Return:
            1 si el metodo se ejecuto con exito caso contrario devuelve 0
        """

        if (minIndex < 0) or (minIndex > maxIndex):
            raise ValueError("Height index range (%d,%d) is not valid" % (minIndex, maxIndex))

        if (maxIndex >= self.dataOut.nHeights):
            maxIndex = self.dataOut.nHeights

        #voltage
        if self.dataOut.flagDataAsBlock:
            """
            Si la data es obtenida por bloques, dimension = [nChannels, nProfiles, nHeis]
            """
            data = self.dataOut.data[:,:, minIndex:maxIndex]
        else:
            data = self.dataOut.data[:, minIndex:maxIndex]

        #         firstHeight = self.dataOut.heightList[minIndex]

        self.dataOut.data = data
        self.dataOut.heightList = self.dataOut.heightList[minIndex:maxIndex]

        if self.dataOut.nHeights <= 1:
            raise ValueError("selectHeights: Too few heights. Current number of heights is %d" %(self.dataOut.nHeights))

        return 1


    def filterByHeights(self, window):

        deltaHeight = self.dataOut.heightList[1] - self.dataOut.heightList[0]

        if window == None:
            window = (self.dataOut.radarControllerHeaderObj.txA/self.dataOut.radarControllerHeaderObj.nBaud) / deltaHeight

        newdelta = deltaHeight * window
        r = self.dataOut.nHeights % window
        newheights = (self.dataOut.nHeights-r)/window

        if newheights <= 1:
            raise ValueError("filterByHeights: Too few heights. Current number of heights is %d and window is %d" %(self.dataOut.nHeights, window))

        if self.dataOut.flagDataAsBlock:
            """
            Si la data es obtenida por bloques, dimension = [nChannels, nProfiles, nHeis]
            """
            buffer = self.dataOut.data[:, :, 0:int(self.dataOut.nHeights-r)]
            buffer = buffer.reshape(self.dataOut.nChannels, self.dataOut.nProfiles, int(self.dataOut.nHeights/window), window)
            buffer = numpy.sum(buffer,3)

        else:
            buffer = self.dataOut.data[:,0:int(self.dataOut.nHeights-r)]
            buffer = buffer.reshape(self.dataOut.nChannels,int(self.dataOut.nHeights/window),int(window))
            buffer = numpy.sum(buffer,2)

        self.dataOut.data = buffer
        self.dataOut.heightList = self.dataOut.heightList[0] + numpy.arange( newheights )*newdelta
        self.dataOut.windowOfFilter = window

    def setH0(self, h0, deltaHeight = None):

        if not deltaHeight:
            deltaHeight = self.dataOut.heightList[1] - self.dataOut.heightList[0]

        nHeights = self.dataOut.nHeights

        newHeiRange = h0 + numpy.arange(nHeights)*deltaHeight

        self.dataOut.heightList = newHeiRange

    def deFlip(self, channelList = []):

        data = self.dataOut.data.copy()

        if self.dataOut.flagDataAsBlock:
            flip = self.flip
            profileList = list(range(self.dataOut.nProfiles))

            if not channelList:
                for thisProfile in profileList:
                    data[:,thisProfile,:] = data[:,thisProfile,:]*flip
                    flip *= -1.0
            else:
                for thisChannel in channelList:
                    if thisChannel not in self.dataOut.channelList:
                        continue

                    for thisProfile in profileList:
                        data[thisChannel,thisProfile,:] = data[thisChannel,thisProfile,:]*flip
                        flip *= -1.0

            self.flip = flip

        else:
            if not channelList:
                data[:,:] = data[:,:]*self.flip
            else:
                for thisChannel in channelList:
                    if thisChannel not in self.dataOut.channelList:
                        continue

                    data[thisChannel,:] = data[thisChannel,:]*self.flip

            self.flip *= -1.

        self.dataOut.data = data

    def setRadarFrequency(self, frequency=None):

        if frequency != None:
            self.dataOut.frequency = frequency

        return 1

    def interpolateHeights(self, topLim, botLim):
        #69 al 72 para julia
        #82-84 para meteoros
        if len(numpy.shape(self.dataOut.data))==2:
            sampInterp = (self.dataOut.data[:,botLim-1] + self.dataOut.data[:,topLim+1])/2
            sampInterp = numpy.transpose(numpy.tile(sampInterp,(topLim-botLim + 1,1)))
            #self.dataOut.data[:,botLim:limSup+1] = sampInterp
            self.dataOut.data[:,botLim:topLim+1] = sampInterp
        else:
            nHeights = self.dataOut.data.shape[2]
            x = numpy.hstack((numpy.arange(botLim),numpy.arange(topLim+1,nHeights)))
            y = self.dataOut.data[:,:,list(range(botLim))+list(range(topLim+1,nHeights))]
            f = interpolate.interp1d(x, y, axis = 2)
            xnew = numpy.arange(botLim,topLim+1)
            ynew = f(xnew)

            self.dataOut.data[:,:,botLim:topLim+1]  = ynew

    # import collections

class CohInt(Operation):

    isConfig = False
    __profIndex = 0
    __byTime = False
    __initime = None
    __lastdatatime = None
    __integrationtime = None
    __buffer = None
    __bufferStride = []
    __dataReady = False
    __profIndexStride = 0
    __dataToPutStride = False
    n = None

    def __init__(self, **kwargs):

        Operation.__init__(self, **kwargs)

        #   self.isConfig = False

    def setup(self, n=None, timeInterval=None, stride=None, overlapping=False, byblock=False):
        """
        Set the parameters of the integration class.

        Inputs:

            n               :    Number of coherent integrations
            timeInterval    :    Time of integration. If the parameter "n" is selected this one does not work
            overlapping     :
        """

        self.__initime = None
        self.__lastdatatime = 0
        self.__buffer = None
        self.__dataReady = False
        self.byblock = byblock
        self.stride = stride

        if n == None and timeInterval == None:
            raise ValueError("n or timeInterval should be specified ...")

        if n != None:
            self.n = n
            self.__byTime = False
        else:
            self.__integrationtime = timeInterval #* 60. #if (type(timeInterval)!=integer) -> change this line
            self.n = 9999
            self.__byTime = True

        if overlapping:
            self.__withOverlapping = True
            self.__buffer = None
        else:
            self.__withOverlapping = False
            self.__buffer = 0

        self.__profIndex = 0

    def putData(self, data):

        """
        Add a profile to the __buffer and increase in one the __profileIndex

        """

        if not self.__withOverlapping:
            #print("inside over")
            self.__buffer += data.copy()
            self.__profIndex += 1
            return

        #Overlapping data
        nChannels, nHeis = data.shape
        #print("show me the light",data.shape)
        data = numpy.reshape(data, (1, nChannels, nHeis))
        #print(data.shape)
        #If the buffer is empty then it takes the data value
        if self.__buffer is None:
            self.__buffer = data
            self.__profIndex += 1
            return

        #If the buffer length is lower than n then stakcing the data value
        if self.__profIndex < self.n:
            self.__buffer = numpy.vstack((self.__buffer, data))
            self.__profIndex += 1
            return

        #If the buffer length is equal to n then replacing the last buffer value with the data value
        self.__buffer = numpy.roll(self.__buffer, -1, axis=0)
        self.__buffer[self.n-1] = data
        self.__profIndex = self.n
        return


    def pushData(self):
        """
        Return the sum of the last profiles and the profiles used in the sum.

        Affected:

        self.__profileIndex

        """

        if not self.__withOverlapping:
            print("ahora que fue")
            data = self.__buffer
            n = self.__profIndex

            self.__buffer = 0
            self.__profIndex = 0

            return data, n

        #print("cual funciona")
        #Integration with Overlapping
        data = numpy.sum(self.__buffer, axis=0)
        # print data
        # raise
        n = self.__profIndex

        return data, n

    def byProfiles(self, data):

        self.__dataReady = False
        avgdata = None
        #         n = None
        # print data
        # raise
        #print("beforeputdata")
        self.putData(data)

        if self.__profIndex == self.n:
            avgdata, n = self.pushData()
            self.__dataReady = True

        return avgdata

    def byTime(self, data, datatime):

        self.__dataReady = False
        avgdata = None
        n = None

        self.putData(data)

        if (datatime - self.__initime) >= self.__integrationtime:
            avgdata, n = self.pushData()
            self.n = n
            self.__dataReady = True

        return avgdata

    def integrateByStride(self, data, datatime):
        # print data
        if self.__profIndex == 0:
            self.__buffer = [[data.copy(), datatime]]
        else:
            self.__buffer.append([data.copy(),datatime])
        self.__profIndex += 1
        self.__dataReady = False

        if self.__profIndex == self.n * self.stride :
            self.__dataToPutStride = True
            self.__profIndexStride = 0
            self.__profIndex = 0
            self.__bufferStride = []
            for i in range(self.stride):
                current = self.__buffer[i::self.stride]
                data = numpy.sum([t[0] for t in current], axis=0)
                avgdatatime = numpy.average([t[1] for t in current])
                # print data
                self.__bufferStride.append((data, avgdatatime))

        if self.__dataToPutStride:
            self.__dataReady = True
            self.__profIndexStride += 1
            if self.__profIndexStride == self.stride:
                self.__dataToPutStride = False
            # print self.__bufferStride[self.__profIndexStride - 1]
            # raise
            return self.__bufferStride[self.__profIndexStride - 1]


        return None, None

    def integrate(self, data, datatime=None):

        if self.__initime == None:
            self.__initime = datatime

        if self.__byTime:
            avgdata = self.byTime(data, datatime)
        else:
            avgdata = self.byProfiles(data)


        self.__lastdatatime = datatime

        if avgdata is None:
            return None, None

        avgdatatime = self.__initime

        deltatime = datatime - self.__lastdatatime

        if not self.__withOverlapping:
            self.__initime = datatime
        else:
            self.__initime += deltatime

        return avgdata, avgdatatime

    def integrateByBlock(self, dataOut):

        times = int(dataOut.data.shape[1]/self.n)
        avgdata = numpy.zeros((dataOut.nChannels, times, dataOut.nHeights), dtype=numpy.complex)

        id_min = 0
        id_max = self.n

        for i in range(times):
            junk = dataOut.data[:,id_min:id_max,:]
            avgdata[:,i,:] = junk.sum(axis=1)
            id_min += self.n
            id_max += self.n

        timeInterval = dataOut.ippSeconds*self.n
        avgdatatime = (times - 1) * timeInterval + dataOut.utctime
        self.__dataReady = True
        return avgdata, avgdatatime

    def run(self, dataOut, n=None, timeInterval=None, stride=None, overlapping=False, byblock=False, **kwargs):

        if not self.isConfig:
            self.setup(n=n, stride=stride, timeInterval=timeInterval, overlapping=overlapping, byblock=byblock, **kwargs)
            self.isConfig = True

        if dataOut.flagDataAsBlock:
            """
            Si la data es leida por bloques, dimension = [nChannels, nProfiles, nHeis]
            """
            avgdata, avgdatatime = self.integrateByBlock(dataOut)
            dataOut.nProfiles /= self.n
        else:
            if stride is None:
                avgdata, avgdatatime = self.integrate(dataOut.data, dataOut.utctime)
            else:
                avgdata, avgdatatime = self.integrateByStride(dataOut.data, dataOut.utctime)


        #   dataOut.timeInterval *= n
        dataOut.flagNoData = True

        if self.__dataReady:
            dataOut.data = avgdata
            dataOut.nCohInt *= self.n
            dataOut.utctime = avgdatatime
            # print avgdata, avgdatatime
            # raise
            #   dataOut.timeInterval = dataOut.ippSeconds * dataOut.nCohInt
            dataOut.flagNoData = False
        return dataOut

class Decoder(Operation):

    isConfig = False
    __profIndex = 0

    code = None

    nCode = None
    nBaud = None

    def __init__(self, **kwargs):

        Operation.__init__(self, **kwargs)

        self.times = None
        self.osamp = None
    #         self.__setValues = False
        self.isConfig = False
        self.setupReq = False
    def setup(self, code, osamp, dataOut):

        self.__profIndex = 0

        self.code = code

        self.nCode = len(code)
        self.nBaud = len(code[0])

        if (osamp != None) and (osamp >1):
            self.osamp = osamp
            self.code = numpy.repeat(code, repeats=self.osamp, axis=1)
            self.nBaud = self.nBaud*self.osamp

        self.__nChannels = dataOut.nChannels
        self.__nProfiles = dataOut.nProfiles
        self.__nHeis = dataOut.nHeights

        if self.__nHeis < self.nBaud:
            raise ValueError('Number of heights (%d) should be greater than number of bauds (%d)' %(self.__nHeis, self.nBaud))

        #Frequency
        __codeBuffer = numpy.zeros((self.nCode, self.__nHeis), dtype=numpy.complex)

        __codeBuffer[:,0:self.nBaud] = self.code

        self.fft_code = numpy.conj(numpy.fft.fft(__codeBuffer, axis=1))

        if dataOut.flagDataAsBlock:

            self.ndatadec = self.__nHeis #- self.nBaud + 1

            self.datadecTime = numpy.zeros((self.__nChannels, self.__nProfiles, self.ndatadec), dtype=numpy.complex)

        else:

            #Time
            self.ndatadec = self.__nHeis #- self.nBaud + 1

            self.datadecTime = numpy.zeros((self.__nChannels, self.ndatadec), dtype=numpy.complex)

    def __convolutionInFreq(self, data):

        fft_code = self.fft_code[self.__profIndex].reshape(1,-1)

        fft_data = numpy.fft.fft(data, axis=1)

        conv = fft_data*fft_code

        data = numpy.fft.ifft(conv,axis=1)

        return data

    def __convolutionInFreqOpt(self, data):

        raise NotImplementedError

    def __convolutionInTime(self, data):

        code = self.code[self.__profIndex]
        for i in range(self.__nChannels):
            self.datadecTime[i,:] = numpy.correlate(data[i,:], code, mode='full')[self.nBaud-1:]

        return self.datadecTime

    def __convolutionByBlockInTime(self, data):

        repetitions = int(self.__nProfiles / self.nCode)
        junk = numpy.lib.stride_tricks.as_strided(self.code, (repetitions, self.code.size), (0, self.code.itemsize))
        junk = junk.flatten()
        code_block = numpy.reshape(junk, (self.nCode*repetitions, self.nBaud))
        profilesList = range(self.__nProfiles)

        for i in range(self.__nChannels):
            for j in profilesList:
                self.datadecTime[i,j,:] = numpy.correlate(data[i,j,:], code_block[j,:], mode='full')[self.nBaud-1:]
        return self.datadecTime

    def __convolutionByBlockInFreq(self, data):

        raise NotImplementedError("Decoder by frequency fro Blocks not implemented")


        fft_code = self.fft_code[self.__profIndex].reshape(1,-1)

        fft_data = numpy.fft.fft(data, axis=2)

        conv = fft_data*fft_code

        data = numpy.fft.ifft(conv,axis=2)

        return data


    def run(self, dataOut, code=None, nCode=None, nBaud=None, mode = 0, osamp=None, times=None):

        if dataOut.flagDecodeData:
            print("This data is already decoded, recoding again ...")

        if not self.isConfig:

            if code is None:
                if dataOut.code is None:
                    raise ValueError("Code could not be read from %s instance. Enter a value in Code parameter" %dataOut.type)

                code = dataOut.code
            else:
                code = numpy.array(code).reshape(nCode,nBaud)
            self.setup(code, osamp, dataOut)

            self.isConfig = True

            if mode == 3:
                sys.stderr.write("Decoder Warning: mode=%d is not valid, using mode=0\n" %mode)

            if times != None:
                sys.stderr.write("Decoder Warning: Argument 'times' in not used anymore\n")

        if self.code is None:
            print("Fail decoding: Code is not defined.")
            return

        self.__nProfiles = dataOut.nProfiles
        datadec = None

        if mode == 3:
            mode = 0

        if dataOut.flagDataAsBlock:
            """
            Decoding when data have been read as block,
            """

            if mode == 0:
                datadec = self.__convolutionByBlockInTime(dataOut.data)
            if mode == 1:
                datadec = self.__convolutionByBlockInFreq(dataOut.data)
        else:
            """
            Decoding when data have been read profile by profile
            """
            if mode == 0:
                datadec = self.__convolutionInTime(dataOut.data)

            if mode == 1:
                datadec = self.__convolutionInFreq(dataOut.data)

            if mode == 2:
                datadec = self.__convolutionInFreqOpt(dataOut.data)

        if datadec is None:
            raise ValueError("Codification mode selected is not valid: mode=%d. Try selecting 0 or 1" %mode)

        dataOut.code = self.code
        dataOut.nCode = self.nCode
        dataOut.nBaud = self.nBaud

        dataOut.data = datadec

        dataOut.heightList = dataOut.heightList[0:datadec.shape[-1]]

        dataOut.flagDecodeData = True #asumo q la data esta decodificada

        if self.__profIndex == self.nCode-1:
            self.__profIndex = 0
            return dataOut

        self.__profIndex += 1

        return dataOut
    #        dataOut.flagDeflipData = True #asumo q la data no esta sin flip


class ProfileConcat(Operation):

    isConfig = False
    buffer = None

    def __init__(self, **kwargs):

        Operation.__init__(self, **kwargs)
        self.profileIndex = 0

    def reset(self):
        self.buffer = numpy.zeros_like(self.buffer)
        self.start_index = 0
        self.times = 1

    def setup(self, data, m, n=1):
        self.buffer = numpy.zeros((data.shape[0],data.shape[1]*m),dtype=type(data[0,0]))
        self.nHeights = data.shape[1]#.nHeights
        self.start_index = 0
        self.times = 1

    def concat(self, data):

        self.buffer[:,self.start_index:self.nHeights*self.times] = data.copy()
        self.start_index = self.start_index + self.nHeights

    def run(self, dataOut, m):
        dataOut.flagNoData = True

        if not self.isConfig:
            self.setup(dataOut.data, m, 1)
            self.isConfig = True

        if dataOut.flagDataAsBlock:
            raise ValueError("ProfileConcat can only be used when voltage have been read profile by profile, getBlock = False")

        else:
            self.concat(dataOut.data)
            self.times += 1
            if self.times > m:
                dataOut.data = self.buffer
                self.reset()
                dataOut.flagNoData = False
                # se deben actualizar mas propiedades del header y del objeto dataOut, por ejemplo, las alturas
                deltaHeight = dataOut.heightList[1] - dataOut.heightList[0]
                xf = dataOut.heightList[0] + dataOut.nHeights * deltaHeight * m
                dataOut.heightList = numpy.arange(dataOut.heightList[0], xf, deltaHeight)
                dataOut.ippSeconds *= m
        return dataOut

class ProfileSelector(Operation):

    profileIndex = None
    # Tamanho total de los perfiles
    nProfiles = None

    def __init__(self, **kwargs):

        Operation.__init__(self, **kwargs)
        self.profileIndex = 0

    def incProfileIndex(self):

        self.profileIndex += 1

        if self.profileIndex >= self.nProfiles:
            self.profileIndex = 0

    def isThisProfileInRange(self, profileIndex, minIndex, maxIndex):

        if profileIndex < minIndex:
            return False

        if profileIndex > maxIndex:
            return False

        return True

    def isThisProfileInList(self, profileIndex, profileList):

        if profileIndex not in profileList:
            return False

        return True

    def run(self, dataOut, profileList=None, profileRangeList=None, beam=None, byblock=False, rangeList = None, nProfiles=None):

        """
        ProfileSelector:

        Inputs:
            profileList        :    Index of profiles selected. Example: profileList = (0,1,2,7,8)

            profileRangeList    :    Minimum and maximum profile indexes. Example: profileRangeList = (4, 30)

            rangeList            :    List of profile ranges. Example: rangeList = ((4, 30), (32, 64), (128, 256))

        """

        if rangeList is not None:
            if type(rangeList[0]) not in (tuple, list):
                rangeList = [rangeList]

        dataOut.flagNoData = True

        if dataOut.flagDataAsBlock:
            """
            data dimension  = [nChannels, nProfiles, nHeis]
            """
            if profileList != None:
                dataOut.data = dataOut.data[:,profileList,:]

            if profileRangeList != None:
                minIndex = profileRangeList[0]
                maxIndex = profileRangeList[1]
                profileList = list(range(minIndex, maxIndex+1))

                dataOut.data = dataOut.data[:,minIndex:maxIndex+1,:]

            if rangeList != None:

                profileList = []

                for thisRange in rangeList:
                    minIndex = thisRange[0]
                    maxIndex = thisRange[1]

                    profileList.extend(list(range(minIndex, maxIndex+1)))

                dataOut.data = dataOut.data[:,profileList,:]

            dataOut.nProfiles = len(profileList)
            dataOut.profileIndex = dataOut.nProfiles - 1
            dataOut.flagNoData = False

            return dataOut

        """
        data dimension  = [nChannels, nHeis]
        """

        if profileList != None:

            if self.isThisProfileInList(dataOut.profileIndex, profileList):

                self.nProfiles = len(profileList)
                dataOut.nProfiles = self.nProfiles
                dataOut.profileIndex = self.profileIndex
                dataOut.flagNoData = False

                self.incProfileIndex()
            return dataOut

        if profileRangeList != None:

            minIndex = profileRangeList[0]
            maxIndex = profileRangeList[1]

            if self.isThisProfileInRange(dataOut.profileIndex, minIndex, maxIndex):

                self.nProfiles = maxIndex - minIndex + 1
                dataOut.nProfiles = self.nProfiles
                dataOut.profileIndex = self.profileIndex
                dataOut.flagNoData = False

                self.incProfileIndex()
            return dataOut

        if rangeList != None:

            nProfiles = 0

            for thisRange in rangeList:
                minIndex = thisRange[0]
                maxIndex = thisRange[1]

                nProfiles += maxIndex - minIndex + 1

            for thisRange in rangeList:

                minIndex = thisRange[0]
                maxIndex = thisRange[1]

                if self.isThisProfileInRange(dataOut.profileIndex, minIndex, maxIndex):

                    self.nProfiles = nProfiles
                    dataOut.nProfiles = self.nProfiles
                    dataOut.profileIndex = self.profileIndex
                    dataOut.flagNoData = False

                    self.incProfileIndex()

                    break

            return dataOut


        if beam != None: #beam is only for AMISR data
            if self.isThisProfileInList(dataOut.profileIndex, dataOut.beamRangeDict[beam]):
                dataOut.flagNoData = False
                dataOut.profileIndex = self.profileIndex

                self.incProfileIndex()

            return dataOut

        raise ValueError("ProfileSelector needs profileList, profileRangeList or rangeList parameter")

        #return False
        return dataOut

class Reshaper(Operation):

    def __init__(self, **kwargs):

        Operation.__init__(self, **kwargs)

        self.__buffer = None
        self.__nitems = 0

    def __appendProfile(self, dataOut, nTxs):

        if self.__buffer is None:
            shape = (dataOut.nChannels, int(dataOut.nHeights/nTxs) )
            self.__buffer = numpy.empty(shape, dtype = dataOut.data.dtype)

        ini = dataOut.nHeights * self.__nitems
        end = ini + dataOut.nHeights

        self.__buffer[:, ini:end] = dataOut.data

        self.__nitems += 1

        return int(self.__nitems*nTxs)

    def __getBuffer(self):

        if self.__nitems == int(1./self.__nTxs):

            self.__nitems = 0

            return self.__buffer.copy()

        return None

    def __checkInputs(self, dataOut, shape, nTxs):

        if shape is None and nTxs is None:
            raise ValueError("Reshaper: shape of factor should be defined")

        if nTxs:
            if nTxs < 0:
                raise ValueError("nTxs should be greater than 0")

            if nTxs < 1 and dataOut.nProfiles % (1./nTxs) != 0:
                raise ValueError("nProfiles= %d is not divisibled by (1./nTxs) = %f" %(dataOut.nProfiles, (1./nTxs)))

            shape = [dataOut.nChannels, dataOut.nProfiles*nTxs, dataOut.nHeights/nTxs]

            return shape, nTxs

        if len(shape) != 2 and len(shape) !=  3:
            raise ValueError("shape dimension should be equal to 2 or 3. shape = (nProfiles, nHeis) or (nChannels, nProfiles, nHeis). Actually shape = (%d, %d, %d)" %(dataOut.nChannels, dataOut.nProfiles, dataOut.nHeights))

        if len(shape) == 2:
            shape_tuple = [dataOut.nChannels]
            shape_tuple.extend(shape)
        else:
            shape_tuple = list(shape)

        nTxs = 1.0*shape_tuple[1]/dataOut.nProfiles

        return shape_tuple, nTxs

    def run(self, dataOut, shape=None, nTxs=None):

        shape_tuple, self.__nTxs = self.__checkInputs(dataOut, shape, nTxs)

        dataOut.flagNoData = True
        profileIndex = None

        if dataOut.flagDataAsBlock:

            dataOut.data = numpy.reshape(dataOut.data, shape_tuple)
            dataOut.flagNoData = False

            profileIndex = int(dataOut.nProfiles*self.__nTxs) - 1

        else:

            if self.__nTxs < 1:

                self.__appendProfile(dataOut, self.__nTxs)
                new_data = self.__getBuffer()

                if new_data is not None:
                    dataOut.data = new_data
                    dataOut.flagNoData = False

                    profileIndex = dataOut.profileIndex*nTxs

            else:
                raise ValueError("nTxs should be greater than 0 and lower than 1, or use VoltageReader(..., getblock=True)")

        deltaHeight = dataOut.heightList[1] - dataOut.heightList[0]

        dataOut.heightList = numpy.arange(dataOut.nHeights/self.__nTxs) * deltaHeight + dataOut.heightList[0]

        dataOut.nProfiles = int(dataOut.nProfiles*self.__nTxs)

        dataOut.profileIndex = profileIndex

        dataOut.ippSeconds /= self.__nTxs

        return dataOut

class SplitProfiles(Operation):

    def __init__(self, **kwargs):

        Operation.__init__(self, **kwargs)

    def run(self, dataOut, n):

        dataOut.flagNoData = True
        profileIndex = None

        if dataOut.flagDataAsBlock:

            #nchannels, nprofiles, nsamples
            shape = dataOut.data.shape

            if shape[2] % n != 0:
                raise ValueError("Could not split the data, n=%d has to be multiple of %d" %(n, shape[2]))

            new_shape = shape[0], shape[1]*n, int(shape[2]/n)

            dataOut.data = numpy.reshape(dataOut.data, new_shape)
            dataOut.flagNoData = False

            profileIndex = int(dataOut.nProfiles/n) - 1

        else:

            raise ValueError("Could not split the data when is read Profile by Profile. Use VoltageReader(..., getblock=True)")

        deltaHeight = dataOut.heightList[1] - dataOut.heightList[0]

        dataOut.heightList = numpy.arange(dataOut.nHeights/n) * deltaHeight + dataOut.heightList[0]

        dataOut.nProfiles = int(dataOut.nProfiles*n)

        dataOut.profileIndex = profileIndex

        dataOut.ippSeconds /= n

        return dataOut

class CombineProfiles(Operation):
    def __init__(self, **kwargs):

        Operation.__init__(self, **kwargs)

        self.__remData = None
        self.__profileIndex = 0

    def run(self, dataOut, n):

        dataOut.flagNoData = True
        profileIndex = None

        if dataOut.flagDataAsBlock:

            #nchannels, nprofiles, nsamples
            shape = dataOut.data.shape
            new_shape = shape[0], shape[1]/n, shape[2]*n

            if shape[1] % n != 0:
                raise ValueError("Could not split the data, n=%d has to be multiple of %d" %(n, shape[1]))

            dataOut.data = numpy.reshape(dataOut.data, new_shape)
            dataOut.flagNoData = False

            profileIndex = int(dataOut.nProfiles*n) - 1

        else:

            #nchannels, nsamples
            if self.__remData is None:
                newData = dataOut.data
            else:
                newData = numpy.concatenate((self.__remData, dataOut.data), axis=1)

            self.__profileIndex += 1

            if self.__profileIndex < n:
                self.__remData = newData
                #continue
                return

            self.__profileIndex = 0
            self.__remData = None

            dataOut.data = newData
            dataOut.flagNoData = False

            profileIndex = dataOut.profileIndex/n


        deltaHeight = dataOut.heightList[1] - dataOut.heightList[0]

        dataOut.heightList = numpy.arange(dataOut.nHeights*n) * deltaHeight + dataOut.heightList[0]

        dataOut.nProfiles = int(dataOut.nProfiles/n)

        dataOut.profileIndex = profileIndex

        dataOut.ippSeconds *= n

        return dataOut



class CreateBlockVoltage(Operation):

    isConfig       = False
    __Index        = 0
    bufferShape    = None
    buffer         = None
    firstdatatime  = None

    def __init__(self,**kwargs):
        Operation.__init__(self,**kwargs)
        self.isConfig = False
        self.__Index = 0
        self.firstdatatime = None

    def setup(self,dataOut, m = None ):
        '''
        m= Numero perfiles
        '''
        #print("CONFIGURANDO CBV")
        self.__nChannels  = dataOut.nChannels
        self.__nHeis      = dataOut.nHeights
        shape             = dataOut.data.shape #nchannels, nprofiles, nsamples
        #print("input nChannels",self.__nChannels)
        #print("input nHeis",self.__nHeis)
        #print("SETUP CREATE BLOCK VOLTAGE")
        #print("input Shape",shape)
        #print("dataOut.nProfiles",dataOut.nProfiles)
        numberSamples     = self.__nHeis
        numberProfile     = int(m)
        dataOut.nProfiles = numberProfile
        #print("new numberProfile",numberProfile)
        #print("new numberSamples",numberSamples)

        self.bufferShape  = shape[0], numberProfile, numberSamples  # nchannels,nprofiles,nsamples
        self.buffer       = numpy.zeros([shape[0], numberProfile, numberSamples])
        self.bufferVel    = numpy.zeros([shape[0], numberProfile, numberSamples])

    def run(self, dataOut, m=None):
        #print("RUN")
        dataOut.flagNoData      = True
        dataOut.flagDataAsBlock = False
        #print("BLOCK INDEX        ",self.__Index)

        if not self.isConfig:
            self.setup(dataOut, m= m)
            self.isConfig = True
        if self.__Index < m:
            #print("PROFINDEX BLOCK         CBV",self.__Index)
            self.buffer[:,self.__Index,:]    = dataOut.data
            #corregir porque debe tener un perfil menos ojo
            self.bufferVel[:,self.__Index,:] = dataOut.data_velocity
            self.__Index += 1
            dataOut.flagNoData =  True

        if self.firstdatatime == None:
            self.firstdatatime = dataOut.utctime

        if self.__Index == m:
            #print("**********************************************")
            #print("self.buffer.shape           ",self.buffer.shape)
            #print("##############",self.firstdatatime)
            ##print("*********************************************")
            ##print("*********************************************")
            ##print("******* nProfiles *******", dataOut.nProfiles)
            ##print("*********************************************")
            ##print("*********************************************")
            dataOut.data            = self.buffer
            dataOut.data_velocity   = self.bufferVel
            dataOut.utctime         = self.firstdatatime
            dataOut.nProfiles       = m
            self.firstdatatime      = None
            dataOut.flagNoData      = False
            dataOut.flagDataAsBlock = True
            self.__Index            = 0
            dataOut.identifierWR    = True
        return dataOut

class PulsePairVoltage(Operation):
    '''
    Function PulsePair(Signal Power, Velocity)
    The real component of Lag[0] provides Intensity Information
    The imag component of Lag[1] Phase provides Velocity Information

    Configuration Parameters:
    nPRF = Number of Several PRF
    theta = Degree Azimuth angel Boundaries

    Input:
          self.dataOut
          lag[N]
    Affected:
          self.dataOut.spc
    '''
    isConfig       = False
    __profIndex    = 0
    __initime      = None
    __lastdatatime = None
    __buffer       = None
    __buffer2      = []
    __buffer3      = None
    __dataReady    = False
    n              = None
    __nch          = 0
    __nHeis        = 0
    removeDC       = False
    ipp            = None
    lambda_        = 0

    def __init__(self,**kwargs):
        Operation.__init__(self,**kwargs)

    def setup(self, dataOut, n = None, removeDC=False):
        '''
        n= Numero de PRF's de entrada
        '''
        self.__initime        = None
        self.__lastdatatime   = 0
        self.__dataReady      = False
        self.__buffer         = 0
        self.__buffer2        = []
        self.__buffer3        = 0
        self.__profIndex      = 0

        self.__nch            = dataOut.nChannels
        self.__nHeis          = dataOut.nHeights
        self.removeDC         = removeDC
        self.lambda_          = 3.0e8/(9345.0e6)
        self.ippSec           = dataOut.ippSeconds
        print("IPPseconds",dataOut.ippSeconds)

        print("ELVALOR DE n es:", n)
        if n == None:
            raise ValueError("n should be specified.")

        if n != None:
            if n<2:
                raise ValueError("n should be greater than 2")

        self.n       = n
        self.__nProf = n

        self.__buffer = numpy.zeros((dataOut.nChannels,
                                           n,
                                           dataOut.nHeights),
                                          dtype='complex')



    def putData(self,data):
        '''
        Add a profile to he __buffer and increase in one the __profiel Index
        '''
        self.__buffer[:,self.__profIndex,:]= data
        self.__profIndex      += 1
        return

    def pushData(self):
        '''
        Return the PULSEPAIR and the profiles used in the operation
        Affected :  self.__profileIndex
        '''

        if self.removeDC==True:
            mean    = numpy.mean(self.__buffer,1)
            tmp     = mean.reshape(self.__nch,1,self.__nHeis)
            dc= numpy.tile(tmp,[1,self.__nProf,1])
            self.__buffer = self.__buffer -  dc

        data_intensity   = numpy.sum(self.__buffer*numpy.conj(self.__buffer),1)/self.n
        pair1            = self.__buffer[:,1:,:]*numpy.conjugate(self.__buffer[:,:-1,:])
        angle=numpy.angle(numpy.sum(pair1,1))*180/(math.pi)
        #print(angle.shape)#print("__ANGLE__") #print("angle",angle[:,:10])
        data_velocity    = (self.lambda_/(4*math.pi*self.ippSec))*numpy.angle(numpy.sum(pair1,1))
        n                = self.__profIndex

        self.__buffer    = numpy.zeros((self.__nch, self.__nProf,self.__nHeis),  dtype='complex')
        self.__profIndex = 0
        return data_intensity,data_velocity,n

    def pulsePairbyProfiles(self,data):

        self.__dataReady     =  False
        data_intensity       =  None
        data_velocity        =  None
        self.putData(data)
        if self.__profIndex  == self.n:
            data_intensity, data_velocity, n   = self.pushData()
            self.__dataReady                   = True

        return data_intensity, data_velocity

    def pulsePairOp(self, data, datatime= None):

        if self.__initime == None:
            self.__initime = datatime

        data_intensity, data_velocity = self.pulsePairbyProfiles(data)
        self.__lastdatatime           = datatime

        if data_intensity is None:
            return None, None, None

        avgdatatime    = self.__initime
        deltatime      = datatime - self.__lastdatatime
        self.__initime = datatime

        return data_intensity, data_velocity, avgdatatime

    def run(self, dataOut,n = None,removeDC= False, overlapping= False,**kwargs):

        if not self.isConfig:
            self.setup(dataOut = dataOut, n    = n , removeDC=removeDC , **kwargs)
            self.isConfig   = True
        #print("*******************")
        #print("print Shape input data:",dataOut.data.shape)
        data_intensity, data_velocity, avgdatatime = self.pulsePairOp(dataOut.data, dataOut.utctime)
        dataOut.flagNoData                         = True

        if self.__dataReady:
            #print("#------------------------------------------------------")
            #print("data_ready",data_intensity.shape)
            dataOut.data            = data_intensity #valor para plotear RTI
            dataOut.nCohInt        *= self.n
            dataOut.data_intensity  = data_intensity #valor para intensidad
            dataOut.data_velocity   = data_velocity  #valor para velocidad
            dataOut.PRFbyAngle      = self.n         #numero de PRF*cada angulo rotado que equivale a un tiempo.
            dataOut.utctime         = avgdatatime
            dataOut.flagNoData      = False
        return dataOut
