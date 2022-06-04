COLOR_WHITE = (238, 238, 210)
COLOR_GREEN = (118, 150, 86)
COLOR_MOVE = (200, 100, 0)
COLOR_WHITE_MOVE = (239, 229, 105)
COLOR_GREEN_MOVE = (179, 185, 43)
COLOR_CAPTURE = (170, 50, 35)

BG_COLOR = (50, 50, 54)

# First letter is chess piece, second letter is color
# P = Pawn | R = Rook | N = Knight | B = Bishop | Q = Queen | K = King
# b = Black | w = White | NA = empty
CHESS_BOARD = [
    ['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],
    ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],
    ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'],
    ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'],
    ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'],
    ['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'],
    ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],
    ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw'],
]

CHESS_PIECE_RES_PATH = "resources/chess/pieces/"
