#!/usr/bin/env python3
import rospy, cv2
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
from sphere_control.msg import drive_msg
import numpy as np

rospy.init_node("home_in")
controller_pub=rospy.Publisher("/controller", drive_msg, queue_size=30)

command=drive_msg()
command.duty_cycle=30

def callback(timer_info):
    global command
    direction=rospy.get_param("/ooi")
    command.dir=0
    if direction == "left":
        command.dir=1
        command.steer=-1
        rospy.set_param("/ooi", "missing")
    elif direction == "right":
        command.dir=1
        command.steer=1
        rospy.set_param("/ooi", "missing")
    controller_pub.publish(command)

timer=rospy.Timer(rospy.Duration(.5), callback)