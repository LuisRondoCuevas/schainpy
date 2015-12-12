
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
    
class Ui_VoltageTab(object):
    
    def setupUi(self):
        
        self.tabVoltage = QtGui.QWidget()
        self.tabVoltage.setObjectName(_fromUtf8("tabVoltage"))
        
        self.gridLayout_3 = QtGui.QGridLayout(self.tabVoltage)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        
        self.frame_4 = QtGui.QFrame(self.tabVoltage)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        
        self.gridLayout_17 = QtGui.QGridLayout(self.frame_4)
        self.gridLayout_17.setObjectName(_fromUtf8("gridLayout_17"))
        self.volOpOk = QtGui.QPushButton(self.frame_4)
        self.volOpOk.setObjectName(_fromUtf8("volOpOk"))
        self.gridLayout_17.addWidget(self.volOpOk, 0, 0, 1, 1)
        self.volGraphClear = QtGui.QPushButton(self.frame_4)
        self.volGraphClear.setObjectName(_fromUtf8("volGraphClear"))
        self.gridLayout_17.addWidget(self.volGraphClear, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.frame_4, 1, 1, 1, 1)
        
        
        self.tabWidgetVoltage = QtGui.QTabWidget(self.tabVoltage)
        self.tabWidgetVoltage.setObjectName(_fromUtf8("tabWidgetVoltage"))
        self.tabopVoltage = QtGui.QWidget()
        self.tabopVoltage.setObjectName(_fromUtf8("tabopVoltage"))
        self.gridLayout = QtGui.QGridLayout(self.tabopVoltage)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        
        self.volOpCebRadarfrequency = QtGui.QCheckBox(self.tabopVoltage)
        self.volOpCebRadarfrequency.setObjectName(_fromUtf8("volOpCebRadarfrequency"))
        self.gridLayout.addWidget(self.volOpCebRadarfrequency, 0, 0, 1, 1)
        
        self.volOpRadarfrequency = QtGui.QLineEdit(self.tabopVoltage)
        self.volOpRadarfrequency.setObjectName(_fromUtf8("volOpRadarfrequency"))
        self.gridLayout.addWidget(self.volOpRadarfrequency, 0, 1, 1, 4)
        
        self.volOpCebChannels = QtGui.QCheckBox(self.tabopVoltage)
        self.volOpCebChannels.setObjectName(_fromUtf8("volOpCebChannels"))
        self.gridLayout.addWidget(self.volOpCebChannels, 1, 0, 1, 1)
        
        self.volOpComChannels = QtGui.QComboBox(self.tabopVoltage)
        self.volOpComChannels.setObjectName(_fromUtf8("volOpComChannels"))
        self.volOpComChannels.addItem(_fromUtf8(""))
        self.volOpComChannels.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.volOpComChannels, 1, 1, 1, 2)
        
        self.volOpChannel = QtGui.QLineEdit(self.tabopVoltage)
        self.volOpChannel.setObjectName(_fromUtf8("volOpChannel"))
        self.gridLayout.addWidget(self.volOpChannel, 1, 3, 1, 2)
        
        
        self.volOpCebHeights = QtGui.QCheckBox(self.tabopVoltage)
        self.volOpCebHeights.setObjectName(_fromUtf8("volOpCebHeights"))
        self.gridLayout.addWidget(self.volOpCebHeights, 3, 0, 1, 1)
        
        self.volOpComHeights = QtGui.QComboBox(self.tabopVoltage)
        self.volOpComHeights.setObjectName(_fromUtf8("volOpComHeights"))
        self.volOpComHeights.addItem(_fromUtf8(""))
        self.volOpComHeights.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.volOpComHeights, 3, 1, 1, 2)
        
        self.volOpHeights = QtGui.QLineEdit(self.tabopVoltage)
        self.volOpHeights.setObjectName(_fromUtf8("volOpHeights"))
        self.gridLayout.addWidget(self.volOpHeights, 3, 3, 1, 2)
        
        
        
        self.volOpCebProfile = QtGui.QCheckBox(self.tabopVoltage)
        self.volOpCebProfile.setObjectName(_fromUtf8("volOpCebProfile"))
        self.gridLayout.addWidget(self.volOpCebProfile, 5, 0, 1, 1)
        
        self.volOpComProfile = QtGui.QComboBox(self.tabopVoltage)
        self.volOpComProfile.setObjectName(_fromUtf8("volOpComProfile"))
        self.volOpComProfile.addItem(_fromUtf8(""))
        self.volOpComProfile.addItem(_fromUtf8(""))
        self.volOpComProfile.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.volOpComProfile, 5, 1, 1, 2)
        
        self.volOpProfile = QtGui.QLineEdit(self.tabopVoltage)
        self.volOpProfile.setObjectName(_fromUtf8("volOpProfile"))
        self.gridLayout.addWidget(self.volOpProfile, 5, 3, 1, 2)

        self.volOpCebReshaper = QtGui.QCheckBox(self.tabopVoltage)
        self.volOpCebReshaper.setObjectName(_fromUtf8("volOpCebReshaper"))
        self.gridLayout.addWidget(self.volOpCebReshaper, 6, 0, 1, 1)
        
        self.volOpReshaper = QtGui.QLineEdit(self.tabopVoltage)
        self.volOpReshaper.setObjectName(_fromUtf8("volOpReshaper"))
        self.gridLayout.addWidget(self.volOpReshaper, 6, 1, 1, 4)
        
        self.volOpCebFilter = QtGui.QCheckBox(self.tabopVoltage)
        self.volOpCebFilter.setObjectName(_fromUtf8("volOpCebFilter"))
        self.gridLayout.addWidget(self.volOpCebFilter, 7, 0, 1, 1)
        
        self.volOpFilter = QtGui.QLineEdit(self.tabopVoltage)
        self.volOpFilter.setObjectName(_fromUtf8("volOpFilter"))
        self.gridLayout.addWidget(self.volOpFilter, 7, 1, 1, 4)
        
#         spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
#         self.gridLayout.addItem(spacerItem, 6, 4, 1, 1)
#         spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
#         self.gridLayout.addItem(spacerItem1, 8, 4, 1, 1)
#         spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
#         self.gridLayout.addItem(spacerItem2, 3, 4, 1, 1)
        
        
        
#         spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
#         self.gridLayout.addItem(spacerItem3, 1, 4, 1, 1)
        
        
        self.volOpCebDecodification = QtGui.QCheckBox(self.tabopVoltage)
        self.volOpCebDecodification.setObjectName(_fromUtf8("volOpCebDecodification"))
        self.gridLayout.addWidget(self.volOpCebDecodification, 8, 0, 1, 1)
        
        self.volLabCodeMode = QtGui.QLabel(self.tabopVoltage)
        self.volLabCodeMode.setObjectName(_fromUtf8("volLabCodeMode"))
        self.gridLayout.addWidget(self.volLabCodeMode, 8, 1, 1, 1)
        
        self.volOpComMode = QtGui.QComboBox(self.tabopVoltage)
        self.volOpComMode.setObjectName(_fromUtf8("volOpComMode"))
        self.volOpComMode.addItem(_fromUtf8(""))
        self.volOpComMode.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.volOpComMode, 8, 2, 1, 3)
        
        self.volLabCodeType = QtGui.QLabel(self.tabopVoltage)
        self.volLabCodeType.setObjectName(_fromUtf8("volLabCodeType"))
        self.gridLayout.addWidget(self.volLabCodeType, 9, 1, 1, 1)
        
        self.volOpComCode = QtGui.QComboBox(self.tabopVoltage)
        self.volOpComCode.setObjectName(_fromUtf8("volOpComCode"))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.volOpComCode.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.volOpComCode, 9, 2, 1, 3)
        
        self.volLabCode = QtGui.QLabel(self.tabopVoltage)
        self.volLabCode.setObjectName(_fromUtf8("volLabCode"))
        self.gridLayout.addWidget(self.volLabCode, 10, 1, 1, 1)
        
        self.volOpCode = QtGui.QLineEdit(self.tabopVoltage)
        self.volOpCode.setObjectName(_fromUtf8("volOpCode"))
        self.gridLayout.addWidget(self.volOpCode, 10, 2, 1, 3)
        
        self.volOpCebFlip = QtGui.QCheckBox(self.tabopVoltage)
        self.volOpCebFlip.setObjectName(_fromUtf8("volOpCebFlip"))
        self.gridLayout.addWidget(self.volOpCebFlip, 11, 0, 1, 1)
        
        self.volOpFlip = QtGui.QLineEdit(self.tabopVoltage)
        self.volOpFlip.setObjectName(_fromUtf8("volOpFlip"))
        self.gridLayout.addWidget(self.volOpFlip, 11, 1, 1, 4)
        
        self.volOpCebCohInt = QtGui.QCheckBox(self.tabopVoltage)
        self.volOpCebCohInt.setObjectName(_fromUtf8("volOpCebCohInt"))
        self.gridLayout.addWidget(self.volOpCebCohInt, 12, 0, 1, 1)
        
        self.volOpCohInt = QtGui.QLineEdit(self.tabopVoltage)
        self.volOpCohInt.setObjectName(_fromUtf8("volOpCohInt"))
        self.gridLayout.addWidget(self.volOpCohInt, 12, 1, 1, 4)
        
        self.volOpCebAdjustHei = QtGui.QCheckBox(self.tabopVoltage)
        self.volOpCebAdjustHei.setObjectName(_fromUtf8("volOpCebAdjustHei"))
        self.gridLayout.addWidget(self.volOpCebAdjustHei, 13, 0, 1, 1)
        
        self.volOpAdjustHei = QtGui.QLineEdit(self.tabopVoltage)
        self.volOpAdjustHei.setObjectName(_fromUtf8("volOpAdjustHei"))
        self.gridLayout.addWidget(self.volOpAdjustHei, 13, 1, 1, 4)
        
        self.tabWidgetVoltage.addTab(self.tabopVoltage, _fromUtf8(""))
        
        self.tabgraphVoltage = QtGui.QWidget()
        self.tabgraphVoltage.setObjectName(_fromUtf8("tabgraphVoltage"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tabgraphVoltage)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem4, 12, 3, 1, 1)
        self.volGraphIntensityRange = QtGui.QLineEdit(self.tabgraphVoltage)
        self.volGraphIntensityRange.setObjectName(_fromUtf8("volGraphIntensityRange"))
        self.gridLayout_6.addWidget(self.volGraphIntensityRange, 9, 1, 1, 6)
        self.volGraphPrefix = QtGui.QLineEdit(self.tabgraphVoltage)
        self.volGraphPrefix.setObjectName(_fromUtf8("volGraphPrefix"))
        self.gridLayout_6.addWidget(self.volGraphPrefix, 2, 1, 1, 6)
        self.volGraphToolPath = QtGui.QToolButton(self.tabgraphVoltage)
        self.volGraphToolPath.setObjectName(_fromUtf8("volGraphToolPath"))
        self.gridLayout_6.addWidget(self.volGraphToolPath, 1, 5, 1, 2)
        self.volGraphPath = QtGui.QLineEdit(self.tabgraphVoltage)
        self.volGraphPath.setObjectName(_fromUtf8("volGraphPath"))
        self.gridLayout_6.addWidget(self.volGraphPath, 1, 1, 1, 4)
        self.label_14 = QtGui.QLabel(self.tabgraphVoltage)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_6.addWidget(self.label_14, 6, 0, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem5, 3, 3, 1, 1)
        self.label_8 = QtGui.QLabel(self.tabgraphVoltage)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_6.addWidget(self.label_8, 8, 0, 1, 1)
        self.label_49 = QtGui.QLabel(self.tabgraphVoltage)
        self.label_49.setObjectName(_fromUtf8("label_49"))
        self.gridLayout_6.addWidget(self.label_49, 4, 3, 1, 1)
        self.label_51 = QtGui.QLabel(self.tabgraphVoltage)
        self.label_51.setObjectName(_fromUtf8("label_51"))
        self.gridLayout_6.addWidget(self.label_51, 9, 0, 1, 1)
        self.volGraphCebshow = QtGui.QCheckBox(self.tabgraphVoltage)
        self.volGraphCebshow.setText(_fromUtf8(""))
        self.volGraphCebshow.setObjectName(_fromUtf8("volGraphCebshow"))
        self.gridLayout_6.addWidget(self.volGraphCebshow, 6, 3, 1, 1)
        self.label_12 = QtGui.QLabel(self.tabgraphVoltage)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_6.addWidget(self.label_12, 1, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.tabgraphVoltage)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_6.addWidget(self.label_13, 2, 0, 1, 1)
        self.label_52 = QtGui.QLabel(self.tabgraphVoltage)
        self.label_52.setObjectName(_fromUtf8("label_52"))
        
        self.gridLayout_6.addWidget(self.label_52, 11, 0, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(40, 12, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem6, 14, 5, 1, 2)
        spacerItem7 = QtGui.QSpacerItem(18, 12, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem7, 14, 3, 1, 1)
        
        self.volLabScopeType = QtGui.QLabel(self.tabgraphVoltage)
        self.volLabScopeType.setObjectName(_fromUtf8("volLabScopeType"))
        self.gridLayout_6.addWidget(self.volLabScopeType, 7, 0, 1, 1)
        
        self.volComScopeType = QtGui.QComboBox(self.tabgraphVoltage)
        self.volComScopeType.setObjectName(_fromUtf8("volComScopeType"))
        self.volComScopeType.addItem(_fromUtf8(""))
        self.volComScopeType.addItem(_fromUtf8(""))
        self.gridLayout_6.addWidget(self.volComScopeType, 7, 1, 1, 6)
        
        self.volGraphChannelList = QtGui.QLineEdit(self.tabgraphVoltage)
        self.volGraphChannelList.setObjectName(_fromUtf8("volGraphChannelList"))
        self.gridLayout_6.addWidget(self.volGraphChannelList, 8, 1, 1, 6)
        
        
        self.volGraphHeightrange = QtGui.QLineEdit(self.tabgraphVoltage)
        self.volGraphHeightrange.setObjectName(_fromUtf8("volGraphHeightrange"))
        self.gridLayout_6.addWidget(self.volGraphHeightrange, 11, 1, 1, 6)
        self.label_50 = QtGui.QLabel(self.tabgraphVoltage)
        self.label_50.setObjectName(_fromUtf8("label_50"))
        self.gridLayout_6.addWidget(self.label_50, 4, 4, 1, 1)
        self.volGraphCebSave = QtGui.QCheckBox(self.tabgraphVoltage)
        self.volGraphCebSave.setText(_fromUtf8(""))
        self.volGraphCebSave.setObjectName(_fromUtf8("volGraphCebSave"))
        self.gridLayout_6.addWidget(self.volGraphCebSave, 6, 4, 1, 1)
        self.tabWidgetVoltage.addTab(self.tabgraphVoltage, _fromUtf8(""))
        
        self.taboutputVoltage = QtGui.QWidget()
        self.taboutputVoltage.setObjectName(_fromUtf8("taboutputVoltage"))
        self.gridLayout_12 = QtGui.QGridLayout(self.taboutputVoltage)
        self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
        self.label_36 = QtGui.QLabel(self.taboutputVoltage)
        self.label_36.setObjectName(_fromUtf8("label_36"))
        self.gridLayout_12.addWidget(self.label_36, 0, 0, 1, 1)
        self.label_37 = QtGui.QLabel(self.taboutputVoltage)
        self.label_37.setObjectName(_fromUtf8("label_37"))
        self.gridLayout_12.addWidget(self.label_37, 1, 0, 1, 1)
        self.volOutputPath = QtGui.QLineEdit(self.taboutputVoltage)
        self.volOutputPath.setObjectName(_fromUtf8("volOutputPath"))
        self.gridLayout_12.addWidget(self.volOutputPath, 1, 2, 1, 1)
        self.volOutputToolPath = QtGui.QToolButton(self.taboutputVoltage)
        self.volOutputToolPath.setObjectName(_fromUtf8("volOutputToolPath"))
        self.gridLayout_12.addWidget(self.volOutputToolPath, 1, 3, 1, 1)
        self.volOutputComData = QtGui.QComboBox(self.taboutputVoltage)
        self.volOutputComData.setObjectName(_fromUtf8("volOutputComData"))
        self.volOutputComData.addItem(_fromUtf8(""))
        self.gridLayout_12.addWidget(self.volOutputComData, 0, 2, 1, 2)
        spacerItem8 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem8, 5, 2, 1, 1)
        self.volOutputblocksperfile = QtGui.QLineEdit(self.taboutputVoltage)
        self.volOutputblocksperfile.setObjectName(_fromUtf8("volOutputblocksperfile"))
        self.gridLayout_12.addWidget(self.volOutputblocksperfile, 3, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.taboutputVoltage)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_12.addWidget(self.label_7, 3, 0, 1, 1)
        self.label_35 = QtGui.QLabel(self.taboutputVoltage)
        self.label_35.setObjectName(_fromUtf8("label_35"))
        self.gridLayout_12.addWidget(self.label_35, 4, 0, 1, 1)
        self.volOutputprofilesperblock = QtGui.QLineEdit(self.taboutputVoltage)
        self.volOutputprofilesperblock.setObjectName(_fromUtf8("volOutputprofilesperblock"))
        self.gridLayout_12.addWidget(self.volOutputprofilesperblock, 4, 2, 1, 1)
        self.tabWidgetVoltage.addTab(self.taboutputVoltage, _fromUtf8(""))
        self.gridLayout_3.addWidget(self.tabWidgetVoltage, 0, 1, 1, 1)
        
        self.tabWidgetProject.addTab(self.tabVoltage, _fromUtf8(""))
        
        self.tabWidgetVoltage.setCurrentIndex(0)
        
    def retranslateUi(self):
         
        self.volOpOk.setText(_translate("MainWindow", "Ok", None))
        self.volGraphClear.setText(_translate("MainWindow", "Clear", None))
        self.volOpComHeights.setItemText(0, _translate("MainWindow", "Value", None))
        self.volOpComHeights.setItemText(1, _translate("MainWindow", "Index", None))
        self.volOpComChannels.setItemText(0, _translate("MainWindow", "Value", None))
        self.volOpComChannels.setItemText(1, _translate("MainWindow", "Index", None))
        self.volOpCebProfile.setText(_translate("MainWindow", "Select Profiles", None))
        self.volOpComProfile.setItemText(0, _translate("MainWindow", "Profile List", None))
        self.volOpComProfile.setItemText(1, _translate("MainWindow", "Profile Range", None))
        self.volOpComProfile.setItemText(2, _translate("MainWindow", "List of Profile Ranges", None))
        self.volOpCebDecodification.setText(_translate("MainWindow", "Decoder:", None))
        self.volOpCebCohInt.setText(_translate("MainWindow", "Coherent Integration:", None))
        self.volOpCebFlip.setText(_translate("MainWindow", "Flip:", None))
        self.volLabCodeType.setText(_translate("MainWindow", "Code type:", None))
        self.volOpCebChannels.setText(_translate("MainWindow", "Select Channels:", None))
        self.volOpCebHeights.setText(_translate("MainWindow", "Select  Heights:", None))
        self.volOpCebFilter.setText(_translate("MainWindow", "Filter:", None))
        self.volOpCebReshaper.setText(_translate("MainWindow", "Reshape data: ", None))
        self.volOpCebRadarfrequency.setText(_translate("MainWindow", "Radar frequency (MHz):", None))
        self.volLabCodeMode.setText(_translate("MainWindow", "Mode:", None))
        self.volLabCode.setText(_translate("MainWindow", "Code:", None))
        self.volOpComCode.setItemText(0, _translate("MainWindow", "Read from header", None))
        self.volOpComCode.setItemText(1, _translate("MainWindow", "Barker 3", None))
        self.volOpComCode.setItemText(2, _translate("MainWindow", "Barker 4", None))
        self.volOpComCode.setItemText(3, _translate("MainWindow", "Barker 5", None))
        self.volOpComCode.setItemText(4, _translate("MainWindow", "Barker 7", None))
        self.volOpComCode.setItemText(5, _translate("MainWindow", "Barker 11", None))
        self.volOpComCode.setItemText(6, _translate("MainWindow", "Barker 13", None))
        self.volOpComCode.setItemText(7, _translate("MainWindow", "Barker 3 +  Comp.", None))
        self.volOpComCode.setItemText(8, _translate("MainWindow", "Barker 4 +  Comp.", None))
        self.volOpComCode.setItemText(9, _translate("MainWindow", "Barker 5 +  Comp.", None))
        self.volOpComCode.setItemText(10, _translate("MainWindow", "Barker 7 +  Comp.", None))
        self.volOpComCode.setItemText(11, _translate("MainWindow", "Barker 11+ Comp.", None))
        self.volOpComCode.setItemText(12, _translate("MainWindow", "Barker 13+ Comp.", None))
        self.volOpComCode.setItemText(13, _translate("MainWindow", "User defined", None))
        self.volOpComMode.setItemText(0, _translate("MainWindow", "Time", None))
        self.volOpComMode.setItemText(1, _translate("MainWindow", "Frequency", None))
        self.volOpCebAdjustHei.setText(_translate("MainWindow", "Calibrate H0:", None))
        
        self.tabWidgetVoltage.setTabText(self.tabWidgetVoltage.indexOf(self.tabopVoltage), _translate("MainWindow", "Operation", None))
        
        self.volGraphToolPath.setText(_translate("MainWindow", "...", None))
        self.label_14.setText(_translate("MainWindow", "Scope:", None))
        self.label_8.setText(_translate("MainWindow", "Channel List:", None))
        self.label_49.setText(_translate("MainWindow", "Show:", None))
        self.label_51.setText(_translate("MainWindow", "Amplitude/Intensity:", None))
        self.label_12.setText(_translate("MainWindow", "Path   :", None))
        self.label_13.setText(_translate("MainWindow", "Figure name:", None))
        self.label_52.setText(_translate("MainWindow", "Height range:", None))
        self.label_50.setText(_translate("MainWindow", "Save:", None))
        
        self.volLabScopeType.setText(_translate("MainWindow", "Scope type:", None))
        self.volComScopeType.setItemText(0, _translate("MainWindow", "I&Q", None))
        self.volComScopeType.setItemText(1, _translate("MainWindow", "Power", None))
        
        self.tabWidgetVoltage.setTabText(self.tabWidgetVoltage.indexOf(self.tabgraphVoltage), _translate("MainWindow", "Graphics", None))
        
        self.label_36.setText(_translate("MainWindow", "Type:", None))
        self.label_37.setText(_translate("MainWindow", "Path:", None))
        self.volOutputToolPath.setText(_translate("MainWindow", "...", None))
        self.volOutputComData.setItemText(0, _translate("MainWindow", ".rawdata", None))
        self.label_7.setText(_translate("MainWindow", "Blocks per File: ", None))
        self.label_35.setText(_translate("MainWindow", "Profiles per Block: ", None))
        self.tabWidgetVoltage.setTabText(self.tabWidgetVoltage.indexOf(self.taboutputVoltage), _translate("MainWindow", "Output", None))
        
        self.tabWidgetProject.setTabText(self.tabWidgetProject.indexOf(self.tabVoltage), _translate("MainWindow", "Voltage", None))
    
        self.__setToolTip()
        
    def __setToolTip(self):
        
        self.volOpChannel.setToolTip('Example: 1,2,3,4,5')    
        self.volOpHeights.setToolTip('Example: 90,180')
        self.volOpFilter.setToolTip('Example: 2')
        self.volOpProfile.setToolTip('Example:0,127')
        self.volOpCohInt.setToolTip('Example: 128')
        self.volOpFlip.setToolTip('ChannelList where flip will be applied. Example: 0,2,3')
        self.volOpOk.setToolTip('If you have finished, please Ok ')
        # tool tip gui volGraph
        self.volGraphIntensityRange.setToolTip('Height range. Example: 50,100')
        self.volGraphHeightrange.setToolTip('Amplitude. Example: 0,10000')
        
        