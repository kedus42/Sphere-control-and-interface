#!/usr/bin/env python3
import rospy, cv2
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import numpy as np

noois=cv2.CascadeClassifier("../haarcascades/haarcascade_lowerbody.xml")

rospy.init_node('find_oois')
camwidth=640
camheight=480
move_threshold=int(camwidth*.8)
ooi_duration=0
duration_threshhold=30
bridge=CvBridge()

def callback(image):
    global ooi_duratioin
    img=bridge.imgmsg_to_cv2(image, 'rgb8')
    oois=noois.detectMultiScale(img, 1.1, 4)
    count=0
    for x,y,w,h in oois:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 1)
        cv2.imshow("found this ooi", img)
        if x+w/2 < int((camwidth/2)-camwidth/10):
            ooi_duratioin+=1
            if ooi_duration>duration_threshhold:
                rospy.set_param("/ooi", "left")
        elif x+w/2 > int((camwidth/2)+camwidth/10):
            ooi_duration-=1
            if ooi_duratioin<-1*duration_threshhold:
                rospy.set_param("/ooi", "right")
        count+=1
        if count==1:
            break
    
rospy.Subscriber("raspicam_node/image_raw", Image, callback=callback)
rospy.spin()