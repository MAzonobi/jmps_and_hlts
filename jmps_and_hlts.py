"""
jmps_and_hlts.py
This file plays a modified version of the game snakes and ladders
"""

import random

GRID_WIDTH = 8
GRID_HEIGHT = 3
DICE_SIDES = 6
ADD = 'add'
SUB = 'sub'
MUL = 'mul'
JMP = 'jmp'
HLT = 'hlt'
NOP = 'nop'
YES = 'yes'

def generate_random_map(length, the_seed=0):
    """
        :param length - the length of the map
        :param the_seed - the seed of the map
        :return: a randomly generated map based on a specific seed, and length.
    """
    if the_seed:
        random.seed(the_seed)
    map_list = []
    for _ in range(length - 2):
        random_points = random.randint(1, 100)
        random_position = random.randint(0, length - 1)
        map_list.append(random.choices(
            ['nop', f'add {random_points}', f'sub {random_points}', f'mul {random_points}', f'jmp {random_position}',
             'hlt'], weights=[5, 2, 2, 2, 3, 1], k=1)[0])

    return ['nop'] + map_list + ['hlt']


def make_grid(table_size):
    """
    :param table_size: this needs to be the length of the map
    :return: returns a display grid that you can then modify with fill_grid_square (it's a 2d-grid of characters)
    """
    floating_square_root = table_size ** (1 / 2)

    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_height = int_square_root
    if int_square_root * (int_square_root - 1) >= table_size:
        table_height -= 1

    the_display_grid = [[' ' if j % GRID_WIDTH else '*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        if i % GRID_HEIGHT else ['*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        for i in range(table_height * GRID_HEIGHT + 1)]
    return the_display_grid


def fill_grid_square(display_grid, size, index, message):
    """
    :param display_grid:  the grid that was made from make_grid
    :param size:  this needs to be the length of the total map, otherwise you may not be able to place things correctly.
    :param index: the index of the position where you want to display the message
    :param message: the message to display in the square at position index, separated by line returns.
    """
    floating_square_root = size ** (1 / 2)
    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_row = index // int_square_root
    table_col = index % int_square_root

    if table_row % 2 == 0:
        column_start = GRID_WIDTH * table_col
    else:
        column_start = GRID_WIDTH * (int_square_root - table_col - 1)

    for r, message_line in enumerate(message.split('\n')):
        for k, c in enumerate(message_line):
            display_grid[GRID_HEIGHT * table_row + 1 + r][column_start + 1 + k] = c


def roll_dice():
    """
        Call this function once per turn.

        :return: returns the dice roll
    """
    return random.randint(1, DICE_SIDES)


def math(command, score):
    """
    This function controls and calculates the math operations for a space landed on
    :param command: The instruction of the space landed on
    :param score: The score after the instruction is executed
    :return: The final score
    """
    # Each if/elif block updates the score using their respective property
    if command[0] == ADD:
        score += int(command[1])

    elif command[0] == SUB:
        score -= int(command[1])

    elif command[0] == MUL:
        score *= int(command[1])

    return score


def play_game(game_map):
    """
    This function simulates the game given the generated game map
    :param game_map: Generates the entire game map
    :return: None
    """
    score = 0
    position = 0
    game_over = False

    while not game_over:
        roll = roll_dice()
        # If the roll exceeds the length of the board, it loops back to the remaining position
        position = (position + roll) % len(game_map)
        # creates a list with the game map instruction for the space
        spot = game_map[position].split()

        # checks for jmp command and updates
        while spot[0] == JMP:
            print(f"Pos: {position} Score: {score}, instruction {spot[0]} Rolled: {roll}")
            position = int(spot[1])
            spot = game_map[position].split()

        # Each if/elif block calls the math function to execute the respective operation
        if ADD in spot:
            score = math(spot, score)

        elif SUB in spot:

            score = math(spot, score)

        elif MUL in spot:
            score = math(spot, score)

        elif spot[0] == HLT:
            game_over = True

        elif spot[0] == NOP:
            pass
        print(f"Pos: {position} Score: {score}, instruction {spot[0]} Rolled: {roll}")
    # Ends the loop and prints the final outcome of the game
    print(f"Final Pos: {position} Final Score: {score}, Instruction {spot[0]}")


def main():
    """
    Serves as the main function for the entire game and asks the user if they would like to play again
    :return: None
    """
    play = play_again("yes")
    while play:
        board = input("Board Size and Seed: ").split()
        # takes the board size in as an integer
        board_size = int(board[0])
        # takes the seed in as an integer
        seed = int(board[1])

        new_map = make_grid(board_size)
        gen_map = generate_random_map(board_size, seed)
        for i in range(len(gen_map)):
            # creates the board, index of each space, and instructions
            fill_grid_square(new_map, board_size, i, f'{i}\n{gen_map[i]}')
        for j in range(len(new_map)):
            print(''.join(new_map[j]))
        play_game(gen_map)
        user_input = input("Would you like to play again? ")
        play = play_again(user_input)


def play_again(user_input):
    """
    After the game is run this function executes based on the user's input to the question
    :param user_input: Checks for the user input on playing again or not
    :return: True or False depending on user input
    """
    # If user input is yes then the game replays otherwise it ends
    if user_input.lower() == YES:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
