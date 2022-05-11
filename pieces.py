import pygame
from typing import List, Tuple
from helpers import possible_plays

NORTH = [-1,0]
SOUTH = [1,0]
EAST = [0,1]
WEST = [0,-1]
SOUTH_EAST = [1,1]
SOUTH_WEST = [1,-1]
NORTH_EAST = [-1,1]
NORTH_WEST = [-1,-1]


class ChessPiece():
    def __init__(self, name: str, x_pos: int, y_pos: int, image: str, color: str, computer=False, in_game=True):
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.in_game = in_game
        self.image = image
        self.color = color
        self.computer = computer
    
    def update_pos(self, new_x_pos: int, new_y_pos: int):
        self.x_pos = new_x_pos
        self.y_pos = new_y_pos
    
    def __str__(self):
        return f"[ {self.name} at <{self.x_pos}, {self.y_pos}> ]"


class Queen(ChessPiece):
    directions = [NORTH, SOUTH, EAST, WEST, NORTH_WEST, SOUTH_WEST, NORTH_EAST, SOUTH_EAST]

    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        return possible_plays(board, self.x_pos, self.y_pos, Queen.directions)
    
    

class King(ChessPiece):
    pass

class Bishop(ChessPiece):
    pass

class Rook(ChessPiece):
    pass

class Knight(ChessPiece):
    pass