from copy import deepcopy

import constants
from Piece import Pawn, Rook, Bishop, Queen, King, Knight


class Board:
    def __init__(self, grid=None):
        if not grid:
            self.grid = [[None for _ in range(constants.SIZE_BOARD)] for _ in range(constants.SIZE_BOARD)]
        else:
            self.grid = grid

    @staticmethod
    def position_to_coordinates(selected_dot):
        coordinate_x = selected_dot[0] * constants.SQUARE_SIZE + constants.MARGIN + constants.SQUARE_SIZE / 2
        coordinate_y = selected_dot[1] * constants.SQUARE_SIZE + constants.MARGIN + constants.SQUARE_SIZE / 2
        return coordinate_x, coordinate_y

    def click_in_board(self, given_point):
        return constants.UP_LEFT[0] <= given_point[0] <= constants.DOWN_RIGHT[0] and constants.UP_LEFT[1] <= \
            given_point[1] <= \
            constants.DOWN_RIGHT[1]

    def detect_square_position_from_click(self, x, y):
        select_square_x = int(
            ((x - constants.MARGIN) / (constants.DOWN_RIGHT[0] - constants.MARGIN)) * constants.SIZE_BOARD)
        select_square_y = int(
            ((y - constants.MARGIN) / (constants.DOWN_RIGHT[1] - constants.MARGIN)) * constants.SIZE_BOARD)
        return select_square_x, select_square_y

    def get_piece(self, selected_square):
        return self.grid[selected_square[0]][selected_square[1]]

    def put_pieces_start_config(self, player1, player2):
        # pawns
        for i in range(constants.SIZE_BOARD):
            self.grid[i][1] = Pawn(player2, i, 1)
            self.grid[i][constants.SIZE_BOARD - 2] = Pawn(player1, i, constants.SIZE_BOARD - 2)
        # rooks
        self.grid[0][constants.SIZE_BOARD - 1] = Rook(player1, 0, constants.SIZE_BOARD - 1)
        self.grid[constants.SIZE_BOARD - 1][constants.SIZE_BOARD - 1] = Rook(player1, constants.SIZE_BOARD - 1,
                                                                             constants.SIZE_BOARD - 1)
        self.grid[0][0] = Rook(player2, 0, 0)
        self.grid[constants.SIZE_BOARD - 1][0] = Rook(player2, constants.SIZE_BOARD - 1, 0)
        # bishops
        self.grid[2][constants.SIZE_BOARD - 1] = Bishop(player1, 2, constants.SIZE_BOARD - 1)
        self.grid[5][constants.SIZE_BOARD - 1] = Bishop(player1, 5, constants.SIZE_BOARD - 1)
        self.grid[2][0] = Bishop(player2, 2, 0)
        self.grid[5][0] = Bishop(player2, 5, 0)
        # queens
        self.grid[3][constants.SIZE_BOARD - 1] = Queen(player1, 3, constants.SIZE_BOARD - 1)
        self.grid[3][0] = Queen(player2, 3, 0)
        # kings
        self.grid[4][constants.SIZE_BOARD - 1] = King(player1, 4, constants.SIZE_BOARD - 1)
        self.grid[4][0] = King(player2, 4, 0)
        # knights
        self.grid[1][constants.SIZE_BOARD - 1] = Knight(player1, 1, constants.SIZE_BOARD - 1)
        self.grid[constants.SIZE_BOARD - 2][constants.SIZE_BOARD - 1] = Knight(player1, constants.SIZE_BOARD - 2,
                                                                               constants.SIZE_BOARD - 1)
        self.grid[constants.SIZE_BOARD - 2][0] = Knight(player2, constants.SIZE_BOARD - 2, 0)
        self.grid[1][0] = Knight(player2, 1, 0)

    def make_move(self, move):
        start_x = move.start_piece.x
        start_y = move.start_piece.y
        self.grid[move.next_pos[0]][move.next_pos[1]] = move.start_piece.return_deep_copied_piece()
        self.grid[move.next_pos[0]][move.next_pos[1]].x = move.next_pos[0]
        self.grid[move.next_pos[0]][move.next_pos[1]].y = move.next_pos[1]
        self.grid[start_x][start_y] = None

    def get_king_pos(self, player_turn):
        for y in range(constants.SIZE_BOARD):
            for x in range(constants.SIZE_BOARD):
                piece = self.grid[x][y]
                if piece:
                    if piece.owner == player_turn and isinstance(piece, King):
                        return piece.x, piece.y

    def return_deep_copied_grid(self):
        deep_copied_grid = [[None for _ in range(constants.SIZE_BOARD)] for _ in range(constants.SIZE_BOARD)]
        for y in range(constants.SIZE_BOARD):
            for x in range(constants.SIZE_BOARD):
                piece = self.grid[x][y]
                if piece:
                    deep_copied_grid[x][y] = piece.return_deep_copied_piece()
        return deep_copied_grid


def my_king_is_in_danger(grid, opponent, king_pos):
    for y in range(constants.SIZE_BOARD):
        for x in range(constants.SIZE_BOARD):
            opponent_piece = grid[x][y]
            if opponent_piece:
                if opponent_piece.owner == opponent:
                    opponent_piece_next_pos = opponent_piece.get_possible_next_moves(grid)
                    if king_pos in opponent_piece_next_pos:
                        return True
    return False


def remove_moves_where_king_is_in_danger(selected_piece_move_options, board, opponent, player_turn):
    allowed_moves = []
    for my_move in selected_piece_move_options:
        deep_copied_grid = board.return_deep_copied_grid()
        new_board = Board(deep_copied_grid)
        new_board.make_move(my_move)
        king_pos = new_board.get_king_pos(player_turn)
        if not my_king_is_in_danger(new_board.grid, opponent, king_pos):
            allowed_moves.append(my_move)
    return allowed_moves
