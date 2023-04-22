import json
from EnumTypes import LogBotID, MessageType, MessageKeys


def from_str_to_list_int(cadena : str):
    numeros = ''.join([char if char.isdigit() else ' ' for char in cadena]).split()
    x = int(numeros[0])
    y = int(numeros[1])
    return x,y


class Message:
    """Clase para obtener los diferentes atributos de los
    mensajes JSON enviados por kafka

    Returns:
        _type_: _description_
    Author:
        Fabio Antonio Valente
    """
    #ID del robot emisor del mensaje
    src_robot : LogBotID
    #ID del robot receptor del mensaje
    dst_robot : LogBotID
    #Tipo de mensaje a enviar
    msg_type : MessageType
    coms_id : int
    package : dict

    #Coordenada X de la ubicacion actual del paquete
    package_current_loc_x : int
    #Coordenada Y de la ubicacion actual del paquete
    package_current_loc_y : int

    #Coordenada X de la ubicacion destino del paquete
    package_destination_loc_x : int
    #Coordenada Y de la ubicacion destino del paquete
    package_destination_loc_y : int

    #Coordenada X de la ubicacion actual del robot
    robot_current_loc_x : int
    #Coordenada Y de la ubicacion actual del robot
    robot_current_loc_y : int

    #ID del robot del campo Status
    status_robot_id : str

    status : dict

    contains_package : bool
    contains_status : bool


    def __init__(self, src_robot : LogBotID, dst_robot : LogBotID, msg_type : MessageType, coms_id : int) -> None:
        """Constructor de la clase Message

        Args:
            src_robot (LogBotID): ID del robot que envia el mensaje
            dst_robot (LogBotID): ID del robot destinatario del mensaje
            msg_type (MessageType): Tipo de mensaje a enviar
            coms_id (int): ID de la conversacion
        """
        self.contains_package = False
        self.contains_status = False
        self.src_robot = src_robot
        self.dst_robot = dst_robot
        self.msg_type = msg_type
        self.coms_id = coms_id
        self.package = None
        self.status = None

    def from_json_to_msg(self, json_msg : str) -> None:
        """A partir de un String de JSON se obtiene los atributos de un Mensaje

        Args:
            json_msg (str): JSON en una cadena de String
        """
        msg : dict = json.loads(json_msg)
        self.src_robot = LogBotID(int(msg[str(MessageKeys.SRC_ROBOT_NAME.value)]))
        self.dst_robot = LogBotID(int(msg[str(MessageKeys.DST_ROBOT_NAME.value)]))
        self.coms_id = int(msg[str(MessageKeys.COMS_ID_NAME.value)])
        self.msg_type = MessageType(int(msg[str(MessageKeys.MSG_TYPE_NAME.value)]))

        if MessageKeys.PACKAGE_NAME.value in msg.keys():
            self.package = dict(msg[MessageKeys.PACKAGE_NAME.value])
            self.package_current_loc_x, self.package_current_loc_y = from_str_to_list_int(self.package[MessageKeys.PACKAGE_SRC_NAME.value])
            self.package_destination_loc_x, self.package_destination_loc_y = from_str_to_list_int(self.package[MessageKeys.PACKAGE_DST_NAME.value])
            self.contains_package = True
        else:
            self.contains_package = False
        
        if MessageKeys.STATUS_NAME.value in msg.keys():
            self.status = dict(msg[MessageKeys.STATUS_NAME.value])
            self.status_robot_id = str(self.status[MessageKeys.ID_ROBOT_STATUS.value])
            self.robot_current_loc_x, self.robot_current_loc_y = from_str_to_list_int(self.status[MessageKeys.ROBOT_LOC.value])
            self.contains_status = True
        else:
            self.contains_status = False
        
    def add_package(self, weigth : int, width : int, length : int, src_loc : str, dst_loc : str) -> None:
        """Agregamos las caracteristicas de un paquete al mensaje

        Args:
            weigth (int): Peso del paquete
            width (int): Anchura del paquete
            length (int): Longitud del paquete
            src_loc (str): Ubicacion actual del paquete, en formato XnnYmm, siendo n y m un int
            dst_loc (str): Ubicacion destino del paquete, en formato XnnYmm, siendo n y m un int
        """
        self.package_current_loc_x, self.package_current_loc_y = from_str_to_list_int(src_loc)
        self.package_destination_loc_x, self.package_destination_loc_y = from_str_to_list_int(dst_loc)
        self.package = {
            MessageKeys.PACKAGE_SRC_NAME.value : str(src_loc),
            MessageKeys.PACKAGE_DST_NAME.value : str(dst_loc),
            MessageKeys.PACKAGE_LENGTH.value : str(length),
            MessageKeys.PACKAGE_WEIGTH.value : str(weigth),
            MessageKeys.PACKAGE_WIDTH.value : str(width)
        }
        self.contains_package = True
        
    def add_status(self,status_robot_id : str, robot_src_loc : str, batery_level = None) -> None:
        """Agregamos el status del robot

        Args:
            status_robot_id (LogBotID): ID del robot del campo status
            robot_src_loc (str): Ubicacion actual del robot en formato XnnYmm, donde m y n son int
            batery_level (_type_, optional): Nivel de bateria como un int. Defaults to None.
        """
        self.status_robot_id = status_robot_id
        self.robot_current_loc_x, self.robot_current_loc_y = from_str_to_list_int(robot_src_loc)
        self.status = {
            MessageKeys.ID_ROBOT_STATUS.value : str(self.status_robot_id),
            MessageKeys.ROBOT_LOC.value : str(robot_src_loc),
            MessageKeys.BATTERY_LEVEL.value : str(batery_level)
        }
        self.contains_status = True
        
    def to_json(self) -> str:
        """_summary_
            Construye un mensaje JSON a partir de los atributos de la clase Mensaje
        Returns:
            str: Un string que es un JSON
        """
        msg = {
            str(MessageKeys.SRC_ROBOT_NAME.value): str(self.src_robot.value),
            str(MessageKeys.DST_ROBOT_NAME.value): str(self.dst_robot.value),
            str(MessageKeys.COMS_ID_NAME.value)  : str(self.coms_id),
            str(MessageKeys.MSG_TYPE_NAME.value) : str(self.msg_type.value)
        }
        if self.contains_package:
            msg[str(MessageKeys.PACKAGE_NAME.value)] = self.package

        if self.contains_status:
            msg[str(MessageKeys.STATUS_NAME.value)] = self.status

        return json.dumps(msg)
    
    