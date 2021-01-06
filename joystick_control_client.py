import pygame, os
pygame.init()
pygame.display.set_caption('JoyStick Example')
surface = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font(None, 20)
linesize = font.get_linesize()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joy in joysticks:
    joy.init()
 
while running:
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
            elif event.button==5:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"looplup\"")
            elif event.button==8:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"balance\"")
            elif event.button==0:
                os.system("mosquitto_pub -h 192.168.43.139 -t \"test\" -m \"togglecc\"")
        
    surface.fill((0,0,0))
 
 
    pygame.display.flip()
    clock.tick(20)
 
pygame.quit()