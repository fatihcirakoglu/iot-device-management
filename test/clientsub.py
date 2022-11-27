import paho.mqtt.client as mqttclient
import time

def on_connect(client,useddata,flags,rc):
    if rc == 0:
        print('Connected successfully to on premise broker')
        client.subscribe("django/iot/2")
        global connected
        connected=True
    else:
        print('Bad connection. Code:', rc)

def on_message(client,userdata,message):
    print("Message received Payload: " + str(message.payload.decode("utf-8")) + " Topic: " + str(message.topic))

connected=False
Messagereceived=False

broker_address="192.168.56.102"
port=1883
user="name"
password="111"

client=mqttclient.Client("MQTT")
client.on_message = on_message
#client.username_pw_set(user,password=password)
client.on_connect = on_connect
client.connect(broker_address,port=port)
client.loop_start()
while connected!=True:
	time.sleep(0.2)

while Messagereceived!=True:
	time.sleep(0.2)

client.loop_stop()