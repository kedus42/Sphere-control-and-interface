import sys, os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
import paho.mqtt.client as mqttClient

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(700, 200, 580, 250)
        self.setStyleSheet("background : grey")

        self.b8 = QtWidgets.QPushButton(self)
        self.b8.setGeometry(50, 75, 100, 100)
        self.b8.setText("Set x,y target")
        self.b8.clicked.connect(self.b8_clicked)

        self.b9 = QtWidgets.QPushButton(self)
        self.b9.setGeometry(250, 75, 100, 100)
        self.b9.setText("Set target \n direction and\n distance")
        self.b9.clicked.connect(self.b9_clicked)

        self.b10 = QtWidgets.QPushButton(self)
        self.b10.setGeometry(450, 75, 100, 100)
        self.b10.setText("Set distance")
        self.b10.clicked.connect(self.b10_clicked)

    def b8_clicked(self):
        self.xy=QInputDialog(self)
        self.x, xpressed=self.xy.getInt(self,"Set x target", "", 0, 0, 250, 1)
        self.y, ypressed=self.xy.getInt(self,"Set y target", "", 0, 0, 250, 1)
        os.system("mosquitto_pub -h 192.168.43.139 -t \"gui\" -m \"xy"+" "+str(self.x)+" "+str(self.y)+" \"")

    
    def b9_clicked(self):
        self.direction_dist=QInputDialog(self)
        self.direction, direction_pressed=self.direction_dist.getInt(self,"Set direction", "", 0, -180, 180, 1)
        self.distance, distance_pressed=self.direction_dist.getInt(self,"Set distance", "", 0, 0, 250, 1)
        os.system("mosquitto_pub -h 192.168.43.139 -t \"gui\" -m \"dd"+" "+str(self.direction)+" "+str(self.distance)+" \"")

    def b10_clicked(self):
        self.set_loopl=QInputDialog(self)
        self.new_loopl, loopl_pressed=self.set_loopl.getInt(self, "Set loopl", "", 0, 0, 250, 1)
        os.system("mosquitto_pub -h 192.168.43.139 -t \"gui\" -m \"di"+" "+str(self.new_loopl)+" \"")

app=QApplication(sys.argv)
win=window()
win.show()
sys.exit(app.exec_())