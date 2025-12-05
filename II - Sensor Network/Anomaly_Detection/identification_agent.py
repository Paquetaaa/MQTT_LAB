import paho.mqtt.client as mqtt
import sys
import statistics


def on_connect(client, userdata, flags, rc):
    print("Identification agent connecté (rc =", rc, ")")
    client.subscribe(userdata["topic"])
    print("Écoute des alertes sur :", userdata["topic"])

def on_message(client, userdata, msg):
    alert_msg = msg.payload.decode() ## Message d'alerte reçu
    print("ALERTE REÇUE")
    print("Topic:", msg.topic)
    print("Message:", alert_msg)

    ## On récupère le sensor qui pose problème à partir du topic d'alerte

    # extraction zone/type/id
    parts = msg.topic.split("/")
    if len(parts) != 4:
        print("Format de topic inattendu : ignoré.")
        return

    zone, datatype, sensor_id, _ = parts

    reset_topic = f"{zone}/{datatype}/{sensor_id}/reset"
    print("Envoi d'un reset au capteur :", sensor_id)

    client.publish(reset_topic, "reset")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 identification_agent.py <topic>")
        print("ex: python identification_agent.py salon/temperature/+/alert")
        sys.exit(1)

    topic = sys.argv[1]

    userdata = {"topic": topic}

    client = mqtt.Client(userdata=userdata)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)

    print("Identification agent démarré")
    client.loop_forever()


