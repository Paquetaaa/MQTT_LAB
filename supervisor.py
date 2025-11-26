import paho.mqtt.client as mqtt
import sys
import time

BIDING = 0
EVALUATE = 1
state = BIDING

deadline = 5

proposed_machines = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('proposal/+')


def on_message(client, userdata, msg):
    global state, BIDING
    if state == BIDING:
        txt = msg.payload.decode()
        topic = msg.topic
        
        print(f"message on topic : {topic}")
        print(f"content : {txt}")
        
    else:
        pass

client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

while True:
    state = BIDING
    client.publish('CPF/', 'call for proposal')
    time.sleep(deadline)
    state = EVALUATE
