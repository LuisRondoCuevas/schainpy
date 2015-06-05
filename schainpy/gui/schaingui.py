#!/usr/bin/env python
import os, sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication

from schainpy.gui.viewcontroller.initwindow import InitWindow
from schainpy.gui.viewcontroller.basicwindow import BasicWindow
from schainpy.gui.viewcontroller.workspace import Workspace

def main():
    
    app = QtGui.QApplication(sys.argv)
    
    Welcome=InitWindow()
    
    if not Welcome.exec_(): 
        sys.exit(-1) 

    WorkPathspace=Workspace()
    if not WorkPathspace.exec_(): 
        sys.exit(-1)
          
    MainGUI=BasicWindow()
    MainGUI.setWorkSpaceGUI(WorkPathspace.dirComBox.currentText())  
    MainGUI.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()