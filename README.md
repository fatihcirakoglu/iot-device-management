# iot-device-management
IoT Device Management Software - My Graduation Project developed in Django for Software Engineering(MSc) SWE-599 course in Boğaziçi University.


## Clone

- Clone this repository to your local machine using `https://github.com/fatihcirakoglu/iot-device-management.git`
 
## Build
- Just clone the repo on your Linux environment and run below command in the folder.

 Debugging Application in Local Environment:  
-	Clone repository from git@github.com:fatihcirakoglu/iot-device-management.git
-	Install and create a MySQL database with credendials below.
  - DB_NAME=iotappdb
  - DB_USER=iotappdbuser
  - DB_PASSWORD=swe573.
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
