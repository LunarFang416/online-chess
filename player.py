from typing import List
from pieces import ChessPiece

class Player:
    def __init__(self, color: int, captured_players: List[ChessPiece]) -> None:
        self.color = color
        self.captured_players = captured_players

    def player_captured(self, player):
        self.captured_players.append(player)