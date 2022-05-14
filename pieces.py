import os
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

WHITE_KING_IMAGE = os.path.join("piecess", "white_king.png")
WHITE_QUEEN_IMAGE = os.path.join("piecess", "white_queen.png")
WHITE_BISHOP_IMAGE = os.path.join("piecess", "white_bishop.png")
WHITE_ROOK_IMAGE = os.path.join("piecess", "white_rook.png")
WHITE_PAWN_IMAGE = os.path.join("piecess", "white_pawn.png")
WHITE_KNIGHT_IMAGE = os.path.join("piecess", "white_knight.png")

BLACK_KING_IMAGE = os.path.join("piecess", "black_king.png")
BLACK_QUEEN_IMAGE = os.path.join("piecess", "black_queen.png")
BLACK_BISHOP_IMAGE = os.path.join("piecess", "black_bishop.png")
BLACK_ROOK_IMAGE = os.path.join("piecess", "black_rook.png")
BLACK_PAWN_IMAGE = os.path.join("piecess", "black_pawn.png")
BLACK_KNIGHT_IMAGE = os.path.join("piecess", "black_knight.png")

# For color 1: white, 0: black

class ChessPiece():
    def __init__(self, x_pos: int, y_pos: int, color: int, **kwargs) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.in_game = True
        self.is_selected = False
        self.computer = kwargs.get("computer")
        self.pawn_move = kwargs.get("pawn_move")
    
    def update_pos(self, new_x_pos: int, new_y_pos: int) -> None:
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
                if board[c_x_pos][c_y_pos].piece == None: 
                    open_spots.append((c_x_pos, c_y_pos))
                    count += 1
                    continue
                elif board[c_x_pos][c_y_pos].piece.color == (not self.color):
                    elimination_spots.append((c_x_pos, c_y_pos))
                break
    
        return (open_spots, elimination_spots) 

    def valid_move(self, board: List[List[int]], new_x_pos: int, new_y_pos: int) -> bool:
        if (new_x_pos, new_y_pos) in self.possible_moves(board)[0]:
            return True
        return False

    def eliminate(self) -> None:
        self.in_game = False

    def __str__(self) -> str:
        return f"[ {self.color} {type(self).__name__} at <{self.x_pos}, {self.y_pos}>]"


class Queen(ChessPiece):
    directions = [NORTH, SOUTH, EAST, WEST, NORTH_WEST, SOUTH_WEST, NORTH_EAST, SOUTH_EAST]
    COLOR = [BLACK_QUEEN_IMAGE, WHITE_QUEEN_IMAGE]
    
    def __init__(self, x_pos: int, y_pos: int, color: int, **kwargs):
        super(Queen, self).__init__(x_pos, y_pos, color, **kwargs)
        self.image = Queen.COLOR[self.color]

    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        return self.possible_plays(board, self.x_pos, self.y_pos, Queen.directions, 8)


class King(ChessPiece):
    directions = [NORTH, SOUTH, EAST, WEST, NORTH_WEST, SOUTH_WEST, NORTH_EAST, SOUTH_EAST]
    COLOR = [BLACK_KING_IMAGE, WHITE_KING_IMAGE]

    def __init__(self, x_pos: int, y_pos: int, color: int, **kwargs):
        super(King, self).__init__(x_pos, y_pos, color, **kwargs)
        self.image = King.COLOR[self.color]
    
    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        return self.possible_plays(board, self.x_pos, self.y_pos, King.directions, 1)

    def is_check_mate(self, board):
        king_possible_moves, king_possible_elims = self.possible_moves(board)
        all_possibilities = king_possible_moves + king_possible_elims

        if not all_possibilities: return False
        outcomes = []
        for x, y in king_possible_moves:
            all_white_targets = []
            for row in board:
                for square in row:
                    if square.piece and square.piece.color == (not self.color):
                        all_white_targets += square.piece.possible_moves(board)[1]

            if (x, y) in all_white_targets: outcomes.append(True)
            else: return False

        board_copy = board[:]

        for x, y in king_possible_elims:
            all_white_targets = []
            temp = board_copy[x][y].piece
            board_copy[x][y].piece = board_copy[self.x_pos][self.y_pos].piece
            board_copy[self.x_pos][self.y_pos].piece = None
            
            for row in board_copy:
                for square in row:
                    if square.piece and square.piece.color == (not self.color):
                        all_white_targets += square.piece.possible_moves(board)[1]

            board_copy[self.x_pos][self.y_pos].piece = board_copy[x][y].piece
            board_copy[x][y].piece = temp
            
            if (x, y) in all_white_targets: outcomes.append(True)
            else: return False
        return True
        


class Bishop(ChessPiece):
    directions = [NORTH_WEST, SOUTH_WEST, NORTH_EAST, SOUTH_EAST]
    COLOR = [BLACK_BISHOP_IMAGE, WHITE_BISHOP_IMAGE]

    def __init__(self, x_pos: int, y_pos: int, color: int, **kwargs):
        super(Bishop, self).__init__(x_pos, y_pos, color, **kwargs)
        self.image = Bishop.COLOR[self.color]
    
    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        return self.possible_plays(board, self.x_pos, self.y_pos, Bishop.directions, 8)

class Rook(ChessPiece):
    directions = [NORTH, SOUTH, EAST, WEST]
    COLOR = [BLACK_ROOK_IMAGE, WHITE_ROOK_IMAGE]

    def __init__(self, x_pos: int, y_pos: int, color: int, **kwargs):
        super(Rook, self).__init__(x_pos, y_pos, color, **kwargs)
        self.image = Rook.COLOR[self.color]

    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        return self.possible_plays(board, self.x_pos, self.y_pos, Rook.directions, 8)


class Pawn(ChessPiece):
    directions = [[SOUTH], [NORTH]]
    elim_directions = [[SOUTH_EAST, SOUTH_WEST], [NORTH_EAST, NORTH_WEST]]
    COLOR = [BLACK_PAWN_IMAGE, WHITE_PAWN_IMAGE]

    def __init__(self, x_pos: int, y_pos: int, color: int, **kwargs):
        super(Pawn, self).__init__(x_pos, y_pos, color, **kwargs)
        self.image = Pawn.COLOR[self.color]

    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        if self.pawn_move == 0:
            reg_moves, elim_moves = self.possible_plays(board, self.x_pos, self.y_pos, Pawn.directions[self.color], 2)
            elim_moves = self.possible_plays(board, self.x_pos, self.y_pos, Pawn.elim_directions[self.color], 1)[1]
            # self.pawn_move += 1
            return (reg_moves, elim_moves)
        else:
            reg_moves, elim_moves = self.possible_plays(board, self.x_pos, self.y_pos, Pawn.directions[self.color], 1)
            elim_moves = self.possible_plays(board, self.x_pos, self.y_pos, Pawn.elim_directions[self.color], 1)[1]

            return (reg_moves, elim_moves)

class Knight(ChessPiece):
    directions = [[2, 1], [2, -1], [-2, -1], [-2, 1], [-1, 2], [-1, -2], [1, 2], [-1, 2]]
    COLOR = [BLACK_KNIGHT_IMAGE, WHITE_KNIGHT_IMAGE]

    def __init__(self, x_pos: int, y_pos: int, color: int, **kwargs):
        super(Knight, self).__init__(x_pos, y_pos, color, **kwargs)
        self.image = Knight.COLOR[self.color]

    def possible_moves(self, board: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        return self.possible_plays(board, self.x_pos, self.y_pos, Knight.directions, 1)