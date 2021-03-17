#!/usr/bin/env python2.7
import time, math
import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import String
from sphere_control.msg import cc_msg
#from sphere_control.srv import IMU, IMUResponse
from Adafruit_BNO055 import BNO055

M3_CW=17
M3_CCW=27
PWM3=13

M4_CW=22
M4_CCW=23
PWM4=19

GPIO.setwarnings(False)
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
bno.begin()

rospy.init_node("server")
#rospy.wait_for_service('imu_server')
server_pub = rospy.Publisher('server', String, queue_size=5)
drive_pub = rospy.Publisher('drive', String, queue_size=5)
cc_pub = rospy.Publisher('cc', cc_msg, queue_size=5)
#imu_client = rospy.ServiceProxy('imu_server', IMU)
#resp=IMUResponse()

class sphere:
    loopl=156
    mdelay=rospy.get_param("/mdelay")
    o_range=5
    bdist=25
    sdist=25
    mpos=0
    limit=5
    target=rospy.get_param("/target")
    move=False
    duty_cycle=rospy.get_param("/duty_cycle")
    k1=12.92254
    k2=-0.57392
    k3=33.42389

    def __init__(self):
        self.loopl=156
        self.mdelay=rospy.get_param("/mdelay")
        self.o_range=5
        self.bdist=25
        self.sdist=25
        self.mpos=0
        self.limit=5
        self.target=rospy.get_param("/target")
        self.move=False
        self.duty_cycle=rospy.get_param("/duty_cycle")
        self.k1=12.92254
        self.k2=-0.57392
        self.k3=33.42389
        
        GPIO.setmode(GPIO.BCM)   
        GPIO.setup(M3_CW, GPIO.OUT)
        GPIO.setup(M3_CCW, GPIO.OUT) 
        GPIO.setup(PWM3, GPIO.OUT) 
        GPIO.setup(M4_CW, GPIO.OUT) 
        GPIO.setup(M4_CCW, GPIO.OUT) 
        GPIO.setup(PWM4, GPIO.OUT)

    def right_turn(self, k=1, d=sdist):
        GPIO.output(M3_CW, GPIO.HIGH)
        GPIO.output(M3_CCW, GPIO.LOW)
        GPIO.output(PWM3, GPIO.HIGH)
        GPIO.output(M4_CCW, GPIO.HIGH)
        GPIO.output(M4_CW, GPIO.LOW)
        GPIO.output(PWM4, GPIO.HIGH)
        time.sleep(float((float(d)*float(k))/float(1000)))
        GPIO.output(M3_CW, GPIO.LOW)
        GPIO.output(M3_CCW, GPIO.LOW)
        GPIO.output(PWM3, GPIO.LOW)
        GPIO.output(M4_CW, GPIO.LOW)
        GPIO.output(M4_CCW, GPIO.LOW)
        GPIO.output(PWM4, GPIO.LOW)
    
    def left_turn(self, k=1, d=sdist):
        GPIO.output(M4_CW, GPIO.HIGH)
        GPIO.output(M4_CCW, GPIO.LOW)
        GPIO.output(PWM4, GPIO.HIGH)
        GPIO.output(M3_CCW, GPIO.HIGH)
        GPIO.output(M3_CW, GPIO.LOW)
        GPIO.output(PWM3, GPIO.HIGH)
        time.sleep(float((float(d)*float(k))/float(1000)))
        GPIO.output(M4_CW, GPIO.LOW)
        GPIO.output(M4_CCW, GPIO.LOW)
        GPIO.output(PWM4, GPIO.LOW)
        GPIO.output(M3_CW, GPIO.LOW)
        GPIO.output(M3_CCW, GPIO.LOW)
        GPIO.output(PWM3, GPIO.LOW)

    def adjust_tilt(self, target=0):
        rospy.loginfo("Adjusting tilt...")
        i=0
        while (i<10):
            y, r, p = bno.read_euler()
            if r > target+5:
                self.left_turn(d=self.sdist)
            elif r < target-5:
                self.right_turn(d=self.sdist)
            else:
                break
            i+=1
            time.sleep(1)
        self.mpos=0
        rospy.loginfo("Finished.")

    def stop(self):
        self.move=False
        
    def cc_motion(self, command='w', facing_target=1, user_def_target=target):
        if facing_target:
                target ,r, p =bno.read_euler()
        else:
                y ,r, p = bno.read_euler()
                target = user_def_target+y
                target%=360
        i=0
        self.move=True
        self.loopl=self.convert_to_loopl(self.loopl)
        cc_message=cc_msg()
        while (i<self.loopl):
                start=time.time()
                y,r,p=bno.read_euler()
                if y < 180:
                        if abs(y-target) < y+abs(360-target):
                                error = y-target
                        else:
                                error = y+(360-target)
                else:
                        if abs(y-target) < target+abs(360-y):
                                error = y-target
                        else:     
                                error = -1*(target + (360-y))
                if error <= -10:
                        if command == 'w':
                                if self.mpos<self.limit:
                                        self.right_turn(d=self.bdist)
                                        self.mpos+=1
                        else:
                                if self.mpos>(-1*self.limit):
                                        self.left_turn(d=self.bdist)
                                        self.mpos-=1        
                elif error >= 10:
                        if command == 'w':
                                if self.mpos>(-1*self.limit):
                                        self.left_turn(d=self.bdist)
                                        self.mpos-=1
                        else:
                                if self.mpos<self.limit:
                                        self.right_turn(d=self.bdist)
                                        self.mpos+=1
                cc_message.error=error
                cc_message.target=target
                cc_message.yaw=y
                cc_pub.publish(cc_message)
                end=time.time()
                dt=end-start
                time.sleep(0.5-dt)
                #time.sleep((float(float((float(2)*float(self.mdelay))/float(1000)))-float(float(self.bdist)/float(1000))))
        server_pub.publish("stop")
        drive_pub.publish("stop")
        self.adjust_tilt()

    def cc_motion_wt_loopl(self, command='w', facing_target=1, user_def_target=target):
        if facing_target:
                target ,r, p = bno.read_euler()
        else:
                y ,r, p = bno.read_euler()
                target = user_def_target+y
        self.move=True
        cc_message=cc_msg()
        while (self.move):
                start=time.time()
                y,r,p=bno.read_euler()
                if y < 180:
                        if abs(y-target) < y+abs(360-target):
                                error = y-target
                        else:
                                error = y+(360-target)
                else:
                        if abs(y-target) < target+abs(360-y):
                                error = y-target
                        else:     
                                error = -1*(target + (360-y))
                if error <= -10:
                        if command == 'w':
                                if self.mpos<self.limit:
                                        self.right_turn(d=self.bdist)
                                        self.mpos+=1
                        else:
                                if self.mpos>(-1*self.limit):
                                        self.left_turn(d=self.bdist)
                                        self.mpos-=1        
                elif error >= 10:
                        if command == 'w':
                                if self.mpos>(-1*self.limit):
                                        self.left_turn(d=self.bdist)
                                        self.mpos-=1
                        else:
                                if self.mpos<self.limit:
                                        self.right_turn(d=self.bdist)
                                        self.mpos+=1
                cc_message.error=error
                cc_message.target=target
                cc_message.yaw=y
                cc_pub.publish(cc_message)
                end=time.time()
                dt=end-start
                time.sleep(0.5-dt)
                #time.sleep((float(float((float(2)*float(self.mdelay))/float(1000)))-float(float(self.bdist)/float(1000))))
        self.adjust_tilt()
    
    def print_to_drive(self, command):
        if command == "forward":
            drive_pub.publish("forward")
        elif command == "backward":
            drive_pub.publish("backward")         

    def set_loopl(self, loopl):
        self.loopl=loopl
    
    def increase_loopl(self):
        self.loopl+=5
        if self.loopl>250:
            self.loopl=250

    def decrease_loopl(self):
        self.loopl-=5
        if self.loopl<5:
            self.loopl=5

    def set_xy(self, x, y):
        direction = 90-math.degrees(math.atan2(x,y))
        self.loopl = math.floor(math.sqrt(x**2+y**2))
        if direction<0:
            direction+=360
        self.cc_motion(command='w', facing_target=0, user_def_target=direction)
    
    def set_direction_dist(self, direction, dist):
        self.loopl=dist
        self.cc_motion(command='w', facing_target=0, user_def_target=direction)

    def increase_target(self):
        self.target=rospy.get_param("/target")
        if self.target>=180:
            self.target=-180
        
    def decrease_target(self):
        self.target=rospy.get_param("/target")
        if self.target<=-180:
            self.target=180

    def increase_dc(self):
        self.duty_cycle=rospy.get_param("/duty_cycle")
        if self.duty_cycle>=100:
            self.duty_cycle=100
    
    def decrease_dc(self):
        self.duty_cycle=rospy.get_param("/duty_cycle")
        if self.duty_cycle<=0:
            self.duty_cycle=0
    
    def increase_mdelay(self):
        self.mdelay=rospy.get_param("/mdelay")
        if self.mdelay>=200:
            self.mdelay=200
    
    def decrease_mdelay(self):
        self.mdelay=rospy.get_param("/mdelay")
        if self.mdelay<=0:
            self.mdelay=0
    def convert_to_loopl(self, meter):
        loopl=int(meter*self.k1+self.duty_cycle*self.k2+self.k3)
        return loopl

Sphere=sphere()
cc=rospy.get_param("/cc")
move="Stop"

def callback(message):
    global cc, target, move
    if message.data=="forward":
        move="forward"
    elif message.data=="backward":
        move="backward"
    elif message.data=="right":
        Sphere.right_turn()
    elif message.data=="left":
        Sphere.left_turn()
    elif message.data=="balance":
        Sphere.adjust_tilt()
    elif message.data=="angleup":
        Sphere.increase_target()
    elif message.data=="angledown":
        Sphere.decrease_target()
    elif message.data=="ccon":
        cc=rospy.get_param("/cc")
        cc=True
    elif message.data=="ccoff":
        cc=rospy.get_param("/cc")
        cc=False
    elif message.data=="stop":
        Sphere.stop()
        move="stop"
    elif message.data=="pwmup":
        Sphere.increase_dc()
    elif message.data=="pwmdown":
        Sphere.decrease_dc()
    elif message.data=="mdelayup":
        Sphere.increase_mdelay()
    elif message.data=="mdelaydown":
        Sphere.decrease_mdelay()

def gui_callback(message):
    if message.data[0]=='x' and message.data[1]=='y':
        xy=[]
        num=""
        for char in message.data[3:]:
            num+=str(char)
            if char ==' ':
                xy.append(int(num))
                num=""
        Sphere.set_xy(xy[0], xy[1])

    elif message.data[0]=='d' and message.data[1]=='d':
        dd=[]
        num=""
        for char in message.data[3:]:
            num+=str(char)
            if char ==' ':
                dd.append(int(num))
                num=""
        Sphere.set_direction_dist(dd[0], dd[1])
    elif message.data[0]=='d' and message.data[1]=='i':
        di=[]
        num=""
        for char in message.data[3:]:
            num+=str(char)
            if char ==' ':
                di.append(int(num))
                num=""
        Sphere.set_direction_dist(0, di[0])

server_sub = rospy.Subscriber('server', String, callback=callback)
gui_sub = rospy.Subscriber('gui', String, gui_callback)

while True:
    if move=="forward" and cc==True:
        Sphere.cc_motion_wt_loopl(command="w", facing_target=0, user_def_target=Sphere.target)
    elif move=="backward" and cc==True:
        Sphere.cc_motion_wt_loopl(command="s", facing_target=0, user_def_target=Sphere.target)
    else:
        pass