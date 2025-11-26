import paho.mqtt.client as mqtt
import random
import time

message = [
    "Bonjour tout le monde!",
    "Bienvenue.",
    "Ce message est envoyé via un broker MQTT.",
    "MQTT est un protocole léger de messagerie.",
    "Il est souvent utilisé dans l'IoT.",
    "Les messages sont publiés sur des topics.",
    "Les clients peuvent s'abonner à ces topics.",
    "Cela permet une communication asynchrone.",
    "Merci ",
    "Au revoir"
]


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("hello")

def on_message(client, userdata, msg):
    print(msg.payload.decode())
    client.disconnect()

def connect_mqtt():
   client.connect("localhost",1883,60)


def send_message():
    for i in range(10):
        temps = random.randint(1,5)
        client.publish("hello", message[i])
        time.sleep(temps)





if __name__ == "__main__":
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    connect_mqtt()

    send_message()

    client.loop_forever()


