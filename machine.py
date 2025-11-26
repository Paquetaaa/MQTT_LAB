import paho.mqtt.client as mqtt
import sys
import time
import random

CLIENT_NAME = sys.argv[1]
JOB_DURATION = 5


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('CPF/')


def on_message(client, userdata, msg):
    global state, BIDING
    
    print("received message")
    
    txt = msg.payload.decode()
    topic = msg.topic
    print(topic)

    if topic == "CPF":
        print("received call")
        
        time.sleep(random.uniform(0, 2)) # time to take desision
        r = random.randint(0, 1)
        
        if r == 0: # take the job
            print("taking the job")
            client.publish(f'proposal/{CLIENT_NAME}', "proposal")
        else: # reject the job
            print("Rejecting the job")
            client.publish(f'proposal/{CLIENT_NAME}', "reject")



client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()