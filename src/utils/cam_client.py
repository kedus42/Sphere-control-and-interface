#!/usr/bin/env python3
import rospy
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import Int32MultiArray
import numpy as np

rospy.init_node('cam_client')

def callback(img):
    img=np.ndarray(img)
    cv2.imshow(img)

cam_sub=rospy.Subscriber('cam_test', Int32MultiArray, callback)
rospy.spin()