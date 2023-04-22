from confluent_kafka import Producer
from confluent_kafka import Consumer
from Message import Message
from KafkaComs import KafkaComs
from EnumTypes import LogBotID, MessageType

#NECESITA INSTALAR UN PAQUETE DE PYTHON  ==> pip install confluent-kafka
#DOCs de la documentacion de confluent-kafka ==> https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html
#El client.properties es un fichero de configuracion para la conexion con el servidor Kafka, NO MODIFICAR

#Ejemplo sencillo de kafka (no de LogBot)
if __name__ == "__main__2":
    def read_ccloud_config(config_file):
        conf = {}
        with open(config_file) as fh:
            for line in fh:
                line = line.strip()
                if len(line) != 0 and line[0] != "#":
                    parameter, value = line.strip().split('=', 1)
                    conf[parameter] = value.strip()
        return conf
    producer = Producer(read_ccloud_config("client.properties"))
    producer.produce("my-topic", key="FFabio", value="hola")
    producer.flush()
    
    print(3)
    props = read_ccloud_config("client.properties")
    props["group.id"] = "python-group-1"
    props["auto.offset.reset"] = "earliest"
    print(1)
    consumer = Consumer(props)
    consumer.subscribe(["my-topic"])
    print(2)
    try:
        print(5)
        msg = consumer.poll(1.0)
        while True:
            print(6)
            print(4)
            if msg is not None and msg.error() is None:
                print("key = {key:12} value = {value:12}".format(key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
            msg = consumer.poll(1.0)
    except KeyboardInterrupt:
         pass
    finally:
         consumer.close()

#Ejemplo de una comunicacion entre el Master y un Slave de LogBot
if __name__ == "__main__":

    print("Inicializar Master y Slave")
    master = KafkaComs(LogBotID.LB_MASTER) #Keras
    slave_1 = KafkaComs(LogBotID.LB_SLAVE_1) #JPS
    slave_2 = KafkaComs(LogBotID.LB_SLAVE_2) #JPS

    print("Construir Mensaje")
    msg_sent_s1 = Message(LogBotID.LB_MASTER, LogBotID.LB_SLAVE_1, MessageType.TASK_MOVE_PACKAGE, 10)
    msg_sent_s1.add_package(70, 90, 100, "X103Y113", "X125X135") #Agregamos un paquete al mensaje
    msg_sent_s1.add_status("slave1", "X109Y129") #Agregamos el Status al mensaje

    msg_sent_s2 = Message(LogBotID.LB_MASTER, LogBotID.LB_SLAVE_2, MessageType.TASK_MOVE_PACKAGE, 20)
    msg_sent_s2.add_package(70, 90, 100, "X133Y143", "X145X165") #Agregamos un paquete al mensaje
    msg_sent_s2.add_status("slave2", "X179Y189") #Agregamos el Status al mensaje
    try:
        print("Enviar Mensaje")
        master.send_msg_to(msg_sent_s1)
        master.send_msg_to(msg_sent_s2)
        print("Mensaje enviado")

        msg_rec = None
        i : int = 0
        #Slave 1 revisa si le han enviado un mensaje
        #NOTA: Puede ocurrir que se envia el mensaje se envia per el Slave no lo recibe hasta dentro de un par de minutos
        #Esto puede ser debido a la conexion con el servidor (esto es en el peor de los casos)
        if True:
            print("SLAVE 1")
            while msg_rec is None:
                msg_rec = slave_1.check_received_msg()
                i += 1
                print(str(i))
            #SIEMPRE REVISAR EL VALOR DEVUELTO POR check_received_msg()
            if msg_rec is None:
                print("Slave no ha recibido ningun mensaje")
            else:
                print("El slave recibio un mensaje")
                print("Emisor => " + str(msg_rec.src_robot.value))
                print("Receptor => " + str(msg_rec.dst_robot.value))
                print("ID Tipo de mensaje => "+ str(msg_rec.msg_type.value))
                print("ID de la conversacion => " + str(msg_rec.coms_id))
                print("Package Current Location => X" + str(msg_rec.package_current_loc_x) + "Y" + str(msg_rec.package_current_loc_y))
                print("Package Final Location => X" + str(msg_rec.package_destination_loc_x) + "Y" + str(msg_rec.package_destination_loc_y))
                print("Status Robot ID => " + str(msg_rec.status_robot_id))
                print("Status Robot Current Location => X" + str(msg_rec.robot_current_loc_x) + "Y" + str(msg_rec.robot_current_loc_y))
                print("Construir Mensaje")
                msg_sent_m1 = Message(LogBotID.LB_SLAVE_1, LogBotID.LB_MASTER, MessageType.ACK, 100)
                msg_sent_m1.add_status("slave1", "X129Y119") #Agregamos el Status al mensaje
                print("Enviar Mensaje")
                slave_1.send_msg_to(msg_sent_m1)
                print("Mensaje enviado")
        
        msg_rec = None
        i : int = 0
        #Slave 2 revisa si le han enviado un mensaje
        #NOTA: Puede ocurrir que se envia el mensaje se envia per el Slave no lo recibe hasta dentro de un par de minutos
        #Esto puede ser debido a la conexion con el servidor (esto es en el peor de los casos)
        if True:
            print("SLAVE 2")
            while msg_rec is None:
                msg_rec = slave_2.check_received_msg()
                i += 1
                print(str(i))
            #SIEMPRE REVISAR EL VALOR DEVUELTO POR check_received_msg()
            if msg_rec is None:
                print("Slave no ha recibido ningun mensaje")
            else:
                print("El slave recibio un mensaje")
                print("Emisor => " + str(msg_rec.src_robot.value))
                print("Receptor => " + str(msg_rec.dst_robot.value))
                print("ID Tipo de mensaje => "+ str(msg_rec.msg_type.value))
                print("ID de la conversacion => " + str(msg_rec.coms_id))
                print("Package Current Location => X" + str(msg_rec.package_current_loc_x) + "Y" + str(msg_rec.package_current_loc_y))
                print("Package Final Location => X" + str(msg_rec.package_destination_loc_x) + "Y" + str(msg_rec.package_destination_loc_y))
                print("Status Robot ID => " + str(msg_rec.status_robot_id))
                print("Status Robot Current Location => X" + str(msg_rec.robot_current_loc_x) + "Y" + str(msg_rec.robot_current_loc_y))
                print("Construir Mensaje")
                msg_sent_m2 = Message(LogBotID.LB_SLAVE_2, LogBotID.LB_MASTER, MessageType.ACK, 200)
                msg_sent_m2.add_status("slave2", "X139Y129") #Agregamos el Status al mensaje
                print("Enviar Mensaje")
                slave_2.send_msg_to(msg_sent_m2)
                print("Mensaje enviado")

       
        msg_rec = None
        i : int = 0
        #Master revisa si le han enviado un mensaje
        #NOTA: Puede ocurrir que se envia el mensaje se envia per el Slave no lo recibe hasta dentro de un par de minutos
        #Esto puede ser debido a la conexion con el servidor (esto es en el peor de los casos)
        if True:
            print("MASTER")
            while msg_rec is None:
                msg_rec = master.check_received_msg()
                i += 1
                print(str(i))
            #SIEMPRE REVISAR EL VALOR DEVUELTO POR check_received_msg()
            if msg_rec is None:
                print("Master no ha recibido ningun mensaje")
            else:
                print("El slave recibio un mensaje")
                print("Emisor => " + str(msg_rec.src_robot.value))
                print("Receptor => " + str(msg_rec.dst_robot.value))
                print("ID Tipo de mensaje => "+ str(msg_rec.msg_type.value))
                print("ID de la conversacion => " + str(msg_rec.coms_id))
                print("Status Robot ID => " + str(msg_rec.status_robot_id))
                print("Status Robot Current Location => X" + str(msg_rec.robot_current_loc_x) + "Y" + str(msg_rec.robot_current_loc_y))

        msg_rec = None
        i : int = 0
        #Master revisa si le han enviado un mensaje
        #NOTA: Puede ocurrir que se envia el mensaje se envia per el Slave no lo recibe hasta dentro de un par de minutos
        #Esto puede ser debido a la conexion con el servidor (esto es en el peor de los casos)
        if True:
            print("MASTER 2do")
            while msg_rec is None:
                msg_rec = master.check_received_msg()
                i += 1
                print(str(i))
            #SIEMPRE REVISAR EL VALOR DEVUELTO POR check_received_msg()
            if msg_rec is None:
                print("Master no ha recibido ningun mensaje")
            else:
                print("El slave recibio un mensaje")
                print("Emisor => " + str(msg_rec.src_robot.value))
                print("Receptor => " + str(msg_rec.dst_robot.value))
                print("ID Tipo de mensaje => "+ str(msg_rec.msg_type.value))
                print("ID de la conversacion => " + str(msg_rec.coms_id))
                print("Status Robot ID => " + str(msg_rec.status_robot_id))
                print("Status Robot Current Location => X" + str(msg_rec.robot_current_loc_x) + "Y" + str(msg_rec.robot_current_loc_y))
        #Cerramos las comunicaciones
        # IMPORTANTE
        
    except KeyboardInterrupt:
        pass
    finally:
        master.end_kafka_coms()
        slave_2.end_kafka_coms()
        slave_1.end_kafka_coms()
    
    
