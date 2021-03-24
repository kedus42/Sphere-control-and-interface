import os
import paho.mqtt.client as mqttClient

def callback(client, userdata, message):

    if chr(message.payload[0])=='x' and chr(message.payload[1])=='y':
        xy=[]
        num=""
        for char in message.payload[3:]:
            num+=str(chr(char))
            if chr(char) ==' ':
                xy.append(int(num))
                num=""
        print(xy[0])
        print(xy[1])

    elif chr(message.payload[0])=='d' and chr(message.payload[1])=='d':
        dd=[]
        num=""
        for char in message.payload[3:]:
            num+=str(chr(char))
            if chr(char) ==' ':
                dd.append(int(num))
                num=""
        print(dd[0])
        print(dd[1])
    elif chr(message.payload[0])=='d' and chr(message.payload[1])=='i':
        di=[]
        num=""
        for char in message.payload[3:]:
            num+=str(chr(char))
            if chr(char) ==' ':
                di.append(int(num))
                num=""
        print(di[0])

broker_address= "10.81.161.34"
client = mqttClient.Client("Drive") 
client.on_message= callback
client.connect(broker_address) 
client.loop_start()  
client.subscribe("gui")
print("Server up")

while True:
    pass