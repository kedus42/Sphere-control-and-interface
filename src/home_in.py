#!/usr/bin/env python3
import rospy, cv2
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
from sphere_control.msg import drive_msg
import numpy as np

steering_pub=rospy.Publisher('server', String, queue_size=30)
drive_pub=rospy.Publisher('drive', String, queue_size=30)
command=drive_msg()
command.duty_cycle=30

def callback(timer_info):
    direction=rospy.get_param("/ooi")
    if direction == "left":
        steering_pub.publish("left")
        drive_pub.publish("forward")
        rospy.set_param("/ooi", "missing")
    elif direction == "right":
        steering_pub.publish("right")
        drive_pub.publish("forward")
        rospy.set_param("/ooi", "missing")
    else:
        drive_pub.publish("stop")

timer=rospy.Timer(rospy.Duration(.5), callback)