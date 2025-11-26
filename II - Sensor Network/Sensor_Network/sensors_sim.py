import subprocess
import time
import random
import signal
import os

# Configuration
ZONES = ["salon", "chambre", "cuisine","sdb"]
DATATYPES = ["temperature", "humidity","CO2"]
SENSORS_PER_ZONE = 2     # nombre initial de capteurs par zone/type
CYCLE_TIME = 5           # durée d’un cycle avant ajout/suppression
KILL_PROBABILITY = 0.3    # probabilité de suppression d’un capteur
SPAWN_PROBABILITY = 0.7   # probabilité de création d’un nouveau capteur


processes = []

def launch_sensor(zone, datatype, sensor_id):
    cmd = ["python3", "sensor.py", zone, datatype, sensor_id]
    ## Nous permet de lancer automatiquement des capteurs
    p = subprocess.Popen(cmd)
    print(f"Capteur lancé : {zone}/{datatype}/{sensor_id}  ")
    return p

def stop_sensor(p, zone, datatype, sensor_id):
    try:
        ## Permet de tuer automatiquement les process lié à des sensors actifs
        os.kill(p.pid, signal.SIGTERM)
        print(f" Capteur arrêté : {zone}/{datatype}/{sensor_id}  ")
    except ProcessLookupError:
        pass

def main():
    # Lancement initial des capteurs
    print(f"\n Activation des premiers capteurs\n")
    for zone in ZONES:
        for datatype in DATATYPES:
            for i in range(SENSORS_PER_ZONE):
                sensor_id = f"{datatype}_{i+1}"
                p = launch_sensor(zone, datatype, sensor_id)
                processes.append((zone, datatype, sensor_id, p))
                time.sleep(0.5)

    print(f"\n Début simulation dynamique \n")

    try:
        while True:
            time.sleep(CYCLE_TIME)

            # Suppression aléatoire de capteurs
            for entry in processes[:]:
                if random.random() < KILL_PROBABILITY:
                    zone, datatype, sensor_id, p = entry
                    stop_sensor(p, zone, datatype, sensor_id)
                    processes.remove(entry)

            # Apparition de nouveaux capteurs
            if random.random() < SPAWN_PROBABILITY:
                zone = random.choice(ZONES)
                datatype = random.choice(DATATYPES)
                new_id = f"{datatype}_{random.randint(100,999)}"
                p = launch_sensor(zone, datatype, new_id)
                processes.append((zone, datatype, new_id, p))

            print(f"Cycle terminé ({len(processes)} capteurs actifs)\n")

    except KeyboardInterrupt:
        print(f"\n Arrêt de tous les capteurs")
        for zone, datatype, sensor_id, p in processes:
            stop_sensor(p, zone, datatype, sensor_id)

if __name__ == "__main__":
    main()
