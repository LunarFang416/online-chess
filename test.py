import pygame
from board import Board
from sys import exit
from client import Client

pygame.init()

WIDTH, HEIGHT = 700, 700
BOARD_WIDTH, BOARD_HEIGHT = 600, 600
MOVE_PLAYED = "!MOVE_PLAYED"
BOARD_UPDATE = "!BOARD_UPDATE"
GAME_OVER = "!GAME_OVER"
CURRENT_MOVE = True

def connect():
    global client
    client = Client()
    return client.board

def text(screen, message, color, x, y):
    wait = pygame.font.Font(None, 65)
    msg = wait.render(message, True, color)
    msg_rect = msg.get_rect(center = (x, y))
    screen.blit(msg, msg_rect)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

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
        if event.type == pygame.MOUSEBUTTONDOWN and client.game >= 2 and client.your_move and (not client.game_over):
            x, y = event.pos
            x , y = x - 50, y - 50
            # Sending it in y - 50, and x - 50 to align coordinates
            if 0 <= x <= BOARD_WIDTH and 0 <= y <= BOARD_HEIGHT:
                move = b.select_sqaure(y, x)
                if move == MOVE_PLAYED:
                    is_end = False
                    if not client.color: 
                        is_winning = client.board.black_king.piece.is_check_mate(client.board.board)
                        if is_winning:
                            client.game_over, client.win = True, False
                            client.send({"type": GAME_OVER, "data": client.board.board, "win": True, "move": True})
                            is_end = True
                    else:
                        is_winning = client.board.white_king.piece.is_check_mate(client.board.board)
                        if is_winning:
                            client.game_over, client.win = True, False
                            client.send({"type": GAME_OVER, "data": client.board.board, "win": True, "move": True})
                            is_end = True
                    if not is_end:
                        CURRENT_MOVE, client.your_move = not CURRENT_MOVE, False
                        client.send({"type": BOARD_UPDATE, "data": client.board.board, "move": True})

    screen.fill("white")
    b.draw(surf)
    screen.blit(surf, surf_rect)

    if client.game < 2: 
        text(screen, "WAITING FOR OPPONENT", 'blue', WIDTH / 2, HEIGHT /2)
        b = client.board = Board(client.color)

    elif not client.game_over:
        if client.your_move: text(screen, "YOUR MOVE", 'blue', WIDTH / 2, HEIGHT - 20)
        else: text(screen, "OPPONENTS MOVE", 'red', WIDTH / 2, HEIGHT - 20)

    else:
        if client.win: text(screen, "YOU WIN :)", 'blue', WIDTH / 2, HEIGHT /2)
        else: text(screen, "YOU LOSE :(", 'red', WIDTH / 2, HEIGHT /2)

    pygame.display.update()
    clock.tick(60)