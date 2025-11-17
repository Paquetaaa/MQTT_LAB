# MQTT_LAB
Ce lab est une introduction aux systèmes multi-agents et plus particulièrement aux communications via un broker MQTT.

Avant d'exécuter du code, lancer un venv :

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# I – Introduction
## Exercice 1 :
Lancement du premier client MQTT :

```
python3 TP1_1client.py
```

## Exercice 2 :
Lancement automatique des deux clients “ping/pong” :

```
python3 launch_pingpong.py
```

# II – Sensor Network

On lance d'abord la simulation des capteurs dans un premier terminal :

```
python3 sensor_sim.py
```

Ce programme crée un certain nombre de capteurs de base, puis à chaque fin de cycle il supprime certains capteurs et en crée de nouveaux avec une certaine probabilité.

## Averaging

Pour lancer un agent de moyenne :

```
python3 averaging.py salon/temperature
```

Il s’abonne à :
`salon/temperature/+`
et publie la moyenne sur :
`salon/temperature/average`

## Interface

Pour afficher les moyennes :

```
python3 Interface.py salon/temperature/average
```

# III – Détection d’anomalies

Agent chargé de détecter les valeurs anormales en fonction d'une fenêtre glissante et d’un seuil à 2 écarts-types.

```
python3 detection_agent.py salon/temperature/+
```

Les alertes sont publiées sur :

```
<zone>/<datatype>/<sensor_id>/alert
```



# Broker MQTT
Les scripts utilisent un broker local sur le port 1883 (ici : shiftr.io).

# Auteurs
Eric Haarlemmer
Lucas Greneche
