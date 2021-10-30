import connectfour 

def get_board_size() -> int: 
    '''get the number of columns and rows'''
    print('Please specify the number of columns and rows of the board') 
    while True: 
        try:  
            columns = int(input('Number of columns: ').strip()) 
            rows = int(input('Number of rows: ').strip())
            break 
        except ValueError: 
            print('Invalid colums and rows number, please try agin') 
    return columns, rows 

def make_new_game(columns, rows): 
    while True: 
        try: 
            new_game = connectfour.new_game(columns, rows) 
            break
        except: 
            print(f'columns must be an int between {connectfour.MIN_COLUMNS} and {connectfour.MAX_COLUMNS}')
            print(f'rows must be an int between {connectfour.MIN_ROWS} and {connectfour.MAX_ROWS}')
    return new_game

def print_format_board(game_state: connectfour.GameState): 
    '''print the board in certain format''' 
    _print_header(game_state) 
    _print_body(game_state)

def print_turn(game_state: connectfour.GameState): 
    '''print who's turn now is'''
    if game_state.turn == 1: 
        print('Now is RED\'s turn') 
    elif game_state.turn == 2: 
        print('Now is YELLOW\'s turn')

def get_move_cmd(game_state: connectfour.GameState): # how to annotate multiple returns
    '''get the move command from user''' 
    print('Please enter your move and column') 
    move = input('Move(DROP / POP): ').strip() 
    column = int(input(f'Column(1, {connectfour.columns(game_state)}): ').strip()) - 1
            
    return move, column

def perform_game_move(game_state: connectfour.GameState) -> connectfour.GameState: 
    '''return the new board and turn after a game move'''
    while True: 
        try: 
            move, column = get_move_cmd(game_state)  
            if move == 'DROP': 
                return connectfour.drop(game_state, column), move, column 
            elif move == 'POP': 
                return connectfour.pop(game_state, column), move, column  
            else: 
                raise connectfour.InvalidMoveError
        except ValueError: 
            print(f'column_number must be an int between 1 and {connectfour.columns(game_state)}.')
        except connectfour.GameOverError: 
            print('Game is over.') 
        except connectfour.InvalidMoveError:
            print('This move cannot be made, please enter the move and column again.')

def _print_header(game_state: connectfour.GameState): 
    '''prin the header of the board'''
    for i in range(1, connectfour.columns(game_state)+1): 
        if i < 10: 
            print(str(i) + '  ', end='') 
        elif i >= 10: 
            print(str(i) + ' ', end='') 
    print('\n')

def _print_body(game_state: connectfour.GameState): 
    '''print the body of the board'''
    for i in range(connectfour.rows(game_state)):
        for j in range(connectfour.columns(game_state)): 
            if game_state.board[j][i] == connectfour.EMPTY: 
                print('.  ', end='') 
            elif game_state.board[j][i] == connectfour.RED: 
                print('R  ', end='') 
            else: 
                print('Y  ', end='')
        print('\n')
