import pygame
from pieces import Queen, Pawn, King, Knight, Rook, Bishop
from board import Board
from sys import exit

WIDTH, HEIGHT = 700, 700
BOARD_WIDTH, BOARD_HEIGHT = 600, 600

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

b = Board(0)
surf = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
surf_rect = surf.get_rect(center = (WIDTH / 2, HEIGHT / 2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            print(event)
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x , y = x - 50, y - 50
            # Sending it in y - 50, and x - 50 as pygame gives coordinates in differnet fipped format
            if 0 <= x <= BOARD_WIDTH and 0 <= y <= BOARD_HEIGHT:
                b.select_sqaure(screen, y, x)
    screen.fill("white")
    b.draw(surf)
    screen.blit(surf, surf_rect)
    pygame.display.update()
    clock.tick(60)