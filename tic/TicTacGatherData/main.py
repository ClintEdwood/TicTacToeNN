""" main module"""
from os import name as os_name
from os import system as os_system
import pandas as pd
from pandas import DataFrame
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


def buildRowObject(board: BoardClass, move: List[int]):
    curr_board = board.board_state
    return {"0 0": [curr_board[0][0]], "0 1": [curr_board[0][1]], "0 2": [curr_board[0][2]],
            "1 0": [curr_board[1][0]], "1 1": [curr_board[1][1]], "1 2": [curr_board[1][2]],
            "2 0": [curr_board[2][0]], "2 1": [curr_board[2][1]], "2 2": [curr_board[2][2]],
            "Move": [str(int(move[0])) + " " + str(int(move[1]))]}


def save_board_state(df: DataFrame, board: BoardClass, move: List[int]):
    new_row = pd.DataFrame(buildRowObject(board, move))
    return pd.concat([df, new_row], ignore_index=True)


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
    # Open data.csv to add more data
    try:
        df = pd.read_csv("data.csv")
    except FileNotFoundError:
        df = pd.DataFrame()

    """main routine - print the game and check for win"""
    won_local = WON_ASCII
    lost_local = LOST_ASCII
    draw_local = DRAW_ASCII

    playing_board = BoardClass()
    player_one = PlayerClass('BOT_RealBob', 'X', True)

    player_name = input('Please input your name: ')
    player_two = PlayerClass(player_name, 'O', False)
    print(f'Hi {player_one.name} your opponent is {player_two.name}!')
    print('Please write your move in coordinates x y.')
    print('(x for the row and y for the column)')

    player_now = player_one
    game_counter = 0

    while True:
        playing_board.print_board()
        move = player_now.player_move(playing_board.next_move(player_two.symbol))

        if not check_input(move):
            clear_term()
            print("Wrong input")
            continue

        if not player_now.bot:
            df = save_board_state(df, playing_board, move)

        x_cord = int(move[0])
        y_cord = int(move[1])

        if playing_board.make_move(x_cord, y_cord, player_now.symbol):
            if playing_board.is_win(playing_board.board_state, player_now.symbol):
                df.to_csv("data.csv", sep=',', index=False)
                clear_term()
                if player_now == player_one:
                    print(won_local)
                else:
                    print(lost_local)
                break

            if game_counter == 8:
                df.to_csv("data.csv", sep=',', index=False)
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
