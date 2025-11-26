import paho.mqtt.client as mqtt
import sys
import time
import random



if len(sys.argv) != 2:
    print("Usage: python machine.py <client_name>")
    sys.exit(1)

NOJOB = 0
WORKING = 1
STATUS = NOJOB
CLIENT_NAME = sys.argv[1]
JOB_DURATION = 5

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('CPF/')
    client.subscribe(f'selection/{CLIENT_NAME}')



def on_message(client, userdata, msg):
    global STATUS, BIDING

    

    
    ##print("received message")
    
    txt = msg.payload.decode()
    ##print(f"message content : {txt}")
    topic = msg.topic
    job_number = txt.split()[-1]
    ##print(f"job number coté client: {job_number}")

    if topic == "CPF":
        ##print("received call")
        
        time.sleep(random.uniform(0, 2)) # time to take desision, random between 0 and 2 seconds
        r = random.randint(0, 1)
        if STATUS == WORKING:
            r = 1
        if r == 0: # take the job
            print(f"{CLIENT_NAME} takes the job "+job_number)
            client.publish(f'proposal/{CLIENT_NAME}', "proposal for job "+job_number)
        else: # reject the job
            print(f"{CLIENT_NAME} rejects the job "+job_number)
            client.publish(f'proposal/{CLIENT_NAME}', "reject job "+job_number)
    elif topic == f'selection/{CLIENT_NAME}':
        if txt == 'YES':
            print(f"{CLIENT_NAME} is selected for the job ")
            STATUS = WORKING
            
        else:
            print(f"{CLIENT_NAME} is rejected for the job ")



client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_start()

while True:
    if STATUS == WORKING:
        print(f"{CLIENT_NAME} working…")
        time.sleep(JOB_DURATION)
        print(f"{CLIENT_NAME} finished job")
        STATUS = NOJOB
    time.sleep(0.5)

