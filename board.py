import pygame
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
    # These values are just temporary
    BOARD_SIDE_LENGTH = 600
    PIECE_SIDE_LENGTH = 30

    def __init__(self) -> None:
        self.rows = 8
        self.col = 8
        self.board = [[None for i in range(8)] for j in range(8)]
        for i in range(len(PIECES_DATA)):
            for piece in PIECES_DATA[i]:
                for x, y in PIECES_DATA[i][piece]:
                    self.board[x][y] = piece(x, y, i)
    
    def draw(self, screen) -> None:
        # Draw board first
        # Just for test, its ugly asf rn
        for row in self.board:
            for piece in row:
                if piece: 
                    piece_image = pygame.image.load(piece.image)
                    piece_image_rect = piece_image.get_rect(bottomleft = (piece.y_pos * Board.PIECE_SIDE_LENGTH, piece.x_pos * Board.PIECE_SIDE_LENGTH))
                    screen.blit(piece_image, piece_image_rect)



# print(PIECES_DATA)
b = Board()
# print(b.draw(pygame.display.set_mode((777, 666))))
