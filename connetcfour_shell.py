import connectfour
import shared_functions

def make_new_game() -> connectfour.GameState:
    '''make the new game''' 
    print('Welcome to the Connect Four Game!') 
    columns, rows = shared_functions.get_board_size() 
    new_game = shared_functions.make_new_game(columns, rows) 
    return new_game

def run(): 
    game_state = make_new_game() 
    shared_functions.print_format_board(game_state) 
    shared_functions.print_turn(game_state) 
    while True:  
        game_state = shared_functions.perform_game_move(game_state)[0]
        shared_functions.print_format_board(game_state) 
        if connectfour.winner(game_state) == 1: 
            print('Game Over, RED wins!') 
            break 
        elif connectfour.winner(game_state) == 2: 
            print('Game Over, YELLOW wins!') 
            break
        shared_functions.print_turn(game_state)

if __name__ == '__main__': 
    run() 