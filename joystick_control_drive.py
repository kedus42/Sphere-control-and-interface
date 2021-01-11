#!/usr/bin/env python3
import time, os, math
import RPi.GPIO as GPIO
import paho.mqtt.client as mqttClient

M12_CW=21
M12_CCW=20
PWM12=12

M3_CW=17
M3_CCW=27
PWM3=13

M4_CW=22
M4_CCW=23
PWM4=19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM12, GPIO.OUT)

class sphere:
    loopl=156
    mdelay=50
    o_range=5
    bdist=25
    sdist=40
    mpos=0
    limit=5
    target=0
    move=False
    pwm_pin=GPIO.PWM(PWM12,1000)
    duty_cycle=75

    def __init__(self):
        self.loopl=156
        self.mdelay=75
        self.o_range=5
        self.bdist=25
        self.sdist=40
        self.mpos=0
        self.limit=5
        self.target=0
        self.move=False
        self.pwm_pin.start(0)
        self.duty_cycle=75
         
        GPIO.setup(M3_CW, GPIO.OUT)
        GPIO.setup(M3_CCW, GPIO.OUT) 
        GPIO.setup(PWM3, GPIO.OUT) 
        GPIO.setup(M4_CW, GPIO.OUT) 
        GPIO.setup(M4_CCW, GPIO.OUT) 
        GPIO.setup(PWM4, GPIO.OUT)
        GPIO.setup(M12_CW, GPIO.OUT) 
        GPIO.setup(M12_CCW, GPIO.OUT) 

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

    def base_motion(self, command="forward"):
        self.move=True
        if command=="forward":
            while self.move:
                GPIO.output(M12_CW, GPIO.HIGH)
                GPIO.output(M12_CCW, GPIO.LOW)
                self.pwm_pin.ChangeDutyCycle(self.duty_cycle)
                time.sleep(float(float(self.mdelay)/float(1000)))
                GPIO.output(M12_CW, GPIO.LOW)
                GPIO.output(M12_CCW, GPIO.LOW)
                self.pwm_pin.ChangeDutyCycle(0)
                time.sleep(float(float(self.mdelay)/float(1000)))
            
            time.sleep(2*float(float(self.mdelay)/float(1000)))
            GPIO.output(M12_CW, GPIO.HIGH)
            self.pwm_pin.ChangeDutyCycle(self.duty_cycle)
            time.sleep(float(float(self.mdelay)/float(1000)))
            GPIO.output(M12_CW, GPIO.LOW)
            GPIO.output(M12_CCW, GPIO.LOW)
            self.pwm_pin.ChangeDutyCycle(0)
        else:
            while self.move:
                GPIO.output(M12_CCW, GPIO.HIGH)
                GPIO.output(M12_CW, GPIO.LOW)
                self.pwm_pin.ChangeDutyCycle(self.duty_cycle)
                time.sleep(float(float(self.mdelay)/float(1000)))
                GPIO.output(M12_CW, GPIO.LOW)
                GPIO.output(M12_CCW, GPIO.LOW)
                self.pwm_pin.ChangeDutyCycle(0)
                time.sleep(float(float(self.mdelay)/float(1000)))
            
            time.sleep(2*float(float(self.mdelay)/float(1000)))
            GPIO.output(M12_CCW, GPIO.HIGH)
            self.pwm_pin.ChangeDutyCycle(self.duty_cycle)
            time.sleep(float(float(self.mdelay)/float(1000)))
            GPIO.output(M12_CW, GPIO.LOW)
            GPIO.output(M12_CCW, GPIO.LOW)
            self.pwm_pin.ChangeDutyCycle(0)

    def stop(self):
        self.move=False
        
    def cc_motion(self, command='w', facing_target=1, user_def_target=target):
        if facing_target:
                target ,r, p = bno.read_euler()
        else:
                y ,r, p = bno.read_euler()
                target = user_def_target+y
        if command=='w':
            self.print_to_drive("forward")
        else:
            self.print_to_drive("backward")
        i=0
        self.move=True
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
                print(self.target, target, y, error)
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
        os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"stop\"")
        os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"stop\"")
        self.adjust_tilt()

    def cc_motion_wt_loopl(self, command='w', facing_target=1, user_def_target=target):
        if facing_target:
                target ,r, p = bno.read_euler()
        else:
                y ,r, p = bno.read_euler()
                target = user_def_target+y
        if command=='w':
            self.print_to_drive("forward")
        else:
            self.print_to_drive("backward")
        i=0
        self.move=True
        while (self.move):
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
                print(self.target, target, y, error)
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
    
    def print_to_drive(self, command):
        if command == "forward":
            os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"forward\"")
        elif command == "backward":
            os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"backward\"")
    
    def set_loopl(self, loopl):
        self.loopl=loopl
    
    def increase_loopl(self):
        self.loopl+=5
        if self.loopl>250:
            self.loopl=250

    def decrease_loopl(self):
        self.loopl-=5
        if self.loopl<5:
            self.loopl=5

    def set_xy(self, x, y):
        direction = 90-math.degrees(math.atan2(x,y))
        self.loopl = math.floor(math.sqrt(x**2+y**2))
        self.cc_motion(command='w', facing_target=0, user_def_target=direction)
    
    def set_direction_dist(self, direction, dist):
        self.loopl=dist
        self.cc_motion(command='w', facing_target=0, user_def_target=direction)

    def increase_target(self):
        self.target+=5
        if self.target>=180:
            self.target=-180
        
    def decrease_target(self):
        self.target-=5
        if self.target<=-180:
            self.target=180

    def increase_dc(self):
        self.duty_cycle+=5
        if self.duty_cycle>=100:
            self.duty_cycle=100
    
    def decrease_dc(self):
        self.duty_cycle-=5
        if self.duty_cycle<=0:
            self.duty_cycle=0
    
    def increase_mdelay(self):
        self.mdelay+=5
        if self.mdelay>=200:
            self.mdelay=200
    
    def decrease_mdelay(self):
        self.mdelay-=5
        if self.mdelay<=0:
            self.mdelay=0

Sphere=sphere()
cc=True
move="stop"

def callback(client, userdata, message):
    global cc, move
    if message.payload=="forward":
        move="forward"
    elif message.payload=="backward":
        move="backward"
    elif message.payload=="stop":
        Sphere.stop()
        move="stop"
    elif message.payload=="angleup":
        Sphere.increase_target()
    elif message.payload=="angledown":
        Sphere.decrease_target()
    elif message.payload=="ccon":
        cc=True
    elif message.payload=="ccoff":
        cc=False
    elif message.payload=="pwmup":
        Sphere.increase_dc()
    elif message.payload=="pwmdown":
        Sphere.decrease_dc()
    elif message.payload=="mdelayup":
        Sphere.increase_mdelay()
    elif message.payload=="mdelaydown":
        Sphere.decrease_mdelay()

broker_address= "192.168.43.139"
client = mqttClient.Client("Drive") 
client.on_message= callback
client.connect(broker_address) 
client.loop_start()  
client.subscribe("drive")
print("Server up")

while True:
    if move=="forward":
        Sphere.base_motion(command="forward")
    elif move=="backward":
        Sphere.base_motion(command="backward")
    else:
        pass