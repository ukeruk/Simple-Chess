# A Pygame Battleship game

# Imports
import pygame
from enum import Enum

import app
import constants


class ChessValues(Enum):
    WHITE = -1
    EMPTY = 0
    BLACK = 1
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
            board[i].append(ChessValues.BLACK if (i + j) % 2 else ChessValues.WHITE)
    return board


class ChessPiece:
    def __init__(self, color, x, y):
        self.piece = self.__class__.__name__
        self.color = color
        self.x = x
        self.y = y


class EmptyPiece:
    def __init__(self):
        self.color = ChessValues.EMPTY


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
        self.moved = False

    def available_moves(self, board):
        moves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if not i == j == 0:
                    if 7 >= self.x + i >= 0 and 7 >= self.y + j >= 0:
                        if board[self.y + j][self.x + i].color.value != self.color.value:
                            moves.append((i, j))

        if not self.moved:
            if isinstance(board[self.y][0], Rook) and board[self.y][0].color == self.color \
                    and board[self.y][0].moved is False:
                if board[self.y][1] == 0 and board[self.y][2] == 0 and board[self.y][3] == 0:
                    moves.append((-2, 0))

            if isinstance(board[self.y][7], Rook) and board[self.y][7].color == self.color \
                    and board[self.y][7].moved is False:
                if board[self.y][5] == 0 and board[self.y][6] == 0:
                    moves.append((2, 0))


class Rook(ChessPiece):
    def __init__(self, color, x, y):
        ChessPiece.__init__(self, color, x, y)
        self.moved = False

    def available_moves(self, board):
        moves = []

        for j in ([0, 1], [1, 0], [-1, 0], [0, -1]):
            move = True
            for i in range(1, 8):
                if move:
                    if 7 >= self.y + i * j[0] >= 0 and 7 >= self.x + i * j[1] >= 0:
                        if board[self.y + i * j[0]][self.x + i * j[1]].color is not self.color:
                            moves.append((i * j[1], i * j[0]))
                        if board[self.y + i * j[0]][self.x + i * j[1]].color.value != ChessValues.EMPTY:
                            move = False
                    else:
                        move = False
        return moves


class Bishop(ChessPiece):
    def __init__(self, color, x, y):
        ChessPiece.__init__(self, color, x, y)

    def available_moves(self, board):
        moves = []

        for j in ([1, 1], [-1, 1], [-1, -1], [1, -1]):
            move = True
            for i in range(1, 8):
                if move:
                    if 7 >= self.y + i * j[0] >= 0 and 7 >= self.x + i * j[1] >= 0:
                        if board[self.y + i * j[0]][self.x + i * j[1]].color is not self.color:
                            moves.append((i * j[1], i * j[0]))
                        if board[self.y + i * j[0]][self.x + i * j[1]].color.value != ChessValues.EMPTY:
                            move = False
                    else:
                        move = False
        return moves


class Knight(ChessPiece):
    def __init__(self, color, x, y):
        ChessPiece.__init__(self, color, x, y)

    def available_moves(self, board):
        moves = []

        for j in ([2, 1], [-2, 1], [-2, -1], [2, -1], [1, 2], [-1, 2], [-1, -2], [1, -2]):
            if 7 >= self.y + j[0] >= 0 and 7 >= self.x + j[1] >= 0:
                if board[self.y + j[0]][self.x + j[1]].color is not self.color:
                    moves.append((j[1], j[0]))
        return moves


class Queen(ChessPiece):
    def __init__(self, color, x, y):
        ChessPiece.__init__(self, color, x, y)

    def available_moves(self, board):
        moves = []

        for j in ([1, 1], [-1, 1], [-1, -1], [1, -1], [0, 1], [1, 0], [-1, 0], [0, -1]):
            move = True
            for i in range(1, 8):
                if move:
                    if 7 >= self.y + i * j[0] >= 0 and 7 >= self.x + i * j[1] >= 0:
                        if board[self.y + i * j[0]][self.x + i * j[1]].color is not self.color:
                            moves.append((i * j[1], i * j[0]))
                        if board[self.y + i * j[0]][self.x + i * j[1]].color.value != ChessValues.EMPTY:
                            move = False
                    else:
                        move = False


class ChessGame:
    def __init__(self):
        self.board = []
        self.create_board()

    def create_board(self):
        brd = constants.CHESS_BOARD
        empty = EmptyPiece()
        for i in range(len(brd)):
            self.board.append([])
            for j in range(len(brd[i])):
                if 'w' in brd[i][j]:
                    color = ChessValues.WHITE
                elif 'b' in brd[i][j]:
                    color = ChessValues.BLACK
                else:
                    self.board[i].append(empty)
                    continue
                match brd[i][j][0]:
                    case 'R':
                        self.board[i].append(Rook(color, j, i))
                        break
                    case 'N':
                        self.board[i].append(Knight(color, j, i))
                        break
                    case 'B':
                        self.board[i].append(Bishop(color, j, i))
                        break
                    case 'Q':
                        self.board[i].append(Queen(color, j, i))
                        break
                    case 'K':
                        self.board[i].append(King(color, j, i))
                        break
                    case 'P':
                        self.board[i].append(Pawn(color, j, i))
                        break


def draw_box(surface, x, y, width, height, color):
    box = pygame.Rect((x, y, width, height))

    pygame.draw.rect(surface, color, box)


def draw_chess_board(surface, board):
    sur_width = surface.get_width()
    sur_height = surface.get_height()

    min_size = min(sur_height, sur_width)
    box_size = min_size / 12
    width_offset = sur_width / 2 - 4 * box_size
    height_offset = sur_height / 2 - 4 * box_size

    for y in range(8):
        for x in range(8):
            if ChessValues.WHITE == board[y][x]:
                draw_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                         width=box_size,
                         height=box_size, color=constants.COLOR_WHITE)
            elif ChessValues.BLACK == board[y][x]:
                draw_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                         width=box_size,
                         height=box_size, color=constants.COLOR_GREEN)
            elif ChessValues.MOVE == board[y][x]:
                draw_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                         width=box_size,
                         height=box_size, color=constants.COLOR_YELLOW)
    pygame.display.flip()


def draw_image(surface, x, y, size, img_name):
    img = pygame.image.load(f"{constants.CHESS_PIECE_RES_PATH}{img_name}")
    img = pygame.transform.scale(img, (size, size))
    surface.blit(img, (x, y))
    pygame.display.flip()


def draw_chess_pieces(surface, board):
    sur_width = surface.get_width()
    sur_height = surface.get_height()

    min_size = min(sur_height, sur_width)
    box_size = min_size / 12
    width_offset = sur_width / 2 - 4 * box_size
    height_offset = sur_height / 2 - 4 * box_size

    for y in range(len(board)):
        for x in range(len(board[y])):
            if not isinstance(board[y][x], EmptyPiece):
                if board[y][x].color == ChessValues.WHITE:
                    color = 'White'
                else:
                    color = 'Black'
                draw_image(surface, x=(width_offset + x * box_size), y=(height_offset + y * box_size), size=box_size,
                           img_name=f'{board[y][x].piece}{color}.png')


pygame.init()

screen = pygame.display.set_mode([1920, 1080], pygame.RESIZABLE)

screen.fill(constants.BG_COLOR)
pygame.display.flip()

chess_board = assign_chess_board_values()

draw_chess_board(screen, chess_board)

game = ChessGame()

draw_chess_pieces(screen, game.board)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            screen.fill(constants.BG_COLOR)
            draw_chess_board(screen, chess_board)

pygame.quit()
