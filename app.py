# A Pygame Battleship game

# Imports
import pygame
from enum import Enum

import constants


class ChessValues(Enum):
    WHITE = 1
    BLACK = 2
    MOVE = 3
    CAPTURE = 4


def assign_chess_board_values():
    return [
        [[ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE],
         [ChessValues.BLACK],
         [ChessValues.WHITE], [ChessValues.BLACK]],
        [[ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK],
         [ChessValues.WHITE],
         [ChessValues.BLACK], [ChessValues.WHITE]],
        [[ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE],
         [ChessValues.BLACK],
         [ChessValues.WHITE], [ChessValues.BLACK]],
        [[ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK],
         [ChessValues.WHITE],
         [ChessValues.BLACK], [ChessValues.WHITE]],
        [[ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE],
         [ChessValues.BLACK],
         [ChessValues.WHITE], [ChessValues.BLACK]],
        [[ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK],
         [ChessValues.WHITE],
         [ChessValues.BLACK], [ChessValues.WHITE]],
        [[ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE],
         [ChessValues.BLACK],
         [ChessValues.WHITE], [ChessValues.BLACK]],
        [[ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK], [ChessValues.WHITE], [ChessValues.BLACK],
         [ChessValues.WHITE],
         [ChessValues.BLACK], [ChessValues.WHITE]],
    ]


class ChessPiece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y


class Pawn(ChessPiece):
    def __init__(self, color, x, y):
        ChessPiece.__init__(color, x, y)

    def available_moves(self, board):
        moves = []

        move_up = 1 if self.color == ChessValues.WHITE else 1

        if self.color == ChessValues.WHITE:
            if board[self.y + 1][self.x] == 0 or board[self.y + 1][self.x] == 0:
                moves.append((0, 1))
        else:
            if self.color == ChessValues.BLACK:
                if board[self.y - 1][self.x] == 0 or board[self.y - 1][self.x] == 0:
                    moves.append((0, -1))

        if self.y == 1:
            if board[self.y + 2 * move_up][self.x] == 0 or board[self.y + 2 * move_up][self.x] == 0:
                moves.append((0, 2 * move_up))
        if self.x > 0:
            if board[self.y + 1 * move_up][self.x - 1] != 0 and board[self.y + 1 * move_up][self.x - 1].color == ChessValues.BLACK:
                moves.append((-1, 1 * move_up))
        if self.x < 7:
            if board[self.y + 1 * move_up][self.x + 1] != 0 and board[self.y + 1 * move_up][self.x + 1].color == ChessValues.BLACK:
                moves.append((1, 1 * move_up))
        return moves


class King(ChessPiece):
    def __init__(self, color, x, y):
        ChessPiece.__init__(color, x, y)


class ChessGame:
    def __init__(self):
        self.board = []


def create_box(surface, x, y, width, height, color):
    box = pygame.Rect((x, y, width, height))

    pygame.draw.rect(surface, color, box)
    pygame.display.flip()


def draw_chess_board(surface, chess_board):
    sur_width = surface.get_width()
    sur_height = surface.get_height()

    box_size = sur_height / 10
    width_offset = (sur_width - sur_height) / 2 + box_size

    for y in range(8):
        for x in range(8):
            if ChessValues.WHITE in chess_board[y][x]:
                create_box(surface=surface, x=(width_offset + x * box_size), y=(box_size + box_size * y),
                           width=box_size,
                           height=box_size, color=constants.COLOR_WHITE)
            elif ChessValues.BLACK in chess_board[y][x]:
                create_box(surface=surface, x=(width_offset + x * box_size), y=(box_size + box_size * y),
                           width=box_size,
                           height=box_size, color=constants.COLOR_GREEN)
            elif ChessValues.MOVE in chess_board[y][x]:
                create_box(surface=surface, x=(width_offset + x * box_size), y=(box_size + box_size * y),
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
