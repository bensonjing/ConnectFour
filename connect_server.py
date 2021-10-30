import socket
from collections import namedtuple

GameConnection = namedtuple('GameConnection', ['socket', 'input', 'output']) 

def connect(host: str, port: int) -> GameConnection: 
    '''connect to the server''' 
    game_socket = socket.socket()
    game_socket.connect((host, port)) 

    game_input = game_socket.makefile('r') 
    game_output = game_socket.makefile('w') 

    return GameConnection(
        socket = game_socket, 
        input = game_input, 
        output = game_output) 

def close(connection: GameConnection): 
    '''close the connection''' 
    connection.input.close() 
    connection.output.close() 
    connection.socket.close()
    

def write_line(connection: GameConnection, line: str): 
    connection.output.write(line + '\r\n') 
    connection.output.flush() 

def read_line(connection: GameConnection): 
    return connection.input.readline().rstrip('\n') 