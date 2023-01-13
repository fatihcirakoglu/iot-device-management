# iot-device-management
IoT Device Management Software - My Graduation Project developed in Django for Software Engineering(MSc) SWE-599 course in Boğaziçi University.

## Scope

IOT device management software scope aims to deliver a on premise software package for small and medium sized commercial or non-commercial users to enable IOT
device tracking and controlling remotely while running on local environment without using any cloud provider. So customers can install this software to their local server and connect their devices to software via MQQT broker by using device specific serial numbers. This working style is cost effective especially for small and mid sized companies for IOT device management since cloud providers are charging much money and there could be no need to have an on hundred percent up time requirement. So our product will be used on local environments and just need internet connection to track devices from plants. By using the snapd interface of ubuntu based operating systems, this application will enable users to have a powerful control on their devices. Snapd application installation support is out of scope for this project since requires complex logic to communicate with Snapd store for Ubuntu core devices.

## Design 

As shown in architecture diagram, there will be three application running standalone and communicating each other.
Django application will manage device management and device information view and storage. It runs statically that means when user enters the related device page, it will check the device status first, if device is offline, the last recorded information on database will be shown on the page, if device is online then the updated information will be requested from this device, database will be updated and updated information will be shown on the page. By using static view, there will not be any unnecessary communication between MQTT broker and clients which supports data usage efficiency. As for MQTT broker, it is a standalone containerized broker which enables to communicate via clients which are connected to this broker remotely. The well known MQTT broker that is eclipse-mosquitto is used in this project. On client side, there is an agent running as a snapd application to retrieve data via snapd rest api which are explained in [1]. This agent is a standalone snapd application that communicates with snapd deemon via snapd rest api which provides below information.

## Architecture
In this architecture, MQTT broker will run standalone and it will not be a built in cloud mqtt borker, also device agent will be compatible only for client devices that run ubuntu based operating systems. Web application will be Django based and will use MySQL database for data storage. Data will be transferred in Json format between application and clients by using publish subscribe communication method. Publish and subscribe topics will end with device serial number as shown below, with this structure every device will send its specific data under its device serial number. Device serial number is a unique number that is owned by each client and it will be supplied to application while creating device page on frontend. This device serial number will be stored in database for every device.

![Architecture](https://user-images.githubusercontent.com/33651899/212283144-908d847d-7a9b-4129-ae78-0c6a2e55d36f.JPG)

- Web application will subscribe: 
```
"django/iot/client/deviceSerialNumber"
```
- Client will subscribe: 
```
"django/iot/server/deviceSerialNumber"
```
- Web application will publish to: 
```
"django/iot/server/deviceSerialNumber"
```
- Client will publish to: 
```
"django/iot/client/deviceSerialNumber"
```

Json file structure will be like below, it will include message code that will help us to identify which command that data belongs to, id is the device serial number and it will be used to identify which device is sending or receiving this command and data is the transferred information between client and server, it could be either a text or a Json file as well.
```
MessagePayload = {
"msgCode": "heartbeat",
"id": "20231",
"data": "online",
}
```

## Implementation
Basic django application has been created and MQTT broker integration has been completed, IOT device management software has been deployed on AWS E2C
mahine and it runs both Mosquitto MQTT broker and Django application via docker container. As explained section 3.1, communication is full dublex and both application
on server side and device in client side can send and receive data via mqtt broker with mqtt protocol. This application doesnt need a cloud platform to run, it can also run on a local machine which has MySQL DB instance and has required port configurations for MQTT broker. There is a resctriction while running on local environment that is the static IP requirement of the machine that runs the MQTT broker since the clients connect to MQTT broker via ip address and a standart port number. Web application uses python’s ”mqtt-paho” library for handling mqtt communication, QOS(Quality of Service) level 2 is used during publish and subscribe over mqtt since this level guarantees that each message is received only once by the intended recipients explained in [2].

There are two use cases in that occurs, in first use case device is offline, in this case device status is shown offline and only general device information is displayed on the screen. Because device information is less likely to change, so it is being shown from database with the last online record in the page. Snap app list is not being shown since it is more likely to change. In second use case, device is online, then device information, snap app list, user list and device up time is retrieved from device, they are saved in database and shown in device page.

Clients agents will be built from below repository by assigning them unique serial numbers. Agent will run as a snapd application on the devices.

https://github.com/fatihcirakoglu/iot-device-agent

## Demo

![4](https://user-images.githubusercontent.com/33651899/212285278-ed044478-2571-4318-9840-ac2f3b34a99a.JPG)
![5](https://user-images.githubusercontent.com/33651899/212285279-362e15bf-c0d3-4dfd-9bc5-a7f81f386d13.JPG)
![6](https://user-images.githubusercontent.com/33651899/212285281-372ba56a-4494-4ce6-9c26-5b7c31855cf0.JPG)
![7](https://user-images.githubusercontent.com/33651899/212285285-4d30e2b2-be2b-4935-92ed-94d13b8e9ed5.JPG)
![8](https://user-images.githubusercontent.com/33651899/212285261-0f6dec43-f0d0-48b1-8f18-8f9e374dfbca.JPG)
![1](https://user-images.githubusercontent.com/33651899/212285265-f8a5fc40-ab43-4045-85ba-2c66ccb21e2b.JPG)
![2](https://user-images.githubusercontent.com/33651899/212285271-bab1ccac-9188-4ad6-be15-be00ae178de3.JPG)
![3](https://user-images.githubusercontent.com/33651899/212285276-c91651fb-a0c6-489c-a956-082efef9be77.JPG)

## Conclusion

In this project, most important parts of IOT device management are implemented, the rest is just Json send, receive and parse operations. One of the challenging
requirement that is the snap application removal from device and installation from the snapcraft app market could not be implemented due to strict deadlines. It could be implemented further. Project deliveries are like below:
- IOTWeb application: https://github.com/fatihcirakoglu/iot-device-management/
- IOT Device Agent: https://github.com/fatihcirakoglu/iot-device-agent/
- Deployment Link: http://ec2-35-173-244-221.compute-1.amazonaws.com/

## References
1. Canonical, “Snapd REST API”, , 2020, https://snapcraft.io/docs/
snapd-api/.
2. MQTT, “MQTT: The Standard for IoT Messaging”, , 2020, https://mqtt.org/.

## Clone

- Clone this repository to your local machine using `https://github.com/fatihcirakoglu/iot-device-management.git`
 
## Build
- Just clone the repo on your Linux environment and run below command in the folder.

 Debugging Application in Local Environment:  
-	Clone repository from git@github.com:fatihcirakoglu/iot-device-management.git
-	Install and create a MySQL database with credendials below.
  - DB_NAME=iotappdb
  - DB_USER=iotappdbuser
  - DB_PASSWORD=sweswe599.
- Go to main project folder where docker compose files reside
- Then run: $ docker-compose -f  docker-compose.yml up
-	Go to any explorer and view: http://localhost

## Setup & Deployment
Viewing Application In AWS machine: 
By using secret key that is provided during creation of machine instance, you can login with below credentials to AWS E2C machine.

$ ssh  -i  djangokey.pem  ec2-user@35.173.244.221

You will be connected to AWS E2C mahine terminal, just go to 
$ cd /home/ec2-user/iot-device-management
Then run:
$ docker-compose -f  docker-compose-production.yml up

Finally project will run and you can view project page with below link:
URI of Project:  http://ec2-35-173-244-221.compute-1.amazonaws.com/

## FAQ

```

```

## Support
Reach out to me via email!
email: fatih.cirakoglu@boun.edu.tr
