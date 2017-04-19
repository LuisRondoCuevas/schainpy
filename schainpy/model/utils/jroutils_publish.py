'''
@author: Juan C. Espinoza
'''

import time
import json
import numpy
import paho.mqtt.client as mqtt
import zmq
import cPickle as pickle
import datetime
from zmq.utils.monitor import recv_monitor_message
from functools import wraps
from threading import Thread
from multiprocessing import Process

from schainpy.model.proc.jroproc_base import Operation, ProcessingUnit

throttle_value = 10

class PrettyFloat(float):
    def __repr__(self):
        return '%.2f' % self

def roundFloats(obj):
    if isinstance(obj, list):
        return map(roundFloats, obj)
    elif isinstance(obj, float):
        return round(obj, 2)

def pretty_floats(obj):
    if isinstance(obj, float):
        return PrettyFloat(obj)
    elif isinstance(obj, dict):
        return dict((k, pretty_floats(v)) for k, v in obj.items())
    elif isinstance(obj, (list, tuple)):
        return map(pretty_floats, obj)
    return obj

class throttle(object):
    """Decorator that prevents a function from being called more than once every
    time period.
    To create a function that cannot be called more than once a minute, but
    will sleep until it can be called:
    @throttle(minutes=1)
    def foo():
      pass

    for i in range(10):
      foo()
      print "This function has run %s times." % i
    """

    def __init__(self, seconds=0, minutes=0, hours=0):
        self.throttle_period = datetime.timedelta(
            seconds=seconds, minutes=minutes, hours=hours
        )
        self.time_of_last_call = datetime.datetime.min

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            now = datetime.datetime.now()
            time_since_last_call = now - self.time_of_last_call
            time_left = self.throttle_period - time_since_last_call

            if time_left > datetime.timedelta(seconds=0):
                return

            self.time_of_last_call = datetime.datetime.now()
            return fn(*args, **kwargs)

        return wrapper


class PublishData(Operation):
    """Clase publish."""

    __MAXNUMX = 100
    __MAXNUMY = 100

    def __init__(self, **kwargs):
        """Inicio."""
        Operation.__init__(self, **kwargs)
        self.isConfig = False
        self.client = None
        self.zeromq = None
        self.mqtt = None

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")
        self.connect()

    def connect(self):
        print 'trying to connect'
        try:
            self.client.connect(
                host=self.host,
                port=self.port,
                keepalive=60*10,
                bind_address='')
            print "connected"
            self.client.loop_start()
            # self.client.publish(
            #     self.topic + 'SETUP',
            #     json.dumps(setup),
            #     retain=True
            #     )
        except:
            print "MQTT Conection error."
            self.client = False

    def setup(self, port=1883, username=None, password=None, clientId="user", zeromq=1, **kwargs):
        self.counter = 0
        self.topic = kwargs.get('topic', 'schain')
        self.delay = kwargs.get('delay', 0)
        self.plottype = kwargs.get('plottype', 'spectra')
        self.host = kwargs.get('host', "10.10.10.82")
        self.port = kwargs.get('port', 3000)
        self.clientId = clientId
        self.cnt = 0
        self.zeromq = zeromq
        self.mqtt = kwargs.get('plottype', 0)
        self.client = None
        setup = []
        if mqtt is 1:
            print 'mqqt es 1'
            self.client = mqtt.Client(
                client_id=self.clientId + self.topic + 'SCHAIN',
                clean_session=True)
            self.client.on_disconnect = self.on_disconnect
            self.connect()
            for plot in self.plottype:
                setup.append({
                    'plot': plot,
                    'topic': self.topic + plot,
                    'title': getattr(self, plot + '_' + 'title', False),
                    'xlabel': getattr(self, plot + '_' + 'xlabel', False),
                    'ylabel': getattr(self, plot + '_' + 'ylabel', False),
                    'xrange': getattr(self, plot + '_' + 'xrange', False),
                    'yrange': getattr(self, plot + '_' + 'yrange', False),
                    'zrange': getattr(self, plot + '_' + 'zrange', False),
                })
        if zeromq is 1:
            context = zmq.Context()
            self.zmq_socket = context.socket(zmq.PUSH)
            server = kwargs.get('server', 'zmq.pipe')
            
            if 'http://' in server:
                address = server
            else:
                address = 'ipc:///tmp/%s' % server
            
            self.zmq_socket.connect(address)
            time.sleep(1)
            print 'zeromq configured'


    def publish_data(self):
        self.dataOut.finished = False
        if self.mqtt is 1:
            yData = self.dataOut.heightList[:2].tolist()
            if self.plottype == 'spectra':
                data = getattr(self.dataOut, 'data_spc')
                z = data/self.dataOut.normFactor
                zdB = 10*numpy.log10(z)
                xlen, ylen = zdB[0].shape
                dx = numpy.floor(xlen/self.__MAXNUMX) + 1
                dy = numpy.floor(ylen/self.__MAXNUMY) + 1
                Z = [0 for i in self.dataOut.channelList]
                for i in self.dataOut.channelList:
                    Z[i] = zdB[i][::dx, ::dy].tolist()
                payload = {
                    'timestamp': self.dataOut.utctime,
                    'data': roundFloats(Z),
                    'channels': ['Ch %s' % ch for ch in self.dataOut.channelList],
                    'interval': self.dataOut.getTimeInterval(),
                    'type': self.plottype,
                    'yData': yData
                }
                # print payload

            elif self.plottype in ('rti', 'power'):
                data = getattr(self.dataOut, 'data_spc')
                z = data/self.dataOut.normFactor
                avg = numpy.average(z, axis=1)
                avgdB = 10*numpy.log10(avg)
                xlen, ylen = z[0].shape
                dy = numpy.floor(ylen/self.__MAXNUMY) + 1
                AVG = [0 for i in self.dataOut.channelList]
                for i in self.dataOut.channelList:
                    AVG[i] = avgdB[i][::dy].tolist()
                payload = {
                    'timestamp': self.dataOut.utctime,
                    'data': roundFloats(AVG),
                    'channels': ['Ch %s' % ch for ch in self.dataOut.channelList],
                    'interval': self.dataOut.getTimeInterval(),
                    'type': self.plottype,
                    'yData': yData
                }
            elif self.plottype == 'noise':
                noise = self.dataOut.getNoise()/self.dataOut.normFactor
                noisedB = 10*numpy.log10(noise)
                payload = {
                    'timestamp': self.dataOut.utctime,
                    'data': roundFloats(noisedB.reshape(-1, 1).tolist()),
                    'channels': ['Ch %s' % ch for ch in self.dataOut.channelList],
                    'interval': self.dataOut.getTimeInterval(),
                    'type': self.plottype,
                    'yData': yData
                }
            elif self.plottype == 'snr':
                data = getattr(self.dataOut, 'data_SNR')
                avgdB = 10*numpy.log10(data)

                ylen = data[0].size
                dy = numpy.floor(ylen/self.__MAXNUMY) + 1
                AVG = [0 for i in self.dataOut.channelList]
                for i in self.dataOut.channelList:
                    AVG[i] = avgdB[i][::dy].tolist()
                payload = {
                    'timestamp': self.dataOut.utctime,
                    'data': roundFloats(AVG),
                    'channels': ['Ch %s' % ch for ch in self.dataOut.channelList],
                    'type': self.plottype,
                    'yData': yData
                }
            else:
                print "Tipo de grafico invalido"
                payload = {
                    'data': 'None',
                    'timestamp': 'None',
                    'type': None
                }
                # print 'Publishing data to {}'.format(self.host)
            self.client.publish(self.topic + self.plottype, json.dumps(payload), qos=0)

        if self.zeromq is 1:
            print '[Sending] {} - {}'.format(self.dataOut.type, self.dataOut.datatime) 
            self.zmq_socket.send_pyobj(self.dataOut)

    def run(self, dataOut, **kwargs):
        self.dataOut = dataOut
        if not self.isConfig:
            self.setup(**kwargs)
            self.isConfig = True

        self.publish_data()
        time.sleep(self.delay)

    def close(self):
        if self.zeromq is 1:
            self.dataOut.finished = True
            self.zmq_socket.send_pyobj(self.dataOut)

        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
