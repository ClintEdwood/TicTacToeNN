"""player module"""

import random


class PlayerClass:
  """player for tic-tac-toe"""

  def __init__(self, name, symbol, bot):
    self.name = name
    self.symbol = symbol
    self.bot = bot

  def player_move(self, legal_moves):
    """return a random valid move for bot"""
    if self.bot:
      return random.choice(legal_moves)

    return input(f"{self.name}'s move: ").split()
