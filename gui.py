import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(700, 200, 580, 500)
        self.setStyleSheet("background : grey")

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setGeometry(150, 200, 110, 100)
        self.b1.setText("Center tilt")
        #self.b1.clicked.connect(self.fire)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setGeometry(100, 50, 100, 100)
        self.b2.setText("ʌ\n|")
        #self.b2.clicked.connect(self.frwd)

        self.b3 = QtWidgets.QPushButton(self)
        self.b3.setGeometry(225, 50, 100, 100)
        self.b3.setText("| ʌ |\n|  |  |")
        #self.b3.clicked.connect(self.frwd)

        self.b4 = QtWidgets.QPushButton(self)
        self.b4.setGeometry(100, 350, 100, 100)
        self.b4.setText("|\nv")
        #self.b4.clicked.connect(self.bckwd)

        self.b5 = QtWidgets.QPushButton(self)
        self.b5.setGeometry(225, 350, 100, 100)
        self.b5.setText("|  |  |\n| v |")
        #self.b5.clicked.connect(self.frwd)

        self.b6 = QtWidgets.QPushButton(self)
        self.b6.setGeometry(300, 200, 80, 100)
        self.b6.setText(">")
        #self.b6.clicked.connect(self.right)

        self.b7 = QtWidgets.QPushButton(self)
        self.b7.setGeometry(30, 200, 80, 100)
        self.b7.setText("<")
        #self.b7.clicked.connect(self.left)

        self.b8 = QtWidgets.QPushButton(self)
        self.b8.setGeometry(450, 50, 100, 100)
        self.b8.setText("Set x,y target")
        self.b8.clicked.connect(self.b8_clicked)

        self.b9 = QtWidgets.QPushButton(self)
        self.b9.setGeometry(450, 200, 100, 100)
        self.b9.setText("Set target \n direction and\n distance")
        self.b9.clicked.connect(self.b9_clicked)

        self.b10 = QtWidgets.QPushButton(self)
        self.b10.setGeometry(450, 350, 100, 100)
        self.b10.setText("Set distance")
        self.b10.clicked.connect(self.b10_clicked)

    def b8_clicked(self):
        self.xy=QInputDialog(self)
        self.x, xpressed=self.xy.getInt(self,"Set x target", "", 0, 0, 250, 1)
        self.y, ypressed=self.xy.getInt(self,"Set y target", "", 0, 0, 250, 1)
    
    def b9_clicked(self):
        self.direction_dist=QInputDialog(self)
        self.direction, direction_pressed=self.direction_dist.getInt(self,"Set direction", "", 0, -180, 180, 1)
        self.distance, distance_pressed=self.direction_dist.getInt(self,"Set distance", "", 0, 0, 250, 1)

    def b10_clicked(self):
        self.set_loopl=QInputDialog(self)
        self.new_loopl, loopl_pressed=self.set_loopl.getInt(self, "Set loopl", "", 0, 0, 250, 1)

app=QApplication(sys.argv)
win=window()
win.show()
sys.exit(app.exec_())