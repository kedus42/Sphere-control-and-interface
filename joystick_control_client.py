import pygame, os
import paho.mqtt.client as mqttClient

class sphere:
    loopl=156
    mdelay=50
    o_range=5
    bdist=25
    sdist=40
    mpos=0
    limit=5
    target=0
    move=False
    duty_cycle=75
    
    def __init__(self):
        self.loopl=156
        self.mdelay=75
        self.o_range=5
        self.bdist=25
        self.sdist=40
        self.mpos=0
        self.limit=5
        self.target=0
        self.move=False
        self.duty_cycle=75

    def increase_target(self):
        self.target+=5
        if self.target>=180:
            self.target=-180
        
    def decrease_target(self):
        self.target-=5
        if self.target<=-180:
            self.target=180

    def increase_dc(self):
        self.duty_cycle+=5
        if self.duty_cycle>=100:
            self.duty_cycle=100
    
    def decrease_dc(self):
        self.duty_cycle-=5
        if self.duty_cycle<=0:
            self.duty_cycle=0
    
    def increase_mdelay(self):
        self.mdelay+=5
        if self.mdelay>=200:
            self.mdelay=200
    
    def decrease_mdelay(self):
        self.mdelay-=5
        if self.mdelay<=0:
            self.mdelay=0

pygame.init()
pygame.display.set_caption('Sphere joystick control')
surface = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(None, 40)
linesize = font.get_linesize()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joy in joysticks:
    joy.init()

cc="On"

Sphere=sphere()

cc_text = font.render('  Course correction: '+str(cc)+'  ', True, (0,0,0), (255,255,255))
ccRect = cc_text.get_rect()
ccRect.center = (150, 60)

target_text = font.render('  Target: '+str(Sphere.target)+'  ', True, (0,0,0), (255,255,255))
targetRect = target_text.get_rect()
targetRect.center = (70, 140)

mdelay_text = font.render('  mdelay: '+str(Sphere.mdelay)+'  ', True, (0,0,0), (255,255,255))
mdelayRect = mdelay_text.get_rect()
mdelayRect.center = (80, 220)

dc_text = font.render('  Duty cycle: '+str(Sphere.duty_cycle)+'  ', True, (0,0,0), (255,255,255))
dcRect = dc_text.get_rect()
dcRect.center = (110, 300)

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYHATMOTION:
            if event.value != (0,0):
        #        print(event.value)
                if event.value[1]==1:
                    os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"pwmup\"")
                    os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"pwmup\"")
                    Sphere.increase_dc()
                elif event.value[1]==-1:
                    os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"pwmdown\"")
                    os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"pwmdown\"")
                    Sphere.decrease_dc()
        #        elif event.value[0]==1:
        #            os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"right\"")
        #        else:
        #            os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"left\"")
        elif event.type == pygame.JOYBUTTONDOWN:
            print(event.button)
            if event.button==4:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"mdelaydown\"")
                os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"mdelaydown\"")
                Sphere.decrease_mdelay()
            elif event.button==5:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"mdelayup\"")
                os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"mdelayup\"")
                Sphere.increase_mdelay()
            elif event.button==8:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"balance\"")
            elif event.button==0:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"ccon\"")
                os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"ccon\"")
                cc="On"
            elif even.button==:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"ccoff\"")
                os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"ccoff\"")
                cc="Off"
            elif event.button==1:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"angleup\"")
                os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"angleup\"")
                Sphere.increase_target()
            elif event.button==2:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"angledown\"")
                os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"angledown\"")
                Sphere.decrease_target()
        elif event.type==pygame.JOYAXISMOTION:
                if event.axis==1:
                    if event.value<=-1:
                        os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"forward\"")
                        send_stop=True
                    elif event.value>=-0.001 and event.value<=0:
                        if send_stop:
                            os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"stop\"")
                            os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"stop\"")
                            send_stop=False
                    elif event.value>=1:
                        os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"backward\"")
                        send_stop=True
                    elif event.value>=-0.001 and event.value<=0:
                        if send_stop:
                            os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"stop\"")
                            os.system("mosquitto_pub -h 192.168.43.139 -t \"drive\" -m \"stop\"")
                            send_stop=False
                elif event.axis==3:
                    if event.value<=-1:
                        os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"left\"")
                    elif event.value>=1:
                        os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"right\"")
                
    pygame.display.flip()
    clock.tick(20)
 
pygame.quit()