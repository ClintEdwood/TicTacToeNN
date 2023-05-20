""" main module"""
from os import name as os_name
from os import system as os_system
from typing import List
from board import BoardClass
from player import PlayerClass

WON_ASCII = """
▄██   ▄    ▄██████▄  ███    █▄        ▄█     █▄   ▄██████▄  ███▄▄▄▄   
███   ██▄ ███    ███ ███    ███      ███     ███ ███    ███ ███▀▀▀██▄ 
███▄▄▄███ ███    ███ ███    ███      ███     ███ ███    ███ ███   ███ 
▀▀▀▀▀▀███ ███    ███ ███    ███      ███     ███ ███    ███ ███   ███ 
▄██   ███ ███    ███ ███    ███      ███     ███ ███    ███ ███   ███ 
███   ███ ███    ███ ███    ███      ███     ███ ███    ███ ███   ███ 
███   ███ ███    ███ ███    ███      ███ ▄█▄ ███ ███    ███ ███   ███ 
 ▀█████▀   ▀██████▀  ████████▀        ▀███▀███▀   ▀██████▀   ▀█   █▀  
"""

LOST_ASCII = """
▄██   ▄    ▄██████▄  ███    █▄        ▄█        ▄██████▄     ▄████████     ███     
███   ██▄ ███    ███ ███    ███      ███       ███    ███   ███    ███ ▀█████████▄ 
███▄▄▄███ ███    ███ ███    ███      ███       ███    ███   ███    █▀     ▀███▀▀██ 
▀▀▀▀▀▀███ ███    ███ ███    ███      ███       ███    ███   ███            ███   ▀ 
▄██   ███ ███    ███ ███    ███      ███       ███    ███ ▀███████████     ███     
███   ███ ███    ███ ███    ███      ███       ███    ███          ███     ███     
███   ███ ███    ███ ███    ███      ███▌    ▄ ███    ███    ▄█    ███     ███     
 ▀█████▀   ▀██████▀  ████████▀       █████▄▄██  ▀██████▀   ▄████████▀     ▄████▀   
                                     ▀
"""

DRAW_ASCII = """
████████▄     ▄████████    ▄████████  ▄█     █▄  
███   ▀███   ███    ███   ███    ███ ███     ███ 
███    ███   ███    ███   ███    ███ ███     ███ 
███    ███  ▄███▄▄▄▄██▀   ███    ███ ███     ███ 
███    ███ ▀▀███▀▀▀▀▀   ▀███████████ ███     ███ 
███    ███ ▀███████████   ███    ███ ███     ███ 
███   ▄███   ███    ███   ███    ███ ███ ▄█▄ ███ 
████████▀    ███    ███   ███    █▀   ▀███▀███▀  
             ███    ███                          
"""


def clear_term():
    """attempt to clear terminal on unix and nt system"""
    # https://stackoverflow.com/a/2084628
    os_system('cls' if os_name == 'nt' else 'clear')

def check_input(inputMove: List[int]) -> bool:
    if len(inputMove) != 2:
        return False
    for i in range(len(inputMove)):
        try:
            num = int(inputMove[i])
            if num > 2 or num < 0:
                return False
        except:
            return False
    return True


def start_game():
    """main routine - print the game and check for win"""
    won_local = WON_ASCII
    lost_local = LOST_ASCII
    draw_local = DRAW_ASCII

    playing_board = BoardClass()
    player_two = PlayerClass('BOT_RealBob', 'O', True)

    player_name = input('Please input your name: ')
    player_one = PlayerClass(player_name, 'X', False)
    print(f'Hi {player_one.name} your opponent is {player_two.name}!')
    print('Please write your move in coordinates x y.')
    print('(x for the row and y for the column)')

    player_now = player_one
    game_counter = 0

    while True:
        playing_board.print_board()
        move = player_now.player_move(playing_board, playing_board.next_move(player_two.symbol))

        if not check_input(move):
            clear_term()
            print("Wrong input")
            continue

        x_cord = int(move[0])
        y_cord = int(move[1])

        if playing_board.make_move(x_cord, y_cord, player_now.symbol):
            if playing_board.is_win(playing_board.board_state, player_now.symbol):
                clear_term()
                if player_now == player_one:
                    print(won_local)
                else:
                    print(lost_local)
                break

            if game_counter == 8:
                clear_term()
                print(draw_local)
                break

            game_counter += 1
            player_now = player_one if player_now == player_two else player_two

        clear_term()


# Main
while True:
    start_game()
    inp = input("Play again? (y/n)\n")
    if inp == "y":
        continue
    elif inp == "n":
        break
    else:
        print("Wrong input")
