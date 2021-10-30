import connect_server
import shared_functions
import connectfour

def make_connection() -> connect_server.GameConnection: 
    '''make connection between client and server'''  
    print("Please specify the host and port") 
    host = input('Host: ').strip() 
    port = int(input('Port: ').strip()) 
    connection = connect_server.connect(host, port) 
    return connection 

def hello(connection: connect_server.GameConnection) -> bool:  
    '''check if username valid and check welcome prompt'''
    username = input('Please specify your username: ').strip()
    connect_server.write_line(connection, f'I32CFSP_HELLO {username}')  
    response = connect_server.read_line(connection) 

    if response == 'WELCOME ' + username: 
        return True 
    else: 
        raise Exception('Invalid Username') 

def make_new_game(connection: connect_server.GameConnection) -> connectfour.GameState:  
    '''make the new game''' 
    if hello(connection): 
        columns, rows = shared_functions.get_board_size() 
        game_state = shared_functions.make_new_game(columns, rows) 
        connect_server.write_line(connection, 'AI_GAME ' + str(columns) + ' ' + str(rows)) 
    return game_state 

def perform_server_move(game_state: connectfour.GameState, 
    move: str, column: int, 
    connection: connect_server.GameConnection) -> connectfour.GameState:  
    '''perform the sever's move on the board''' 
    if move == 'DROP': 
        return connectfour.drop(game_state, column-1)
    elif move == 'POP': 
        return connectfour.pop(game_state, column-1)
    else: 
        connect_server.close(connection)
        raise Exception('Invalid Input, connection closed')  


def client_move(connection: connect_server.GameConnection, game_state: connectfour.GameState) -> connectfour.GameState:
    '''perform clinet move on the board'''  
    response = connect_server.read_line(connection) 
    if response == 'READY': 
        shared_functions.print_turn(game_state)
        game_state, move, column = shared_functions.perform_game_move(game_state) 
        connect_server.write_line(connection, move + ' ' + str(column+1)) 
        shared_functions.print_format_board(game_state) 
        return game_state
    elif response == 'WINNER_RED' or 'WINNER_YELLOW': 
        print('Game is over! ' + response[7:] + ' wins') 
        connect_server.close(connection) 
        raise connectfour.GameOverError 

def server_move(connection: connect_server.GameConnection, game_state: connectfour.GameState) -> connectfour.GameState: 
    '''receive and perform server move''' 
    try: 
        shared_functions.print_turn(game_state) 
        response = connect_server.read_line(connection).split()
        move, column = response[0], int(response[1])
        game_state = perform_server_move(game_state, move, column, connection)   
        shared_functions.print_format_board(game_state)  
        return game_state
    except: 
        raise Exception('Invalid Input, connection closed') 

def check_response(connection: connect_server.GameConnection): 
    '''check the response by server''' 
    response = connect_server.read_line(connection) 
    if response == 'OKAY': 
        pass  
    elif response == 'WINNER_RED' or 'WINNER_YELLOW': 
        print('Game is over! ' + response[7:] + ' wins') 
        connect_server.close(connection) 
        raise connectfour.GameOverError
    elif response == 'IVALID': 
        raise ValueError 

def run(): 
    connection = make_connection() 
    game_state = make_new_game(connection)
    shared_functions.print_format_board(game_state) 
    while True: 
        try: 
            game_state = client_move(connection, game_state)
            check_response(connection) 
            game_state = server_move(connection, game_state) 
        except connectfour.GameOverError: 
            break 

if __name__ == '__main__': 
    run() 