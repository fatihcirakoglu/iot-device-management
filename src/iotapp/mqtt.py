import paho.mqtt.client as mqttclient
import time
import logging
from django.conf import settings

#logging.basicConfig(filename='mqttconf/log/mosquitto.log', level=logging.INFO,
#                    format='%(levelname)s:%(message)s')

def on_connect(client,useddata,flags,rc):
    if rc == 0:
        client.subscribe("django/iot")
        print('Connected successfully subs')
        global connected
        connected=True
    elif rc ==1:
        print("MQTT Connection failed : Incorrect protocol version | RESULT CODE: " + str(rc))
    elif rc ==2:
        print("MQTT Connection failed : Invalid client identifier | RESULT CODE: " + str(rc))
    elif rc ==3:
        print("MQTT Connection failed : Server error | RESULT CODE: " + str(rc))
    elif rc ==4:
        print("MQTT Connection failed : Bad username or password | RESULT CODE: " + str(rc))
    elif rc ==5:
        print("MQTT Connection failed : Not authorised | RESULT CODE: " + str(rc))
    else:
        print("MQTT Connection failed - Unknown | RESULT CODE: Undefined")

def on_message(client,userdata,message):
    print("Message received Payload: " + str(message.payload.decode("utf-8")) + " Topic: " + str(message.topic))

def on_publish(client, userdata, mid):
    print('PUBLISHED DATA: ' + str(mid))

#def on_log(client, userdata, level, buf):
#    print('LOG: ' + str(buf))

connected=False
#Messagereceived=False

#broker_address="192.168.56.102"
#port=1883
#user="name"
#password="111"

client=mqttclient.Client("MQTT")
#client.username_pw_set(user,password=password)


client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)
client.on_connect = on_connect
#client.on_log = on_log
client.on_message = on_message
client.on_publish = on_publish

client.loop_start()


#client.subscribe("mqtt/secondcode")

while connected!=True:
	time.sleep(0.2)

#while Messagereceived!=True:
#	time.sleep(0.2)

#client.loop_stop()