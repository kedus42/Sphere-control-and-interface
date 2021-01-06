#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
import serial
import os 
from Adafruit_BNO055 import BNO055
import time
import math
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog

M3_CW=17
M3_CCW=27
PWM3=13

M4_CW=22
M4_CCW=23
PWM4=19

bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
bno.begin()

ser=serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

class sphere:
    loopl=156
    mdelay=50
    o_range=5
    bdist=25
    sdist=40
    mpos=0
    limit=5
    def __init__(self):
        self.loopl=156
        self.mdelay=50
        self.o_range=5
        self.bdist=25
        self.sdist=40
        self.mpos=0
        self.limit=5
        
        GPIO.setmode(GPIO.BCM)   
        GPIO.setup(M3_CW, GPIO.OUT)
        GPIO.setup(M3_CCW, GPIO.OUT) 
        GPIO.setup(PWM3, GPIO.OUT) 
        GPIO.setup(M4_CW, GPIO.OUT) 
        GPIO.setup(M4_CCW, GPIO.OUT) 
        GPIO.setup(PWM4, GPIO.OUT)

    def right_turn(self, k=1, d=sdist):
        GPIO.output(M3_CW, GPIO.HIGH)
        GPIO.output(M3_CCW, GPIO.LOW)
        GPIO.output(PWM3, GPIO.HIGH)
        GPIO.output(M4_CCW, GPIO.HIGH)
        GPIO.output(M4_CW, GPIO.LOW)
        GPIO.output(PWM4, GPIO.HIGH)
        time.sleep(float((float(d)*float(k))/float(1000)))
        GPIO.output(M3_CW, GPIO.LOW)
        GPIO.output(M3_CCW, GPIO.LOW)
        GPIO.output(PWM3, GPIO.LOW)
        GPIO.output(M4_CW, GPIO.LOW)
        GPIO.output(M4_CCW, GPIO.LOW)
        GPIO.output(PWM4, GPIO.LOW)
    
    def left_turn(self, k=1, d=sdist):
        GPIO.output(M4_CW, GPIO.HIGH)
        GPIO.output(M4_CCW, GPIO.LOW)
        GPIO.output(PWM4, GPIO.HIGH)
        GPIO.output(M3_CCW, GPIO.HIGH)
        GPIO.output(M3_CW, GPIO.LOW)
        GPIO.output(PWM3, GPIO.HIGH)
        time.sleep(float((float(d)*float(k))/float(1000)))
        GPIO.output(M4_CW, GPIO.LOW)
        GPIO.output(M4_CCW, GPIO.LOW)
        GPIO.output(PWM4, GPIO.LOW)
        GPIO.output(M3_CW, GPIO.LOW)
        GPIO.output(M3_CCW, GPIO.LOW)
        GPIO.output(PWM3, GPIO.LOW)

    def adjust_tilt(self, target=0):
        i=0
        while (i<10):
            y,r,p=bno.read_euler()
            if r > target+5:
                self.left_turn(d=self.sdist)
            if r < target-5:
                self.right_turn(d=self.sdist)
            i+=1
            time.sleep(1)
        self.mpos=0

    def cc_motion(self, command='w', facing_target=1, user_def_target=0):
        if facing_target:
                target ,r, p = bno.read_euler()
        else:
                target = user_def_target
        ser.write(command.encode('utf-8'))
        time.sleep(1)
        i=0
        while (i<self.loopl):
                y,r,p=bno.read_euler()
                if y < 180:
                        if abs(y-target) < y+abs(360-target):
                                error = y-target
                        else:
                                error = y+(360-target)
                else:
                        if abs(y-target) < target+abs(360-y):
                                error = y-target
                        else:     
                                error = -1*(target + (360-y))
                print(target, y, error)
                if error <= -5:
                        if command == 'w':
                                if self.mpos<self.limit:
                                        self.right_turn(d=self.bdist)
                                        print("Right correction")
                                        self.mpos+=1
                        else:
                                if self.mpos>(-1*self.limit):
                                        self.left_turn(d=self.bdist)
                                        self.mpos-=1        
                elif error >= 5:
                        if command == 'w':
                                if self.mpos>(-1*self.limit):
                                        self.left_turn(d=self.bdist)
                                        print("Left correction")
                                        self.mpos-=1
                        else:
                                if self.mpos<self.limit:
                                        self.right_turn(d=self.bdist)
                                        self.mpos+=1
                i+=1
                time.sleep((float(float((float(2)*float(self.mdelay))/float(1000)))-float(float(self.bdist)/float(1000))))
        self.adjust_tilt()
    
    def send_to_arduino(self, command):
        ser.write(command.encode('utf-8'))
        time.sleep(1.5)
    
    def set_loopl(self, loopl):
        self.loopl=loopl
        command=str(self.loopl)
        ser.write(command.encode('utf-8'))
        time.sleep(1.5)
    
    def increase_loopl(self):
        self.loopl+=5
        if self.loopl>250:
            self.loopl=250
        command=str(self.loopl)
        ser.write(command.encode('utf-8'))
        time.sleep(1.5)

    def decrease_loopl(self):
        self.loopl-=5
        if self.loopl<5:
            self.loopl=5
        command=str(self.loopl)
        ser.write(command.encode('utf-8'))
        time.sleep(1.5)

    def set_xy(self, x, y):
        yaw,r,p=bno.read_euler()
        direction = yaw+90-math.degrees(math.atan2(x,y))
        self.loopl = math.floor(math.sqrt(x**2+y**2))
        command=str(self.loopl)
        ser.write(command.encode('utf-8'))
        time.sleep(1.5)
        self.cc_motion(command='w', facing_target=0, user_def_target=direction)
    
    def set_direction_dist(self, direction, dist):
        yaw ,r, p = bno.read_euler()
        direction=direction+yaw
        self.loopl=dist
        command=str(self.loopl)
        ser.write(command.encode('utf-8'))
        time.sleep(1.5)
        self.cc_motion(command='w', facing_target=0, user_def_target=direction)

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(700, 200, 580, 500)
        self.setStyleSheet("background : grey")
        self.sphere=sphere()

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setGeometry(150, 200, 110, 100)
        self.b1.setText("Center tilt")
        self.b1.clicked.connect(self.sphere.adjust_tilt())

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setGeometry(100, 50, 100, 100)
        self.b2.setText("ʌ\n|")
        self.b2.clicked.connect(self.sphere.send_to_arduino('f'))

        self.b3 = QtWidgets.QPushButton(self)
        self.b3.setGeometry(225, 50, 100, 100)
        self.b3.setText("| ʌ |\n|  |  |")
        self.b3.clicked.connect(self.sphere.cc_motion(command='w'))

        self.b4 = QtWidgets.QPushButton(self)
        self.b4.setGeometry(100, 350, 100, 100)
        self.b4.setText("|\nv")
        self.b4.clicked.connect(self.sphere.send_to_arduino('s'))

        self.b5 = QtWidgets.QPushButton(self)
        self.b5.setGeometry(225, 350, 100, 100)
        self.b5.setText("|  |  |\n| v |")
        self.b5.clicked.connect(self.sphere.cc_motion(command='s'))

        self.b6 = QtWidgets.QPushButton(self)
        self.b6.setGeometry(300, 200, 80, 100)
        self.b6.setText(">")
        self.b6.clicked.connect(self.sphere.right_turn())

        self.b7 = QtWidgets.QPushButton(self)
        self.b7.setGeometry(30, 200, 80, 100)
        self.b7.setText("<")
        self.b7.clicked.connect(self.sphere.left_turn())

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
        if xpressed and ypressed:
            self.sphere.set_xy(self.x, self.y)
    
    def b9_clicked(self):
        self.direction_dist=QInputDialog(self)
        self.direction, direction_pressed=self.direction_dist.getInt(self,"Set direction", "", 0, -180, 180, 1)
        self.distance, distance_pressed=self.direction_dist.getInt(self,"Set distance", "", 0, 0, 250, 1)
        if direction_pressed and distance_pressed:
            self.sphere.set_direction_dist(self.direction, self.dist)

    def b10_clicked(self):
        self.set_loopl=QInputDialog(self)
        self.new_loopl, loopl_pressed=self.set_loopl.getInt(self, "Set loopl", "", 0, 0, 250, 1)
        if loopl_pressed:
            self.sphere.set_loopl(self.new_loopl)

app=QApplication(sys.argv)
win=window()
win.show()
sys.exit(app.exec_())
#check