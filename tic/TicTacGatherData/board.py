"""board module"""
from copy import deepcopy


class BoardClass:
    """playing board for tic-tac-toe"""

    def __init__(self):
        self.board_state = self.create_board()

    @staticmethod
    def create_board():
        """create playing board"""
        board = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
        return board

    def print_board(self):
        """print the board state"""
        guard_string = '-' * 13
        print('    0   1   2')
        print(f'  {guard_string}')
        row_count = 0
        for row in self.board_state:
            print(f"""{row_count} | {row[0]} | {row[1]} | {row[2]} |
  {guard_string}""")
            row_count += 1

    def make_move(self, x_cord, y_cord, symbol):
        """make a move with a given symbol
    also check validity"""
        if self.move_valid(x_cord, y_cord):
            self.board_state[x_cord][y_cord] = symbol
            return True

        return False

    def move_valid(self, x_cord, y_cord):
        """check if a move is valid"""
        if 0 <= x_cord < len(self.board_state[0]):
            if 0 <= y_cord < len(self.board_state[0]):
                return self.board_state[x_cord][y_cord] == '.'

        return False

    @staticmethod
    def is_win(board, symbol):
        """check if the game is won"""
        return any([  # row
            board[0][0] == board[0][1] == board[0][2] == symbol,
            board[1][0] == board[1][1] == board[1][2] == symbol,
            board[2][0] == board[2][1] == board[2][2] == symbol,
            # cross
            board[0][0] == board[1][1] == board[2][2] == symbol,
            board[2][0] == board[1][1] == board[0][2] == symbol,
            # column
            board[0][0] == board[1][0] == board[2][0] == symbol,
            board[0][1] == board[1][1] == board[2][1] == symbol,
            board[0][2] == board[1][2] == board[2][2] == symbol
        ])

    def legal_moves(self):
        """return a list of all legal moves at a board state"""
        return [(row, col) for row in range(3) for col in range(3)
                if self.board_state[row][col] == '.']

    def next_move(self, symbol):
        """return list of legal moves or a winning move"""
        legal_moves = self.legal_moves()
        test_board = deepcopy(self.board_state)

        for x_cord, y_cord in legal_moves:
            test_board[x_cord][y_cord] = symbol
            if self.is_win(test_board, symbol):
                return [(x_cord, y_cord)]

            test_board[x_cord][y_cord] = '.'

        return legal_moves
