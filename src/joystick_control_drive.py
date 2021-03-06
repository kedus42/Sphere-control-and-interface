#!/usr/bin/env python2.7
import time, os, math
import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import String

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

rospy.init_node("driver")
#rospy.wait_for_service('imu_server')

class sphere:
    loopl=156
    mdelay=rospy.get_param("/mdelay")
    o_range=5
    bdist=25
    sdist=40
    mpos=0
    limit=20
    target=rospy.get_param("/target")
    move=False
    pwm_pin=GPIO.PWM(PWM12,1000)
    duty_cycle=rospy.get_param("/duty_cycle")
    k1=12.92254
    k2=-0.57392
    k3=33.42389

    def __init__(self):
        self.loopl=156
        self.mdelay=rospy.get_param("/mdelay")
        self.o_range=5
        self.bdist=25
        self.sdist=40
        self.mpos=0
        self.limit=20
        self.target=rospy.get_param("/target")
        self.move=False
        self.pwm_pin.start(0)
        self.duty_cycle=rospy.get_param("/duty_cycle")
        self.k1=12.92254
        self.k2=-0.57392
        self.k3=33.42389

        GPIO.setup(M12_CW, GPIO.OUT) 
        GPIO.setup(M12_CCW, GPIO.OUT)

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
        if direction<0:
            direction+=360
        self.cc_motion(command='w', facing_target=0, user_def_target=direction)
    
    def set_direction_dist(self, direction, dist):
        self.loopl=dist
        self.cc_motion(command='w', facing_target=0, user_def_target=direction)

    def increase_target(self):
        self.target=rospy.get_param("/target")
        if self.target>=180:
            self.target=-180
        
    def decrease_target(self):
        self.target=rospy.get_param("/target")
        if self.target<=-180:
            self.target=180

    def increase_dc(self):
        self.duty_cycle=rospy.get_param("/duty_cycle")
        if self.duty_cycle>=100:
            self.duty_cycle=100
    
    def decrease_dc(self):
        self.duty_cycle=rospy.get_param("/duty_cycle")
        if self.duty_cycle<=0:
            self.duty_cycle=0
    
    def increase_mdelay(self):
        self.mdelay=rospy.get_param("/mdelay")
        if self.mdelay>=200:
            self.mdelay=200
    
    def decrease_mdelay(self):
        self.mdelay=rospy.get_param("/mdelay")
        if self.mdelay<=0:
            self.mdelay=0
    def convert_to_loopl(self, meter):
        loopl=int(meter*k1+self.duty_cycle*k2+k3)
        return loopl

Sphere=sphere()
cc=rospy.get_param("/cc")
move="stop"

def callback(message):
    global cc, move
    if message.data=="forward":
        move="forward"
    elif message.data=="backward":
        move="backward"
    elif message.data=="stop":
        Sphere.stop()
        move="stop"
    elif message.data=="angleup":
        Sphere.increase_target()
    elif message.data=="angledown":
        Sphere.decrease_target()
    elif message.data=="ccon":
        cc=rospy.get_param("/cc")
    elif message.data=="ccoff":
        cc=rospy.get_param("/cc")
    elif message.data=="pwmup":
        Sphere.increase_dc()
    elif message.data=="pwmdown":
        Sphere.decrease_dc()
    elif message.data=="mdelayup":
        Sphere.increase_mdelay()
    elif message.data=="mdelaydown":
        Sphere.decrease_mdelay()

driver_sub=rospy.Subscriber('drive', String, callback=callback)

while True:
    if move=="forward":
        Sphere.base_motion(command="forward")
    elif move=="backward":
        Sphere.base_motion(command="backward")
    else:
        pass