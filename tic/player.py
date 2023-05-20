"""player module"""

import pandas as pd
import numpy as np
from board import BoardClass
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder

features = ["0 0", "0 1", "0 2", "1 0", "1 1", "1 2", "2 0", "2 1", "2 2"]
CLASSES = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]


# Auxilary function to translate the current field to model lingo
def feed_board(board: BoardClass):
    curr_board = board.board_state
    dict = {"0 0": [curr_board[0][0]], "0 1": [curr_board[0][1]], "0 2": [curr_board[0][2]],
            "1 0": [curr_board[1][0]], "1 1": [curr_board[1][1]], "1 2": [curr_board[1][2]],
            "2 0": [curr_board[2][0]], "2 1": [curr_board[2][1]], "2 2": [curr_board[2][2]]}
    conv_df = pd.DataFrame.from_dict(dict)
    le_X = LabelEncoder()
    le_X.fit(np.unique(conv_df))
    return np.array([le_X.transform(samp) for samp in conv_df.values])


class PlayerClass:
    """player for tic-tac-toe"""

    def __init__(self, name, symbol, bot):
        self.name = name
        self.symbol = symbol
        self.bot = bot
        self.model = load_model("tictacModel")

    def player_move(self, board_state: BoardClass, legal_moves):
        """return a predicted valid move for bot"""
        if self.bot:
            return self.move_prediction_by_model(board_state, legal_moves)
        return input(f"{self.name}'s move: ").split()

    def move_prediction_by_model(self, board_state: BoardClass, legal_moves):
        predictions = self.model.predict(feed_board(board_state))[0].tolist()
        while True:
            rec_index = predictions.index(max(predictions))
            pred = CLASSES[rec_index]

            if not pred in legal_moves:
                predictions[rec_index] = -1
                continue
            return pred
