#!/usr/bin/env python2.7
import rospy
from Adafruit_BNO055 import BNO055
import rospy
from sphere_control.srv import IMU, IMUResponse

rospy.init_node('imu_server')

bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
bno.begin()

def callback(req):
    resp=IMUResponse()
    resp.yaw, resp.roll, resp.pitch = bno.read_euler()
    return resp

server = rospy.Service('imu_server', IMU, callback)
rospy.spin()