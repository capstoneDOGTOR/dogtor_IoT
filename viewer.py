import struct
import os
import pyqtgraph
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QDialog
from PyQt5.QtCore import pyqtSlot, QTimer, Qt, QThread, pyqtSignal
import pandas as pd
from pandas import DataFrame
import serial
import time
import binascii
import glob
import cv2
from datetime import datetime
import numpy as np

import boto3
from multiprocessing import Process, Array
import sys
from botocore.exceptions import ClientError

import threading    
import bluepy.btle
from bluepy.btle import *
import boto3

class Window(QWidget):
    graph_send = pyqtSignal(list)
    graphPen_send = pyqtSignal(list)
    indicator_send = pyqtSignal(list)
    saveVideo_send = pyqtSignal()

    def __init__(self):
        super().__init__()
        # layout
        vBox = QVBoxLayout()
        hBox = []
        iBox = []
        # self.stringAxis = []
        self.graphList = []
        self.graphPen = []
        self.groupBoxList = []
        self.indicatorList = []

        hBox.append(QHBoxLayout())
        hBox.append(QHBoxLayout())
        hBox.append(QHBoxLayout())

        iBox.append(QVBoxLayout())
        iBox.append(QVBoxLayout())
        iBox.append(QVBoxLayout())
        iBox.append(QVBoxLayout())
        iBox.append(QVBoxLayout())
        iBox.append(QVBoxLayout())

        font_tick = QtGui.QFont('Bahnschrift SemiLight', 8)
        font = QtGui.QFont('Bahnschrift SemiLight', 12)
        font.setBold(True)
        self.setFont(font)
        labelStyle = {'color': '#828282', 'font-size': '9pt'}

        # graph
        # self.stringAxis.append(pyqtgraph.AxisItem(orientation='bottom'))
        # self.stringAxis.append(pyqtgraph.AxisItem(orientation='bottom'))

        # self.graphList.append(pyqtgraph.PlotWidget(
        #     axisItems={'bottom': self.stringAxis[0]}))
        # self.graphList.append(pyqtgraph.PlotWidget(
        #     axisItems={'bottom': self.stringAxis[1]}))

        self.graphList.append(pyqtgraph.PlotWidget())

        # self.graphList.append(pyqtgraph.PlotWidget())

        self.graphList[0].setTitle("AccelZ", color="#828282", size="12pt")
        # self.graphList[1].setTitle("AccelZ_o", color="#828282", size="12pt")

        for graph in self.graphList:
            graph.getPlotItem().titleLabel.item.setFont(font)
            graph.setLabel('left', 'AccelZ', units='g', **labelStyle)
            graph.setLabel('bottom', 'Sensor Data', **labelStyle)
            graph.getAxis('bottom').setStyle(
                tickFont=font_tick, tickTextOffset=6)
            graph.getAxis('left').setStyle(
                tickFont=font_tick, tickTextOffset=6)
            graph.showGrid(x=True, y=True)
            graph.setBackground((240, 240, 240))
            # graph.enableAutoRange(axis='x')
            graph.enableAutoRange(axis='y', y=100)

        self.graphPen.append(self.graphList[0].plot(pen=pyqtgraph.mkPen(
            color=(44, 106, 180), width=0, style=QtCore.Qt.SolidLine)))
        # self.graphPen.append(self.graphList[1].plot(pen=pyqtgraph.mkPen(
        #     color=(44, 106, 180), width=1, style=QtCore.Qt.SolidLine)))

        self.groupBoxList.append(QGroupBox('Count'))
        self.groupBoxList.append(QGroupBox('Temp(°C)'))
        self.groupBoxList.append(QGroupBox('Pressure(kPa)'))
        self.groupBoxList.append(QGroupBox('Volt(V) '))
        self.groupBoxList.append(QGroupBox('Speed(km/h)'))
        self.groupBoxList.append(QGroupBox('Data loss'))

       
        # self.groupBoxList.append(QGroupBox('Option'))
        self.indicatorList.append(QLabel('0', self))
        self.indicatorList.append(QLabel('0', self))
        self.indicatorList.append(QLabel('0', self))
        self.indicatorList.append(QLabel('0', self))
        self.indicatorList.append(QLabel('0', self))
        self.indicatorList.append(QLabel('0', self))

        indicatorFont = self.indicatorList[0].font()
        indicatorFont.setFamily('Bahnschrift SemiLight')
        indicatorFont.setPointSize(15)
        indicatorFont.setBold(True)

        self.indicatorList[0].setStyleSheet("color:rgb(120, 120, 120);" "background-color:rgb(250,250,250);"
                                            "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                            "border-radius: 5px")
        self.indicatorList[1].setStyleSheet("color:rgb(203, 26, 126);" "background-color:rgb(250,250,250);"
                                            "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                            "border-radius: 5px")
        self.indicatorList[2].setStyleSheet("color:rgb(44, 106, 180);" "background-color:rgb(250,250,250);"
                                            "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                            "border-radius: 5px")
        self.indicatorList[3].setStyleSheet("color:rgb(120, 120, 120);" "background-color:rgb(250,250,250);"
                                            "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                            "border-radius: 5px")
        self.indicatorList[4].setStyleSheet("color:rgb(120, 120, 120);" "background-color:rgb(250,250,250);"
                                            "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                            "border-radius: 5px")
        self.indicatorList[5].setStyleSheet("color:rgb(120, 120, 120);" "background-color:rgb(250,250,250);"
                                            "border-style: solid;" "border-width: 1px;" "border-color: rgb(200,200,200);"
                                            "border-radius: 5px")

                                            
        for i in range(len(self.indicatorList)):
            self.indicatorList[i].setAlignment(Qt.AlignCenter)
            self.indicatorList[i].setFont(indicatorFont)
            iBox[i].addWidget(self.indicatorList[i])
            self.groupBoxList[i].setLayout(iBox[i])
            hBox[2].addWidget(self.groupBoxList[i])

        hBox[0].addWidget(self.graphList[0])
        # hBox[1].addWidget(self.graphList[1])

        vBox.addLayout(hBox[0])
        # vBox.addLayout(hBox[1])
        vBox.addLayout(hBox[2])

        self.setLayout(vBox)
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle("MHE Smart Wheel")

        self.show()

        self.background = BackgroundGUI()
        self.rcv_data = RCV_DATA()


        self.rcv_data.data_send.connect(self.background.updateGraph)
        self.rcv_data.TPVdata_send.connect(self.background.updateindicator)
        self.rcv_data.control_cam.connect(self.rcv_cam.control_CAM)


        self.graph_send.connect(self.background.rcv_graph)
        self.graphPen_send.connect(self.background.rcv_pen)
        self.indicator_send.connect(self.background.rcv_indicator)

        self.rcv_cam.frame_send.connect(self.cam_win.setFrame)

        self.graph_send.emit(self.graphList)
        self.graphPen_send.emit(self.graphPen)
        self.indicator_send.emit(self.indicatorList)

        self.saveVideo_send.connect(self.rcv_cam.saveVideo)
        self.saveVideo_send.connect(self.cam_win.closeWindow)
        self.cam_win.saveVideo.connect(self.rcv_cam.saveVideo)

        self.gps.send_speed.connect(self.background.get_speed)
        self.gps.send_sppedToCSV.connect(self.rcv_data.get_speed)
        self.background.start()
        self.rcv_data.start()

    
    
    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.saveVideo_send.emit()
        return super().closeEvent(a0)

    def keyReleaseEvent(self, e):
        print(e.key())
        if e.key() == Qt.Key_Escape :
            self.saveVideo_send.emit()
            self.close()
        
####################################################################################################
####################################################################################################
class BackgroundGUI (QThread):
    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.isRun = False
        self.accel_z = []
        self.accel_z_o = []
        self.sequence = []
        self.offet = 0
        self.graphList = []
        self.graphPen = []
        self.indicatorList = []
        self.count = 0
        self.data_size = 1500
        self.sequenceREVERS = [i for i in range(-self.data_size-1, 0)]
        self.tempGraph = pyqtgraph.PlotWidget()
        self.tempGraph.plot(pen=pyqtgraph.mkPen(
            color=(44, 106, 180), width=0, style=QtCore.Qt.SolidLine))

    def run(self):
        return

    @pyqtSlot(list)
    def rcv_indicator(self, indicatorList):
        self.indicatorList = indicatorList

    @pyqtSlot(list)
    def rcv_graph(self, graphList):
        self.graphList = graphList

    @pyqtSlot(list)
    def rcv_pen(self, penList):
        self.graphPen = penList

    @pyqtSlot(list)
    def updateGraph(self, sensorData):
        if sensorData:
            self.count = sensorData[0]
            self.accel_z.append(sensorData[1])
            # self.accel_z_o.append(sensorData[2])
            if len(self.sequence) > self.data_size:
                del self.accel_z[0]
                # del self.accel_z_o[0]
                self.graphList[0].setXRange(-self.data_size, 0)
                # print(len (self.sequenceREVERS) , len(self.accel_z))
                self.graphPen[0].setData(self.sequenceREVERS, self.accel_z)
                self.indicatorList[0].setText(str(sensorData[0])) #cnt
                self.indicatorList[5].setText(str(sensorData[4])) #dataloss     
            else:
                self.sequence.append(len(self.sequence))
                self.graphList[0].setXRange(self.data_size, 0)
                self.graphPen[0].setData(self.sequence, self.accel_z)
                self.indicatorList[0].setText(str(sensorData[0])) #cnt
                self.indicatorList[5].setText(str(sensorData[4])) #dataloss     

            # self.indicatorList[1].setText(str(sensorData[1]))
            # self.indicatorList[2].setText(str(sensorData[2]))
        else:
            pass
        
    @pyqtSlot(list)
    def updateindicator(self, tpvData):
        self.indicatorList[1].setText(str(tpvData[0]))
        self.indicatorList[2].setText(str(format(tpvData[1], ".2f")))
        self.indicatorList[3].setText(str(tpvData[2])) #voltage

    @pyqtSlot(str)
    def get_speed(self, speed):
        self.indicatorList[4].setText(speed)



####################################################################################################
####################################################################################################
class RCV_DATA (QThread):
    data_send = pyqtSignal(list)
    TPVdata_send = pyqtSignal(list)
    control_cam = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.isRun = False

        self.sensorData = []
        self.tpvData = []
        self.compData = []

    
    def sendData(self):
        self.data_send.emit(self.sensorData)


    def run(self):
        delegate = []
        peripheral = self.findDevice()
        if len(peripheral) :
            pass
        else :
            print ("The device cannot be found")
            return 
        for device in peripheral :
            delegate.append(MyDelegate(device))
            device.setDelegate(delegate[-1])
            print(device.addr," : Notification is turned on for Raw_data")
        # Peripherals[iter].writeCharacteristic(hMotionC, struct.pack('<bb', 0x01, 0x00), withResponse=True)
        # t = threading.Thread(target = RCV_IMU, args = (device))
        # threads.append(t)
        p = peripheral[-1]
        p.writeCharacteristic(36, struct.pack('<bb', 0x01, 0x00), True)
        while (True) :
            if p.waitForNotifications(1.0) :
                pass
            else :
                print("Waiting")
        pass

    def findDevice (self) : 
        target_name = "BT04-A"   # target device name
        target_address = None     # target device address
        scanner = Scanner()
        devices = scanner.scan(3.0)
        peripheral = []
        for dev in devices:
            # print (dev)
            for (_, _, value) in dev.getScanData():
                if target_name in value: 
                    target_address = dev.addr
                    print(target_address)
                    # create peripheral class
                    peripheral.append(Peripheral(target_address, "public"))
                    print("I Find Device")
        return peripheral



class MyDelegate(DefaultDelegate):                    #Constructor (run once on startup)
    def __init__(self, params):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):      #func is caled on notifications
        # motion_data = struct.unpack('hhhhhhhhh',data) # 18byte
        print(data)
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)


        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
