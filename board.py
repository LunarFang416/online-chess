import pygame
from typing import List, Tuple
from pieces import King, Queen, Pawn, Rook, Bishop, Knight, ChessPiece

WHITE_PAWN_POS = [[6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7]]
WHITE_QUEEN_POS = [[7, 3]]
WHITE_KING_POS = [[7, 4]]
WHITE_ROOK_POS = [[7, 0], [7, 7]]
WHITE_BISHOP_POS = [[7, 2], [7, 5]]
WHITE_KNIGHT_POS = [[7, 1], [7, 6]]

BLACK_PAWN_POS = [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7]]
BLACK_QUEEN_POS = [[0, 3]]
BLACK_KING_POS = [[0, 4]]
BLACK_ROOK_POS = [[0, 0], [0, 7]]
BLACK_BISHOP_POS = [[0, 2], [0, 5]]
BLACK_KNIGHT_POS = [[0, 1], [0, 6]]

PIECES_DATA = [
    [0, {Queen: BLACK_QUEEN_POS, Pawn: BLACK_PAWN_POS, King: BLACK_KING_POS, Rook: BLACK_ROOK_POS, Bishop: BLACK_BISHOP_POS, Knight: BLACK_KNIGHT_POS}],
    [1, {Queen: WHITE_QUEEN_POS, Pawn: WHITE_PAWN_POS, King: WHITE_KING_POS, Rook: WHITE_ROOK_POS, Bishop: WHITE_BISHOP_POS, Knight: WHITE_KNIGHT_POS}],
]

class Board:
    # These values are just temporary
    BOARD_SIDE_LENGTH = 600
    PIECE_SIDE_LENGTH = 600/8

    def __init__(self, color: int) -> None:
        # Color will make sure that the players color is facing them
        self.color = color
        self.rows = 8
        self.col = 8
        self.board = [[[None, {"data":''}] for i in range(8)] for j in range(8)]
        for i in range(len(PIECES_DATA)):
            for piece in PIECES_DATA[i][1]:
                for x, y in PIECES_DATA[i][1][piece]:
                    print(x, y)
                    self.board[x][y][0] = piece(x, y, PIECES_DATA[i][0])

        color = "#ADD8E6"
        isWhite=True
        for i in range(8):
            for j in range(8):
                if(isWhite==1):
                    color="#ADD8E6"
                else :
                    color="#a7ffb5"
                if self.color:
                    self.board[i][j][1] = {"sq_x":Board.PIECE_SIDE_LENGTH*j, "sq_y": Board.PIECE_SIDE_LENGTH*i, "side_length": Board.PIECE_SIDE_LENGTH, "color":color}
                else:
                    self.board[i][j][1] = {"sq_x":Board.PIECE_SIDE_LENGTH*(7 - j), "sq_y": Board.PIECE_SIDE_LENGTH*(7 - i), "side_length": Board.PIECE_SIDE_LENGTH, "color":color}

                print(self.board[i][j][0])
                isWhite = not isWhite
            isWhite = not isWhite
        print(self.board)

    def draw(self, screen) -> None:
        for row in self.board:
            for data in row:
                pygame.draw.rect(screen,data[1]['color'],pygame.Rect(data[1]['sq_x'], data[1]['sq_y'], data[1]['side_length'], data[1]['side_length']))
                if data[0]:
                    piece_image = pygame.image.load(data[0].image)
                    piece_image_rect = piece_image.get_rect(topleft = (data[1]['sq_x'], data[1]['sq_y']))
                    screen.blit(piece_image, piece_image_rect)

