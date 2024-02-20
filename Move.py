import Piece


class Move:
    def __init__(self, start_piece: Piece, next_pos: (int, int), is_eat):
        self.start_piece = start_piece
        self.next_pos = next_pos
        self.is_eat = is_eat

    def __eq__(self, __o: object) -> bool:
        return self.next_pos == __o

