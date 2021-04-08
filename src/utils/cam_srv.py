#!/usr/bin/env python3
import rospy
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import Int32MultiArray, MultiArrayLayout
import cv2
import numpy as np

rospy.init_node('cam_server')
cam_pub=rospy.Publisher('cam_test', Int32MultiArray, queue_size=10)
img=cv2.imread("joystick.png")
cam_height=img.shape[0]
cam_width=img.shape[1]
a=Int32MultiArray()
np.reshape(img, (1, -1))
img=np.asarray(img)

layout=MultiArrayLayout()
layout.dim[0].size=cam_height
layout.dim[0].stride=3*cam_height*cam_width
layout.dim[1].size=cam_width
layout.dim[1].stride=3*cam_width
layout.dim[2].size=3
layout.dim[2].stride=3

a.data=img
a.layout.dim[0].size=cam_height
print(type(img))
rate=rospy.Rate(3)
while not rospy.is_shutdown():
    cam_pub.publish(a)