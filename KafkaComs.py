from Message import Message
from confluent_kafka import Producer, Consumer
from EnumTypes import LogBotID, Topics, MessageType

def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf

class KafkaComs:
    """Clase KafkaComs, que se encarga de las comunicaciones con Apache Kafka

    Returns:
        _type_: _description_
    Author:
        Fabio Antonio Valente
    """

    logbot_id : LogBotID
    producer : Producer
    consumer : Consumer

    def __init__(self, logbot_id : LogBotID) -> None:
        """Constructor de la clase KafkaComs

        Args:
            logbot_id (LogBotID): ID del robot
        """
        props : dict
        group : str
        self.logbot_id = logbot_id
        if self.logbot_id == LogBotID.LB_MASTER:
            props = read_ccloud_config("master.properties")
            group = "python-group-1"
        elif self.logbot_id == LogBotID.LB_SLAVE_1:
            props = read_ccloud_config("slave1.properties")
            group = "python-group-2"
        elif self.logbot_id == LogBotID.LB_SLAVE_2:
            props = read_ccloud_config("slave2.properties")
            group = "python-group-3"

        self.producer = Producer(props)
        props["group.id"] = group
        props["auto.offset.reset"] = "earliest"
        self.consumer = Consumer(props)
        try:
            if self.logbot_id == LogBotID.LB_MASTER:
                self.consumer.subscribe([Topics.MASTER_INBOX.value])
                
            elif self.logbot_id == LogBotID.LB_SLAVE_1:
                self.consumer.subscribe([Topics.SLAVE_1_INBOX.value])
                
            elif self.logbot_id == LogBotID.LB_SLAVE_2:
                self.consumer.subscribe([Topics.SLAVE_2_INBOX.value])

        except Exception:
            print("ERROR in subscribing in topics Consumer Id: "+str(self.logbot_id.value))

    #Este metodo solo lo ejecuta el robot que ejecuta Keras (MASTER)
    def send_msg_to(self, message : Message) -> None:
        """Envia un mensaje al destinatario de message

        Args:
            message (Message): Mensaje a enviar
        """
        topic = Topics.NO_TOPIC
        if message.dst_robot == LogBotID.LB_SLAVE_1:
            topic = Topics.SLAVE_1_INBOX
        elif message.dst_robot == LogBotID.LB_SLAVE_2:
            topic = Topics.SLAVE_2_INBOX
        elif message.dst_robot == LogBotID.LB_MASTER:
            topic = Topics.MASTER_INBOX
        else:
            print("NO TOPIC")
        try:
            self.producer.produce(topic.value, key = str(message.coms_id), value = message.to_json())
            self.producer.flush()
        except Exception:
            print("ERROR in sending message to Producer Id: "+str(self.logbot_id.value))
    
    #Este metodo solo lo ejecuta los robots que ejecuta JPS (SLAVE_1 y SLAVE_2)
    def send_msg_to_master(self, message : Message) -> None:
        """Envia un mensaje al Master

        Args:
            message (Message): Mensaje a enviar
        """
        if self.logbot_id is not LogBotID.LB_MASTER:
            try:
                self.producer.produce(Topics.MASTER_INBOX.value, key = str(message.coms_id), value = message.to_json())
                self.producer.flush()
            except Exception:
                print("ERROR in sending message to master Producer Id: "+str(self.logbot_id.value))

    def check_received_msg(self):
        """Verifica si se ha recibido un mensaje

        Returns:
            None: No se ha recibido ningun mensaje
            Message : Se ha recibido un nuevo mensaje
        """
        try:
            #Si durante 15 segundos no se recibe ningun mensaje, se devuelve None
            msg = self.consumer.poll(15.0)
            if msg is not None:
                if msg.error() is None:
                    print("Se recibio un mensaje nuevo")
                    msg_str : str = str(msg.value().decode("utf-8"))
                    message = Message(None, None, None, None)
                    message.from_json_to_msg(msg_str)
                    return message
                else:
                    print("Ha ocurrido un error con el mensaje")
                    return None
            else:
                print("No se ha recibido ningun mensaje LogBotID "+str(self.logbot_id.value))
                return None
        except Exception:
            print("Exception: Error in receiving message in LogBotID "+str(self.logbot_id.value))
            return None
       
    def end_kafka_coms(self) -> None:
        """Finaliza las comunicaciones con Kafka
        """
        self.consumer.close()
        



        
    