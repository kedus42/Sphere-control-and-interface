#!/usr/bin/env python2.7
import rospy
import picamera
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

rospy.init_node('cam_server')
bridge = CvBridge()
camera_pub=rospy.Publisher('cam', Image, queue_size=30)
camera=picamera.PiCamera()
camera.vflip=True
rate=Rate(float(1/30))
while True:
    camera.capture('latest.jpg')
    image_message = cv2.imread('latest.jpg')
    cv_image = bridge.cv2_to_imgmsg(image_message, "bgr8")
    camera_pub.publish(cv_image)
    rate.sleep()