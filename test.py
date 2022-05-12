import pygame
from pieces import Queen, Pawn, King, Knight, Rook, Bishop
from board import Board
from sys import exit
pygame.init()

# q = Queen(name="queen", color="black", x_pos=0, y_pos=0)

# test_board = [[None for i in range(8)] for j in range(8)]


# # q = Knight(name="queen", x_pos=4, y_pos=4, in_game = True, color=1)

# print(Queen.directions)

#([(6, 5), (6, 3), (2, 3), (2, 5), (3, 6), (3, 2), (5, 6), (3, 6)], [])


screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

piece = pygame.image.load("chess_pieces/black_king.svg")
piece_surface = piece.get_rect(center = (600, 600))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            print(event)
            pygame.quit()
            exit()
    screen.fill("blue")
    b = Board()
    b.draw(screen)
    pygame.display.update()
    clock.tick(60)