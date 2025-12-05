import paho.mqtt.client as mqtt
import sys
import statistics

WINDOW = 20  # taille de la fenêtre glissante
buffers = {}  # dictionnaire pour stocker les fenêtres glissantes par capteur

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    topic = userdata["topic"]
    client.subscribe(topic)

def on_message(client, userdata, msg):
    topic = msg.topic           # ex: chambre/temperature/sensor_1
    payload = msg.payload.decode()

    try:
        value = float(payload)
    except:
        print("Valeur non-numérique, ignorée:", payload)
        return

    parts = topic.split("/")
    if len(parts) != 3:
        print("Topic inattendu, ignoré:", topic)
        return

    zone, datatype, sensor_id = parts
    sensor_key = f"{zone}/{datatype}/{sensor_id}"
    # récupérer ou créer la fenêtre glissante
    buf = buffers.setdefault(sensor_key, [])
    buf.append(value)

    if len(buf) > WINDOW:
        buf.pop(0)

    # on attend d'avoir suffisamment de valeurs pour être statistiquement stable
    if len(buf) < 5:
        return

    mean = statistics.mean(buf)
    stdev = statistics.pstdev(buf)  # écart-type 

    # On part du principe qu'un sensor est anormal s'il dépasse de plus de 2 écarts-types la moyenne
    seuil = mean + 2 * stdev

    # détection
    if value > seuil or value < mean - 2 * stdev:
        alert_topic = f"{zone}/{datatype}/{sensor_id}/alert"
        alert_msg = (
            f"ANOMALIE DETECTEE | sensor={sensor_id} \n"
            f"zone={zone} type={datatype} \n"
            f"value={value} mean={mean:.2f} variance={stdev:.2f}\n"
        )
        client.publish(alert_topic, alert_msg)
        print(f"[ALERTE] {alert_msg}")

    



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 detection_agent.py <topic> <MAX> ex: chambre/temperature/+")
        sys.exit(1)

    topic = sys.argv[1]

    userdata = {
        'topic': topic,
    }

    client = mqtt.Client(userdata=userdata)
    client.connect("localhost",1883,60)

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


