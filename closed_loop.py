#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
import serial
import os 
from Adafruit_BNO055 import BNO055
import time
import math

mpos=0
limit=5

bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
bno.begin()

M3_CW=17
M3_CCW=27
PWM3=13

M4_CW=22
M4_CCW=23
PWM4=19

loopl=156
mdelay=50
o_range=5
bdist=25
sdist=40

ser=serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()
GPIO.setmode(GPIO.BCM)   
GPIO.setup(M3_CW, GPIO.OUT)
GPIO.setup(M3_CCW, GPIO.OUT) 
GPIO.setup(PWM3, GPIO.OUT) 
GPIO.setup(M4_CW, GPIO.OUT) 
GPIO.setup(M4_CCW, GPIO.OUT) 
GPIO.setup(PWM4, GPIO.OUT)

def turn1(k=1, d=sdist):
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

def turn2(k=1, d=sdist):
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

def adjust_tilt(target=0):
        global mpos, sdist
        i=0
        while (i<10):
                y,r,p=bno.read_euler()
                if r > target+5:
                        turn2(d=sdist)
                if r < target-5:
                        turn1(d=sdist)
                i+=1
                time.sleep(1)
                mpos=0

def cc_motion(command='w', facing_target=1, user_def_target=0):
        global mpos, loopl, mdelay, bdist
        if facing_target:
                target ,r, p = bno.read_euler()
        else:
                target = user_def_target
        ser.write(command.encode('utf-8'))
        time.sleep(1)
        i=0
        while (i<loopl):
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
                                if mpos<limit:
                                        turn1(d=bdist)
                                        print("Right correction")
                                        mpos+=1
                        else:
                                if mpos>(-1*limit):
                                        turn2(d=bdist)
                                        mpos-=1        
                elif error >= 5:
                        if command == 'w':
                                if mpos>(-1*limit):
                                        turn2(d=bdist)
                                        print("Left correction")
                                        mpos-=1
                        else:
                                if mpos<limit:
                                        turn1(d=bdist)
                                        mpos+=1
                i+=1
                time.sleep((float(float((float(2)*float(mdelay))/float(1000)))-float(float(bdist)/float(1000))))
        adjust_tilt()

def print_controls():
        print("\n--------------------Controls--------------------\n")
        print("w,s yaw-controlled forward and backward")
        print("r,f simple forward and backward")
        print("a,d swing pendulums left and right")
        print("t neutral tilt")
        print("l start direction and distance controlled motion")
        print("k move to a user defined x,y position")
        print("j set loopl")
        #print("o,p decrease/increase length of forward and backward swings")
        print("4,5 set max pendulum range (Only for \"odometer\")")
        print("n,m toggle visibility of your commands")
        print("b exit")
        print("\nFollow each command with Enter\n")

print_controls()

while True:
        os.system("stty -echo")
        command=raw_input()
        os.system("stty echo")
        command=str(command)
        if command == 'b':
                break
        if command == 'n':
                os.system("stty echo")
        elif command == 'm':
                os.system("stty -echo")
                print_controls()
        elif command == 'w' or command == 's':
                cc_motion(command=command)
        elif command == 'a':
                turn2()
        elif command == 'd':
                turn1()
        elif command == 't':
                adjust_tilt()
        elif command == 'l':
                y ,r, p = bno.read_euler()
                #print("The sphere is facing", y, "degrees")
                print("Enter direction of motion")
                direction=raw_input()
                direction=int(direction)+y
                print("Enter the \"distance\" to be traveled")
                command=raw_input()
                loopl=int(command)
                command=str(loopl)
                ser.write(command.encode('utf-8'))
                time.sleep(1.5)
                cc_motion(command='w', facing_target=0, user_def_target=direction)
                print_controls()
        elif command=='k':
                print("Enter the x,y coordinates of the target position relative to the sphere")
                yaw ,r, p = bno.read_euler()
                x=raw_input()
                y=raw_input()
                x=int(x)
                y=int(y)
                direction = yaw+90-math.degrees(math.atan2(x,y))
                loopl = math.floor(math.sqrt(x**2+y**2))
                command=str(loopl)
                ser.write(command.encode('utf-8'))
                time.sleep(1.5)
                cc_motion(command='w', facing_target=0, user_def_target=direction)
                print_controls()
        elif command=='j':
                print("Enter the new number of swings per motion(loopl)")
                temp=raw_input()
                loopl=int(temp)
                command=str(loopl)
                ser.write(command.encode('utf-8'))
        else:   
                if command=='o':
                        mdelay-=25
                        if mdelay < 25:
                                mdelay=25
                        print("loopl: ", loopl)
                        print("mdelay: ", mdelay)
                        print("range: ", o_range)
                elif command=='p':
                        mdelay+=25
                        print("loopl: ", loopl)
                        print("mdelay: ", mdelay)
                        print("range: ", o_range)
                elif command=='4':
                        o_range=4
                        print("loopl: ", loopl)
                        print("mdelay: ", mdelay)
                        print("range: ", o_range)
                elif command=='5':
                        o_range=5
                        print("loopl: ", loopl)
                        print("mdelay: ", mdelay)
                        print("range: ", o_range)

                ser.write(command.encode('utf-8'))