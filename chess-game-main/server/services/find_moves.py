from models.piece import *
from models.board import *
import json

def find_moves(board, selected_player):
    c = Board(board, selected_player)
    # print (c.board)
    # for i in c.board:
    #     for j in c.board[i]:
    #         # print (type(c.board[i][j]))
    #         # c.board[i][j].find_possible_moves()
    #         # print (c.board[i][j].out())
    return {
        'board': c.display_board(), 
        'selectedPlayer': reverse_selected_player(selected_player),
        'isBlackCheck': c.is_black_check,
        'isWhiteCheck': c.is_white_check,
    }
    # return board

def reverse_selected_player(selected_player):
    print (selected_player)
    if selected_player == 'WHITE':
        return 'BLACK'
    else:
        return 'WHITE'