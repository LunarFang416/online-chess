import pygame
from typing import List, Tuple
from helpers import legal_move

NORTH = [-1,0]
SOUTH = [1,0]
EAST = [0,1]
WEST = [0,-1]
SOUTH_EAST = [1,1]
SOUTH_WEST = [1,-1]
NORTH_EAST = [-1,1]
NORTH_WEST = [-1,-1]

# For color 1: white, 0: black

class ChessPiece():
    # def __init__(self, name: str, x_pos: int, y_pos: int, image: str, color: int, computer=False, in_game=True):
    #     self.name = name
    #     self.x_pos = x_pos
    #     self.y_pos = y_pos
    #     self.in_game = in_game
    #     self.image = image
    #     self.color = color
    #     self.computer = computer

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name")
        self.x_pos = kwargs.get("x_pos")
        self.y_pos = kwargs.get("y_pos")
        self.in_game = kwargs.get("in_game")
        self.image = kwargs.get("image")
        self.color = kwargs.get("color")
        self.computer = kwargs.get("computer")
        self.pawn_move = kwargs.get("pawn_move")
    
    def update_pos(self, new_x_pos: int, new_y_pos: int):
        self.x_pos = new_x_pos
        self.y_pos = new_y_pos

    def possible_plays(self, board: List[List[int]], x_pos: int, y_pos: int, directions: List[List[int]], max_distance : int) -> Tuple[List[List[int]], List[List[int]]]:
        open_spots = []
        elimination_spots = []
        row, col = len(board), len(board[0])
        for r_dir, c_dir in directions: 
            c_x_pos, c_y_pos = x_pos, y_pos
            count = 0
            while legal_move(c_x_pos, c_y_pos, r_dir, c_dir, row, col) and count != max_distance:
                c_x_pos += r_dir
                c_y_pos += c_dir
                if board[c_x_pos][c_y_pos] == None: 
                    open_spots.append((c_x_pos, c_y_pos))
                    count += 1
                    continue
                elif board[c_x_pos][c_y_pos].color == (not self.color):
                    elimination_spots.append((c_x_pos, c_y_pos))
                break
                

        return (open_spots, elimination_spots) 

    def valid_move(self, board: List[List[int]], new_x_pos: int, new_y_pos: int) -> bool:
        if (new_x_pos, new_y_pos) in self.possible_moves(board)[0]:
            return True
        return False
    
    def __str__(self):
        return f"[ {self.name} at <{self.x_pos}, {self.y_pos}> ]"


class Queen(ChessPiece):
    directions = [NORTH, SOUTH, EAST, WEST, NORTH_WEST, SOUTH_WEST, NORTH_EAST, SOUTH_EAST]

    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        return self.possible_plays(board, self.x_pos, self.y_pos, Queen.directions, 8)


class King(ChessPiece):
    directions = [NORTH, SOUTH, EAST, WEST, NORTH_WEST, SOUTH_WEST, NORTH_EAST, SOUTH_EAST]
    
    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        return self.possible_plays(board, self.x_pos, self.y_pos, King.directions, 1)


class Bishop(ChessPiece):
    directions = [NORTH_WEST, SOUTH_WEST, NORTH_EAST, SOUTH_EAST]
    
    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        return self.possible_plays(board, self.x_pos, self.y_pos, Bishop.directions, 8)

class Rook(ChessPiece):
    directions = [NORTH, SOUTH, EAST, WEST]

    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        return self.possible_plays(board, self.x_pos, self.y_pos, Rook.directions, 8)


class Pawn:
    directions = [NORTH]
    elim_directions = [NORTH_EAST, NORTH_WEST]

    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        if self.pawn_move == 0:
            reg_moves, elim_moves = self.possible_plays(board, self.x_pos, self.y_pos, Pawn.directions, 2)
            elim_moves += self.possible_plays(board, self.x_pos, self.y_pos, Pawn.elim_directions, 1)[1]

            return (reg_moves, elim_moves)
        else:
            reg_moves, elim_moves = self.possible_plays(board, self.x_pos, self.y_pos, Pawn.directions, 1)
            elim_moves += self.possible_plays(board, self.x_pos, self.y_pos, Pawn.elim_directions, 1)[1]

            return (reg_moves, elim_moves)

class Knight(ChessPiece):
    directions = [[2, 1], [2, -1], [-2, -1], [-2, 1], [-1, 2], [-1, -2], [1, 2], [-1, 2]]

    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        return self.possible_plays(board, self.x_pos, self.y_pos, Knight.directions, 1)