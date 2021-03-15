#!/usr/bin/env python2.7
import rospy
import time
from sensor_msgs.msg import CompressedImage, Joy
from std_msgs import String
from cv_bridge import CvBridge
import numpy as np

nduckie=cv2.CascadeClassifier("../haarcascades/duckie_cascade_stage10.xml")

rospy.init_node('honing')
steering_pub=rospy.Publisher('server', String, queue_size=30)
drive_pub=rospy.Publisher('drive', String, queue_size=30)
camwidth=50
camheight=50
move_threshold=int(camwidth*.8)
bridge=CvBridge()

def callback(image):
    img=bridge.imgmsg_to_cv2(image, 'rgb8')
    oois=nduckie.detectMultiScale(img, 1.1, 4)
    count=0
    for x,y,w,h in oois:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 1)
        cv2.imshow("found this ooi", img)
        if x+w/2 < int((camwidth/2)-camwidth/10):
            steering_pub.publish("left")
        elif x+w/2 > int((camwidth/2)+camwidth/10):
            steering_pub.publish("right")
        if w < move_threshold:
            #rospy.set_param("/duty_cycle", int((w/camwidth)*75)
            drive_pub.publish("forward")
        elif w > move_threshold:
            drive_pub.publish("stop")
        count+=1
        if count =1:
            break
    if count == 0:
        drive_pub.publish("stop")
    

camera_sub=rospy.Subscriber('/raspicam_node/image_raw', Image, callback=callback)
rospy.spin()