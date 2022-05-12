from typing import List, Tuple
from pieces import King, Queen, Pawn, Rook, Bishop, Knight, ChessPiece

WHITE_PAWN_POS = [[6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7]]
WHITE_QUEEN_POS = [[7, 3]]
WHITE_KING_POS = [[7, 4]]
WHITE_ROOK_POS = [[7, 0], [7, 7]]
WHITE_BISHOP_POS = [[7, 2], [7, 5]]
WHITE_KNIGHT_POS = [[7, 1], [7, 6]]

BLACK_PAWN_POS = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7]]
BLACK_QUEEN_POS = [[0, 3]]
BLACK_KING_POS = [[0, 4]]
BLACK_ROOK_POS = [[0, 0], [0, 7]]
BLACK_BISHOP_POS = [[0, 2], [0, 5]]
BLACK_KNIGHT_POS = [[0, 1], [0, 6]]

PIECES_DATA = [
    {Queen: WHITE_QUEEN_POS, Pawn: WHITE_PAWN_POS, King: WHITE_KING_POS, Rook: WHITE_ROOK_POS, Bishop: WHITE_BISHOP_POS, Knight: WHITE_KNIGHT_POS},
    {Queen: BLACK_QUEEN_POS, Pawn: BLACK_PAWN_POS, King: BLACK_KING_POS, Rook: BLACK_ROOK_POS, Bishop: BLACK_BISHOP_POS, Knight: BLACK_KNIGHT_POS}
]

class Board:
    def __init__(self):
        self.rows = 8
        self.col = 8
        self.board = [[None for i in range(8)] for j in range(8)]
        for i in range(len(PIECES_DATA)):
            for piece in PIECES_DATA[i]:
                for x, y in PIECES_DATA[i][piece]:
                    self.board[x][y] = piece(x, y, i)
                

        print(self.board)
    


print(PIECES_DATA)
b = Board()
