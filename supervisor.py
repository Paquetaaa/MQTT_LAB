import paho.mqtt.client as mqtt
import sys
import time
import random



BIDING = 0
EVALUATE = 1
state = BIDING

deadline = 5
JOB_NUMBER = 0

proposed_machines = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('proposal/+')


def on_message(client, userdata, msg):
    global state, BIDING
    if state == BIDING:
        txt = msg.payload.decode()
        topic = msg.topic
        
        
        ##print(f"message on topic : {topic}")
        ##print(f"content : {txt}")
        job_number = txt.split()[-1]
        ##print(f"job number coté superviseur: {job_number}")
        if txt.startswith("proposal"):
            proposed_machines.append(topic.split('/')[1])
            print(f"machine {topic.split('/')[1]} added in proposed machines list")
            print(len(proposed_machines))
            print(f"machine {topic.split('/')[1]} proposed for job {job_number}")
        elif txt.startswith("reject"):
            print(f"machine {topic.split('/')[1]} rejected job {job_number}")
        
    else:
        pass

client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_start()

while True:
    state = BIDING
    client.publish('CPF/', 'call for proposal, job number '+str(JOB_NUMBER))
    JOB_NUMBER += 1
    time.sleep(deadline)
    state = EVALUATE
    if len(proposed_machines) > 0:
        n = len(proposed_machines)
        r = random.randint(0, n-1)
        selected_machine = proposed_machines[r]
        print(f"machine {selected_machine} is selected for the job")
        client.publish(f'selection/{selected_machine}', 'YES')
        for m in proposed_machines:
            if m != selected_machine:
                print(f"machine {m} is rejected for the job")
                client.publish(f'selection/{m}', 'NO')
        proposed_machines = []
        
    else:
        print("no machine proposed for the job")
    

