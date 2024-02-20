import sys
import constants
from Board import Board, remove_moves_where_king_is_in_danger
from GameState import GameState
from Piece import King
from Player import Player
import pygame


PLAYER_1_COLOR: [0, 0, 255]
PLAYER_2_COLOR: [255, 0, 0]


def draw_dots(screen, grid, selected_piece, selected_piece_move_options):
    for y in range(constants.SIZE_BOARD):
        for x in range(constants.SIZE_BOARD):
            piece = grid[x][y]
            if piece:
                piece_position = Board.position_to_coordinates((x, y))
                piece.draw_piece(screen, piece_position)
    if selected_piece:
        selected_color = constants.PLAYER_1_COLOR_SELECTED if selected_piece.owner.color == constants.PLAYER_1_COLOR else constants.PLAYER_2_COLOR_SELECTED
        pygame.draw.rect(screen, selected_color, (
            constants.MARGIN + constants.SQUARE_SIZE * selected_piece.x,
            constants.MARGIN + constants.SQUARE_SIZE * selected_piece.y,
            constants.SQUARE_SIZE, constants.SQUARE_SIZE),3)
    if len(selected_piece_move_options) > 0:
        for move_option in selected_piece_move_options:
            dot_color = constants.RED if move_option.is_eat else constants.GREEN
            pygame.draw.circle(screen, dot_color, Board.position_to_coordinates(move_option.next_pos),
                                7)


def animate_piece_movement(piece, end_x, end_y, screen, grid):
    start_x, start_y = piece.x, piece.y
    # Define animation parameters
    animation_duration = 0.3  # in seconds
    frames_per_second = 100
    total_frames = int(animation_duration * frames_per_second)

    # Calculate distance to move per frame (in relative positions)

    # Translate relative positions to absolute positions
    start_abs_x, start_abs_y = Board.position_to_coordinates((start_x, start_y))
    end_abs_x, end_abs_y = Board.position_to_coordinates((end_x, end_y))

    delta_x = (end_abs_x - start_abs_x) / total_frames
    delta_y = (end_abs_y - start_abs_y) / total_frames
    # Perform animation
    for frame in range(total_frames):
        # Calculate current position
        current_abs_x = start_abs_x + delta_x * frame
        current_abs_y = start_abs_y + delta_y * frame
        Game.draw_board(screen)
        draw_dots(screen, grid, None, [])
        piece.draw_piece(screen, (current_abs_x, current_abs_y))

        # Redraw only the moving piece dot

        # Delay to control FPS
        pygame.display.flip()

        pygame.time.Clock().tick(frames_per_second)

    # Ensure the piece is at the correct final position
    # selected_piece.x = end_x
    # selected_piece.y = end_y
    # pass


class Game:
    def __init__(self, player1_name, player2_name):
        self.player1 = Player(player1_name, constants.PLAYER_1_COLOR, constants.PLAYER_1_DIRECTION, [])
        self.player2 = Player(player2_name, constants.PLAYER_2_COLOR, constants.PLAYER_2_DIRECTION, [])
        self.board = Board()
        self.board.put_pieces_start_config(self.player1, self.player2)
        self.game_state = GameState(self.player1, None, [], False)
        self.game_runs = True
        pygame.init()
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption("Chekcers")
        chess_icon = pygame.image.load('assets/images/black_pawn.png')
        pygame.display.set_icon(chess_icon)
        self.clock = pygame.time.Clock()

    def run_game(self):
        while self.game_runs:
            self.screen.fill(constants.WHITE)
            self.draw_board(self.screen)
            draw_dots(self.screen, self.board.grid, self.game_state.selected_piece, self.game_state.selected_piece_move_options)
            self.draw_score(self.screen, self.player1, self.player2, self.game_state.player_turn, self.game_state.winner, self.game_state.echec_et_mat)
            self.handle_events()
            pygame.display.flip()
            # Control the frames per second (FPS)
            self.clock.tick(100)

    @staticmethod
    def draw_board(screen):
        margin = constants.MARGIN
        board_height = min([constants.WIDTH, constants.HEIGHT]) - 2 * margin

        for j in range(constants.SIZE_BOARD):
            for i in range(constants.SIZE_BOARD):
                if (j + i) % 2 != 0 and i < constants.SIZE_BOARD:
                    square_color = constants.BROWN
                else:
                    square_color = constants.WHITE
                pygame.draw.rect(screen, square_color, (
                    margin + constants.SQUARE_SIZE * i, margin + constants.SQUARE_SIZE * j,
                    constants.SQUARE_SIZE, constants.SQUARE_SIZE))

        for i in range(constants.SIZE_BOARD + 1):
            start_pos_vertical = (margin + (board_height / constants.SIZE_BOARD) * i, margin)
            end_pos_vertical = (margin + board_height / constants.SIZE_BOARD * i, board_height + margin)
            pygame.draw.line(screen, constants.BOARD_COLOR, start_pos_vertical, end_pos_vertical,
                             constants.BOARD_LINE_WIDTH)
            start_pos_horizontal = (margin, margin + (board_height / constants.SIZE_BOARD) * i)
            end_pos_horizontal = (board_height + margin, board_height / constants.SIZE_BOARD * i + margin)
            pygame.draw.line(screen, constants.BOARD_COLOR, start_pos_horizontal, end_pos_horizontal,
                             constants.BOARD_LINE_WIDTH)

    @staticmethod
    def draw_score(screen, player1, player2, player_turn, winner, echec_et_mac):
        board_height = min([constants.WIDTH, constants.HEIGHT]) - 2 * constants.MARGIN
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)

        player1_text_surface = my_font.render(player1.name, False, player1.color)
        player2_text_surface = my_font.render(player2.name, False, constants.GREY)

        player1_score_x = constants.SQUARE_SIZE * constants.SIZE_BOARD + constants.MARGIN * 2
        player2_score_x = player1_score_x + len(player1.name) * 30 + constants.MARGIN * 2

        player1_score_text_surface = my_font.render(str(len(player1.captured_pieces)), False, (0, 0, 0))
        player2_score_text_surface = my_font.render(str(len(player2.captured_pieces)), False, (0, 0, 0))

        current_player_x = player1_score_x if player_turn == player1 else player2_score_x

        winner_text_surface = None
        if winner:
            if echec_et_mac:
                winner_text_surface = my_font.render(winner.name + " is the Winner !! Echet et mat", False, (0, 0, 0))
            else:
                winner_text_surface = my_font.render(winner.name + " is the Winner !!", False, (0, 0, 0))

        # Draw player names and scores
        screen.blit(player1_text_surface, (player1_score_x, len(player1.captured_pieces)))
        screen.blit(player2_text_surface, (player2_score_x, len(player2.captured_pieces)))
        x_line = board_height + constants.MARGIN + 0.5*(constants.WIDTH - (board_height + constants.MARGIN))
        pygame.draw.line(screen, constants.BOARD_COLOR,
                         (x_line, constants.MARGIN), (x_line, 600), constants.BOARD_LINE_WIDTH)
        screen.blit(player1_score_text_surface, (player1_score_x, 60))
        screen.blit(player2_score_text_surface, (player2_score_x, 60))
        start_x = x_line + 4
        start_y = 40
        counter = 0
        for piece in game.player2.captured_pieces:
            if counter % 3 == 0:
                start_y = start_y + 80
                start_x = x_line + 4
            piece.draw_piece_abs_position(screen, (start_x, start_y))
            start_x = start_x + 50
            counter+=1

        start_x = board_height + constants.MARGIN + 50
        start_y = 40
        counter = 0
        for piece in game.player1.captured_pieces:
            if counter % 3 == 0:
                start_y = start_y + 80
                start_x = board_height + constants.MARGIN + 50
            piece.draw_piece_abs_position(screen, (start_x, start_y))
            start_x = start_x + 50
            counter+=1

        # Highlight current player
        pygame.draw.rect(screen, constants.BLACK, (current_player_x - 5, 0, 120, 60), 2)

        # Draw winner message
        if winner_text_surface:
            screen.blit(winner_text_surface, (player1_score_x + constants.SQUARE_SIZE * 2, 180))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if self.board.click_in_board((x, y)):
                    if not self.game_state.winner:
                        selected_x, selected_y = self.board.detect_square_position_from_click(x, y)
                        self.handle_click_on_square(selected_x, selected_y)
                        self.detect_if_winner()

    def detect_if_winner(self):
        player1_has_king = sum(1 for row in self.board.grid for piece in row if isinstance(piece, King) and getattr(getattr(piece, "owner", None), "color", None) == self.player1.color)
        player2_has_king = sum(1 for row in self.board.grid for piece in row if isinstance(piece, King) and getattr(getattr(piece, "owner", None), "color", None) == self.player2.color)
        if not player1_has_king or not player2_has_king:
            self.game_state.winner = self.player1 if not player2_has_king else self.player2
        opponent = self.player1 if self.game_state.player_turn == self.player2 else self.player2
        if self.detect_if_echec_et_mat(opponent):
            self.game_state.echec_et_mat = True
            self.game_state.winner = opponent

    def handle_click_on_square(self, selected_x, selected_y):
        piece_clicked = self.board.get_piece((selected_x, selected_y))
        if piece_clicked:
            if (selected_x, selected_y) in self.game_state.selected_piece_move_options:
                selected_move = None
                for z in self.game_state.selected_piece_move_options:
                    if z == (selected_x, selected_y):
                        selected_move = z
                if selected_move.is_eat:
                    selected_x = self.game_state.selected_piece.x
                    selected_y = self.game_state.selected_piece.y

                    self.game_state.player_turn.captured_pieces.append(self.board.grid[selected_move.next_pos[0]][selected_move.next_pos[1]])
                    self.board.grid[selected_x][selected_y] = None
                    animate_piece_movement(self.game_state.selected_piece, selected_move.next_pos[0], selected_move.next_pos[1], self.screen, self.board.grid)
                    self.board.grid[selected_move.next_pos[0]][selected_move.next_pos[1]] = self.game_state.selected_piece
                    self.board.grid[selected_move.next_pos[0]][selected_move.next_pos[1]].x = selected_move.next_pos[0]
                    self.board.grid[selected_move.next_pos[0]][selected_move.next_pos[1]].y = selected_move.next_pos[1]
                    self.game_state.selected_piece = None
                    self.game_state.selected_piece_move_options = []
                    self.change_player_turn()

            elif self.game_state.player_turn != piece_clicked.owner:
                #not your turn
                self.game_state.selected_piece = None
                self.game_state.selected_piece_move_options = []
                return
            else:
                self.game_state.selected_piece = piece_clicked
                self.game_state.selected_piece_move_options = self.game_state.selected_piece.get_possible_next_moves(self.board.grid)
                opponent = self.player1 if self.game_state.player_turn == self.player2 else self.player2
                self.game_state.selected_piece_move_options = remove_moves_where_king_is_in_danger(self.game_state.selected_piece_move_options, self.board, opponent, self.game_state.player_turn)
        elif (selected_x, selected_y) in self.game_state.selected_piece_move_options:
            self.board.grid[self.game_state.selected_piece.x][self.game_state.selected_piece.y] = None
            animate_piece_movement(self.game_state.selected_piece, selected_x, selected_y, self.screen, self.board.grid)
            self.game_state.selected_piece.x = selected_x
            self.game_state.selected_piece.y = selected_y
            self.board.grid[selected_x][selected_y] = self.game_state.selected_piece
            self.game_state.selected_piece = None
            self.game_state.selected_piece_move_options = []
            self.change_player_turn()
        else:
            self.game_state.selected_piece = None
            self.game_state.selected_piece_move_options = []

    def change_player_turn(self):
        self.game_state.player_turn = self.player2 if self.game_state.player_turn == self.player1 else self.player1

    def detect_if_echec_et_mat(self, opponent):
        for y in range(constants.SIZE_BOARD):
            for x in range(constants.SIZE_BOARD):
                piece = self.board.grid[x][y]
                if piece:
                    if piece.owner == self.game_state.player_turn:
                        piece_next_moves = piece.get_possible_next_moves(self.board.grid)
                        piece_legal_moves = remove_moves_where_king_is_in_danger(piece_next_moves, self.board, opponent, self.game_state.player_turn)
                        if piece_legal_moves:
                            return False
        return True


if __name__ == "__main__":
    game = Game("Player1", "Player2")
    game.run_game()
