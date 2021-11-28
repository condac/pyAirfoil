import parser
import traceback
import os
import sys
import json
from PyQt5 import QtWidgets, uic

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

import plotWidget

SRC_PATH = os.path.dirname(os.path.abspath(__file__))

af = parser.AirfoilFile()
af.readFromFile("test.afl")



class MainW(QMainWindow):
    def __init__(self):
        super(MainW,self).__init__()

        self.initUI()

    def initUI(self):
        
        self.currentFileName = ""

        self.ui = uic.loadUi(SRC_PATH+os.sep+".."+os.sep+"ui"+os.sep+"main.ui", self)
        try:
            f = open(SRC_PATH + os.sep + ".." + os.sep + "VERSION", "r")
            ver = f.read()
            print(ver)
            self.versionstring = ver.replace("\n", "")
        except Exception as err:
            print(err)
            self.versionstring = os.environ.get("GIT_VERSION", ".v")

        #versionstring = os.environ.get("GIT_VERSION", "v0.0.0")
        self.setWindowTitle("pyAirfoil "+self.versionstring)
        
        self.plot = plotWidget.PlotWidget(af)
        self.ui.gridLayout_3.addWidget(self.plot, 0, 2, 14, 4)
        
        self.ui.updateButton.clicked.connect(self.onupdateButton)
        self.ui.updateGraphButton.clicked.connect(self.onupdateGraphButton)
        self.ui.actionOpen.triggered.connect(self.onActionOpen)
        self.ui.actionSave.triggered.connect(self.onActionSave)
        self.ui.actionSave_as.triggered.connect(self.onActionSaveAs)
        self.ui.actionExport_X_Plane_Airfoil.triggered.connect(self.onActionExport)
        self.ui.actionImport_X_Plane_Airfoil.triggered.connect(self.onActionImport)


    def onActionOpen(self):
        global af
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Load configfile")
        dialog.setNameFilter("pyAirfoil File (*.pyafl)")
        dialog.setFileMode(QFileDialog.ExistingFile)
        
        if dialog.exec_() == QDialog.Accepted:
            filename = str(dialog.selectedFiles()[0])
            af = parser.AirfoilFile()
            af.loadConfigFile(filename)
            self.setUiValues()
            self.plot = plotWidget.PlotWidget(af)
            self.ui.gridLayout_3.addWidget(self.plot, 0, 2, 14, 4)
            
            fname = QFileInfo(filename).fileName()
            self.setWindowTitle(fname+" ("+filename+") pyAirfoil "+self.versionstring)
            self.currentFileName = filename

        return
        
    def onActionSave(self): 
        if (self.currentFileName != ""):
            af.saveConfigFile(self.currentFileName)
        else:
            self.onActionSaveAs()
        return
        
    def onActionSaveAs(self):
        filename = QFileDialog.getSaveFileName(self, "Save configfile", "", filter="pyAirfoil File (*.pyafl)")

        # dialog = QFileDialog(self)
        # dialog.setWindowTitle("Save configfile")
        # dialog.setNameFilter("pyAirfoil File (*.pyafl)")
        # dialog.setFileMode(QFileDialog.AnyFile)
        
        #if dialog.exec_() == QDialog.Accepted:
        if filename:
            print(filename)
            (filename, filetype) = filename
            if not filename.endswith(".pyafl"):
                filename = filename +".pyafl"
            #filename = str(dialog.selectedFiles()[0])
            af.saveConfigFile(filename)
            
            fname = QFileInfo(filename).fileName()
            self.setWindowTitle(fname+" ("+filename+") pyAirfoil "+self.versionstring)
            self.currentFileName = filename
            
        return
        
    def onActionExport(self):
        filename = QFileDialog.getSaveFileName(self, "Export X-Plane Airfoil", "", filter="Airfoil File (*.afl)")

        if filename:
            print(filename)
            (filename, filetype) = filename
            if not filename.endswith(".afl"):
                filename = filename +".afl"
            af.saveFile(filename)
                
        # dialog = QFileDialog(self)
        # dialog.setWindowTitle("Export X-Plane Airfoil")
        # dialog.setNameFilter("Airfoil File (*.afl)")
        # dialog.setFileMode(QFileDialog.AnyFile)
        # 
        # if dialog.exec_() == QDialog.Accepted:
        #     filename = str(dialog.selectedFiles()[0])
        #     af.saveFile(filename)
        return
        
    def onActionImport(self):
        global af
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Import X-Plane Airfoil")
        dialog.setNameFilter("Airfoil File (*.afl)")
        dialog.setFileMode(QFileDialog.ExistingFile)
        
        if dialog.exec_() == QDialog.Accepted:
            filename = str(dialog.selectedFiles()[0])
            af = parser.AirfoilFile()
            af.readFromFile(filename)
        return
    
    def onupdateGraphButton(self):
        self.plot = plotWidget.PlotWidget(af)
        self.ui.gridLayout_3.addWidget(self.plot, 0, 2, 14, 4)
        
    def onupdateButton(self):
        print("update")
        self.readUiValues()
        
        # Lift
        if af.c["u_liftPoints"]:
            af.createDataFromPoints(af.c["cl"], af.c["u_liftPointsText"], multi=af.c["u_liftMulti"])
            
        if af.c["u_liftSym"]:
            af.makeSymetric(af.c["cl"])
        
        #Drag
        if af.c["u_dragSin"]:
            af.createDrag(af.c["u_dragMin"], af.c["u_dragMax"])
        if af.c["u_dragPoints"]:
            af.createDataFromPoints(af.c["cd"], af.c["u_dragPointsText"])
        
        if af.c["u_dragSym"]:
            af.makeSymetricAbs(af.c["cd"])
        
        
        #Pitch
        if af.c["u_pitchPoints"]:
            af.createDataFromPoints(af.c["cm"], af.c["u_pitchPointsText"])
        if af.c["u_pitchSym"]:
            af.makeSymetric(af.c["cm"])
        
            
        self.plot = plotWidget.PlotWidget(af)
        self.ui.gridLayout_3.addWidget(self.plot, 0, 2, 14, 4)

        #af.saveFile("output.afl")
        #af.saveConfigFile("output.pyafl")

    def readUiValues(self):
        af.c["u_liftSym"] = self.ui.checkBox_liftSym.isChecked()
        af.c["u_liftPoints"] = self.ui.checkBox_liftPoints.isChecked()
        af.c["u_liftMulti"] = self.ui.liftMulti.value()
        af.c["u_liftPointsText"] = self.ui.textEditLiftPoints.toPlainText()
        
        # Drag
        af.c["u_dragSym"] = self.ui.checkBox_dragSym.isChecked()
        af.c["u_dragKeep"] = self.ui.checkBox_dragKeep.isChecked()
        af.c["u_dragPoints"] = self.ui.checkBox_dragPoints.isChecked()
        af.c["u_dragSin"] = self.ui.checkBox_dragSin.isChecked()
        #af.c["u_dragMulti"] = self.ui.dragMulti.value()
        af.c["u_dragMin"] = self.ui.dragMin.value()
        af.c["u_dragMax"] = self.ui.dragMax.value()
        af.c["u_dragPointsText"] = self.ui.textEditDragPoints.toPlainText()
        
        # pitch
        af.c["u_pitchSym"] = self.ui.checkBox_pitchSym.isChecked()
        af.c["u_pitchPoints"] = self.ui.checkBox_pitchPoints.isChecked()
        af.c["u_pitchPointsText"] = self.ui.textEditPitchPoints.toPlainText()
        
        # dataheader stuff
        
        af.c["dh_aMin"] = self.ui.dh_aMin.value()
        af.c["dh_aMax"] = self.ui.dh_aMax.value()
        af.c["h_mach"] = 0.970
        
    def setUiValues(self):
        self.ui.checkBox_liftSym.setChecked(af.c["u_liftSym"])# = self.ui.checkBox_liftSym.isChecked()
        self.ui.checkBox_liftPoints.setChecked(af.c["u_liftPoints"])
        self.ui.liftMulti.setValue(af.c["u_liftMulti"])# = self.ui.liftMulti.value()
        self.ui.textEditLiftPoints.setText(af.c["u_liftPointsText"]) # = self.ui.textEditLiftPoints.toPlainText()
        
        # Drag
        self.ui.checkBox_dragSym.setChecked(af.c["u_dragSym"])# = self.ui.checkBox_liftSym.isChecked()
        self.ui.checkBox_dragKeep.setChecked(af.c["u_dragKeep"])
        self.ui.checkBox_dragPoints.setChecked(af.c["u_dragPoints"])# = self.ui.checkBox_liftSym.isChecked()
        self.ui.checkBox_dragSin.setChecked(af.c["u_dragSin"])
        #self.ui.liftMulti.setValue(af.c["u_liftMulti"])# = self.ui.liftMulti.value()
        self.ui.dragMin.setValue(af.c["u_dragMin"])
        self.ui.dragMax.setValue(af.c["u_dragMax"])
        self.ui.textEditDragPoints.setText(af.c["u_dragPointsText"]) # = self.ui.textEditLiftPoints.toPlainText()
        
        
        # Pitch
        self.ui.checkBox_pitchSym.setChecked(af.c["u_pitchSym"])# = self.ui.checkBox_liftSym.isChecked()
        self.ui.checkBox_pitchPoints.setChecked(af.c["u_pitchPoints"])
        self.ui.textEditPitchPoints.setText(af.c["u_pitchPointsText"]) # = self.ui.textEditLiftPoints.toPlainText()

        # dataheader stuff
        if ("dh_aMin" in af.c):
            self.ui.dh_aMin.setValue( float(af.c["dh_aMin"]) ) 
            self.ui.dh_aMax.setValue( float(af.c["dh_aMax"])  )

if __name__ == "__main__":
    
    try:
        app = QApplication(sys.argv)

        win = MainW()
        win.show()
        sys.exit(app.exec_())
    except Exception as err:
        exception_type = type(err).__name__
        print(exception_type)
        #nl.netLog(f"exception {exception_type}")
        #nl.netLog(f"stacktrace {traceback.format_exc()}")
        print(traceback.format_exc())
        os._exit(1)