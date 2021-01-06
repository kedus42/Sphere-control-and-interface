#!/usr/bin/env python3
import serial
import os 

ser=serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

print("\n--------------------Controls--------------------\n")
print("w,s forward and backward")
print("a,d swing pendulums left and right")
#print("q,e rotate on the spot")
print("c center pendulums")
print("x,v swing pendulums to middle left and right arc positions")
print("o,p decrease/increase distance traveled by forward and backward commands")
print("h,j decrease/increase pendulum swing distance")
print("k,l decrease/increase length of forward and backward swings")
print("4,5 set max pendulum range (Only for \"odometer\")")
print("n,m toggle visibility of your commands")
print("b exit")
print("\nFollow each command with Enter\n")

loopl=10
mdelay=100
o_range=5
os.system("stty -echo")

while True:
        command=raw_input()
        command=str(command)
        if command == 'b':
                break
        if command == 'n':
                os.system("stty echo")
        elif command == 'm':
                os.system("stty -echo")
                print("\n--------------------Controls--------------------\n")
                print("w,s forward and backward")
                print("a,d swing pendulums left and right")
                #print("q,e rotate on the spot")
                print("c center pendulums")
                print("x,v swing pendulums to middle left and right arc positions")
                print("o,p decrease/increase distance traveled by forward and backward commands")
                print("k,l decrease/increase length of forward and backward swings")
                print("4,5 set max pendulum range (Only for \"odometer\")")
                print("n,m toggle visibility of your commands")
                print("b exit")
                print("\nFollow each command with Enter\n")
        else:   
                if command=='o':
                        loopl-=2
                        if loopl < 2:
                                loopl=2
                        print("loopl: ", loopl)
                        print("mdelay: ", mdelay)
                        print("range: ", o_range)
                elif command=='p':
                        loopl+=2
                        print("loopl: ", loopl)
                        print("mdelay: ", mdelay)
                        print("range: ", o_range)
                elif command=='k':
                        mdelay-=25
                        if mdelay < 25:
                                mdelay=25
                        print("loopl: ", loopl)
                        print("mdelay: ", mdelay)
                        print("range: ", o_range)
                elif command=='l':
                        mdelay+=25
                        print("loopl: ", loopl)
                        print("mdelay: ", mdelay)
                        print("range: ", o_range)
                elif command=='4':
                        o_range=4
                        print("loopl: ", loopl)
                        print("mdelay: ", mdelay)
                        print("range: ", o_range)
                elif command=='5':
                        o_range=5
                        print("loopl: ", loopl)
                        print("mdelay: ", mdelay)
                        print("range: ", o_range)

                ser.write(command.encode('utf-8'))

os.system("stty echo")