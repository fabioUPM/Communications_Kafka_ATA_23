from enum import Enum

#Todas esta clases son constantes que facilitan la construccion 
#del JSON y la construccion del Message a partir de un JSON

class LogBotID(Enum):
    """IDs para identificar los robots en la comunicion

    Args:
        Enum ([type]): [description]
    Author:
        Fabio Antonio Valente
    """
    #Robot que ejecuta keras
    LB_MASTER:int = 1

    #Robots que ejecutan JPS
    LB_SLAVE_1 :int= 2
    LB_SLAVE_2 :int= 3


class MessageType(Enum):
    """Tipos de mensajes que se pueden enviar

    Args:
        Enum ([type]): [description]
    Author:
        Fabio Antonio Valente
    """

    TASK_MOVE_PACKAGE:int = 10
    ACK :int= 20
    NACK:int = -1
    TASK_COMPLETED:int = 30
    TASK_FAILED :int = -2

class MessageKeys(Enum):
    """Los 'keys' del JSON que se va a enviar

    Args:
        Enum ([type]): [description]
    Author:
        Fabio Antonio Valente
    """

    SRC_ROBOT_NAME : str = "src_robot"
    DST_ROBOT_NAME : str = "dst_robot"
    COMS_ID_NAME : str = "coms_id"
    MSG_TYPE_NAME : str = "msg_type"

    PACKAGE_NAME : str = "package"
    PACKAGE_SRC_NAME : str = "src_loc"
    PACKAGE_DST_NAME : str = "dst_loc"
    PACKAGE_WEIGTH : str = "weigth"
    PACKAGE_LENGTH : str = "length"
    PACKAGE_WIDTH : str = "width"

    STATUS_NAME : str = "status"
    ID_ROBOT_STATUS : str = "robot_id"
    ROBOT_LOC   : str = "robot_location"
    BATTERY_LEVEL : str = "battery"

class Topics(Enum):
    """Topics para la comunicacion entre los robots

    Args:
        Enum ([type]): [description]
    Author:
        Fabio Antonio Valente
    """

    NO_TOPIC : str = "no_topic"
    MASTER_INBOX : str = "MASTER-INBOX"
    SLAVE_1_INBOX : str = "SLAVE-1-INBOX"
    SLAVE_2_INBOX : str = "SLAVE-2-INBOX"

