# Communications_Kafka_ATA_23
Public Repository for the implementation of LogBot communication system using Kafka for ATA 2023

The code consists of two classes (KafkaComs and Message), and EnumTypes (to declare constants).

KafkaComs ==> In charge of connecting to the Kafka server and provide an easy-to-use interface for other systems.
![image](https://user-images.githubusercontent.com/125271845/233798088-8f8de678-8a34-4b39-a3e4-f361879a7502.png)
![image](https://user-images.githubusercontent.com/125271845/233798098-bf3bf950-075f-420b-acd3-fc1a79874f19.png)

Message ==> In charge of building a message that will go through the Kafka server. It has the capability of converting it to a JSON message and vice versa.
![image](https://user-images.githubusercontent.com/125271845/233798105-5a125626-54bb-4bd2-91b7-aae123461a45.png)

EnumTypes ==> Define some "constants" for building the JSON Message and identify each LogBot (Master, Slave1 and Slave2)

Main ==> It has the test explained in the document Hito 4, where the master will send one message to each slave, and both slaves will reply to the master. Messages that are received form the slaves and master are printed in the console

![image](https://user-images.githubusercontent.com/125271845/233798078-0de1c3b4-9cde-41f9-aa44-7e79857015d9.png)
