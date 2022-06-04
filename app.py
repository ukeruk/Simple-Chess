# A Pygame Battleship game

# Imports
import time

import pygame
from enum import Enum
import constants


class ChessValues(Enum):
    WHITE = -1
    EMPTY = 0
    BLACK = 1
    HIGHLIGHT = 2
    HOVER = 3
    MOVING = 4
    MOVE_WHITE = 5
    MOVE_BLACK = 6
    CAPTURE = 7
    CHECK = 8


def assign_chess_board_values():
    board = []
    for i in range(8):
        board.append([])
        for j in range(8):
            board[i].append(ChessValues.BLACK if (i + j) % 2 else ChessValues.WHITE)
    return board


#   ------------------------------------------------------------------
#   ---------------------------Chess Pieces---------------------------
#   ------------------------------------------------------------------


class ChessPiece:
    def __init__(self, color, x, y):
        self.piece = self.__class__.__name__
        self.color = color
        self.x = x
        self.y = y

    def move(self, x, y):
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
        if isinstance(board[self.y + move_up][self.x], EmptyPiece):
            moves.append((0, move_up))

        if (self.y == 1 and move_up == 1) or (self.y == 6 and move_up == -1):
            if isinstance(board[self.y + 2 * move_up][self.x], EmptyPiece) and isinstance(board[self.y + move_up][self.x], EmptyPiece):
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
        return moves


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
                        if board[self.y + i * j[0]][self.x + i * j[1]].color != ChessValues.EMPTY:
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
                        if board[self.y + i * j[0]][self.x + i * j[1]].color != ChessValues.EMPTY:
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
        return moves


#   ------------------------------------------------------------------
#   ----------------------------Game Logic----------------------------
#   ------------------------------------------------------------------


class ChessGame:
    def __init__(self, checkered_board):
        self.board = []
        self.checkered_board = checkered_board
        self.create_board()
        self.turn = ChessValues.WHITE
        self.moving = None

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
                    case 'N':
                        self.board[i].append(Knight(color, j, i))
                    case 'B':
                        self.board[i].append(Bishop(color, j, i))
                    case 'Q':
                        self.board[i].append(Queen(color, j, i))
                    case 'K':
                        self.board[i].append(King(color, j, i))
                    case 'P':
                        self.board[i].append(Pawn(color, j, i))

    # manages piece movement
    def move(self, point):
        if point is not None:
            x = point[0]
            y = point[1]
            if self.moving is None:
                if self.board[y][x].color == self.turn:
                    moves = self.board[y][x].available_moves(self.board)
                    if len(moves) > 0:
                        self.checkered_board[y][x] = ChessValues.MOVING
                        self.moving = (x, y)
                        for move in moves:
                            if self.board[y + move[1]][x + move[0]].color.value == -1 * self.turn.value:
                                self.checkered_board[y + move[1]][x + move[0]] = ChessValues.CAPTURE
                            else:
                                if self.checkered_board[y + move[1]][x + move[0]] == ChessValues.WHITE:
                                    self.checkered_board[y + move[1]][x + move[0]] = ChessValues.MOVE_WHITE
                                else:
                                    self.checkered_board[y + move[1]][x + move[0]] = ChessValues.MOVE_BLACK
            else:
                if self.board[y][x].color == self.turn:
                    self.checkered_board = assign_chess_board_values()
                    self.moving = None
                    self.move(point)
                elif ChessValues.MOVE_WHITE.value <= self.checkered_board[y][x].value <= ChessValues.CAPTURE.value:
                    self.board[y][x] = self.board[self.moving[1]][self.moving[0]]
                    self.board[y][x].move(x, y)
                    self.board[self.moving[1]][self.moving[0]] = EmptyPiece()
                    self.moving = None
                    self.checkered_board = assign_chess_board_values()
                    self.turn = ChessValues(self.turn.value * -1)


#   ------------------------------------------------------------------
#   --------------------------GUI Functions---------------------------
#   ------------------------------------------------------------------


# used to draw the individual checkered boxes
def draw_box(surface, x, y, width, height, color):
    box = pygame.Rect((x, y, width, height))
    pygame.draw.rect(surface, color, box)


# draws the entire checkered board
def draw_chess_board(surface, board):
    sur_width = surface.get_width()
    sur_height = surface.get_height()

    min_size = min(sur_height, sur_width)
    box_size = min_size / 12
    width_offset = sur_width / 2 - 4 * box_size
    height_offset = sur_height / 2 - 4 * box_size

    for y in range(8):
        for x in range(8):
            match board[y][x]:
                case ChessValues.WHITE:
                    draw_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                             width=box_size,
                             height=box_size, color=constants.COLOR_WHITE)
                case ChessValues.BLACK:
                    draw_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                             width=box_size,
                             height=box_size, color=constants.COLOR_GREEN)
                case ChessValues.MOVE_WHITE:
                    draw_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                             width=box_size,
                             height=box_size, color=constants.COLOR_WHITE_MOVE)
                case ChessValues.MOVE_BLACK:
                    draw_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                             width=box_size,
                             height=box_size, color=constants.COLOR_GREEN_MOVE)
                case ChessValues.MOVING:
                    draw_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                             width=box_size,
                             height=box_size, color=constants.COLOR_MOVE)
                case ChessValues.CAPTURE:
                    draw_box(surface=surface, x=(width_offset + x * box_size), y=(height_offset + box_size * y),
                             width=box_size,
                             height=box_size, color=constants.COLOR_CAPTURE)


def draw_image(surface, x, y, img):
    surface.blit(img, (x, y))


# returns a loaded image from directory
def load_image(size, img_name):
    img = pygame.image.load(f"{constants.CHESS_PIECE_RES_PATH}{img_name}.png")

    # transforms the image size to fit the board checkers
    img = pygame.transform.scale(img, (size, size))
    return img


# loads all images to memory for future use
def load_images(surface, images):
    sur_width = surface.get_width()
    sur_height = surface.get_height()

    min_size = min(sur_height, sur_width)
    box_size = min_size / 12

    for color in ['Black', 'White']:
        for piece in ['Pawn', 'Rook', 'Knight', 'Bishop', 'King', 'Queen']:
            images[f'{piece}{color}'] = load_image(size=(0.9 * box_size), img_name=f'{piece}{color}')


# draws the chess piece images to the board in accordance to game state
def draw_chess_pieces(surface, board, images):
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
                draw_image(surface, x=(width_offset + x * box_size + box_size * 0.05),
                           y=(height_offset + y * box_size + box_size * 0.05),
                           img=images[f'{board[y][x].piece}{color}'])
    pygame.display.flip()


# checks if the area clicked on is on the board:
#   if so it returns the corresponding x and y in the game array
#   otherwise it returns none
def click_on_chess_board(surface, x, y):
    sur_width = surface.get_width()
    sur_height = surface.get_height()

    min_size = min(sur_height, sur_width)
    box_size = min_size / 12
    width_offset = sur_width / 2 - 4 * box_size
    height_offset = sur_height / 2 - 4 * box_size

    if width_offset < x < width_offset + box_size * 8 and height_offset < y < height_offset + box_size * 8:
        c_x = c_y = 0
        while x - (width_offset + c_x * box_size) > box_size:
            c_x += 1
        while y - (height_offset + c_y * box_size) > box_size:
            c_y += 1
        return c_x, c_y
    return None


#   ------------------------------------------------------------------
#   -------------------Main variables and game loop-------------------
#   ------------------------------------------------------------------


pygame.init()

screen = pygame.display.set_mode([1920, 1080], pygame.RESIZABLE)

screen.fill(constants.BG_COLOR)

chess_piece_images = {}
load_images(screen, chess_piece_images)

game = ChessGame(assign_chess_board_values())

draw_chess_board(screen, game.checkered_board)
draw_chess_pieces(screen, game.board, chess_piece_images)
pygame.display.flip()

running = True
while running:

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False

            case pygame.VIDEORESIZE:
                screen.fill(constants.BG_COLOR)
                load_images(screen, chess_piece_images)
                draw_chess_board(screen, game.checkered_board)
                draw_chess_pieces(screen, game.board, chess_piece_images)
                pygame.display.flip()

            case pygame.MOUSEBUTTONDOWN:
                game.move(click_on_chess_board(screen, event.pos[0], event.pos[1]))
                draw_chess_board(screen, game.checkered_board)
                draw_chess_pieces(screen, game.board, chess_piece_images)
                pygame.display.flip()
    time.sleep(0.1)

pygame.quit()
