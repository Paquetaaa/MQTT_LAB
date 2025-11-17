# MQTT_LAB

Ce lab est une introduction aux systeme multiagent et plus particulièrement aux broker MQTT

Avant d'éxécuter du code, lancer un venv

'''
python -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
'''
## I Introduction
### Exercice 1 : 


'''
python3 TP1_1client.py
'''


### Exercice 2 :

'''
python3 launch_pingpong.py
'''


## II Sensor Network
On lance tout d'abbord la simulation des sensors dans un premier terminal avec 

'''
python3 sensor_sim.py
'''

Ce programme crée un certain nombre de sensor de base, puis à chaque fin de cycle, supprime certains sensors et en crée de nouveaux avec un certains pourcentage de chance.
