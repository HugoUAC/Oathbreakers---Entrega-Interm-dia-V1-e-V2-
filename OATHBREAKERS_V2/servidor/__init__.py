import socket


COMMAND_SIZE = 10
INT_SIZE = 8
MOVE_UP = "move_up   "
MOVE_DOWN = "move_down "
MOVE_LEFT = "move_left "
MOVE_RIGHT = "move_right"


ADD_OP = "add      "
OBJ_OP = "obj_obj  "
SYM_OP = "sym      "
SUB_OP = "sub      "
BYE_OP = "bye      "
END_OP = "stop     "
PORT = 35000
BROADCAST_PORT = 35001

#Vai buscar diretamente o ip do servidor, para o cliente se conseguir conectar
SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())  
