import json
from threading import Thread
import time
import logging
#from django.conf import settings
import paho.mqtt.client as mqtt

ClientDict = {}

class ClientInfoObject(object):
    def __init__(self,id):
        self.id = id
        self.status = 0
    def getId(self):
        return self.id

class MqttCommunication(object):

    def __init__(self,clientId,host,port,publishTopicBase,subscribeTopicBase):

        self.current_module = "Mqtt Communication class"
        self.clientID = clientId
        self.name = clientId
        self.DEBUG = False
        self.MQTT_HOST = host
        self.MQTT_PORT = port
        self.MQTT_KEEPALIVE = 60
        self.MQTT_USERNAME = ""
        self.MQTT_PASSWORD = ""
        self.MQTT_CLIENT_ID = self.clientID
        self.MQTT_PUBLISH_TOPIC_BASE = publishTopicBase 
        self.MQTT_SUBSCRIBE_TOPIC_BASE = subscribeTopicBase
        self.MQTT_TOPIC = ""
        self.MQTT_QOS = 0
        self.MQTT_RETAIN = None
        self.MQTT_CLEAN_SESSION = None
        self.MQTT_LWT = ""

        self.client = mqtt.Client(self.MQTT_CLIENT_ID, clean_session=self.MQTT_CLEAN_SESSION)
        self.on_connect = None
        self.on_disconnect = None
        self.on_message = None
        self.on_subscribe = None
        self.on_unsubscribe = None
        self.on_publish = None
        self.client.on_connect = self.mqtt_on_connect
        self.client.on_message = self.mqtt_on_message
        self.client.on_disconnect = self.mqtt_on_disconnect
        self.client.on_subscribe = self.mqtt_on_subscribe
        self.client.on_unsubscribe = self.mqtt_on_unsubscribe
        self.client.on_publish = self.mqtt_on_publish
        logging.basicConfig(level = logging.INFO)

    def connectHost(self,mqtt_host,mqtt_port,mqtt_username,mqtt_password,mqtt_keeplive):
        self.MQTT_USERNAME = mqtt_username
        self.MQTT_PASSWORD = mqtt_password
        self.MQTT_HOST = mqtt_host
        self.MQTT_PORT = mqtt_port
        self.MQTT_KEEPALIVE = mqtt_keeplive

        try:
            self.client.username_pw_set(self.MQTT_USERNAME, self.MQTT_PASSWORD)
            logging.info(self.client.connect_async(self.MQTT_HOST,self.MQTT_PORT,self.MQTT_KEEPALIVE))
            self.client.loop_start()
        
        except Exception as e:
            logging.info ("Error connecting to %s:%d: %s" % (mqtt_host, mqtt_port, str(e)))

        return True

    def loop(self):
        while True:
            self.client.loop(10)
            print('LOOPING:')
            time.sleep(1000)

    def disconnectHost(self):
        self.client.disconnect()
        return True

    def mqttSettings(self,qos,mqtt_retain,mqtt_clean_session,mqtt_lwt):
        self.MQTT_QOS = qos
        self.MQTT_RETAIN = mqtt_retain
        self.MQTT_CLEAN_SESSION = mqtt_clean_session
        self.MQTT_LWT = mqtt_lwt
        return True

    def subscribeTopic(self,topic,id):
        self.MQTT_TOPIC = topic
        self.client.subscribe(self.MQTT_TOPIC, qos=self.MQTT_QOS)
        logging.info("Subscribe with mid " + str(self.MQTT_TOPIC) + " received.")
        
        object = ClientInfoObject(id) 
        ClientDict[str(object.getId())] = object
        
        return True

    def unsubscribeTopic(self,topic):
        self.client.unsubscribe(self.MQTT_TOPIC)
        return True

    def setClientId(self,clientID):
        self.MQTT_CLIENT_ID= clientID
        return True

    def getClientId(self):
        return self.MQTT_CLIENT_ID

    def publishData(self,topic,message,qos):
        self.client.publish(topic,message,qos)
        logging.info("Publish with " + " message: " + message + " topic: " + str(topic) + " sent.")
        return True

    # The callback for when the client receives a CONNACK response from the server.
    def mqtt_on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to %s:%s" % (self.MQTT_HOST, self.MQTT_PORT))
            time.sleep(3)

        elif rc == 1:
            logging.info ("Connection refused - unacceptable protocol version")
        elif rc == 2:
            logging.info ("Connection refused - identifier rejected")
        elif rc == 3:
            logging.info ("Connection refused - server unavailable")
        elif rc == 4:
            logging.info ("Connection refused - bad user name or password")
        elif rc == 5:
            logging.info ("Connection refused - not authorised")
        else:
            logging.info ("Connection failed - result code %d" % (rc))

    # The callback for when a PUBLISH message is received from the server.
    def mqtt_on_message(self , client, userdata, msg):
        logging.info("Message received " + msg.topic+" : "+str(msg.payload))
        json_tree = json.loads(msg.payload)
        print(json_tree)
        if json_tree.get('msgCode') == "heartbeat":
            if json_tree.get('data') == "online":
                ClientDict[json_tree.get('id')].status = 1
                logging.debug("device is online")
            else:
                ClientDict[json_tree.get('id')].status = 0
                logging.debug("device is offline")
                
    def mqtt_on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logging.info("Unexpected disconnection.")
            #self.client.loop_stop()
        else:
            logging.info('hello from disconnect')

    def mqtt_on_publish(self, client, userdata, mid):
        logging.debug("Publised message with mid " + str(mid))

    def mqtt_on_subscribe(self,client, userdata, mid, granted_qos):
        logging.info("Subscribe with mid " + str(mid) + " received.")

    def mqtt_on_unsubscribe(self, client, userdata, mid):
        logging.debug("Unsubscribe with mid " + str(mid) + " received.")

agentIface = MqttCommunication("Server","35.173.244.221",1883,"django/iot/server/","django/iot/client/")
agentIface.connectHost(agentIface.MQTT_HOST,agentIface.MQTT_PORT,agentIface.MQTT_USERNAME,agentIface.MQTT_PASSWORD,agentIface.MQTT_KEEPALIVE)

...
# create and start the daemon thread
print('Starting background task...')
daemon = Thread(target=agentIface.loop, daemon=True, name='Monitor')
daemon.start()
