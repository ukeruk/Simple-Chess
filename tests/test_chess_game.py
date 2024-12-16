import pytest
from main.app import *

def test_check():
    test_chessgame = ChessGame([])
    board = []
    for j in range(8):
        board.append([])
        for k in range(8):
            board[j].append(EmptyPiece())
    board[0][1] = King(ChessValues.BLACK, 0, 1)
    board[2][0] = Queen(ChessValues.WHITE, 2, 0)

    test_chessgame.board = board
    test_chessgame.moving = (2, 0)

    test_chessgame.encaps((2, 1))

    assert test_chessgame.in_check is not None
    

