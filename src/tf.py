#!/usr/bin/env python2.7
import rospy
import tf
import RPi.GPIO as GPIO
from Adafruit_BNO055 import BNO055

rospy.init_node("tf")

GPIO.setwarnings(False)
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
bno.begin()

br=tf.TransformBroadcaster()

rate=Rate(30)
while True and not rospy.is_shutdown():
    y,r,p=bno.read_euler()
    br.sendTransform((0, 0, 0), tf.transformations.quaternion_from_euler(r, p, y), rospy.Time.now(), "sphere", "world")
    rate.sleep()