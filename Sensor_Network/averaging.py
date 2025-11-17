import paho.mqtt.client as mqtt
import json
import time
import threading
import statistics
import sys

# Dictionnaire global pour stocker les valeurs reçues
total = 0
periodicity = 10
nb_message = 0


def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    client.subscribe(sys.argv[1] + '/+')

def on_message(client, userdata, msg):
    global total, periodicity, nb_message

    #print("Message reçu",msg.payload.decode())
    split = msg.topic.split(',')
    value = float(msg.payload.decode())
    total += value
    nb_message += 1

    if nb_message == periodicity:
        average = total / nb_message
        #print(f"Moyenne des {nb_message} derniers messages: {average}")
        total = 0
        nb_message = 0
        client.publish(sys.argv[1] + '/average', average)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python averaging.py <room/datatype>")
        sys.exit(1)

    client = mqtt.Client()
    client.connect("localhost",1883,60)


    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()

