import rospy, cv2

noois=cv2.CascadeClassifier("/home/kedus/Workspace/catkin_ws/src/sphere_control/haarcascades/haarcascade_lowerbody.xml")

img=cv2.imread("test.webp")
cv2.imshow("test_img", img)
#img=cv2.resize(img, (1920,1080))
img = cv2.GaussianBlur(img,(51,51),0)
oois=noois.detectMultiScale(img, 1.1, 0)
for x,y,w,h in oois:
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0))
cv2.imshow("detected dudes", img)
cv2.waitKey(0)