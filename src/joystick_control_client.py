#!/usr/bin/env python3
import pygame
import rospy
from std_msgs.msg import String

rospy.init_node("client")

class sphere:
    loopl=156
    mdelay=rospy.get_param("/mdelay")
    o_range=5
    bdist=25
    sdist=40
    mpos=0
    limit=5
    target=rospy.get_param("/target")
    move=False
    duty_cycle=rospy.get_param("/duty_cycle")
    
    def __init__(self):
        self.loopl=156
        self.mdelay=rospy.get_param("/mdelay")
        self.o_range=5
        self.bdist=25
        self.sdist=40
        self.mpos=0
        self.limit=5
        self.target=rospy.get_param("/target")
        self.move=False
        self.duty_cycle=rospy.get_param("/duty_cycle")

    def increase_target(self):
        self.target+=5
        if self.target>=180:
            self.target=-180
        rospy.set_param('/target', self.target)
        
    def decrease_target(self):
        self.target-=5
        if self.target<=-180:
            self.target=180
        rospy.set_param('/target', self.target)

    def increase_dc(self):
        self.duty_cycle+=5
        if self.duty_cycle>=100:
            self.duty_cycle=100
        rospy.set_param('/duty_cycle', self.duty_cycle)
    
    def decrease_dc(self):
        self.duty_cycle-=5
        if self.duty_cycle<=0:
            self.duty_cycle=0
        rospy.set_param('/duty_cycle', self.duty_cycle)
    
    def increase_mdelay(self):
        self.mdelay+=5
        if self.mdelay>=200:
            self.mdelay=200
        rospy.set_param('/mdelay', self.mdelay)
    
    def decrease_mdelay(self):
        self.mdelay-=5
        if self.mdelay<=0:
            self.mdelay=0
        rospy.set_param('/mdelay', self.mdelay)

server_pub = rospy.Publisher('server', String, queue_size=5)
drive_pub = rospy.Publisher('drive', String, queue_size=5)

pygame.init()
pygame.display.set_caption('Sphere joystick control')
surface = pygame.display.set_mode((875, 325))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(None, 40)
linesize = font.get_linesize()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joy in joysticks:
    joy.init()

cc=rospy.get_param("/cc")
if cc==True:
    cc="On"
else:
    cc="Off"

Sphere=sphere()

cc_text = font.render('  Course correction: '+str(cc)+'  ', True, (0,0,0), (255,255,255))
ccRect = cc_text.get_rect()
ccRect.center = (160, 60)

target_text = font.render('  Target: '+str(Sphere.target)+'  ', True, (0,0,0), (255,255,255))
targetRect = target_text.get_rect()
targetRect.center = (60, 140)

mdelay_text = font.render('  mdelay: '+str(Sphere.mdelay)+'  ', True, (0,0,0), (255,255,255))
mdelayRect = mdelay_text.get_rect()
mdelayRect.center = (75, 220)

dc_text = font.render('  Duty cycle: '+str(Sphere.duty_cycle)+'  ', True, (0,0,0), (255,255,255))
dcRect = dc_text.get_rect()
dcRect.center = (95, 300)

controls = pygame.image.load('/home/kedus/Workspace/catkin_ws/src/sphere_control/src/joystick.png')

send_stop=False

while running:
    cc_text = font.render('  Course correction: '+str(cc)+'  ', True, (0,0,0), (255,255,255))
    target_text = font.render('  Target: '+str(Sphere.target)+'  ', True, (0,0,0), (255,255,255))
    mdelay_text = font.render('  mdelay: '+str(Sphere.mdelay)+'  ', True, (0,0,0), (255,255,255))
    dc_text = font.render('  Duty cycle: '+str(Sphere.duty_cycle)+'  ', True, (0,0,0), (255,255,255))
    
    surface.fill((0,0,0))
    surface.blit(mdelay_text, mdelayRect)
    surface.blit(target_text, targetRect)
    surface.blit(cc_text, ccRect)
    surface.blit(dc_text, dcRect)
    surface.blit(controls, (340,10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYHATMOTION:
            if event.value != (0,0):
                if event.value[1]==1:
                    Sphere.increase_dc()
                    server_pub.publish("pwmup")
                    drive_pub.publish("pwmup")
                elif event.value[1]==-1:
                    Sphere.decrease_dc()
                    server_pub.publish("pwmdown")
                    drive_pub.publish("pwmdown")
        elif event.type == pygame.JOYBUTTONDOWN:
            print(event.button)
            if event.button==2:#X
                Sphere.decrease_mdelay()
                server_pub.publish("mdelaydown")
                drive_pub.publish("mdelaydown")
            elif event.button==1:#B
                Sphere.increase_mdelay()
                server_pub.publish("mdelayup")
                drive_pub.publish("mdelayup")
            elif event.button==8:#Start
                server_pub.publish("balance")
            elif event.button==3:#Y
                rospy.set_param("/cc", "True")
                server_pub.publish("ccon")
                drive_pub.publish("ccon")
                cc="On"
            elif event.button==0:#A
                rospy.set_param("/cc", "False")
                server_pub.publish("ccoff")
                drive_pub.publish("ccoff")
                cc="Off"
            elif event.button==5:#RB
                Sphere.increase_target()
                server_pub.publish("angleup")
                drive_pub.publish("angleup")
            elif event.button==4:#LB
                Sphere.decrease_target()
                server_pub.publish("angledown")
                drive_pub.publish("angledown")
        elif event.type==pygame.JOYAXISMOTION:
                if event.axis==1:
                    if event.value<=-1:
                        server_pub.publish("forward")
                        send_stop=True
                    elif event.value>=-0.001 and event.value<=0:
                        if send_stop:
                            server_pub.publish("stop")
                            drive_pub.publish("stop")
                            send_stop=False
                    elif event.value>=1:
                            server_pub.publish("backward")
                            send_stop=True
                    elif event.value>=-0.001 and event.value<=0:
                        if send_stop:
                            server_pub.publish("stop")
                            drive_pub.publish("stop")
                            send_stop=False
                elif event.axis==3:
                    if event.value<=-1:
                        server_pub.publish("left")
                    elif event.value>=1:
                        server_pub.publish("right")
                
    pygame.display.flip()
    clock.tick(20)
 
pygame.quit()