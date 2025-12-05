import paho.mqtt.client as mqtt
import random
import time
import sys


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe(sys.argv[1] + '/+')


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 sensor.py <room> <datatype> <appareil>")
        sys.exit(1)
    client = mqtt.Client()
    client.connect("localhost",1883,60)

    while True:
        topic = sys.argv[1]
        datatype = sys.argv[2]
        appareil = sys.argv[3]
        zone_id = f"{topic}/{datatype}/{appareil}"
        data = round(random.uniform(20.0, 25.0), 2)
        message = f'{{"zone_id": "{zone_id}", {sys.argv[2]} : {data}}}'
        #print(message)
    
        client.publish(zone_id, data)
        time.sleep(1)


