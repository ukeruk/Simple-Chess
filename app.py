# A Pygame Battleship game

# Imports
import pygame
from enum import Enum

import constants


class ChessValues(Enum):
    BLACK = -1
    EMPTY = 0
    WHITE = 1
    HIGHLIGHT = 2
    HOVER = 3
    MOVE = 4
    CAPTURE = 5
    CHECK = 6


def assign_chess_board_values():
    board = []
    for i in range(8):
        board.append([])
        for j in range(8):
            board[i].append(ChessValues.BLACK if (i+j) % 2 else ChessValues.WHITE)
    return board


class ChessPiece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y


class Pawn(ChessPiece):
    def __init__(self, color, x, y):
        ChessPiece.__init__(self, color, x, y)

    def available_moves(self, board):
        moves = []

        move_up = self.color.value

        if board[self.y + move_up][self.x] == 0:
            moves.append((0, move_up))

        if (self.y == 1 and move_up == 1) or (self.y == 6 and move_up == -1):
            if board[self.y + 2 * move_up][self.x] == 0 and board[self.y + move_up][self.x] == 0:
                moves.append((0, 2 * move_up))

        if self.x > 0:
            if board[self.y + 1 * move_up][self.x - 1].color.value == -1 * self.color.value:
                moves.append((-1, 1 * move_up))

        if self.x < 7:
            if board[self.y + 1 * move_up][self.x + 1].color.value == -1 * self.color.value:
                moves.append((1, 1 * move_up))
        return moves


class King(ChessPiece):
    def __init__(self, color, x, y):
        ChessPiece.__init__(self, color, x, y)


class ChessGame:
    def __init__(self):
        self.board = []


def create_box(surface, x, y, width, height, color):
    box = pygame.Rect((x, y, width, height))

    pygame.draw.rect(surface, color, box)


def draw_chess_board(surface, chess_board):
    sur_width = surface.get_width()
    sur_height = surface.get_height()

    min_size = min(sur_height, sur_width)
    box_size = min_size / 12
    width_offset = sur_width / 2 - 4 * box_size
    height_offset = sur_height / 2 - 4 * box_size

    for y in range(8):
        for x in range(8):
            if ChessValues.WHITE == chess_board[y][x]:
                create_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                           width=box_size,
                           height=box_size, color=constants.COLOR_WHITE)
            elif ChessValues.BLACK == chess_board[y][x]:
                create_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                           width=box_size,
                           height=box_size, color=constants.COLOR_GREEN)
            elif ChessValues.MOVE == chess_board[y][x]:
                create_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                           width=box_size,
                           height=box_size, color=constants.COLOR_YELLOW)
    pygame.display.flip()


pygame.init()

screen = pygame.display.set_mode([1920, 1080], pygame.RESIZABLE)

screen.fill((75, 75, 75))
pygame.display.flip()

chess_board = assign_chess_board_values()

draw_chess_board(screen, chess_board)

running = True
while running:

    draw_chess_board(screen, chess_board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            screen.fill((75, 75, 75))
            draw_chess_board(screen, chess_board)

pygame.quit()
