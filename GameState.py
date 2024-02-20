import Piece
from Player import Player


class GameState:
    def __init__(self, player_turn: Player, selected_piece: Piece, selected_piece_move_options, echec_et_mat):
        self.player_turn = player_turn
        self.selected_piece = selected_piece
        self.selected_piece_move_options = selected_piece_move_options
        self.winner = None
        self.echec_et_mat = False
