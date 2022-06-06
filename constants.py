SCREEN_BOX_RATIO = 12

COLOR_WHITE = (238, 238, 210)
COLOR_GREEN = (118, 150, 86)
COLOR_MOVE = (200, 100, 0)
COLOR_NO_MOVES = (235, 222, 61)
COLOR_WHITE_MOVE = (239, 229, 105)
COLOR_GREEN_MOVE = (179, 185, 43)
COLOR_CAPTURE = (170, 50, 35)
COLOR_PROMOTION = (222, 222, 169)

BG_COLOR = (48, 46, 43)

IMAGE_BOX_OFFSET = 0.1

# First letter is chess piece, second letter is color
# P = Pawn | R = Rook | N = Knight | B = Bishop | Q = Queen | K = King
# b = Black | w = White | NA = empty

CHESS_BOARD = [
    ['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],
    ['Pb', 'Pw', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],
    ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'],
    ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'],
    ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'],
    ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'],
    ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pb', 'Pw'],
    ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw'],
]

FONT_RES_PATH = "resources/fonts/"
CHESS_PIECE_RES_PATH = "resources/chess/pieces/"
