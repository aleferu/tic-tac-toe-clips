#!/usr/bin/env python3


# Made by aleferu
# https://github.com/aleferu/tic-tac-toe


from numpy import zeros as npZeros
from clips import Environment as ClipsEnvironment
from rules import custom_rules


def ask_another_game():
    """
    Asks user if the program starts other game.
    The function makes sure the input is valid.

    Returns:
        bool: True if user wants another game. False if not.
    """
    valid_answer = False
    result = False
    print('\nDo you want to play another game?')
    print('Valid inputs for yes: y, Y, yes, YES, Yes')
    print('Valid inputs for no: n, N, no, NO, No')
    while not valid_answer:
        received_input = input('Write here: ')
        if received_input in {'y', 'Y', 'yes', 'YES', 'Yes'}:
            result = True
            valid_answer = True
        elif received_input in {'n', 'N', 'no', 'NO', 'No'}:
            result = False
            valid_answer = True
        else:
            print('Please provide a valid input. Let\'s try again.')
    return result


def agent_turn(board):
    """
    Function where CLIPS is being executed.

    Args:
        board (numpy arr 3x3): Current board state.

    Returns:
        (int, int): Square where the agent will put its o.
    """
    env = ClipsEnvironment()
    square_template = """
        (deftemplate square
            (slot coord_x (type INTEGER))           
            (slot coord_y (type INTEGER))
            (slot type (type INTEGER))
            (slot chosen (type INTEGER)))
        """
    env.build(square_template)
    square_template = env.find_template('square') # shadowing
    for coord_x in range(3):
        for coord_y in range(3):
            square_template.assert_fact(coord_x=coord_x, 
                                        coord_y=coord_y, 
                                        type=int(board[coord_x, coord_y]),
                                        chosen=0)

    # Here we build all the rules located at 'rules.py'.
    # Generally, 4/5 rules per function.
    # The exceptions are the last 2 rules.
    # For more information, refer to README.md at GitHub.
    for rule in custom_rules:
        env.build(rule)

    print()   # Cleaner output
    env.run() # Magic happens

    # Debug info if you're curious
    # Prints the facts
    debug = True
    if debug: # Debug info
        for f in env.facts():
            print(f)

    # We look for our answer
    # For more information on how a square is selected refer to README.md at GitHub.
    maximum = ((0, 0), 0)
    for f in env.facts():
        if f.template == square_template:
            if maximum[1] < f['chosen']:
                maximum = ((f['coord_x'], f['coord_y']), f['chosen'])
    return maximum[0]


def player_won(player, board):
    """
    Function that given the current state of the board and
    the player that just played, if looks if that player just won.

    Args:
        player (str):           String that represents the player.
                                This way we know who just played.
        board (numpy arr 3x3): Current state of the board.

    Returns:
        bool: True if player won. False if not.
    """
    looking_for = -1
    if player == 'user':
        looking_for = 1
    elif player == 'agent':
        looking_for = 2

    for i in range(3):
        if (board[i] == looking_for).all():                # Rows (-)
            return True
        if (board[:, i] == looking_for).all():             # Columns (|)
            return True
    if (board[::, ::-1].diagonal() == looking_for).all():  # Other diagonal (/)
        return True
    return (board.diagonal() == looking_for).all()         # Diagonal (\)


def show_board(board):
    """
    Prints the board.

    Args:
        board (numpy arr 3x3): Current state of the board.
    """
    mapping = {0: ' ', 1: 'x', 2: 'o'}
    print('-------')
    for coord_x in range(3):
        for coord_y in range(3):
            print(f'|{mapping[board[coord_x, coord_y]]}', end='')
        print('|')
        print('-------')


def ask_user_coordinates(board):
    """
    Function that asks the user for the coordinates of his turn.

    Args:
        board (numpy arr 3x3): Current state of the board.

    Returns:
        (int, int): Square where the x is going to be placed.
    """
    valid_answer_x, valid_answer_y = False, False
    coord_x, coord_y = 0, 0
    print('\nYour turn!')
    while not valid_answer_x:
        coord_x = input(f'Input coordinate x [Range 0-2]: ')
        try:
            coord_x = int(coord_x)
            if coord_x < 0 or coord_x > 2:
                raise Exception()
            valid_answer_x = True
        except:
            print('Invalid input for coordinate x, please try again.')

    while not valid_answer_y:
        coord_y = input(f'Input coordinate y [Range 0-2]: ')
        try:
            coord_y = int(coord_y)
            if coord_y < 0 or coord_y > 2:
                raise Exception()
            valid_answer_y = True
        except:
            print('Invalid input for coordinate y, please try again.')

    if board[coord_x, coord_y] != 0:
        print(f'The board is already occupied at {(coord_x, coord_y)}, please try again.')
        (coord_x, coord_y) = ask_user_coordinates(board)

    return (coord_x, coord_y)


def ask_who_starts():
    """
    Function that asks the user who starts (user or agent).
    The function makes sure the input is valid.

    Returns:
        str: 'user' if user wants to start.
             'agent' if user wants the agent to start.
    """
    valid_answer = False
    result = ''
    print('\nWho starts: user (x) or agent (o)?')
    print('Valid input for user: u, U, x')
    print('Valid input for agent: a, A, o')
    while not valid_answer:
        user_input = input('Who starts? Input here: ')
        if user_input in {'u', 'U', 'x'}:
            result = 'user'
            valid_answer = True
        elif user_input in {'a', 'A', 'o'}:
            result = 'agent'
            valid_answer = True
        else:
            print('Not a valid input, please try again.')
    return result


def start_game():
    """
    Function that implements the game's logic.
    All the other functions are called from this one.
    The function initializes all of the game's variables.
    """
    # Welcome
    print('\n=========================================')
    print('Game is starting!')
    print('Squares are represented as (x,y)')
    print('Upper left square is (0,0)')
    print('Lower right square (2,2)')
    print('=========================================')

    # Variable initialization
    turn_of = ask_who_starts() # user, agent
    board = npZeros(9, dtype=int).reshape(3, 3) # 0 (empty)
                                                # 1 (x)
                                                # 2 (o)
    turn_counter = 0
    game_being_played = True

    print(f'\nInitial board:')
    show_board(board)

    # Game loop
    print(f'\nThe game is starting, {turn_of}\'s turn!\n')
    while game_being_played:
        turn_counter += 1

        # User turn
        if turn_of == 'user':
            coords = ask_user_coordinates(board)
            print(f'\nA x will be placed at {coords}.')
            board[coords] = 1
            game_being_played = not player_won('user', board)
            if not game_being_played:
                print('\nGame\'s over, the user won! Thank you for playing.')

        # Agent turn
        if turn_of == 'agent':
            coords = agent_turn(board)
            print(f'\nA o will be placed at {coords}.')
            board[coords] = 2
            game_being_played = not player_won('agent', board)
            if not game_being_played:
                print('\nGame\'s over, the agent won! Thank you for playing.')
        
        # Current board
        show_board(board)

        # Draw?
        if turn_counter == 9 and game_being_played:
            print('\nGame\'s over, it\'s a draw! Thank you for playing.\n')
            game_being_played = False

        # Turn change
        turn_of = 'agent' if turn_of == 'user' else 'user'

    # Another game?
    if ask_another_game():
        start_game()


# main()
if __name__ == '__main__':
    start_game()
