import paho.mqtt.client as mqtt
import random
import time
import sys

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    client.subscribe(sys.argv[1])

def on_message(client, userdata, msg):
    print("Message reçu",msg.payload.decode())
    print("Topic:", msg.topic)
    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Interface.py <topic> ex: chambre/temperature/average")
        sys.exit(1)

    client = mqtt.Client()
    client.connect("localhost",1883,60)

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


