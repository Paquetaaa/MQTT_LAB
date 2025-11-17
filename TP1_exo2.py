import paho.mqtt.client as mqtt
import random
import time
import sys


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sys.argv[1])

def on_message(client, userdata, msg):
    print(msg.payload.decode())
    time.sleep(1)
    if msg.payload.decode() == sys.argv[1]:
        client.publish(sys.argv[2],sys.argv[2])





def main():
  if len(sys.argv) != 3:
        print("Usage: python3 TP1_exo2.py <word1> <word2>")
        sys.exit(1)

  client = mqtt.Client()
  client.connect("localhost",1883,60)


  client.on_connect = on_connect
  client.on_message = on_message


  client.publish(sys.argv[2],sys.argv[2])
  client.loop_forever()
      


if __name__ == "__main__":
    main()