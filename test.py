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
    screen.fill("blue")
    b.draw(surf)
    screen.blit(surf, surf_rect)
    pygame.display.update()
    clock.tick(60)