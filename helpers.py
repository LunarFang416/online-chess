from typing import List, Tuple

def legal_move(x_pos: int, y_pos: int, r_dir: int, c_dir, max_row:int, max_col) -> bool:
    return 0 <= x_pos + r_dir < max_row and 0 <= y_pos + c_dir < max_col

def possible_plays(board: List[List[int]], x_pos: int, y_pos: int, directions: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
    open_spots = []
    elimination_spots = []
    row, col = len(board), len(board[0])
    for r_dir, c_dir in directions: 
        c_x_pos, c_y_pos = x_pos, y_pos
        while legal_move(c_x_pos, c_y_pos, r_dir, c_dir, row, col):
            c_x_pos += r_dir
            c_y_pos += c_dir
            if board[c_x_pos][c_y_pos] == None: 
                open_spots.append((c_x_pos, c_y_pos))
            elif board[c_x_pos][c_y_pos].color:
                elimination_spots.append((c_x_pos, c_y_pos))
                break

    return (open_spots, elimination_spots)    
