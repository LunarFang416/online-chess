import pygame
from pieces import Queen, Pawn, King, Knight, Rook, Bishop
from board import Board
from sys import exit
from client import Client

WIDTH, HEIGHT = 700, 700
BOARD_WIDTH, BOARD_HEIGHT = 600, 600
MOVE_PLAYED = "!MOVE_PLAYED"
BOARD_UPDATE = "!BOARD_UPDATE"

def connect():
    global client
    client = Client()
    return client.board

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

wait = pygame.font.Font(None, 65)
msg = wait.render("WAITING FOR OPPONENT", True, 'blue')
msg_rect = msg.get_rect(center = (WIDTH / 2, HEIGHT /2))

b = connect()

surf = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
surf_rect = surf.get_rect(center = (WIDTH / 2, HEIGHT / 2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            print(event)
            client.disconnect()
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and client.game >= 2:
            x, y = event.pos
            x , y = x - 50, y - 50
            # Sending it in y - 50, and x - 50 as pygame gives coordinates in differnet fipped format
            if 0 <= x <= BOARD_WIDTH and 0 <= y <= BOARD_HEIGHT:
                move = b.select_sqaure(screen, y, x)
                if move == MOVE_PLAYED: 
                    client.send({"type": BOARD_UPDATE, "data": client.board.board})
    screen.fill("white")
    b.draw(surf)
    screen.blit(surf, surf_rect)
    if client.game < 2: 
        screen.blit(msg, msg_rect)
    pygame.display.update()
    clock.tick(60)