#!/usr/bin/env python
'''
Created on Jul 7, 2014

@author: roj-idl71
'''
import os, sys

from schainpy.controller import Project

if __name__ == '__main__':
    desc = "Segundo Test"

    controllerObj = Project()
    controllerObj.setup(id='191', name='test01', description=desc)

    proc1 = controllerObj.addProcUnit(name='ReceiverData')
    proc1.addParameter(name='realtime', value='0', format='bool')
    proc1.addParameter(name='plottypes', value='snr', format='str')
    proc1.addParameter(name='throttle', value='5', format='int')
    proc1.addParameter(name='interactive', value='0', format='bool')
    # proc1.addParameter(name='server', value='tcp://10.10.10.82:7000', format='str')
    ## TODO Agregar direccion de server de publicacion a graficos como variable
    op3 = proc1.addOperation(name='PlotSNRData', optype='other')
    op3.addParameter(name='wintitle', value='Julia 150Km', format='str')
    op3.addParameter(name='zmax', value='30', format='int')
    op3.addParameter(name='zmin', value='-10', format='int')
    op3.addParameter(name='save', value='/home/nanosat/Pictures', format='str')
    op3.addParameter(name='show', value='0', format='bool')
    # #
    # op4 = proc1.addOperation(name='PlotDOPData', optype='other')
    # op4.addParameter(name='wintitle', value='Julia 150Km', format='str')
    # op4.addParameter(name='save', value='/home/nanosat/Pictures', format='str')
    # op4.addParameter(name='show', value='0', format='bool')
    # op4.addParameter(name='colormap', value='jet', format='str')

    # op1 = proc1.addOperation(name='PlotRTIData', optype='other')
    # op1.addParameter(name='wintitle', value='Julia 150Km', format='str')
    # op1.addParameter(name='save', value='/home/nanosat/Pictures', format='str')
    # op1.addParameter(name='show', value='0', format='bool')
    # op1.addParameter(name='colormap', value='jet', format='str')
    # #
    # op2 = proc1.addOperation(name='PlotCOHData', optype='other')
    # op2.addParameter(name='wintitle', value='Julia 150Km', format='str')
    # op2.addParameter(name='save', value='/home/nanosat/Pictures', format='str')
    # op2.addParameter(name='colormap', value='jet', format='str')
    # op2.addParameter(name='show', value='0', format='bool')
    # # # #
    # op6 = proc1.addOperation(name='PlotPHASEData', optype='other')
    # op6.addParameter(name='wintitle', value='Julia 150Km', format='str')
    # op6.addParameter(name='save', value='/home/nanosat/Pictures', format='str')
    # op6.addParameter(name='show', value='1', format='bool')
    # #
    # # proc2 = controllerObj.addProcUnit(name='ReceiverData')
    # # proc2.addParameter(name='server', value='juanca', format='str')
    # # proc2.addParameter(name='plottypes', value='snr,dop', format='str')
    # #



    controllerObj.start()
