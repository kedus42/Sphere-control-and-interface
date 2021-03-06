import rospy
import picamera
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


bridge = CvBridge()
camera_pub=rospy.Publisher('cam', Image, queue_size=30)
camera=picamera.PiCamera()
camera.vflip=True
while True:
    start=time.time()
    camera.capture('latest.jpg')
    image_message = cv2.imread('latest.jpg')
    cv_image = bridge.cv2_to_imgmsg(image_message, "bgr8")
    camera_pub.publish(cv_image)
    end=time.time()
    time.sleep(1/30-(start-end))