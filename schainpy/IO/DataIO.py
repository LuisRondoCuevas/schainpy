'''
Created on 23/01/2012

@author $Author$
@version $Id$
@version $Id$
'''

import os, sys
import glob
import time
import numpy
import fnmatch
import time, datetime

path = os.path.split(os.getcwd())[0]
sys.path.append(path)

from Model.JROHeader import *
from Model.JROData import JROData

def checkForRealPath(path, year, doy, set, ext):
    """
    Por ser Linux Case Sensitive entonces checkForRealPath encuentra el nombre correcto de un path,
    Prueba por varias combinaciones de nombres entre mayusculas y minusculas para determinar
    el path exacto de un determinado file.
    
    Example    :
        nombre correcto del file es  .../.../D2009307/P2009307367.ext
        
        Entonces la funcion prueba con las siguientes combinaciones
            .../.../x2009307/y2009307367.ext
            .../.../x2009307/Y2009307367.ext
            .../.../X2009307/y2009307367.ext
            .../.../X2009307/Y2009307367.ext
        siendo para este caso, la ultima combinacion de letras, identica al file buscado 
        
    Return:
        Si encuentra la cobinacion adecuada devuelve el path completo y el nombre del file 
        caso contrario devuelve None como path y el la ultima combinacion de nombre en mayusculas 
        para el filename  
    """
    filepath = None
    find_flag = False
    filename = None

    if ext.lower() == ".r": #voltage
        header1 = "dD"
        header2 = "dD"
    elif ext.lower() == ".pdata": #spectra
        header1 = "dD"
        header2 = "pP"
    else:
        return None, filename
            
    for dir in header1: #barrido por las dos combinaciones posibles de "D"
        for fil in header2: #barrido por las dos combinaciones posibles de "D"
            doypath = "%s%04d%03d" % ( dir, year, doy ) #formo el nombre del directorio xYYYYDDD (x=d o x=D)
            filename = "%s%04d%03d%03d%s" % ( fil, year, doy, set, ext ) #formo el nombre del file xYYYYDDDSSS.ext
            filepath = os.path.join( path, doypath, filename ) #formo el path completo
            if os.path.exists( filepath ): #verifico que exista
                find_flag = True
                break
        if find_flag:
            break

    if not(find_flag):
        return None, filename

    return filepath, filename


def isNumber(str):
    """
    Chequea si el conjunto de caracteres que componen un string puede ser convertidos a un numero.

    Excepciones: 
        Si un determinado string no puede ser convertido a numero
    Input:
        str, string al cual se le analiza para determinar si convertible a un numero o no
        
    Return:
        True    :    si el string es uno numerico
        False   :    no es un string numerico
    """
    try:
        float( str )
        return True
    except:
        return False


def isThisFileinRange(filename, startUTSeconds, endUTSeconds):
    """
    Esta funcion determina si un archivo de datos se encuentra o no dentro del rango de fecha especificado.
    
    Inputs:
        filename            :    nombre completo del archivo de datos en formato Jicamarca (.r)
        
        startUTSeconds      :    fecha inicial del rango seleccionado. La fecha esta dada en
                                 segundos contados desde 01/01/1970.
        endUTSeconds        :    fecha final del rango seleccionado. La fecha esta dada en
                                 segundos contados desde 01/01/1970.
    
    Return:
        Boolean    :    Retorna True si el archivo de datos contiene datos en el rango de
                        fecha especificado, de lo contrario retorna False.
    
    Excepciones:
        Si el archivo no existe o no puede ser abierto
        Si la cabecera no puede ser leida.
        
    """
    m_BasicHeader = BasicHeader()
    
    try:
        fp = open(filename,'rb')
    except:
        raise IOError, "The file %s can't be opened" %(filename)
    
    sts = m_BasicHeader.read(fp)
    fp.close()
    
    if not(sts):
        print "Skipping the file %s because it has not a valid header" %(filename)
        return 0
    
    if not ((startUTSeconds <= m_BasicHeader.utc) and (endUTSeconds > m_BasicHeader.utc)):
        return 0
    
    return 1

        
def getlastFileFromPath(path, ext):
    """
    Depura el fileList dejando solo los que cumplan el formato de "PYYYYDDDSSS.ext"
    al final de la depuracion devuelve el ultimo file de la lista que quedo.  
    
    Input: 
        fileList    :    lista conteniendo todos los files (sin path) que componen una determinada carpeta
        ext         :    extension de los files contenidos en una carpeta 
            
    Return:
        El ultimo file de una determinada carpeta, no se considera el path.
    """
    validFilelist = []
    fileList = os.listdir(path)
    
    # 0 1234 567 89A BCDE
    # H YYYY DDD SSS .ext
    
    for file in fileList:
        try:
            year = int(file[1:5])
            doy  = int(file[5:8])
        
            if (os.path.splitext(file)[-1].upper() != ext.upper()) : continue
        except:
            continue

        validFilelist.append(file)

    if validFilelist:
        validFilelist = sorted( validFilelist, key=str.lower )
        return validFilelist[-1]

    return None


class DataReader():
    
    def __init__(self):
        pass


class DataWriter():
    
    def __init__(self):
        pass
    
    
class JRODataReader(DataReader):
    
    """
    Esta clase es usada como la clase padre de las clases DataReader,
    contiene todos lo metodos necesarios para leer datos desde archivos en formato
    jicamarca o pdata (.r o .pdata). La lectura de los datos siempre se realiza por bloques. Los datos
    leidos son array de 3 dimensiones:

                      Para Voltajes  -  perfiles * alturas * canales  
                                        
                      Para Spectra   -  paresCanalesIguales    * alturas * perfiles  (Self Spectra)
                                        paresCanalesDiferentes * alturas * perfiles  (Cross Spectra)
                                        canales * alturas                            (DC Channels)
        
    y son almacenados en su buffer respectivo.
     
    Esta clase contiene instancias (objetos) de las clases BasicHeader, SystemHeader, 
    RadarControllerHeader y DataObj. Los tres primeros se usan para almacenar informacion de la
    cabecera de datos (metadata), y el cuarto (DataObj) para obtener y almacenar los datos desde
    el buffer cada vez que se ejecute el metodo "getData".
    """
    
    m_BasicHeader = BasicHeader()
    
    m_SystemHeader = SystemHeader()
    
    m_RadarControllerHeader = RadarControllerHeader()
    
    m_ProcessingHeader = ProcessingHeader()
    
    m_DataObj = None
    
    heightList = None
    
    online = 0
    
    fp = None
    
    fileSizeByHeader = None
    
    filenameList = []
    
    filename = None
    
    fileSize = None
    
    firstHeaderSize = 0
    
    basicHeaderSize = 24
    
    dataType = None
    
    maxTimeStep = 30
        
    flagNoMoreFiles = 0
    
    set = 0
    
    ext = None
    
    path = None
    
    delay  = 3   #seconds
    
    nTries  = 3  #quantity tries
    
    nFiles = 3   #number of files for searching
    
    nBlocks = 0
    
    flagIsNewFile = 1

    ippSeconds = 0

    flagResetProcessing = 0    

    flagIsNewBlock = 0
    
    nReadBlocks = 0

    blocksize = 0

    datablockIndex = 9999
    
    
    #speed of light
    c = 3E8
    
    def __init__(self, m_DataObj=None):
        raise ValueError, "This class can't be instanced"




    
    def hasNotDataInBuffer(self):
        raise ValueError, "Not implemented"


    def readBlock(self):
        raise ValueError, "This method has not been implemented"

    def getData( self ):
        raise ValueError, "This method has not been implemented"
    
    def __rdSystemHeader(self, fp=None):
        
        if fp == None:
            fp = self.fp
            
        self.m_SystemHeader.read(fp)

    
    def __rdRadarControllerHeader(self, fp=None):
        if fp == None:
            fp = self.fp
            
        self.m_RadarControllerHeader.read(fp)

        
    def __rdProcessingHeader(self, fp=None):
        if fp == None:
            fp = self.fp
            
        self.m_ProcessingHeader.read(fp)


    def __rdBasicHeader(self, fp=None):
        
        if fp == None:
            fp = self.fp
            
        self.m_BasicHeader.read(fp)
    
    def getBlockDimension(self):
        raise ValueError, "No implemented"
       
    def __readFirstHeader(self):
        """ 
        Lectura del First Header, es decir el Basic Header y el Long Header
            
        Affected:
            self.m_BasicHeader
            self.m_SystemHeader
            self.m_RadarControllerHeader
            self.m_ProcessingHeader
            self.firstHeaderSize
            self.heightList
            self.dataType
            self.fileSizeByHeader
            self.ippSeconds
            
        Return: 
            None
        """
        self.__rdBasicHeader()
        self.__rdSystemHeader()
        self.__rdRadarControllerHeader()
        self.__rdProcessingHeader()
        self.firstHeaderSize = self.m_BasicHeader.size
        
        data_type=int(numpy.log2((self.m_ProcessingHeader.processFlags & PROCFLAG.DATATYPE_MASK))-numpy.log2(PROCFLAG.DATATYPE_CHAR))
        if data_type == 0:
            tmp = numpy.dtype([('real','<i1'),('imag','<i1')])
            
        elif data_type == 1:
            tmp = numpy.dtype([('real','<i2'),('imag','<i2')])
            
        elif data_type == 2:
            tmp = numpy.dtype([('real','<i4'),('imag','<i4')])
            
        elif data_type == 3:
            tmp = numpy.dtype([('real','<i8'),('imag','<i8')])
            
        elif data_type == 4:
            tmp = numpy.dtype([('real','<f4'),('imag','<f4')])
            
        elif data_type == 5:
            tmp = numpy.dtype([('real','<f8'),('imag','<f8')])
            
        else:
            raise ValueError, 'Data type was not defined'
        
        xi = self.m_ProcessingHeader.firstHeight
        step = self.m_ProcessingHeader.deltaHeight
        xf = xi + self.m_ProcessingHeader.numHeights*step
        
        self.heightList = numpy.arange(xi, xf, step)
        self.channelList = numpy.arange(self.m_SystemHeader.numChannels)
        self.dataType = tmp
        self.fileSizeByHeader = self.m_ProcessingHeader.dataBlocksPerFile * self.m_ProcessingHeader.blockSize + self.firstHeaderSize + self.basicHeaderSize*(self.m_ProcessingHeader.dataBlocksPerFile - 1)
        self.ippSeconds = 2 * 1000 * self.m_RadarControllerHeader.ipp / self.c
        
        self.getBlockDimension()


    def __setNextFileOnline(self):
        """
        Busca el siguiente file que tenga suficiente data para ser leida, dentro de un folder especifico, si
        no encuentra un file valido espera un tiempo determinado y luego busca en los posibles n files
        siguientes.   
            
        Affected: 
            self.flagIsNewFile
            self.filename
            self.fileSize
            self.fp
            self.set
            self.flagNoMoreFiles

        Return: 
            0    : si luego de una busqueda del siguiente file valido este no pudo ser encontrado
            1    : si el file fue abierto con exito y esta listo a ser leido
        
        Excepciones: 
            Si un determinado file no puede ser abierto
        """
        nFiles = 0
        fileOk_flag = False        
        firstTime_flag = True

        self.set += 1
        
        #busca el 1er file disponible
        file, filename = checkForRealPath( self.path, self.year, self.doy, self.set, self.ext )
        if file:
            if self.__verifyFile(file, False):
                fileOk_flag = True

        #si no encuentra un file entonces espera y vuelve a buscar
        if not(fileOk_flag): 
            for nFiles in range(self.nFiles+1): #busco en los siguientes self.nFiles+1 files posibles

                if firstTime_flag: #si es la 1era vez entonces hace el for self.nTries veces  
                    tries = self.nTries
                else:
                    tries = 1 #si no es la 1era vez entonces solo lo hace una vez
                    
                for nTries in range( tries ): 
                    if firstTime_flag:
                        print "\tWaiting %0.2f sec for new \"%s\" file, try %03d ..." % ( self.delay, filename, nTries+1 ) 
                        time.sleep( self.delay )
                    else:
                        print "\tSearching next \"%s%04d%03d%03d%s\" file ..." % (self.optchar, self.year, self.doy, self.set, self.ext)
                    
                    file, filename = checkForRealPath( self.path, self.year, self.doy, self.set, self.ext )
                    if file:
                        if self.__verifyFile(file):
                            fileOk_flag = True
                            break
                    
                if fileOk_flag:
                    break

                firstTime_flag = False

                print "\tSkipping the file \"%s\" due to this file doesn't exist yet" % filename
                self.set += 1
                    
                if nFiles == (self.nFiles-1): #si no encuentro el file buscado cambio de carpeta y busco en la siguiente carpeta
                    self.set = 0
                    self.doy += 1

        if fileOk_flag:
            self.fileSize = os.path.getsize( file )
            self.filename = file
            self.flagIsNewFile = 1
            if self.fp != None: self.fp.close() 
            self.fp = open(file)
            self.flagNoMoreFiles = 0
            print 'Setting the file: %s' % file
        else:
            self.fileSize = 0
            self.filename = None
            self.flagIsNewFile = 0
            self.fp = None
            self.flagNoMoreFiles = 1
            print 'No more Files'

        return fileOk_flag


    def __setNextFileOffline(self):
        """ 
        Busca el siguiente file dentro de un folder que tenga suficiente data para ser leida
            
        Affected: 
            self.flagIsNewFile
            self.fileIndex
            self.filename
            self.fileSize
            self.fp

        Return: 
            0    : si un determinado file no puede ser abierto
            1    : si el file fue abierto con exito 
        
        Excepciones: 
            Si un determinado file no puede ser abierto
        """
        idFile = self.fileIndex
        while(True):
            
            idFile += 1
            
            if not(idFile < len(self.filenameList)):
                self.flagNoMoreFiles = 1
                print 'No more Files'
                return 0
            
            filename = self.filenameList[idFile]
            fileSize = os.path.getsize(filename)
            
            try:
                fp = open(filename,'rb')
            except:
                raise IOError, "The file %s can't be opened" %filename
            
            currentSize = fileSize - fp.tell()
            neededSize = self.m_ProcessingHeader.blockSize + self.firstHeaderSize
            
            if (currentSize < neededSize):
                print "Skipping the file %s due to it hasn't enough data" %filename
                continue
            
            break
        
        self.flagIsNewFile = 1
        self.fileIndex = idFile
        self.filename = filename
        self.fileSize = fileSize
        self.fp = fp
        
        print 'Setting the file: %s'%self.filename
        
        return 1
    

    def setNextFile(self):
        """ 
        Determina el siguiente file a leer y si hay uno disponible lee el First Header
            
        Affected: 
            self.m_BasicHeader
            self.m_SystemHeader
            self.m_RadarControllerHeader
            self.m_ProcessingHeader
            self.firstHeaderSize

        Return: 
            0    :    Si no hay files disponibles
            1    :    Si hay mas files disponibles
        """
        if self.fp != None:
            self.fp.close()

        if self.online:
            newFile = self.__setNextFileOnline()
        else:
            newFile = self.__setNextFileOffline()
        
        if self.flagNoMoreFiles:
            sys.exit(0)

        if not(newFile):
            return 0
        
        self.__readFirstHeader()
        self.nBlocks = 0
        return 1
        
    
    def __setNewBlock(self):
        """ 
        Lee el Basic Header y posiciona le file pointer en la posicion inicial del bloque a leer

        Affected: 
            self.m_BasicHeader
            self.flagNoContinuousBlock
            self.ns

        Return: 
            0    :    Si el file no tiene un Basic Header que pueda ser leido
            1    :    Si se pudo leer el Basic Header
        """
        if self.fp == None:
            return 0
        
        if self.flagIsNewFile:
            return 1
        
        currentSize = self.fileSize - self.fp.tell()
        neededSize = self.m_ProcessingHeader.blockSize + self.basicHeaderSize
        
        #If there is enough data setting new data block
        if ( currentSize >= neededSize ):
            self.__rdBasicHeader()
            return 1
        
        #si es OnLine y ademas aun no se han leido un bloque completo entonces se espera por uno valido
        elif (self.nBlocks != self.m_ProcessingHeader.dataBlocksPerFile) and self.online:
            for nTries in range( self.nTries ):

                fpointer = self.fp.tell()
                self.fp.close()

                print "\tWaiting %0.2f sec for the next block, try %03d ..." % (self.delay, nTries+1)
                time.sleep( self.delay )

                self.fp = open( self.filename, 'rb' )
                self.fp.seek( fpointer )

                self.fileSize = os.path.getsize( self.filename )
                currentSize = self.fileSize - self.fp.tell()
                neededSize = self.m_ProcessingHeader.blockSize + self.basicHeaderSize

                if ( currentSize >= neededSize ):
                    self.__rdBasicHeader()
                    return 1
                
        #Setting new file 
        if not( self.setNextFile() ):
            return 0
        
        deltaTime = self.m_BasicHeader.utc - self.lastUTTime # check this
        
        self.flagResetProcessing = 0
        
        if deltaTime > self.maxTimeStep:
            self.flagResetProcessing = 1
            #self.nReadBlocks = 0
            
        return 1

    
    def __searchFilesOnLine(self, path, startDateTime=None, endDateTime=None, expLabel = "", ext = None):
        """
        Busca el ultimo archivo de la ultima carpeta (determinada o no por startDateTime) y
        devuelve el archivo encontrado ademas de otros datos.
        
        Input: 
            path             :    carpeta donde estan contenidos los files que contiene data  
            startDateTime    :    punto especifico en el tiempo del cual se requiere la data
            ext              :    extension de los files  

        Return:
            year        :    el anho
            doy         :    el numero de dia del anho
            set         :    el set del archivo
            filename    :    el ultimo file de una determinada carpeta
            directory   :    eL directorio donde esta el file encontrado
        """
        dirList = []
        pathList = []
        directory = None
        
        for thisPath in os.listdir(path):
            if os.path.isdir(os.path.join(path,thisPath)):
                dirList.append(thisPath)

        if not(dirList):
            return None, None, None, None, None

        dirList = sorted( dirList, key=str.lower )

        if startDateTime:
            thisDateTime = startDateTime
            if endDateTime == None: endDateTime = startDateTime
            
            while(thisDateTime <= endDateTime):
                year = thisDateTime.timetuple().tm_year
                doy = thisDateTime.timetuple().tm_yday
                
                match = fnmatch.filter(dirList, '?' + '%4.4d%3.3d' % (year,doy))
                if len(match) == 0:
                    thisDateTime += datetime.timedelta(1)
                    continue
                
                pathList.append(os.path.join(path,match[0], expLabel))
                thisDateTime += datetime.timedelta(1)

            if not(pathList):
                print "\tNo files in range: %s - %s" %(startDateTime.ctime(), endDateTime.ctime())
                return None, None, None, None, None

            directory = pathList[0]
            
        else:
            directory = dirList[-1]
            directory = os.path.join(path,directory)

        filename = getlastFileFromPath(directory, ext)

        if not(filename):
            return None, None, None, None, None

        if not(self.__verifyFile(os.path.join(directory, filename))):
            return None, None, None, None, None

        year = int( filename[1:5] )
        doy  = int( filename[5:8] )
        set  = int( filename[8:11] )        
        
        return directory, filename, year, doy, set


    def __searchFilesOffLine(self, path, startDateTime, endDateTime, set=None, expLabel = "", ext = ".r"):
        """
        Realiza una busqueda de los archivos que coincidan con los parametros
        especificados y se encuentren ubicados en el path indicado. Para realizar una busqueda
        correcta la estructura de directorios debe ser la siguiente:
        
        ...path/D[yyyy][ddd]/expLabel/D[yyyy][ddd][sss].ext
        
        [yyyy]: anio
        [ddd] : dia del anio
        [sss] : set del archivo        
        
        Inputs:
            path           :    Directorio de datos donde se realizara la busqueda. Todos los
                                ficheros que concidan con el criterio de busqueda seran
                                almacenados en una lista y luego retornados.
            startDateTime  :    Fecha inicial. Rechaza todos los archivos donde 
                                file end time < startDateTime (obejto datetime.datetime)
                                                         
            endDateTime    :    Fecha final. Rechaza todos los archivos donde 
                                file start time > endDateTime (obejto datetime.datetime)
            
            set            :    Set del primer archivo a leer. Por defecto None
            
            expLabel       :    Nombre del subdirectorio de datos.  Por defecto ""
            
            ext            :    Extension de los archivos a leer. Por defecto .r
            
        Return:
            
            (pathList, filenameList)
            
            pathList        :    Lista de directorios donde se encontraron archivos dentro 
                                 de los parametros especificados
            filenameList    :    Lista de archivos (ruta completa) que coincidieron con los
                                 parametros especificados.
        
        Variables afectadas:
        
            self.filenameList:    Lista de archivos (ruta completa) que la clase utiliza
                                  como fuente para leer los bloque de datos, si se termina
                                  de leer todos los bloques de datos de un determinado 
                                  archivo se pasa al siguiente archivo de la lista.
             
        Excepciones:
        
        """
        
        print "Searching files ..."
        
        dirList = []
        for thisPath in os.listdir(path):
            if os.path.isdir(os.path.join(path,thisPath)):
                dirList.append(thisPath)

        if not(dirList):
            return None, None

        pathList = []
        
        thisDateTime = startDateTime
        
        while(thisDateTime <= endDateTime):
            year = thisDateTime.timetuple().tm_year
            doy = thisDateTime.timetuple().tm_yday
            
            match = fnmatch.filter(dirList, '?' + '%4.4d%3.3d' % (year,doy))
            if len(match) == 0:
                thisDateTime += datetime.timedelta(1)
                continue
            
            pathList.append(os.path.join(path,match[0],expLabel))
            thisDateTime += datetime.timedelta(1)
        
        startUtSeconds = time.mktime(startDateTime.timetuple())
        endUtSeconds = time.mktime(endDateTime.timetuple())
        
        filenameList = []
        for thisPath in pathList:
            fileList = glob.glob1(thisPath, "*%s" %ext)
            fileList.sort()
            for file in fileList:
                filename = os.path.join(thisPath,file)
                if isThisFileinRange(filename, startUtSeconds, endUtSeconds):
                    filenameList.append(filename)
                    
        if not(filenameList):
            return None, None

        self.filenameList = filenameList
        
        return pathList, filenameList


    def __verifyFile(self, filename, msgFlag=True):
        """
        Verifica que el filename tenga data valida, para ello leo el FirstHeader del file 
        
        Return:
            0    :    file no valido para ser leido
            1    :    file valido para ser leido
        """
        m_BasicHeader = BasicHeader()
        m_SystemHeader = SystemHeader()
        m_RadarControllerHeader = RadarControllerHeader()
        m_ProcessingHeader = ProcessingHeader()
        flagFileOK = False
        
        try:
            fp = open( filename,'rb' ) #lectura binaria
        except:
            if msgFlag:
                print "The file %s can't be opened" % (filename)
        
        try:
            if not( m_BasicHeader.read(fp) ): raise ValueError 
            if not( m_SystemHeader.read(fp) ): raise ValueError
            if not( m_RadarControllerHeader.read(fp) ): raise ValueError
            if not( m_ProcessingHeader.read(fp) ): raise ValueError
            data_type = int(numpy.log2((m_ProcessingHeader.processFlags & PROCFLAG.DATATYPE_MASK))-numpy.log2(PROCFLAG.DATATYPE_CHAR))
            if m_BasicHeader.size > self.basicHeaderSize:
                flagFileOK = True
        except:
            if msgFlag:
                print "\tThe file %s is empty or it hasn't enough data" % filename
        
        fp.close()
        
        if not(flagFileOK):
            return 0
        
        return 1

    
    def setup(self, path, startDateTime=None, endDateTime=None, set=0, expLabel = "", ext = None, online = 0):
        """
        setup configura los parametros de lectura de la clase DataReader.
        
        Si el modo de lectura es offline, primero se realiza una busqueda de todos los archivos
        que coincidan con los parametros especificados; esta lista de archivos son almacenados en
        self.filenameList.
        
        Input:
            path                :    Directorios donde se ubican los datos a leer. Dentro de este
                                     directorio deberia de estar subdirectorios de la forma:
                                     
                                     path/D[yyyy][ddd]/expLabel/P[yyyy][ddd][sss][ext]
            
            startDateTime       :    Fecha inicial. Rechaza todos los archivos donde
                                     file end time < startDatetime (obejto datetime.datetime)
            
            endDateTime         :    Fecha final. Si no es None, rechaza todos los archivos donde
                                     file end time < startDatetime (obejto datetime.datetime)
            
            set                 :    Set del primer archivo a leer. Por defecto None
            
            expLabel            :    Nombre del subdirectorio de datos.  Por defecto ""
            
            ext                 :    Extension de los archivos a leer. Por defecto .r
            
            online              :    Si es == a 0 entonces busca files que cumplan con las condiciones dadas
            
        Return:
            0    :    Si no encuentra files que cumplan con las condiciones dadas
            1    :    Si encuentra files que cumplan con las condiciones dadas
        
        Affected:
            self.startUTCSeconds
            self.endUTCSeconds
            self.startYear 
            self.endYear
            self.startDoy
            self.endDoy
            self.pathList
            self.filenameList 
            self.online
        """
        
        if ext == None:
            ext = self.ext
            
        if online:
            print "Searching files ..."  
            doypath, file, year, doy, set = self.__searchFilesOnLine(path, startDateTime, endDateTime, expLabel, ext)        

            if not(doypath):
                for nTries in range( self.nTries ):
                    print '\tWaiting %0.2f sec for valid file in %s: try %02d ...' % (self.delay, path, nTries+1)
                    time.sleep( self.delay )
                    doypath, file, year, doy, set = self.__searchFilesOnLine(path, startDateTime, endDateTime, expLabel, ext)        
                    if doypath:
                        break
            
            if not(doypath):
                print "There 'isn't valied files in %s" % path
                return 0
        
            self.year = year
            self.doy  = doy
            self.set  = set - 1
            self.path = path

        else: # offline
            pathList, filenameList = self.__searchFilesOffLine(path, startDateTime, endDateTime, set, expLabel, ext)
            if not(pathList):
                print "No files in range: %s - %s" %(startDateTime.ctime(), endDateTime.ctime())
                return 0

            self.fileIndex = -1 
            self.pathList = pathList
            self.filenameList = filenameList
             
        self.online = online
        self.ext = ext

        ext = ext.lower()

        if not( self.setNextFile() ):
            if (startDateTime != None) and (endDateTime != None):
                print "No files in range: %s - %s" %(startDateTime.ctime(), endDateTime.ctime())
            elif startDateTime != None:
                print "No files in : %s" % startDateTime.ctime()
            else:
                print "No files"
            return 0
        
        if startDateTime != None:
            self.startUTCSeconds = time.mktime(startDateTime.timetuple())
            self.startYear = startDateTime.timetuple().tm_year 
            self.startDoy = startDateTime.timetuple().tm_yday
        
        if endDateTime != None:
            self.endUTCSeconds = time.mktime(endDateTime.timetuple())
            self.endYear = endDateTime.timetuple().tm_year
            self.endDoy = endDateTime.timetuple().tm_yday
        #call fillHeaderValues() - to Data Object
        
        self.m_DataObj.m_BasicHeader = self.m_BasicHeader.copy()
        self.m_DataObj.m_ProcessingHeader = self.m_ProcessingHeader.copy()
        self.m_DataObj.m_RadarControllerHeader = self.m_RadarControllerHeader.copy()
        self.m_DataObj.m_SystemHeader = self.m_SystemHeader.copy()
        self.m_DataObj.dataType = self.dataType
            
        return 1 

    
    def readNextBlock(self):
        """ 
        Establece un nuevo bloque de datos a leer y los lee, si es que no existiese
        mas bloques disponibles en el archivo actual salta al siguiente.

        Affected: 
            self.lastUTTime

        Return: None
        """
        if not(self.__setNewBlock()):
            return 0
        
        if not(self.readBlock()):
            return 0
        
        self.lastUTTime = self.m_BasicHeader.utc
        
        return 1


class JRODataWriter(DataWriter):

    """ 
    Esta clase permite escribir datos a archivos procesados (.r o ,pdata). La escritura
    de los datos siempre se realiza por bloques. 
    """
    
    m_BasicHeader = BasicHeader()
    
    m_SystemHeader = SystemHeader()
    
    m_RadarControllerHeader = RadarControllerHeader()
    
    m_ProcessingHeader = ProcessingHeader()
    
    fp = None
    
    blocksCounter = 0
    
    flagIsNewFile = 1
    
    nWriteBlocks = 0 
    
    flagIsNewBlock = 0
    
    flagNoMoreFiles = 0

    m_DataObj = None

    fp = None
        
    blocksCounter = 0
        
    flagIsNewFile = 1
        
    nWriteBlocks = 0 
        
    flagIsNewBlock = 0
        
    flagNoMoreFiles = 0

    setFile = None
        
    dataType = None
        
    path = None
        
    noMoreFiles = 0
        
    filename = None
        
    m_BasicHeader = None
    
    m_SystemHeader = None
    
    m_RadarControllerHeader = None
    
    m_ProcessingHeader = None

    
    def __init__(self, m_DataObj=None):
        raise ValueError, "Not implemented"


    def hasAllDataInBuffer(self):
        raise ValueError, "Not implemented"


    def setBlockDimension(self):
        raise ValueError, "Not implemented"

    
    def writeBlock(self):
        raise ValueError, "No implemented"


    def putData(self):
        raise ValueError, "No implemented"

    
    def __writeFirstHeader(self):
        """
        Escribe el primer header del file es decir el Basic header y el Long header (SystemHeader, RadarControllerHeader, ProcessingHeader)
        
        Affected:
            __dataType
            
        Return:
            None
        """
        self.__writeBasicHeader()
        self.__wrSystemHeader()
        self.__wrRadarControllerHeader()
        self.__wrProcessingHeader()
        self.dataType = self.m_DataObj.dataType
            
            
    def __writeBasicHeader(self, fp=None):
        """
        Escribe solo el Basic header en el file creado

        Return:
            None
        """
        if fp == None:
            fp = self.fp
            
        self.m_DataObj.m_BasicHeader.write(fp)

    
    def __wrSystemHeader(self, fp=None):
        """
        Escribe solo el System header en el file creado

        Return:
            None
        """
        if fp == None:
            fp = self.fp
            
        self.m_DataObj.m_SystemHeader.write(fp)

    
    def __wrRadarControllerHeader(self, fp=None):
        """
        Escribe solo el RadarController header en el file creado

        Return:
            None
        """
        if fp == None:
            fp = self.fp
        
        self.m_DataObj.m_RadarControllerHeader.write(fp)

        
    def __wrProcessingHeader(self, fp=None):
        """
        Escribe solo el Processing header en el file creado

        Return:
            None
        """
        if fp == None:
            fp = self.fp
            
        self.m_DataObj.m_ProcessingHeader.write(fp)
    
    
    def setNextFile(self):
        """ 
        Determina el siguiente file que sera escrito

        Affected: 
            self.filename
            self.subfolder
            self.fp
            self.setFile
            self.flagIsNewFile

        Return:
            0    :    Si el archivo no puede ser escrito
            1    :    Si el archivo esta listo para ser escrito
        """
        ext = self.ext
        path = self.path
        
        if self.fp != None:
            self.fp.close()
        
        timeTuple = time.localtime( self.m_DataObj.m_BasicHeader.utc )
        subfolder = 'D%4.4d%3.3d' % (timeTuple.tm_year,timeTuple.tm_yday)

        tmp = os.path.join( path, subfolder )
        if not( os.path.exists(tmp) ):
            os.mkdir(tmp)
            self.setFile = -1 #inicializo mi contador de seteo
        else:
            filesList = os.listdir( tmp )
            if len( filesList ) > 0:
                filesList = sorted( filesList, key=str.lower )
                filen = filesList[-1]
                # el filename debera tener el siguiente formato
                # 0 1234 567 89A BCDE (hex)
                # x YYYY DDD SSS .ext
                if isNumber( filen[8:11] ):
                    self.setFile = int( filen[8:11] ) #inicializo mi contador de seteo al seteo del ultimo file
                else:    
                    self.setFile = -1
            else:
                self.setFile = -1 #inicializo mi contador de seteo
                
        setFile = self.setFile
        setFile += 1
                
        file = '%s%4.4d%3.3d%3.3d%s' % (self.optchar,
                                        timeTuple.tm_year,
                                        timeTuple.tm_yday,
                                        setFile,
                                        ext )

        filename = os.path.join( path, subfolder, file )

        fp = open( filename,'wb' )
        
        self.blocksCounter = 0
        
        #guardando atributos 
        self.filename = filename
        self.subfolder = subfolder
        self.fp = fp
        self.setFile = setFile
        self.flagIsNewFile = 1
        
        print 'Writing the file: %s'%self.filename
        
        self.__writeFirstHeader()
        
        return 1


    def __setNewBlock(self):
        """
        Si es un nuevo file escribe el First Header caso contrario escribe solo el Basic Header
        
        Return:
            0    :    si no pudo escribir nada
            1    :    Si escribio el Basic el First Header
        """        
        if self.fp == None:
            self.setNextFile()
        
        if self.flagIsNewFile:
            return 1
        
        if self.blocksCounter < self.m_ProcessingHeader.dataBlocksPerFile:
            self.__writeBasicHeader()
            return 1
        
        if not( self.setNextFile() ):
            return 0
        
        return 1


    def writeNextBlock(self):
        """
        Selecciona el bloque siguiente de datos y los escribe en un file
            
        Return: 
            0    :    Si no hizo pudo escribir el bloque de datos 
            1    :    Si no pudo escribir el bloque de datos
        """
        if not( self.__setNewBlock() ):
            return 0
        
        self.writeBlock()

        return 1
    

    def getHeader(self):
        """
        Obtiene una copia del First Header
         
        Affected:
            self.m_BasicHeader
            self.m_SystemHeader
            self.m_RadarControllerHeader
            self.m_ProcessingHeader
            self.dataType

        Return: 
            None
        """
        self.m_BasicHeader = self.m_DataObj.m_BasicHeader.copy()
        self.m_SystemHeader = self.m_DataObj.m_SystemHeader.copy()
        self.m_RadarControllerHeader = self.m_DataObj.m_RadarControllerHeader.copy()
        self.m_ProcessingHeader = self.m_DataObj.m_ProcessingHeader.copy()
        self.dataType = self.m_DataObj.dataType
    
    
    def setup(self, path, set=0, ext=None):
        """
        Setea el tipo de formato en la cual sera guardada la data y escribe el First Header 
            
        Inputs:
            path      :    el path destino en el cual se escribiran los files a crear
            format    :    formato en el cual sera salvado un file
            set       :    el setebo del file
            
        Return:
            0    :    Si no realizo un buen seteo
            1    :    Si realizo un buen seteo 
        """
        
        if ext == None:
            ext = self.ext
        
        ext = ext.lower()

        self.path = path
        self.setFile = set - 1
        self.ext = ext
        #self.format = format
        self.getHeader()

        self.setBlockDimension()
        
        if not( self.setNextFile() ):
            print "There isn't a next file"
            return 0

        return 1
