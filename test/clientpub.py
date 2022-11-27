import paho.mqtt.client as mqttclient
import time

def on_connect(client,useddata,flags,rc):
    if rc == 0:
        print('Connected successfully ccc')
        global connected
        connected=True
    else:
        print('Bad connection. Code:', rc)

connected=False
broker_address="192.168.56.102"
port=1883
user="name"
password="111"

client=mqttclient.Client("MQTT")
#client.username_pw_set(user,password=password)
client.on_connect=on_connect
client.connect(broker_address,port=port)
client.loop_start()
while connected!=True:
	time.sleep(0.2)
mi = client.publish("mqtt/secondcode","Hello MQTT fatih client 1")
mi.wait_for_publish()

client.disconnect()
client.loop_stop()
print('Stop publish')