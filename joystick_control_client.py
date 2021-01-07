import pygame, os
pygame.init()
pygame.display.set_caption('Sphere joystick control')
surface = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(None, 40)
linesize = font.get_linesize()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joy in joysticks:
    joy.init()

loopl=156
target=0
cc="On"

cc_text = font.render('  Course correction: '+str(cc)+'  ', True, (0,0,0), (255,255,255))
ccRect = cc_text.get_rect()
ccRect.center = (150, 60)

target_text = font.render('  target: '+str(target)+'  ', True, (0,0,0), (255,255,255))
targetRect = target_text.get_rect()
targetRect.center = (70, 140)

loopl_text = font.render('  loopl: '+str(loopl)+'  ', True, (0,0,0), (255,255,255))
looplRect = loopl_text.get_rect()
looplRect.center = (80, 220)

while running:
    #surface.fill((34,139,34))
    cc_text = font.render('  Course correction: '+str(cc)+'  ', True, (0,0,0), (255,255,255))
    target_text = font.render('  target: '+str(target)+'  ', True, (0,0,0), (255,255,255))
    loopl_text = font.render('  loopl: '+str(loopl)+'  ', True, (0,0,0), (255,255,255))
    
    surface.fill((0,0,0))
    surface.blit(loopl_text, looplRect)
    surface.blit(target_text, targetRect)
    surface.blit(cc_text, ccRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYHATMOTION:
            if event.value != (0,0):
                print(event.value)
                if event.value[1]==1:
                    os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"forward\"")
                elif event.value[1]==-1:
                    os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"backward\"")
                elif event.value[0]==1:
                    os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"right\"")
                else:
                    os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"left\"")
        elif event.type == pygame.JOYBUTTONDOWN:
            print(event.button)
            if event.button==4:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"loopldown\"")
                loopl-=5
            elif event.button==5:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"looplup\"")
                loopl+=5
            elif event.button==8:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"balance\"")
            elif event.button==0:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"togglecc\"")
                if cc == "On":
                    cc = "Off"
                else:
                    cc = "On"
            elif event.button==1:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"angleup\"")
                target+=5
            elif event.button==2:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"angledown\"")
                target-=5

    pygame.display.flip()
    clock.tick(20)
 
pygame.quit()