def legal_move(x_pos: int, y_pos: int, r_dir: int, c_dir, max_row:int, max_col) -> bool:
    return 0 <= x_pos + r_dir < max_row and 0 <= y_pos + c_dir < max_col
