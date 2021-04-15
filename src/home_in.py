#!/usr/bin/env python2.7
import rospy, cv2
from std_msgs.msg import String
#from cv_bridge import CvBridge
import numpy as np
from sphere_control.msg import drive_msg
import picamera
from picamera.array import PiRGBArray

noois=cv2.CascadeClassifier("home/pi/ros_catkin_ws/src/sphere_control/haarcascades/haarcascade_lowerbody.xml")

rospy.init_node('home_in')
camwidth=1920
camheight=1080
upper_threshold=int(camwidth*.8)
lower_threshold=int(camwidth*.1)
steer_dist=25

#bridge=CvBridge()
steering_pub=rospy.Publisher('controller', drive_msg, queue_size=3)

camera=picamera.PiCamera()
rawCapture = PiRGBArray(camera)
camera.resolution=(1280,720)
camera.vflip=True
camera.hflip=True
fps=2.0
greatestw=0

def callback(image):
    global greatestw
    command=drive_msg()
    camera.capture('latest.jpg')
    img = cv2.imread('latest.jpg')
    #camera.capture(rawCapture, format="bgr")
    #img = rawCapture.array
    oois=noois.detectMultiScale(img, 1.1, 0)
    count=0
    for x,y,w,h in oois:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 1)
        if w<upper_threshold and w>lower_threshold:
            command.dir=1
            command.steer_dist=steer_dist
            command.duty_cycle=30
            if w>greatestw:
                greatesw=w
                if x+w/2 < int((camwidth/2)-camwidth/10):
                    command.steer=-1
                elif x+w/2 > int((camwidth/2)+camwidth/10):
                    command.steer=1
                else:
                    command.steer=0
    cv2.imshow("sphere cam at "+ str(fps)+" fps", img)
    cv2.imwrite("detected imgs.jpg", img)
    steering_pub.publish(command)

timer=rospy.Timer(rospy.Duration(1.0/fps), callback)
#rospy.Subscriber("raspicam_node/image_raw", Image, callback=callback)
rospy.spin()