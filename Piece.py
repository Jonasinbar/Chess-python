from copy import deepcopy

import constants
from Move import Move
from Player import Player
import pygame
import abc

from helper import RangeOrder


def position_is_in_board(position):
    x, y = position
    size = constants.SIZE_BOARD
    return 0 <= x < size and 0 <= y < size


class BasePiece(abc.ABC):
    def __init__(self, owner: Player, x: int, y: int):
        self.owner = owner
        self.x = x
        self.y = y
        self.image = None

    @abc.abstractmethod
    def get_possible_next_moves(self, grid):
        pass

    def return_deep_copied_piece(self):
        piece_class = type(self)
        # Create a new instance of the same class
        copied_piece = piece_class(Player(self.owner.name, self.owner.color, self.owner.direction, None), deepcopy(self.x), deepcopy(self.y))
        return copied_piece

    def draw_piece(self, screen, piece_position):
        img_ratio = 0.6 if isinstance(self, Pawn) else 0.8
        if not self.image:
            img_path = constants.IMGS_DIR + '_'.join((self.owner.color, type(self).__name__)).lower() + '.png'
            imp = pygame.image.load(img_path).convert_alpha()
            piece_size = constants.SQUARE_SIZE * img_ratio
            piece_small = pygame.transform.scale(imp, (piece_size, piece_size))
            self.image = piece_small
        piece_abs_position = (
        piece_position[0] - constants.SQUARE_SIZE * img_ratio / 2, piece_position[1] - constants.SQUARE_SIZE * img_ratio / 2)
        screen.blit(self.image, piece_abs_position)

    def draw_piece_abs_position(self, screen, piece_abs_position):
        img_ratio = 0.6 if isinstance(self, Pawn) else 0.8
        if not self.image:
            img_path = constants.IMGS_DIR + '_'.join((self.owner.color, type(self).__name__)).lower() + '.png'
            imp = pygame.image.load(img_path).convert_alpha()
            piece_size = constants.SQUARE_SIZE * img_ratio
            piece_small = pygame.transform.scale(imp, (piece_size, piece_size))
            self.image = piece_small
        screen.blit(self.image, piece_abs_position)

    def get_only_possible_positions_for_line(self, positions, grid):
        possible_positions = []
        for pos in positions:
            current_square = grid[pos[0]][pos[1]]
            if current_square:
                if current_square.owner == self.owner:
                    return possible_positions
                else:
                    possible_positions.append(Move(self, pos, is_eat=True))
                    return possible_positions
            else:
                possible_positions.append(Move(self, pos, is_eat=False))
        return possible_positions


class Pawn(BasePiece):
    def get_possible_next_moves(self, grid):
        next_pos = []
        if self.owner.direction == constants.UP_DIRECTION:
            pos = (self.x, self.y - 1)
            pos_obj = grid[pos[0]][pos[1]]
            if not pos_obj:
                next_pos.append(Move(self, pos, is_eat=False))
                if self.is_in_start_pos():
                    pos = (self.x, self.y - 2)
                    pos_obj = grid[pos[0]][pos[1]]
                    if not pos_obj:
                        next_pos.append(Move(self, pos, is_eat=False))
        if self.owner.direction == constants.DOWN_DIRECTION:
            pos = (self.x, self.y + 1)
            pos_obj = grid[pos[0]][pos[1]]
            if not pos_obj:
                next_pos.append(Move(self, pos, is_eat=False))
                if self.is_in_start_pos():
                    pos = (self.x, self.y + 2)
                    pos_obj = grid[pos[0]][pos[1]]
                    if not pos_obj:
                        next_pos.append(Move(self, pos, is_eat=False))
        return next_pos + self.get_eat_pos_pawn(grid)

    def is_in_start_pos(self):
        if self.owner.direction == constants.DOWN_DIRECTION:
            return self.y == 1
        return self.y == constants.SIZE_BOARD - 2

    def get_eat_pos_pawn(self, grid):
        eat_pos = []
        if self.owner.direction == constants.DOWN_DIRECTION:
            down_left = (self.x - 1, self.y + 1)
            down_right = (self.x + 1, self.y + 1)
            if position_is_in_board(down_left):
                if grid[down_left[0]][down_left[1]]:
                    if grid[down_left[0]][down_left[1]].owner != self.owner:
                        eat_pos.append(Move(self, down_left, is_eat=True))
            if position_is_in_board(down_right):
                if grid[down_right[0]][down_right[1]]:
                    if grid[down_right[0]][down_right[1]].owner != self.owner:
                        eat_pos.append(Move(self, down_right, is_eat=True))
        else:
            up_left = (self.x - 1, self.y - 1)
            up_right = (self.x + 1, self.y - 1)
            if position_is_in_board(up_left):
                if grid[up_left[0]][up_left[1]]:
                    if grid[up_left[0]][up_left[1]].owner != self.owner:
                        eat_pos.append(Move(self, up_left, is_eat=True))
            if position_is_in_board(up_right):
                if grid[up_right[0]][up_right[1]]:
                    if grid[up_right[0]][up_right[1]].owner != self.owner:
                        eat_pos.append(Move(self, up_right, is_eat=True))
        return eat_pos


class Rook(BasePiece):
    def get_possible_next_moves(self, grid):
        up_moves = [(self.x, i) for i in RangeOrder(self.y - 1, 0 - 1) if i <= constants.SIZE_BOARD and i < self.y]
        down_moves = [(self.x, i) for i in RangeOrder(self.y + 1, constants.SIZE_BOARD) if i > 0 and i > self.y]
        left_moves = [(i, self.y) for i in RangeOrder(self.x - 1, 0 - 1) if i <= constants.SIZE_BOARD and i < self.x]
        right_moves = [(i, self.y) for i in RangeOrder(self.x + 1, constants.SIZE_BOARD) if i > 0 and i > self.x]
        return self.get_only_possible_positions_for_line(up_moves, grid) + self.get_only_possible_positions_for_line(
            down_moves, grid) + self.get_only_possible_positions_for_line(left_moves,
                                                                          grid) + self.get_only_possible_positions_for_line(
            right_moves, grid)


class Bishop(BasePiece):
    def get_possible_next_moves(self, grid):
        up_right = [(self.x + i, self.y - i) for i in range(1, min(constants.SIZE_BOARD - 1 - self.x, self.y) + 1)]
        up_left = [(self.x - i, self.y - i) for i in range(1, min(self.x, self.y) + 1)]
        down_right = [(self.x + i, self.y + i) for i in
                      range(1, min(constants.SIZE_BOARD - 1 - self.x, constants.SIZE_BOARD - 1 - self.y) + 1)]
        down_left = [(self.x - i, self.y + i) for i in range(1, min(self.x, constants.SIZE_BOARD - 1 - self.y) + 1)]
        return self.get_only_possible_positions_for_line(up_right, grid) + self.get_only_possible_positions_for_line(
            up_left, grid) + self.get_only_possible_positions_for_line(down_right,
                                                                       grid) + self.get_only_possible_positions_for_line(
            down_left, grid)


class Queen(BasePiece):
    def get_possible_next_moves(self, grid):
        up_right = self.get_only_possible_positions_for_line(
            [(self.x + i, self.y - i) for i in range(1, min(constants.SIZE_BOARD - 1 - self.x, self.y) + 1)], grid)
        up_left = self.get_only_possible_positions_for_line(
            [(self.x - i, self.y - i) for i in range(1, min(self.x, self.y) + 1)], grid)
        down_right = self.get_only_possible_positions_for_line([(self.x + i, self.y + i) for i in range(1,
                                                                                                        min(constants.SIZE_BOARD - 1 - self.x,
                                                                                                            constants.SIZE_BOARD - 1 - self.y) + 1)],
                                                               grid)
        down_left = self.get_only_possible_positions_for_line(
            [(self.x - i, self.y + i) for i in range(1, min(self.x, constants.SIZE_BOARD - 1 - self.y) + 1)], grid)
        up_moves = self.get_only_possible_positions_for_line(
            [(self.x, i) for i in RangeOrder(self.y - 1, 0 - 1) if i <= constants.SIZE_BOARD and i < self.y], grid)
        down_moves = self.get_only_possible_positions_for_line(
            [(self.x, i) for i in RangeOrder(self.y + 1, constants.SIZE_BOARD) if i > 0 and i > self.y], grid)
        left_moves = self.get_only_possible_positions_for_line(
            [(i, self.y) for i in RangeOrder(self.x - 1, 0 - 1) if i <= constants.SIZE_BOARD and i < self.x], grid)
        right_moves = self.get_only_possible_positions_for_line(
            [(i, self.y) for i in RangeOrder(self.x + 1, constants.SIZE_BOARD) if i > 0 and i > self.x], grid)
        return up_right + up_left + down_right + down_left + up_moves + down_moves + left_moves + right_moves


class King(BasePiece):
    def get_possible_next_moves(self, grid):
        up_left = [(self.x - 1, self.y - 1)]
        up_right = [(self.x + 1, self.y - 1)]
        down_left = [(self.x - 1, self.y + 1)]
        down_right = [(self.x + 1, self.y + 1)]
        up = [(self.x, self.y - 1)]
        down = [(self.x, self.y + 1)]
        right = [(self.x + 1, self.y)]
        left = [(self.x - 1, self.y)]
        next_pos = up_right + up_left + down_right + down_left + up + down + right + left
        next_pos_in_board = [pos for pos in next_pos if position_is_in_board(pos)]
        return [Move(self, empty_pos, is_eat=False) for empty_pos in next_pos_in_board if
                not getattr(grid[empty_pos[0]][empty_pos[1]], "owner", "") == self.owner] + [
            Move(self, empty_pos, is_eat=True) for empty_pos in next_pos_in_board if
            grid[empty_pos[0]][empty_pos[1]] and getattr(grid[empty_pos[0]][empty_pos[1]], "owner", "") != self.owner]


class Knight(BasePiece):

    def get_possible_next_moves(self, grid):
        up_left = [(self.x - 1, self.y - 2)]
        up_right = [(self.x + 1, self.y - 2)]
        down_left = [(self.x - 1, self.y + 2)]
        down_right = [(self.x + 1, self.y + 2)]
        left_up = [(self.x - 2, self.y - 1)]
        right_up = [(self.x + 2, self.y - 1)]
        left_down = [(self.x - 2, self.y + 1)]
        right_down = [(self.x + 2, self.y + 1)]
        next_pos = up_right + up_left + down_right + down_left + left_up + right_up + left_down + right_down
        next_pos_in_board = [pos for pos in next_pos if position_is_in_board(pos)]
        return [Move(self, empty_pos, is_eat=False) for empty_pos in next_pos_in_board if
                not getattr(grid[empty_pos[0]][empty_pos[1]], "owner", "") == self.owner] + [
            Move(self, empty_pos, is_eat=True) for empty_pos in next_pos_in_board if
            grid[empty_pos[0]][empty_pos[1]] and getattr(grid[empty_pos[0]][empty_pos[1]], "owner", "") != self.owner]
