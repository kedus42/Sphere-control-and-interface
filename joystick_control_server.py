#!/usr/bin/env python3
import time, serial, os, math
import RPi.GPIO as GPIO
from Adafruit_BNO055 import BNO055
import paho.mqtt.client as mqttClient

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
    target=0
    def __init__(self):
        self.loopl=156
        self.mdelay=50
        self.o_range=5
        self.bdist=25
        self.sdist=40
        self.mpos=0
        self.limit=5
        self.target=0
        
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

    def cc_motion(self, command='w', facing_target=1, user_def_target=target):
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
        time.sleep(1)

    def decrease_loopl(self):
        self.loopl-=5
        if self.loopl<5:
            self.loopl=5
        command=str(self.loopl)
        ser.write(command.encode('utf-8'))
        time.sleep(1)

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

    def increase_target(self):
        self.target+=5
        if self.target>=180:
            self.target=-180
        
    def decrease_target(self):
        self.target-=5
        if self.target<=-180:
            self.target=180

Sphere=sphere()
cc=True

def callback(client, userdata, message):
    global cc, target
    print(message.payload)
    if message.payload=="forward":
        if not cc:
            Sphere.send_to_arduino("w")
            Sphere.adjust_tilt()
        else:
            Sphere.cc_motion(command="w", facing_target=0)
    elif message.payload=="backward":
        if not cc:
            Sphere.send_to_arduino("s")
            Sphere.adjust_tilt()
        else:
            Sphere.cc_motion(command="s", facing_target=0)
    elif message.payload=="right":
        Sphere.right_turn()
    elif message.payload=="left":
        Sphere.left_turn()
    elif message.payload=="looplup":
        Sphere.increase_loopl()
    elif message.payload=="loopldown":
        Sphere.decrease_loopl()
    elif message.payload=="balance":
        Sphere.adjust_tilt()
    elif message.payload=="angleup":
        Sphere.increase_target()
    elif message.payload=="angledown":
        Sphere.decrease_target()
    elif message.payload=="togglecc":
        if cc == False:
            cc = True
        else:
            cc=False

broker_address= "192.168.43.139"
client = mqttClient.Client("Python") 
client.on_message= callback
client.connect(broker_address) 
client.loop_start()  
client.subscribe("test")
print("Server up")
while True:
    pass