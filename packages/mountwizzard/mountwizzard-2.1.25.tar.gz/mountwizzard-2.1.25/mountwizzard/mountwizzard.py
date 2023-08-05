############################################################
# -*- coding: utf-8 -*-
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.5
#
# Michael Würtenberger
# (c) 2016, 2017
#
# Licence APL2.0
#
############################################################

# import basic stuff
import logging
import logging.handlers
import sys
import json
import time
import datetime
import os
# import for the PyQt5 Framework
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# import the UI part, which is done via QT Designer and exported
from support.mw_widget import MwWidget
from support.wizzard_main_ui import Ui_WizzardMainDialog
# commands to threads
from queue import Queue
# import mount functions of other classes
from support.mount_thread import Mount
from support.model_thread import Model
from support.coordinate_widget import ShowCoordinatePopup
from support.image_widget import ShowImagePopup
from support.analyse import ShowAnalysePopup
from support.dome_thread import Dome
from support.weather_thread import Weather
from support.stick_thread import Stick
from support.relays import Relays
from support.data_thread import Data

# matplotlib
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
from matplotlib import figure as figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# numerics
import numpy
import math


class ShowModel(FigureCanvas):

    def __init__(self, parent=None):
        self.fig = figure.Figure(dpi=75, facecolor=(25/256, 25/256, 25/256))
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)


class MountWizzardApp(MwWidget):
    logger = logging.getLogger(__name__)                                                                                    # logging enabling

    def __init__(self):
        super(MountWizzardApp, self).__init__()                                                                             # Initialize Class for UI
        self.modifiers = None                                                                                               # for the mouse handling
        self.config = {}                                                                                                    # configuration data, which is stored
        self.ui = Ui_WizzardMainDialog()                                                                                    # load the dialog from "DESIGNER"
        self.ui.setupUi(self)                                                                                               # initialising the GUI
        self.ui.windowTitle.setPalette(self.palette)                                                                        # title color
        self.initUI()                                                                                                       # adapt the window to our purpose
        self.ui.build.setText(BUILD_NO)
        self.commandQueue = Queue()                                                                                         # queue for sending command to mount
        self.mountDataQueue = Queue()                                                                                       # queue for sending data back to gui
        self.modelLogQueue = Queue()                                                                                        # queue for showing the modeling progress
        self.messageQueue = Queue()                                                                                         # queue for showing messages in Gui from threads
        self.commandDataQueue = Queue()                                                                                     # queue for command to data thread for downloading data
        self.relays = Relays(self)                                                                                          # Web base relays box for Booting and CCD / Heater On / OFF
        self.dome = Dome(self)                                                                                              # dome control
        self.mount = Mount(self)                                                                                            # Mount -> everything with mount and alignment
        self.weather = Weather(self)                                                                                        # Stickstation Thread
        self.stick = Stick(self)                                                                                            # Stickstation Thread
        self.model = Model(self)                                                                                            # transferring ui and mount object as well
        self.data = Data(self)                                                                                              # data thread for downloading topics
        self.analysePopup = ShowAnalysePopup(self)                                                                          # windows for analyse data
        self.coordinatePopup = ShowCoordinatePopup(self)                                                                    # window for modeling points
        self.imagePopup = ShowImagePopup(self)                                                                              # window for imaging
        helper = QVBoxLayout(self.ui.model)                                                                                 # adding box layout for matplotlib
        helper.setContentsMargins(0, 0, 0, 0)                                                                               # set margins to 0 -> box in qt is frameless
        self.modelWidget = ShowModel(self.ui.model)                                                                         # build the polar plot widget
        # noinspection PyArgumentList
        helper.addWidget(self.modelWidget)                                                                                  # add widget to view
        self.loadConfig()
        self.model.cameraPlateChooser()
        self.mount.mountDriverChooser()
        self.mount.signalMountConnected.connect(self.setMountStatus)                                                        # status from thread
        self.mount.start()                                                                                                  # starting polling thread
        self.weather.signalWeatherData.connect(self.fillWeatherData)                                                        # connecting the signal
        self.weather.signalWeatherConnected.connect(self.setWeatherStatus)                                                  # status from thread
        self.weather.start()                                                                                                # starting polling thread
        self.stick.signalStickData.connect(self.fillStickData)                                                              # connecting the signal for data
        self.stick.signalStickConnected.connect(self.setStickStatus)                                                        # status from thread
        self.stick.start()                                                                                                  # starting polling thread
        self.dome.signalDomeConnected.connect(self.setDomeStatus)                                                           # status from thread
        self.dome.start()                                                                                                   # starting polling thread
        self.model.signalModelConnected.connect(self.setCameraPlateStatus)                                                  # status from thread
        self.model.start()                                                                                                  # starting polling thread
        self.data.start()                                                                                                   # starting data thread
        self.mappingFunctions()                                                                                             # mapping the functions to ui
        self.mainLoop()                                                                                                     # starting loop for cyclic data to gui from threads
        self.ui.le_mwWorkingDir.setText(os.getcwd())                                                                        # put working directory into gui

    # noinspection PyArgumentList
    def mappingFunctions(self):
        self.ui.btn_mountQuit.clicked.connect(self.saveConfigQuit)
        self.ui.btn_mountSave.clicked.connect(self.saveConfigCont)
        self.ui.btn_selectClose.clicked.connect(lambda: QCoreApplication.instance().quit())
        self.ui.btn_shutdownQuit.clicked.connect(self.shutdownQuit)
        # self.ui.btn_camPlateConnected.clicked.connect(self.startCamPlateApp)
        self.ui.btn_mountPark.clicked.connect(lambda: self.commandQueue.put('hP'))
        self.ui.btn_mountUnpark.clicked.connect(lambda: self.commandQueue.put('PO'))
        self.ui.btn_startTracking.clicked.connect(lambda: self.commandQueue.put('AP'))
        self.ui.btn_stopTracking.clicked.connect(lambda: self.commandQueue.put('RT9'))
        self.ui.btn_setTrackingLunar.clicked.connect(lambda: self.commandQueue.put('RT0'))
        self.ui.btn_setTrackingSolar.clicked.connect(lambda: self.commandQueue.put('RT1'))
        self.ui.btn_setTrackingSideral.clicked.connect(lambda: self.commandQueue.put('RT2'))
        self.ui.btn_stop.clicked.connect(lambda: self.commandQueue.put('STOP'))
        self.ui.btn_mountPos1.clicked.connect(self.mountPosition1)
        self.ui.btn_mountPos2.clicked.connect(self.mountPosition2)
        self.ui.btn_mountPos3.clicked.connect(self.mountPosition3)
        self.ui.btn_mountPos4.clicked.connect(self.mountPosition4)
        self.ui.btn_mountPos5.clicked.connect(self.mountPosition5)
        self.ui.btn_mountPos6.clicked.connect(self.mountPosition6)
        self.ui.le_parkPos1Text.textChanged.connect(lambda: self.ui.btn_mountPos1.setText(self.ui.le_parkPos1Text.text()))
        self.ui.le_parkPos2Text.textChanged.connect(lambda: self.ui.btn_mountPos2.setText(self.ui.le_parkPos2Text.text()))
        self.ui.le_parkPos3Text.textChanged.connect(lambda: self.ui.btn_mountPos3.setText(self.ui.le_parkPos3Text.text()))
        self.ui.le_parkPos4Text.textChanged.connect(lambda: self.ui.btn_mountPos4.setText(self.ui.le_parkPos4Text.text()))
        self.ui.le_parkPos5Text.textChanged.connect(lambda: self.ui.btn_mountPos5.setText(self.ui.le_parkPos5Text.text()))
        self.ui.le_parkPos6Text.textChanged.connect(lambda: self.ui.btn_mountPos6.setText(self.ui.le_parkPos6Text.text()))
        self.ui.btn_setHorizonLimitHigh.clicked.connect(self.setHorizonLimitHigh)
        self.ui.btn_setHorizonLimitLow.clicked.connect(self.setHorizonLimitLow)
        self.ui.btn_setSlewRate.clicked.connect(self.setSlewRate)
        self.ui.btn_setDualTracking.clicked.connect(self.setDualTracking)
        self.ui.btn_setUnattendedFlip.clicked.connect(self.setUnattendedFlip)
        self.ui.btn_setupMountDriver.clicked.connect(lambda: self.commandQueue.put('SetupAscomDriver'))
        self.ui.btn_setupDomeDriver.clicked.connect(lambda: self.dome.setupDriver())
        self.ui.btn_setupStickDriver.clicked.connect(lambda: self.stick.setupDriver())
        self.ui.btn_setupWeatherDriver.clicked.connect(lambda: self.weather.setupDriver())
        self.ui.btn_setupAscomCameraDriver.clicked.connect(lambda: self.model.AscomCamera.setupDriverCamera())
        self.ui.btn_setRefractionParameters.clicked.connect(lambda: self.commandQueue.put('SetRefractionParameter'))
        self.ui.btn_runBaseModel.clicked.connect(lambda: self.model.signalModelCommand.emit('RunBaseModel'))
        self.ui.btn_cancelModel.clicked.connect(lambda: self.model.signalModelCommand.emit('CancelModel'))
        self.ui.btn_runRefinementModel.clicked.connect(lambda: self.model.signalModelCommand.emit('RunRefinementModel'))
        self.ui.btn_runBatchModel.clicked.connect(lambda: self.model.signalModelCommand.emit('RunBatchModel'))
        self.ui.btn_clearAlignmentModel.clicked.connect(lambda: self.model.signalModelCommand.emit('ClearAlignmentModel'))
        self.ui.btn_selectImageDirectoryName.clicked.connect(self.selectImageDirectoryName)
        self.ui.btn_selectHorizonPointsFileName.clicked.connect(self.selectHorizonPointsFileName)
        self.ui.checkUseMinimumHorizonLine.stateChanged.connect(self.selectHorizonPointsMode)
        self.ui.altitudeMinimumHorizon.valueChanged.connect(self.selectHorizonPointsMode)
        self.ui.btn_selectModelPointsFileName.clicked.connect(self.selectModelPointsFileName)
        self.ui.btn_selectAnalyseFileName.clicked.connect(self.selectAnalyseFileName)
        self.ui.btn_showActualModel.clicked.connect(lambda: self.commandQueue.put('ShowAlignmentModel'))
        self.ui.checkPolarPlot.clicked.connect(self.setShowAlignmentModelMode)
        self.ui.btn_setRefractionCorrection.clicked.connect(self.setRefractionCorrection)
        self.ui.btn_runTargetRMSAlignment.clicked.connect(lambda: self.commandQueue.put('RunTargetRMSAlignment'))
        self.ui.btn_deleteWorstPoint.clicked.connect(lambda: self.commandQueue.put('DeleteWorstPoint'))
        self.ui.btn_sortRefinementPoints.clicked.connect(lambda: self.model.signalModelCommand.emit('SortRefinementPoints'))
        self.ui.btn_deleteBelowHorizonLine.clicked.connect(lambda: self.model.signalModelCommand.emit('DeleteBelowHorizonLine'))
        self.ui.btn_plateSolveSync.clicked.connect(lambda: self.model.signalModelCommand.emit('PlateSolveSync'))
        self.ui.btn_deletePoints.clicked.connect(lambda: self.model.signalModelCommand.emit('DeletePoints'))
        self.ui.btn_flipMount.clicked.connect(lambda: self.commandQueue.put('FLIP'))
        self.ui.btn_loadRefinementPoints.clicked.connect(lambda: self.model.signalModelCommand.emit('LoadRefinementPoints'))
        self.ui.btn_loadBasePoints.clicked.connect(lambda: self.model.signalModelCommand.emit('LoadBasePoints'))
        self.ui.btn_saveBackupModel.clicked.connect(lambda: self.commandQueue.put('SaveBackupModel'))
        self.ui.btn_loadBackupModel.clicked.connect(lambda: self.commandQueue.put('LoadBackupModel'))
        self.ui.btn_saveSimpleModel.clicked.connect(lambda: self.commandQueue.put('SaveSimpleModel'))
        self.ui.btn_loadSimpleModel.clicked.connect(lambda: self.commandQueue.put('LoadSimpleModel'))
        self.ui.btn_saveRefinementModel.clicked.connect(lambda: self.commandQueue.put('SaveRefinementModel'))
        self.ui.btn_loadRefinementModel.clicked.connect(lambda: self.commandQueue.put('LoadRefinementModel'))
        self.ui.btn_saveBaseModel.clicked.connect(lambda: self.commandQueue.put('SaveBaseModel'))
        self.ui.btn_loadBaseModel.clicked.connect(lambda: self.commandQueue.put('LoadBaseModel'))
        self.ui.btn_saveDSO1Model.clicked.connect(lambda: self.commandQueue.put('SaveDSO1Model'))
        self.ui.btn_loadDSO1Model.clicked.connect(lambda: self.commandQueue.put('LoadDSO1Model'))
        self.ui.btn_saveDSO2Model.clicked.connect(lambda: self.commandQueue.put('SaveDSO2Model'))
        self.ui.btn_loadDSO2Model.clicked.connect(lambda: self.commandQueue.put('LoadDSO2Model'))
        self.ui.btn_generateDSOPoints.clicked.connect(lambda: self.model.signalModelCommand.emit('GenerateDSOPoints'))
        self.ui.numberHoursDSO.valueChanged.connect(lambda: self.model.signalModelCommand.emit('GenerateDSOPoints'))
        self.ui.numberPointsDSO.valueChanged.connect(lambda: self.model.signalModelCommand.emit('GenerateDSOPoints'))
        self.ui.numberHoursPreview.valueChanged.connect(lambda: self.model.signalModelCommand.emit('GenerateDSOPoints'))
        self.ui.btn_generateDensePoints.clicked.connect(lambda: self.model.signalModelCommand.emit('GenerateDensePoints'))
        self.ui.btn_generateNormalPoints.clicked.connect(lambda: self.model.signalModelCommand.emit('GenerateNormalPoints'))
        self.ui.btn_generateGridPoints.clicked.connect(lambda: self.model.signalModelCommand.emit('GenerateGridPoints'))
        self.ui.numberGridPointsRow.valueChanged.connect(lambda: self.model.signalModelCommand.emit('GenerateGridPoints'))
        self.ui.numberGridPointsCol.valueChanged.connect(lambda: self.model.signalModelCommand.emit('GenerateGridPoints'))
        self.ui.btn_generateBasePoints.clicked.connect(lambda: self.model.signalModelCommand.emit('GenerateBasePoints'))
        self.ui.btn_runCheckModel.clicked.connect(lambda: self.model.signalModelCommand.emit('RunCheckModel'))
        self.ui.btn_runAllModel.clicked.connect(lambda: self.model.signalModelCommand.emit('RunAllModel'))
        self.ui.btn_runTimeChangeModel.clicked.connect(lambda: self.model.signalModelCommand.emit('RunTimeChangeModel'))
        self.ui.btn_cancelAnalyseModel.clicked.connect(lambda: self.model.signalModelCommand.emit('CancelAnalyseModel'))
        self.ui.btn_runHystereseModel.clicked.connect(lambda: self.model.signalModelCommand.emit('RunHystereseModel'))
        self.ui.btn_openAnalyseWindow.clicked.connect(self.showAnalyseWindow)
        self.ui.btn_openCoordinateWindow.clicked.connect(self.showCoordinateWindow)
        self.ui.btn_bootMount.clicked.connect(lambda: self.relays.bootMount())
        self.ui.btn_switchCCD.clicked.connect(lambda: self.relays.switchCCD())
        self.ui.btn_switchHeater.clicked.connect(lambda: self.relays.switchHeater())
        self.ui.rb_cameraSGPro.clicked.connect(self.model.cameraPlateChooser)
        self.ui.rb_cameraTSX.clicked.connect(self.model.cameraPlateChooser)
        self.ui.rb_cameraASCOM.clicked.connect(self.model.cameraPlateChooser)
        self.ui.btn_downloadEarthrotation.clicked.connect(lambda: self.commandDataQueue.put('EARTHROTATION'))
        self.ui.btn_downloadSpacestations.clicked.connect(lambda: self.commandDataQueue.put('SPACESTATIONS'))
        self.ui.btn_downloadSatbrighest.clicked.connect(lambda: self.commandDataQueue.put('SATBRIGHTEST'))
        self.ui.btn_downloadAsteroids.clicked.connect(lambda: self.commandDataQueue.put('ASTEROIDS'))
        self.ui.btn_downloadComets.clicked.connect(lambda: self.commandDataQueue.put('COMETS'))
        self.ui.btn_downloadAll.clicked.connect(lambda: self.commandDataQueue.put('ALL'))
        self.ui.btn_uploadMount.clicked.connect(lambda: self.commandDataQueue.put('UPLOADMOUNT'))
        self.ui.btn_selectUpdaterFileName.clicked.connect(self.selectUpdaterFileName)
        self.ui.rb_ascomMount.clicked.connect(self.mount.mountDriverChooser)
        self.ui.rb_directMount.clicked.connect(self.mount.mountDriverChooser)

    def showModelErrorPolar(self):
        if not self.model.modelData:
            return
        data = dict()
        for i in range(0, len(self.model.modelData)):
            for (keyData, valueData) in self.model.modelData[i].items():
                if keyData in data:
                    data[keyData].append(valueData)
                else:
                    data[keyData] = [valueData]
        self.modelWidget.fig.clf()
        self.modelWidget.axes = self.modelWidget.fig.add_subplot(1, 1, 1, polar=True)
        self.modelWidget.axes.grid(True, color='gray')
        self.modelWidget.fig.subplots_adjust(left=0.025, right=0.975, bottom=0.075, top=0.925)
        self.modelWidget.axes.set_facecolor((32/256, 32/256, 32/256))
        self.modelWidget.axes.tick_params(axis='x', colors='white')
        self.modelWidget.axes.tick_params(axis='y', colors='white')
        self.modelWidget.axes.set_theta_zero_location('N')
        self.modelWidget.axes.set_theta_direction(-1)
        self.modelWidget.axes.set_yticks(range(0, 90, 10))
        yLabel = ['', '80', '', '60', '', '40', '', '20', '', '0']
        self.modelWidget.axes.set_yticklabels(yLabel, color='white')
        azimuth = numpy.asarray(data['azimuth'])
        altitude = numpy.asarray(data['altitude'])
        # self.modelWidget.axes.plot(azimuth / 180.0 * math.pi, 90 - altitude, color='black')
        cm = plt.cm.get_cmap('RdYlGn_r')
        colors = numpy.asarray(data['modelError'])
        # noinspection PyTypeChecker
        scaleError = int(max(colors) / 4 + 1) * 4
        area = [125 if x >= max(colors) else 50 for x in data['modelError']]
        theta = azimuth / 180.0 * math.pi
        r = 90 - altitude
        scatter = self.modelWidget.axes.scatter(theta, r, c=colors, vmin=0, vmax=scaleError, s=area, cmap=cm)
        scatter.set_alpha(0.75)
        colorbar = self.modelWidget.fig.colorbar(scatter)
        colorbar.set_label('Error [arcsec]', color='white')
        plt.setp(plt.getp(colorbar.ax.axes, 'yticklabels'), color='white')
        self.modelWidget.axes.set_rmax(90)
        self.modelWidget.axes.set_rmin(0)
        self.modelWidget.draw()

    def loadConfig(self):
        try:
            with open('config/config.cfg', 'r') as data_file:
                self.config = json.load(data_file)
            data_file.close()
            self.model.loadHorizonPoints(str(self.config['HorizonPointsFileName']))
            self.ui.le_parkPos1Text.setText(self.config['ParkPosText1'])
            self.ui.le_altParkPos1.setText(self.config['ParkPosAlt1'])
            self.ui.le_azParkPos1.setText(self.config['ParkPosAz1'])
            self.ui.btn_mountPos1.setText(self.ui.le_parkPos1Text.text())
            self.ui.le_parkPos2Text.setText(self.config['ParkPosText2'])
            self.ui.le_altParkPos2.setText(self.config['ParkPosAlt2'])
            self.ui.le_azParkPos2.setText(self.config['ParkPosAz2'])
            self.ui.btn_mountPos2.setText(self.ui.le_parkPos2Text.text())
            self.ui.le_parkPos3Text.setText(self.config['ParkPosText3'])
            self.ui.le_altParkPos3.setText(self.config['ParkPosAlt3'])
            self.ui.le_azParkPos3.setText(self.config['ParkPosAz3'])
            self.ui.btn_mountPos3.setText(self.ui.le_parkPos3Text.text())
            self.ui.le_parkPos4Text.setText(self.config['ParkPosText4'])
            self.ui.le_altParkPos4.setText(self.config['ParkPosAlt4'])
            self.ui.le_azParkPos4.setText(self.config['ParkPosAz4'])
            self.ui.btn_mountPos4.setText(self.ui.le_parkPos4Text.text())
            self.ui.le_parkPos5Text.setText(self.config['ParkPosText5'])
            self.ui.le_altParkPos5.setText(self.config['ParkPosAlt5'])
            self.ui.le_azParkPos5.setText(self.config['ParkPosAz5'])
            self.ui.btn_mountPos5.setText(self.ui.le_parkPos5Text.text())
            self.ui.le_parkPos6Text.setText(self.config['ParkPosText6'])
            self.ui.le_altParkPos6.setText(self.config['ParkPosAlt6'])
            self.ui.le_azParkPos6.setText(self.config['ParkPosAz6'])
            self.ui.btn_mountPos6.setText(self.ui.le_parkPos6Text.text())
            self.ui.le_modelPointsFileName.setText(self.config['ModelPointsFileName'])
            self.ui.le_horizonPointsFileName.setText(self.config['HorizonPointsFileName'])
            self.ui.checkUseMinimumHorizonLine.setChecked(self.config['CheckUseMinimumHorizonLine'])
            self.ui.altitudeMinimumHorizon.setValue(self.config['AltitudeMinimumHorizon'])
            self.ui.le_imageDirectoryName.setText(self.config['ImageDirectoryName'])
            self.ui.rb_cameraTSX.setChecked(self.config['CameraTSX'])
            self.ui.rb_cameraSGPro.setChecked(self.config['CameraSGPro'])
            self.ui.rb_cameraASCOM.setChecked(self.config['CameraASCOM'])
            self.ui.cameraBin.setValue(self.config['CameraBin'])
            self.ui.cameraExposure.setValue(self.config['CameraExposure'])
            self.ui.isoSetting.setValue(self.config['ISOSetting'])
            self.ui.checkFastDownload.setChecked(self.config['CheckFastDownload'])
            self.ui.settlingTime.setValue(self.config['SettlingTime'])
            self.ui.checkUseBlindSolve.setChecked(self.config['CheckUseBlindSolve'])
            self.ui.targetRMS.setValue(self.config['TargetRMS'])
            self.ui.pixelSize.setValue(self.config['PixelSize'])
            self.ui.focalLength.setValue(self.config['FocalLength'])
            self.ui.scaleSubframe.setValue(self.config['ScaleSubframe'])
            self.ui.checkDoSubframe.setChecked(self.config['CheckDoSubframe'])
            self.ui.checkAutoRefraction.setChecked(self.config['CheckAutoRefraction'])
            self.ui.checkKeepImages.setChecked(self.config['CheckKeepImages'])
            self.ui.checkRunTrackingWidget.setChecked(self.config['CheckRunTrackingWidget'])
            self.ui.checkClearModelFirst.setChecked(self.config['CheckClearModelFirst'])
            self.ui.checkKeepRefinement.setChecked(self.config['CheckKeepRefinement'])
            self.ui.altitudeBase.setValue(self.config['AltitudeBase'])
            self.ui.azimuthBase.setValue(self.config['AzimuthBase'])
            self.ui.numberGridPointsCol.setValue(self.config['NumberGridPointsCol'])
            self.ui.numberGridPointsRow.setValue(self.config['NumberGridPointsRow'])
            self.ui.numberPointsDSO.setValue(self.config['NumberPointsDSO'])
            self.ui.numberHoursDSO.setValue(self.config['NumberHoursDSO'])
            self.ui.le_analyseFileName.setText(self.config['AnalyseFileName'])
            self.ui.altitudeTimeChange.setValue(self.config['AltitudeTimeChange'])
            self.ui.azimuthTimeChange.setValue(self.config['AzimuthTimeChange'])
            self.ui.numberRunsTimeChange.setValue(self.config['NumberRunsTimeChange'])
            self.ui.delayTimeTimeChange.setValue(self.config['DelayTimeTimeChange'])
            self.ui.altitudeHysterese1.setValue(self.config['AltitudeHysterese1'])
            self.ui.altitudeHysterese2.setValue(self.config['AltitudeHysterese2'])
            self.ui.azimuthHysterese1.setValue(self.config['AzimuthHysterese1'])
            self.ui.azimuthHysterese2.setValue(self.config['AzimuthHysterese2'])
            self.ui.numberRunsHysterese.setValue(self.config['NumberRunsHysterese'])
            self.ui.delayTimeHysterese.setValue(self.config['DelayTimeHysterese'])
            self.ui.le_mountIP.setText(self.config['MountIP'])
            self.ui.le_relayIP.setText(self.config['RelayIP'])
            self.dome.driverName = self.config['ASCOMDomeDriverName']
            self.stick.driverName = self.config['ASCOMStickDriverName']
            self.mount.MountAscom.driverName = self.config['ASCOMTelescopeDriverName']
            self.weather.driverName = self.config['ASCOMWeatherDriverName']
            self.model.AscomCamera.driverNameCamera = self.config['ASCOMCameraDriverName']
            self.model.AscomCamera.driverNamePlateSolver = self.config['ASCOMPlateSolverDriverName']
            self.move(self.config['WindowPositionX'], self.config['WindowPositionY'])
            self.analysePopup.ui.scalePlotRA.setValue(self.config['ScalePlotRA'])
            self.analysePopup.ui.scalePlotDEC.setValue(self.config['ScalePlotDEC'])
            self.analysePopup.ui.scalePlotError.setValue(self.config['ScalePlotError'])
            self.analysePopup.move(self.config['AnalysePopupWindowPositionX'], self.config['AnalysePopupWindowPositionY'])
            self.analysePopup.showStatus = self.config['AnalysePopupWindowShowStatus']
            self.coordinatePopup.move(self.config['CoordinatePopupWindowPositionX'], self.config['CoordinatePopupWindowPositionY'])
            self.coordinatePopup.showStatus = self.config['CoordinatePopupWindowShowStatus']
            self.imagePopup.move(self.config['ImagePopupWindowPositionX'], self.config['ImagePopupWindowPositionY'])
            self.imagePopup.showStatus = self.config['ImagePopupWindowShowStatus']
            self.ui.rb_directMount.setChecked(self.config['DirectMount'])
            self.ui.rb_ascomMount.setChecked(self.config['AscomMount'])
            self.ui.le_updaterFileName.setText(self.config['UpdaterFileName'])
        except Exception as e:
            self.messageQueue.put('Config.cfg could not be loaded !')
            self.logger.error('loadConfig -> item in config.cfg not loaded error:{0}'.format(e))
            return

    def saveConfig(self):
        self.config['ParkPosText1'] = self.ui.le_parkPos1Text.text()
        self.config['ParkPosAlt1'] = self.ui.le_altParkPos1.text()
        self.config['ParkPosAz1'] = self.ui.le_azParkPos1.text()
        self.config['ParkPosText2'] = self.ui.le_parkPos2Text.text()
        self.config['ParkPosAlt2'] = self.ui.le_altParkPos2.text()
        self.config['ParkPosAz2'] = self.ui.le_azParkPos2.text()
        self.config['ParkPosText3'] = self.ui.le_parkPos3Text.text()
        self.config['ParkPosAlt3'] = self.ui.le_altParkPos3.text()
        self.config['ParkPosAz3'] = self.ui.le_azParkPos3.text()
        self.config['ParkPosText4'] = self.ui.le_parkPos4Text.text()
        self.config['ParkPosAlt4'] = self.ui.le_altParkPos4.text()
        self.config['ParkPosAz4'] = self.ui.le_azParkPos4.text()
        self.config['ParkPosText5'] = self.ui.le_parkPos5Text.text()
        self.config['ParkPosAlt5'] = self.ui.le_altParkPos5.text()
        self.config['ParkPosAz5'] = self.ui.le_azParkPos5.text()
        self.config['ParkPosText6'] = self.ui.le_parkPos6Text.text()
        self.config['ParkPosAlt6'] = self.ui.le_altParkPos6.text()
        self.config['ParkPosAz6'] = self.ui.le_azParkPos6.text()
        self.config['ModelPointsFileName'] = self.ui.le_modelPointsFileName.text()
        self.config['HorizonPointsFileName'] = self.ui.le_horizonPointsFileName.text()
        self.config['CheckUseMinimumHorizonLine'] = self.ui.checkUseMinimumHorizonLine.isChecked()
        self.config['AltitudeMinimumHorizon'] = self.ui.altitudeMinimumHorizon.value()
        self.config['ImageDirectoryName'] = self.ui.le_imageDirectoryName.text()
        self.config['CameraTSX'] = self.ui.rb_cameraTSX.isChecked()
        self.config['CameraSGPro'] = self.ui.rb_cameraSGPro.isChecked()
        self.config['CameraASCOM'] = self.ui.rb_cameraASCOM.isChecked()
        self.config['CameraBin'] = self.ui.cameraBin.value()
        self.config['CameraExposure'] = self.ui.cameraExposure.value()
        self.config['CheckFastDownload'] = self.ui.checkFastDownload.isChecked()
        self.config['ISOSetting'] = self.ui.isoSetting.value()
        self.config['SettlingTime'] = self.ui.settlingTime.value()
        self.config['CheckUseBlindSolve'] = self.ui.checkUseBlindSolve.isChecked()
        self.config['TargetRMS'] = self.ui.targetRMS.value()
        self.config['PixelSize'] = self.ui.pixelSize.value()
        self.config['FocalLength'] = self.ui.focalLength.value()
        self.config['ScaleSubframe'] = self.ui.scaleSubframe.value()
        self.config['CheckDoSubframe'] = self.ui.checkDoSubframe.isChecked()
        self.config['CheckAutoRefraction'] = self.ui.checkAutoRefraction.isChecked()
        self.config['CheckKeepImages'] = self.ui.checkKeepImages.isChecked()
        self.config['CheckRunTrackingWidget'] = self.ui.checkRunTrackingWidget.isChecked()
        self.config['AltitudeBase'] = self.ui.altitudeBase.value()
        self.config['AzimuthBase'] = self.ui.azimuthBase.value()
        self.config['NumberGridPointsRow'] = self.ui.numberGridPointsRow.value()
        self.config['NumberGridPointsCol'] = self.ui.numberGridPointsCol.value()
        self.config['NumberPointsDSO'] = self.ui.numberPointsDSO.value()
        self.config['NumberHoursDSO'] = self.ui.numberHoursDSO.value()
        self.config['WindowPositionX'] = self.pos().x()
        self.config['WindowPositionY'] = self.pos().y()
        self.config['AnalysePopupWindowPositionX'] = self.analysePopup.pos().x()
        self.config['AnalysePopupWindowPositionY'] = self.analysePopup.pos().y()
        self.config['AnalysePopupWindowShowStatus'] = self.analysePopup.showStatus
        self.config['CoordinatePopupWindowPositionX'] = self.coordinatePopup.pos().x()
        self.config['CoordinatePopupWindowPositionY'] = self.coordinatePopup.pos().y()
        self.config['CoordinatePopupWindowShowStatus'] = self.coordinatePopup.showStatus
        self.config['ImagePopupWindowPositionX'] = self.imagePopup.pos().x()
        self.config['ImagePopupWindowPositionY'] = self.imagePopup.pos().y()
        self.config['ImagePopupWindowShowStatus'] = self.imagePopup.showStatus
        self.config['ScalePlotRA'] = self.analysePopup.ui.scalePlotRA.value()
        self.config['ScalePlotDEC'] = self.analysePopup.ui.scalePlotDEC.value()
        self.config['ScalePlotError'] = self.analysePopup.ui.scalePlotError.value()
        self.config['AnalyseFileName'] = self.ui.le_analyseFileName.text()
        self.config['AltitudeTimeChange'] = self.ui.altitudeTimeChange.value()
        self.config['AzimuthTimeChange'] = self.ui.azimuthTimeChange.value()
        self.config['NumberRunsTimeChange'] = self.ui.numberRunsTimeChange.value()
        self.config['DelayTimeTimeChange'] = self.ui.delayTimeTimeChange.value()
        self.config['AltitudeHysterese1'] = self.ui.altitudeHysterese1.value()
        self.config['AltitudeHysterese2'] = self.ui.altitudeHysterese2.value()
        self.config['AzimuthHysterese1'] = self.ui.azimuthHysterese1.value()
        self.config['AzimuthHysterese2'] = self.ui.azimuthHysterese2.value()
        self.config['NumberRunsHysterese'] = self.ui.numberRunsHysterese.value()
        self.config['DelayTimeHysterese'] = self.ui.delayTimeHysterese.value()
        self.config['MountIP'] = self.ui.le_mountIP.text()
        self.config['RelayIP'] = self.ui.le_relayIP.text()
        self.config['ASCOMDomeDriverName'] = self.dome.driverName
        self.config['ASCOMStickDriverName'] = self.stick.driverName
        self.config['ASCOMTelescopeDriverName'] = self.mount.MountAscom.driverName
        self.config['ASCOMWeatherDriverName'] = self.weather.driverName
        self.config['ASCOMCameraDriverName'] = self.model.AscomCamera.driverNameCamera
        self.config['ASCOMPlateSolverDriverName'] = self.model.AscomCamera.driverNamePlateSolver
        self.config['CheckClearModelFirst'] = self.ui.checkClearModelFirst.isChecked()
        self.config['CheckKeepRefinement'] = self.ui.checkKeepRefinement.isChecked()
        self.config['DirectMount'] = self.ui.rb_directMount.isChecked()
        self.config['AscomMount'] = self.ui.rb_ascomMount.isChecked()
        self.config['UpdaterFileName'] = self.ui.le_updaterFileName.text()
        try:
            if not os.path.isdir(os.getcwd() + '/config'):                                                                  # if config dir doesn't exist, make it
                os.makedirs(os.getcwd() + '/config')                                                                        # if path doesn't exist, generate is
            with open('config/config.cfg', 'w') as outfile:
                json.dump(self.config, outfile)
            outfile.close()
        except Exception as e:
            self.messageQueue.put('Config.cfg could not be saved !')
            self.logger.error('loadConfig -> item in config.cfg not saved error {0}'.format(e))
            return
        self.mount.saveActualModel()                                                                                        # save current loaded model from mount

    def saveConfigQuit(self):
        self.saveConfig()
        # noinspection PyArgumentList
        QCoreApplication.instance().quit()

    def saveConfigCont(self):
        self.saveConfig()
        self.messageQueue.put('Configuration saved.')

    def selectModelPointsFileName(self):
        dlg = QFileDialog()
        dlg.setViewMode(QFileDialog.List)
        dlg.setNameFilter("Text files (*.txt)")
        dlg.setFileMode(QFileDialog.ExistingFile)
        # noinspection PyArgumentList
        a = dlg.getOpenFileName(self, 'Open file', os.getcwd()+'/config', 'Text files (*.txt)')
        if a[0] != '':
            self.ui.le_modelPointsFileName.setText(os.path.basename(a[0]))
        else:
            self.logger.warning('selectModelPointsFile -> no file selected')

    def selectAnalyseFileName(self):
        dlg = QFileDialog()
        dlg.setViewMode(QFileDialog.List)
        dlg.setNameFilter("Data Files (*.dat)")
        dlg.setFileMode(QFileDialog.AnyFile)
        # noinspection PyArgumentList
        a = dlg.getOpenFileName(self, 'Open file', os.getcwd()+'/analysedata', 'Data Files (*.dat)')
        if a[0] != '':
            self.ui.le_analyseFileName.setText(os.path.basename(a[0]))
        else:
            self.logger.warning('selectAnalyseFile -> no file selected')

    def showAnalyseWindow(self):
        self.analysePopup.getData()
        self.analysePopup.ui.windowTitle.setText('Analyse:    ' + self.ui.le_analyseFileName.text())
        self.analysePopup.showDecError()
        self.analysePopup.showStatus = True
        self.analysePopup.setVisible(True)

    def showCoordinateWindow(self):
        self.coordinatePopup.showStatus = True
        self.coordinatePopup.setVisible(True)

    def selectImageDirectoryName(self):
        dlg = QFileDialog()
        dlg.setViewMode(QFileDialog.List)
        dlg.setFileMode(QFileDialog.DirectoryOnly)
        # noinspection PyArgumentList
        a = dlg.getExistingDirectory(self, 'Select directory', os.getcwd())
        if len(a) > 0:
            self.ui.le_imageDirectoryName.setText(a)
        else:
            self.logger.warning('selectModelPointsFile -> no file selected')

    def selectHorizonPointsMode(self):
        self.model.loadHorizonPoints(self.ui.le_horizonPointsFileName.text())
        self.coordinatePopup.redrawCoordinateWindow()

    def selectHorizonPointsFileName(self):
        dlg = QFileDialog()
        dlg.setViewMode(QFileDialog.List)
        dlg.setNameFilter("Text files (*.txt)")
        dlg.setFileMode(QFileDialog.ExistingFile)
        # noinspection PyArgumentList
        a = dlg.getOpenFileName(self, 'Open file', os.getcwd()+'/config', 'Text files (*.txt)')
        if a[0] != '':
            self.ui.le_horizonPointsFileName.setText(os.path.basename(a[0]))
            self.model.loadHorizonPoints(os.path.basename(a[0]))
            self.ui.checkUseMinimumHorizonLine.setChecked(False)
            self.coordinatePopup.redrawCoordinateWindow()

    def selectUpdaterFileName(self):
        dlg = QFileDialog()
        dlg.setViewMode(QFileDialog.List)
        dlg.setNameFilter("Application (*.exe)")
        dlg.setFileMode(QFileDialog.ExistingFile)
        # noinspection PyArgumentList
        a = dlg.getOpenFileName(self, 'Open file', 'c:\\', 'Application (*.exe)')
        if a[0] != '':
            self.ui.le_updaterFileName.setText(a[0])

    def shutdownQuit(self):
        self.saveConfig()
        self.commandQueue.put('shutdown')
        time.sleep(1)
        # noinspection PyArgumentList
        QCoreApplication.instance().quit()

    def setHorizonLimitHigh(self):
        _value = int(self.ui.le_horizonLimitHigh.text())
        if _value < 0:
            _value = 0
        elif _value > 90:
            _value = 90
        self.commandQueue.put('Sh+{0:02d}'.format(_value))

    def setHorizonLimitLow(self):
        _value = int(self.ui.le_horizonLimitLow.text())
        if _value < 0:
            _value = 0
        elif _value > 90:
            _value = 90
        self.commandQueue.put('So+{0:02d}'.format(_value))

    def setDualTracking(self):
        _value = self.ui.le_telescopeDualTrack.text()
        if _value == 'ON':
            _value = 0
            self.ui.le_telescopeDualTrack.setText('OFF')
        else:
            _value = 1
            self.ui.le_telescopeDualTrack.setText('ON')
        self.commandQueue.put('Sdat{0:01d}'.format(_value))

    def setUnattendedFlip(self):
        _value = self.ui.le_telescopeUnattendedFlip.text()
        if _value == 'ON':
            _value = 0
            self.ui.le_telescopeUnattendedFlip.setText('OFF')
        else:
            _value = 1
            self.ui.le_telescopeUnattendedFlip.setText('ON')
        self.commandQueue.put('Suaf{0: 01d}'.format(_value))

    def setSlewRate(self):
        _value = int(self.ui.le_slewRate.text())
        if _value < 1:
            _value = 1
        elif _value > 15:
            _value = 15
        self.commandQueue.put('Sw{0:02d}'.format(_value))

    def setRefractionCorrection(self):
        _value = self.ui.le_refractionStatus.text()
        if _value == 'ON':
            _value = 0
            self.ui.le_refractionStatus.setText('OFF')
        else:
            _value = 1
            self.ui.le_refractionStatus.setText('ON')
        self.commandQueue.put('SREF{0: 01d}'.format(_value))

    def mountPosition1(self):
        self.commandQueue.put('PO')                                                                                         # unpark first
        self.commandQueue.put('Sz{0:03d}*00'.format(int(self.ui.le_azParkPos1.text())))                                     # set az
        self.commandQueue.put('Sa+{0:02d}*00'.format(int(self.ui.le_altParkPos1.text())))                                   # set alt
        self.commandQueue.put('MA')                                                                                         # start Slewing

    def mountPosition2(self):
        self.commandQueue.put('PO')                                                                                         # unpark first
        self.commandQueue.put('Sz{0:03d}*00'.format(int(self.ui.le_azParkPos2.text())))                                     # set az
        self.commandQueue.put('Sa+{0:02d}*00'.format(int(self.ui.le_altParkPos2.text())))                                   # set alt
        self.commandQueue.put('MA')                                                                                         # start Slewing

    def mountPosition3(self):
        self.commandQueue.put('PO')                                                                                         # unpark first
        self.commandQueue.put('Sz{0:03d}*00'.format(int(self.ui.le_azParkPos3.text())))                                     # set az
        self.commandQueue.put('Sa+{0:02d}*00'.format(int(self.ui.le_altParkPos3.text())))                                   # set alt
        self.commandQueue.put('MA')                                                                                         # start Slewing

    def mountPosition4(self):
        self.commandQueue.put('PO')                                                                                         # unpark first
        self.commandQueue.put('Sz{0:03d}*00'.format(int(self.ui.le_azParkPos4.text())))                                     # set az
        self.commandQueue.put('Sa+{0:02d}*00'.format(int(self.ui.le_altParkPos4.text())))                                   # set alt
        self.commandQueue.put('MA')                                                                                         # start Slewing

    def mountPosition5(self):
        self.commandQueue.put('PO')                                                                                         # unpark first
        self.commandQueue.put('Sz{0:03d}*00'.format(int(self.ui.le_azParkPos5.text())))                                     # set az
        self.commandQueue.put('Sa+{0:02d}*00'.format(int(self.ui.le_altParkPos5.text())))                                   # set alt
        self.commandQueue.put('MA')                                                                                         # start Slewing

    def mountPosition6(self):
        self.commandQueue.put('PO')                                                                                         # unpark first
        self.commandQueue.put('Sz{0:03d}*00'.format(int(self.ui.le_azParkPos6.text())))                                     # set az
        self.commandQueue.put('Sa+{0:02d}*00'.format(int(self.ui.le_altParkPos6.text())))                                   # set alt
        self.commandQueue.put('MA')                                                                                         # start Slewing
    #
    # mount handling
    #

    @QtCore.Slot(bool)
    def setMountStatus(self, status):
        if status:
            self.ui.btn_driverMountConnected.setStyleSheet('QPushButton {background-color: green;}')
        else:
            self.ui.btn_driverMountConnected.setStyleSheet('QPushButton {background-color: red;}')

    def setShowAlignmentModelMode(self):
        if self.ui.checkPolarPlot.isChecked():
            self.ui.alignErrorStars.setVisible(False)
        else:
            self.ui.alignErrorStars.setVisible(True)

    @QtCore.Slot(dict)
    def fillMountData(self, data):
        if data['Name'] == 'Reply':
            pass
        if data['Name'] == 'GetDualAxisTracking':
            if data['Value'] == '1':
                self.ui.le_telescopeDualTrack.setText('ON')
            else:
                self.ui.le_telescopeDualTrack.setText('OFF')
        if data['Name'] == 'NumberAlignmentStars':
            self.ui.le_alignNumberStars.setText(str(data['Value']))
        if data['Name'] == 'ModelRMSError':
            self.ui.le_alignError.setText(str(data['Value']))
        if data['Name'] == 'ModelStarError':
            if data['Value'] == 'delete':
                self.ui.alignErrorStars.setText('')
            else:
                self.ui.alignErrorStars.setText(self.ui.alignErrorStars.toPlainText() + data['Value'])
                self.ui.alignErrorStars.moveCursor(QTextCursor.End)
        if data['Name'] == 'GetCurrentHorizonLimitLow':
            self.ui.le_horizonLimitLow.setText(str(data['Value']))
        if data['Name'] == 'GetCurrentHorizonLimitHigh':
            self.ui.le_horizonLimitHigh.setText(str(data['Value']))
        if data['Name'] == 'GetCurrentSiteLongitude':
            self.ui.le_siteLongitude.setText(str(data['Value']))
        if data['Name'] == 'GetCurrentSiteLatitude':
            self.ui.le_siteLatitude.setText(str(data['Value']))
        if data['Name'] == 'GetCurrentSiteElevation':
            self.ui.le_siteElevation.setText(str(data['Value']))
        if data['Name'] == 'GetLocalTime':
            self.ui.le_localTime.setText(str(data['Value']))
        if data['Name'] == 'GetTelescopeTempDEC':
            self.ui.le_telescopeTempDECMotor.setText(str(data['Value']))
        if data['Name'] == 'GetRefractionTemperature':
            self.ui.le_refractionTemperature.setText(str(data['Value']))
        if data['Name'] == 'GetRefractionPressure':
            self.ui.le_refractionPressure.setText(str(data['Value']))
        if data['Name'] == 'GetRefractionStatus':
            if data['Value'] == '1':
                self.ui.le_refractionStatus.setText('ON')
            else:
                self.ui.le_refractionStatus.setText('OFF')
        if data['Name'] == 'GetMountStatus':
            self.ui.le_mountStatus.setText(str(self.mount.statusReference[data['Value']]))
        if data['Name'] == 'GetTelescopeDEC':
            self.ui.le_telescopeDEC.setText(data['Value'])
        if data['Name'] == 'GetTelescopeRA':
            self.ui.le_telescopeRA.setText(str(data['Value']))
        if data['Name'] == 'GetTelescopeAltitude':
            self.ui.le_telescopeAltitude.setText(str(data['Value']))
            self.coordinatePopup.ui.le_telescopeAltitude.setText(str(data['Value']))
        if data['Name'] == 'GetTelescopeAzimuth':
            self.ui.le_telescopeAzimut.setText(str(data['Value']))
            self.coordinatePopup.ui.le_telescopeAzimut.setText(str(data['Value']))
        if data['Name'] == 'GetSlewRate':
            self.ui.le_slewRate.setText(str(data['Value']))
        if data['Name'] == 'GetMeridianLimitTrack':
            self.ui.le_meridianLimitTrack.setText(str(data['Value']))
        if data['Name'] == 'GetMeridianLimitSlew':
            self.ui.le_meridianLimitSlew.setText(str(data['Value']))
        if data['Name'] == 'GetUnattendedFlip':
            if data['Value'] == '1':
                self.ui.le_telescopeUnattendedFlip.setText('ON')
            else:
                self.ui.le_telescopeUnattendedFlip.setText('OFF')
        if data['Name'] == 'GetTimeToFlip':
            self.ui.le_timeToFlip.setText(str(data['Value']))
        if data['Name'] == 'GetTimeToMeridian':
            self.ui.le_timeToMeridian.setText(str(data['Value']))
        if data['Name'] == 'GetFirmwareProductName':
            self.ui.le_firmwareProductName.setText(str(data['Value']))
        if data['Name'] == 'GetFirmwareNumber':
            self.ui.le_firmwareNumber.setText(str(data['Value']))
        if data['Name'] == 'GetFirmwareDate':
            self.ui.le_firmwareDate.setText(str(data['Value']))
        if data['Name'] == 'GetFirmwareTime':
            self.ui.le_firmwareTime.setText(str(data['Value']))
        if data['Name'] == 'GetHardwareVersion':
            self.ui.le_hardwareVersion.setText(str(data['Value']))
        if data['Name'] == 'GetTelescopePierSide':
            self.ui.le_telescopePierSide.setText(str(data['Value']))

    @QtCore.Slot(int)
    def setStickStatus(self, status):
        if status == 1:
            self.ui.btn_driverStickConnected.setStyleSheet('QPushButton {background-color: green;}')
        elif status == 2:
            self.ui.btn_driverStickConnected.setStyleSheet('QPushButton {background-color: gray;}')
        else:
            self.ui.btn_driverStickConnected.setStyleSheet('QPushButton {background-color: red;}')

    @QtCore.Slot(dict)
    def fillStickData(self, data):
        # data from Stickstation via signal connected
        self.ui.le_dewPointStick.setText('{0:4.1f}'.format(data['DewPoint']))
        self.ui.le_temperatureStick.setText('{0:4.1f}'.format(data['Temperature']))
        self.ui.le_humidityStick.setText('{0:4.1f}'.format(data['Humidity']))
        self.ui.le_pressureStick.setText('{0:4.1f}'.format(data['Pressure']))

    @QtCore.Slot(int)
    def setWeatherStatus(self, status):
        if status == 1:
            self.ui.btn_driverWeatherConnected.setStyleSheet('QPushButton {background-color: green;}')
        elif status == 2:
            self.ui.btn_driverWeatherConnected.setStyleSheet('QPushButton {background-color: grey;}')
        else:
            self.ui.btn_driverWeatherConnected.setStyleSheet('QPushButton {background-color: red;}')

    @QtCore.Slot(dict)
    def fillWeatherData(self, data):
        # data from Stickstation via signal connected
        self.ui.le_dewPointWeather.setText('{0:4.1f}'.format(data['DewPoint']))
        self.ui.le_temperatureWeather.setText('{0:4.1f}'.format(data['Temperature']))
        self.ui.le_humidityWeather.setText('{0:4.1f}'.format(data['Humidity']))
        self.ui.le_pressureWeather.setText('{0:4.1f}'.format(data['Pressure']))
        self.ui.le_cloudCoverWeather.setText('{0:4.1f}'.format(data['CloudCover']))
        self.ui.le_rainRateWeather.setText('{0:4.1f}'.format(data['RainRate']))
        self.ui.le_windSpeedWeather.setText('{0:4.1f}'.format(data['WindSpeed']))
        self.ui.le_windDirectionWeather.setText('{0:4.1f}'.format(data['WindDirection']))

    @QtCore.Slot(bool)
    def setCameraPlateStatus(self, status):
        if status:
            self.ui.btn_camPlateConnected.setStyleSheet('QPushButton {background-color: green;}')
        else:
            self.ui.btn_camPlateConnected.setStyleSheet('QPushButton {background-color: red;}')

    @QtCore.Slot(int)
    def setDomeStatus(self, status):
        if status == 1:
            self.ui.btn_domeConnected.setStyleSheet('QPushButton {background-color: green;}')
        elif status == 2:
            self.ui.btn_domeConnected.setStyleSheet('QPushButton {background-color: grey;}')
        else:
            self.ui.btn_domeConnected.setStyleSheet('QPushButton {background-color: red;}')

    def mainLoop(self):
        while not self.mountDataQueue.empty():                                                                              # checking data transfer from mount to GUI
            data = self.mountDataQueue.get()                                                                                # get the data from the queue
            self.fillMountData(data)                                                                                        # write dta in gui
            self.mountDataQueue.task_done()
        while not self.messageQueue.empty():                                                                                # do i have error messages ?
            text = self.messageQueue.get()                                                                                  # get the message
            self.ui.errorStatus.setText(self.ui.errorStatus.toPlainText() + text + '\n')                                    # write it to window
            self.messageQueue.task_done()
            self.ui.errorStatus.moveCursor(QTextCursor.End)                                                                 # move cursor
        while not self.modelLogQueue.empty():                                                                               # checking if in queue is something to do
            text = self.modelLogQueue.get()                                                                                 # if yes, getting the work command
            if text == 'delete':                                                                                            # delete logfile for modeling
                self.coordinatePopup.ui.modellingLog.setText('')                                                            # reset window text
            elif text == 'backspace':
                self.coordinatePopup.ui.modellingLog.setText(self.coordinatePopup.ui.modellingLog.toPlainText()[:-6])
            else:
                self.coordinatePopup.ui.modellingLog.setText(self.coordinatePopup.ui.modellingLog.toPlainText() + text)     # otherwise add text at the end
            self.coordinatePopup.ui.modellingLog.moveCursor(QTextCursor.End)                                                # and move cursor up
            self.modelLogQueue.task_done()
        # noinspection PyCallByClass,PyTypeChecker
        QTimer.singleShot(200, self.mainLoop)                                                                               # 200ms repeat time cyclic


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")

    BUILD_NO = '2.1.25'

    def except_hook(typeException, valueException, tbackException):                                                         # manage unhandled exception here
        logging.error('Exception: type:{0} value:{1} tback:{2}'.format(typeException, valueException, tbackException))      # write to logger
        sys.__excepthook__(typeException, valueException, tbackException)                                                   # then call the default handler

    name = 'mount.{0}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
    handler = logging.handlers.RotatingFileHandler(name, backupCount=3)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(threadName)15s] - %(message)s',
                        handlers=[handler], datefmt='%Y-%m-%d %H:%M:%S')
    if not os.path.isdir(os.getcwd() + '/analysedata'):                                                                     # if analyse dir doesn't exist, make it
        os.makedirs(os.getcwd() + '/analysedata')                                                                           # if path doesn't exist, generate is
    if not os.path.isdir(os.getcwd() + '/images'):                                                                          # if images dir doesn't exist, make it
        os.makedirs(os.getcwd() + '/images')                                                                                # if path doesn't exist, generate is
    if not os.path.isdir(os.getcwd() + '/config'):                                                                          # if config dir doesn't exist, make it
        os.makedirs(os.getcwd() + '/config')                                                                                # if path doesn't exist, generate is
    logging.error('----------------------------------------')                                                               # start message logger
    logging.error('MountWizzard v' + BUILD_NO + ' started !')                                                                # start message logger
    logging.error('----------------------------------------')                                                               # start message logger
    logging.error('main           -> working directory: {0}'.format(os.getcwd()))
    app = QApplication(sys.argv)                                                                                            # built application
    sys.excepthook = except_hook                                                                                            # manage except hooks for logging
    # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
    app.setStyle(QStyleFactory.create('Fusion'))                                                                            # set theme
    mountApp = MountWizzardApp()                                                                                            # instantiate Application
    mountApp.loadConfig()
    mountApp.show()
    # if mountApp.analysePopup.showStatus:                                                                                  # if windows was shown last run, open it directly
    #    mountApp.showAnalyseWindow()                                                                                       # show it
    if mountApp.coordinatePopup.showStatus:                                                                                 # if windows was shown last run, open it directly
        mountApp.coordinatePopup.redrawCoordinateWindow()                                                                   # update content
        mountApp.showCoordinateWindow()                                                                                     # show it
    sys.exit(app.exec_())                                                                                                   # close application
