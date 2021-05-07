#!/usr/bin/env python2.7
import time, os, math
import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import String
from sphere_control.msg import drive_msg

M12_CW=5
M12_CCW=6
PWM12=25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM12, GPIO.OUT)

GPIO.setup(M12_CW, GPIO.OUT) 
GPIO.setup(M12_CCW, GPIO.OUT)

pwm_pin=GPIO.PWM(PWM12,1000)
pwm_pin.start(0)

GPIO.output(M12_CW, GPIO.HIGH)
GPIO.output(M12_CCW, GPIO.LOW)
pwm_pin.ChangeDutyCycle(50)
rospy.sleep(5)
GPIO.output(M12_CW, GPIO.LOW)
GPIO.output(M12_CCW, GPIO.LOW)
pwm_pin.ChangeDutyCycle(0)