#!/usr/bin/env python2.7
import rospy, cv2
from std_msgs.msg import String
#from cv_bridge import CvBridge
import numpy as np
from sphere_control.msg import drive_msg
import picamera

noois=cv2.CascadeClassifier("../../haarcascades/haarcascade_lowerbody.xml")

rospy.init_node('home_in')
camwidth=640
camheight=480
move_threshold=int(camwidth*.8)
steer_dist=25

#bridge=CvBridge()
steering_pub=rospy.Publisher('controller', drive_msg, queue_size=3)

camera=picamera.PiCamera()
camera.vflip=True
fps=2.0

def callback(image):
    command=drive_msg()
    camera.capture('latest.jpg')
    img = cv2.imread('latest.jpg')
    oois=noois.detectMultiScale(img, 1.1, 3)
    count=0
    for x,y,w,h in oois:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 1)
        if w<move_threshold:
            command.dir=1
            command.steer_dist=steer_dist
            command.duty_cycle=30
            if x+w/2 < int((camwidth/2)-camwidth/10):
                command.steer=-1
            elif x+w/2 > int((camwidth/2)+camwidth/10):
                command.steer=1
        count+=1
        if count==1:
            break
    cv2.imshow("sphere cam at "+ str(fps)+" fps", img)
    cv2.imwrite("detected imgs.jpg", img)
    steering_pub.publish(command)

timer=rospy.Timer(rospy.Duration(1.0/fps), callback)
#rospy.Subscriber("raspicam_node/image_raw", Image, callback=callback)
rospy.spin()