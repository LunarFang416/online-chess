import pygame
from board import Board
from sys import exit
from client import Client

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

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

wait = pygame.font.Font(None, 65)
msg = wait.render("WAITING FOR OPPONENT", True, 'blue')
msg_rect = msg.get_rect(center = (WIDTH / 2, HEIGHT /2))

your_move = wait.render("YOUR MOVE", True, 'blue')
your_move_rect = your_move.get_rect(center = (WIDTH / 2, HEIGHT - 20))

opp_move = wait.render("OPPONENTS MOVE", True, 'red')
opp_move_rect = opp_move.get_rect(center = (WIDTH / 2, HEIGHT - 20))

win_msg = wait.render("YOU WIN :)", True, 'blue')
win_msg_rect = win_msg.get_rect(center = (WIDTH / 2, HEIGHT /2))

lose_msg = wait.render("YOU LOSE :(", True, 'red')
lose_msg_rect = lose_msg.get_rect(center = (WIDTH / 2, HEIGHT /2))

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
            # Sending it in y - 50, and x - 50 as pygame gives coordinates in differnet fipped format
            if 0 <= x <= BOARD_WIDTH and 0 <= y <= BOARD_HEIGHT:
                move = b.select_sqaure(screen, y, x)
                if move == MOVE_PLAYED:
                    is_end = False
                    if not client.color: 
                        is_winning = client.board.black_king.piece.is_check_mate(client.board.board)
                        if is_winning:
                            client.game_over = True
                            client.win = False
                            client.send({"type": GAME_OVER, "data": client.board.board, "win":True,"move": True})
                            is_end = True
                        else:
                            is_winning = client.board.white_king.piece.is_check_mate(client.board.board)
                            if is_winning:
                                client.game_over = True
                                client.win = False
                                client.send({"type": GAME_OVER, "data": client.board.board, "win":True,"move": True})
                                is_end = True
                    if not is_end:
                        CURRENT_MOVE = not CURRENT_MOVE
                        client.your_move = False
                        client.send({"type": BOARD_UPDATE, "data": client.board.board, "move": True})

    screen.fill("white")
    b.draw(surf)
    screen.blit(surf, surf_rect)
    if client.game < 2: 
        screen.blit(msg, msg_rect)
        b = client.board = Board(client.color)
    elif not client.game_over:
        if client.your_move:
            screen.blit(your_move, your_move_rect)
        else:
            screen.blit(opp_move, opp_move_rect)
    else:
        if client.win:
            screen.blit(win_msg, win_msg_rect)
        else:
            screen.blit(lose_msg, lose_msg_rect)

    pygame.display.update()
    clock.tick(60)