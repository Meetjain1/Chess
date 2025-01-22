from services.constants import row_index, col_index, empty_board
from models.piece import *
import copy

class Board:
    def __init__(self, board, selected_player, original=True):
        self.board = empty_board()


        self.is_black_check = False
        self.is_white_check = False

        self.white_king = (None, None)
        self.black_king = (None, None)

        # attack positions of white pieces (attacking black team)
        self.white_attack_positions = set()
        # attack positions of black pieces (attacking white team)
        self.black_attack_positions = set()

        self.selected_player = selected_player

        self.map_pieces(board)
        self.get_exact_moves(self.board)

        self.is_check()

        # this prevents infinite recursion
        if original:
            self.remove_check_moves(self.selected_player)

    def map_pieces(self, board):
        '''
        will put the pieces in the correct place on the board and find all possible moves
        for each piece
        '''
        for row in row_index:
            for col in col_index:
                if board[row][col]:
                    if isinstance(board[row][col], Piece):
                        self.board[row][col] = board[row][col]
                        if isinstance(board[row][col], King):
                            if board[row][col].is_white:
                                self.white_king = (row, col)
                            else:
                                self.black_king = (row, col)
                        continue
                    piece_type = board[row][col]['type'].split('-')[0]
                    is_dead = board[row][col]['isDead']
                    is_white = board[row][col]['isWhite']
                    unmoved = board[row][col]['unmoved'] if ('unmoved' in board[row][col]) else False
                    position = [row, col]
                    if piece_type == 'pawn':
                        self.board[row][col] = Pawn(is_dead=is_dead, is_white=is_white, position=position, unmoved=unmoved)
                    elif piece_type == 'rook':
                        self.board[row][col] = Rook(is_dead=is_dead, is_white=is_white, position=position, unmoved=unmoved)
                    elif piece_type == 'knight':
                        self.board[row][col] = Knight(is_dead=is_dead, is_white=is_white, position=position, unmoved=unmoved)
                    elif piece_type == 'bishop':
                        self.board[row][col] = Bishop(is_dead=is_dead, is_white=is_white, position=position, unmoved=unmoved)
                    elif piece_type == 'queen':
                        self.board[row][col] = Queen(is_dead=is_dead, is_white=is_white, position=position, unmoved=unmoved)
                    elif piece_type == 'king':
                        self.board[row][col] = King(is_dead=is_dead, is_white=is_white, position=position, unmoved=unmoved)
                        if is_white:
                            self.white_king = (row, col)
                        else:
                            self.black_king = (row, col)

    def get_exact_moves(self, board):
        '''
        finds exact moves for pieces (takes into account the selected player) and appends them to 
        moves in pieces
        * this will need to be refactored to deal with check
        * remember to add en passant
        * remember to add castle - done
        '''
        for row in row_index:
            for col in col_index:
                # only adds moves to the current player
                if board[row][col]:# and self.xnor(a = (self.selected_player == 'BLACK'), b = self.board[row][col].is_white):

                    piece = board[row][col]
                    row_i, col_i = row_index.index(row), col_index.index(col)
                    board_range = range(0,8) 

                    # This doesn't yet include en passant
                    if piece.type == 'pawn':
                        self.find_pawn_moves(row, col, piece, row_i, col_i, board_range)

                    elif piece.type == 'rook':
                        self.find_rook_moves(row, col, piece, row_i, col_i, board_range)

                    elif piece.type == 'knight':
                        self.find_knight_moves(row, col, piece, row_i, col_i, board_range)
                        
                    elif piece.type == 'bishop':
                        self.find_bishop_moves(row, col, piece, row_i, col_i, board_range)

                    elif piece.type == 'queen':
                        self.find_queen_moves(row, col, piece, row_i, col_i, board_range)

                    # This doesn't yet include castle
                    elif piece.type == 'king':
                        self.find_king_moves(row, col, piece, row_i, col_i, board_range)

    def find_pawn_moves(self, row, col, piece, row_i, col_i, board_range):
        attack_positions = []
        all_possible_moves = piece.find_possible_moves()

        # will identify positions on the board that the pawn can attack (if on board)
        if not piece.is_white:
            if (row_i+1 in board_range) and (col_i+1 in board_range):
                attack_positions.append([row_index[row_i+1], col_index[col_i+1]])
            if (row_i+1 in board_range) and (col_i-1 in board_range):
                attack_positions.append([row_index[row_i+1], col_index[col_i-1]])

            # en passant moves
            # if (row_i == 4) and (col_i+1 in board_range):
            #     attack_positions.append([row_index[row_i+1], col_index[col_i+1]])
            # if (row_i == 4) and (col_i-1 in board_range):
            #     attack_positions.append([row_index[row_i+1], col_index[col_i-1]])

            

        else:
            if (row_i-1 in board_range) and (col_i+1 in board_range):
                attack_positions.append([row_index[row_i-1], col_index[col_i+1]])
            if (row_i-1 in board_range) and (col_i-1 in board_range):
                attack_positions.append([row_index[row_i-1], col_index[col_i-1]])

            # en passant moves
            # if (row_i == 3) and (col_i+1 in board_range):
            #     attack_positions.append([row_index[row_i-1], col_index[col_i+1]])
            # if (row_i == 3) and (col_i-1 in board_range):
            #     attack_positions.append([row_index[row_i-1], col_index[col_i-1]])
            
        # adds possible attacking moves
        for position in attack_positions:
            attack_piece = self.board[position[0]][position[1]]
            self.add_attack_position(piece, position)
            if attack_piece and (attack_piece.is_white is not piece.is_white):
                self.add_move_if_valid(piece = piece, position = position, is_kill = True)
        # adds the possible moves if there is no piece in the way
        for position in all_possible_moves:
            blocking_piece = self.board[position[0]][position[1]]
            if len(position) > 2:
                blocking_piece_2 = self.board[position[2]][position[1]]
            else:
                blocking_piece_2 = None
            if not blocking_piece and not blocking_piece_2:
                self.add_move_if_valid(piece = piece, position = position, is_kill = False)
        
        # print (piece.moves)

    def find_rook_moves(self, row, col, piece, row_i, col_i, board_range):
        # this doesn't use the find all moves function
        # checks all 4 directions with a separate loop
        for i in board_range:
            if (row_i+i in board_range):
                position = [row_index[row_i+i], col]
                if position != piece.position:
                    attack_piece = self.board[row_index[row_i+i]][col]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:    
            if (row_i-i in board_range):
                position = [row_index[row_i-i], col]
                if position != piece.position:
                    attack_piece = self.board[row_index[row_i-i]][col]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:
            if (col_i+i in board_range):
                position = [row, col_index[col_i+i]]
                if position != piece.position:
                    attack_piece = self.board[row][col_index[col_i+i]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:
            if (col_i-i in board_range):
                position = [row, col_index[col_i-i]]
                if position != piece.position:
                    attack_piece = self.board[row][col_index[col_i-i]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)

    def find_knight_moves(self, row, col, piece, row_i, col_i, board_range):
        all_possible_moves = piece.find_possible_moves()

        for position in all_possible_moves:
            attack_piece = self.board[position[0]][position[1]]
            if attack_piece and (attack_piece.is_white != piece.is_white):
                self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                self.add_attack_position(piece, position)
            elif not attack_piece:
                self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                self.add_attack_position(piece, position)

    def find_bishop_moves(self, row, col, piece, row_i, col_i, board_range):
        '''
        does not use find all move function in piece
        '''
        for i in board_range:
            if row_i+i in board_range and col_i+i in board_range:
                position = [row_index[row_i+i], col_index[col_i+i]]
                if position != piece.position:
                    attack_piece = self.board[position[0]][position[1]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:
            if row_i+i in board_range and col_i-i in board_range:
                position = [row_index[row_i+i], col_index[col_i-i]]
                if position != piece.position:
                    attack_piece = self.board[position[0]][position[1]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:
            if row_i-i in board_range and col_i+i in board_range:
                position = [row_index[row_i-i], col_index[col_i+i]]
                if position != piece.position:
                    attack_piece = self.board[position[0]][position[1]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:
            if row_i-i in board_range and col_i-i in board_range:
                position = [row_index[row_i-i], col_index[col_i-i]]
                if position != piece.position:
                    attack_piece = self.board[position[0]][position[1]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)

    def find_queen_moves(self, row, col, piece, row_i, col_i, board_range):
        '''
        does not use find all move function in piece
        '''
        # Vertical & Horizontal
        for i in board_range:
            if (row_i+i in board_range):
                position = [row_index[row_i+i], col]
                if position != piece.position:
                    attack_piece = self.board[row_index[row_i+i]][col]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:    
            if (row_i-i in board_range):
                position = [row_index[row_i-i], col]
                if position != piece.position:
                    attack_piece = self.board[row_index[row_i-i]][col]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:
            if (col_i+i in board_range):
                position = [row, col_index[col_i+i]]
                if position != piece.position:
                    attack_piece = self.board[row][col_index[col_i+i]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:
            if (col_i-i in board_range):
                position = [row, col_index[col_i-i]]
                if position != piece.position:
                    attack_piece = self.board[row][col_index[col_i-i]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)

        # Diagonal
        for i in board_range:
            if row_i+i in board_range and col_i+i in board_range:
                position = [row_index[row_i+i], col_index[col_i+i]]
                if position != piece.position:
                    attack_piece = self.board[position[0]][position[1]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:
            if row_i+i in board_range and col_i-i in board_range:
                position = [row_index[row_i+i], col_index[col_i-i]]
                if position != piece.position:
                    attack_piece = self.board[position[0]][position[1]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:
            if row_i-i in board_range and col_i+i in board_range:
                position = [row_index[row_i-i], col_index[col_i+i]]
                if position != piece.position:
                    attack_piece = self.board[position[0]][position[1]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)
        for i in board_range:
            if row_i-i in board_range and col_i-i in board_range:
                position = [row_index[row_i-i], col_index[col_i-i]]
                if position != piece.position:
                    attack_piece = self.board[position[0]][position[1]]
                    if attack_piece:
                        if attack_piece.is_white is not piece.is_white:
                            self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                            self.add_attack_position(piece, position)
                        break
                    self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                    self.add_attack_position(piece, position)

    def find_king_moves(self, row, col, piece, row_i, col_i, board_range):
        all_possible_moves = piece.find_possible_moves()

        for position in all_possible_moves:
            attack_piece = self.board[position[0]][position[1]]
            if attack_piece and (attack_piece.is_white != piece.is_white):
                self.add_move_if_valid(piece = piece, position = position, is_kill = True)
                self.add_attack_position(piece, position)
            elif not attack_piece:
                self.add_move_if_valid(piece = piece, position = position, is_kill = False)
                self.add_attack_position(piece, position)

        # castle moves
        if self.board[row][col_index[0]] and piece.unmoved and self.board[row][col_index[0]].unmoved:
            is_empty = True
            for i in [1, 2, 3]:
                if self.board[row][col_index[i]]:
                    is_empty = False
            if is_empty:
                self.add_move_if_valid(
                    piece=piece,
                    position = [row, col_index[1]],
                    is_kill = False,
                    castle = {
                        'rookStartPosition': [row, col_index[0]], 
                        'rookEndPosition': [row, col_index[2]], 
                    }
                )
        if self.board[row][col_index[7]] and piece.unmoved and self.board[row][col_index[7]] and self.board[row][col_index[7]].unmoved:
            is_empty = True
            for i in [5, 6]:
                if self.board[row][col_index[i]]:
                    is_empty = False
            if is_empty:
                self.add_move_if_valid(
                    piece=piece,
                    position = [row, col_index[6]],
                    is_kill = False,
                    castle = {
                        'rookStartPosition': [row, col_index[7]], 
                        'rookEndPosition': [row, col_index[5]], 
                    }
                )

    def display_board(self):
        output_board = empty_board()
        for row in row_index:
            for col in col_index:
                if self.board[row][col]:
                    output_board[row][col] = self.board[row][col].out()

        return output_board

    def xnor(self, a, b):
        if a == b:
            return True
        return False

    def add_move_if_valid(self, piece, position, is_kill, castle=None):
        if self.xnor(a = (self.selected_player == 'BLACK'), b = piece.is_white):
            piece.add_move(position = position, is_kill = is_kill, castle = castle)

    def is_check(self):
        if self.white_king in self.black_attack_positions:
            self.is_white_check = True
        if self.black_king in self.white_attack_positions:
            self.is_black_check = True

    def add_attack_position(self, piece, position):
        '''
        instead of using a list, it may be better to store this as a board matrix
        '''
        if piece.is_white:
            self.white_attack_positions.add((position[0], position[1]))
        else:
            self.black_attack_positions.add((position[0], position[1]))

    def remove_check_moves(self, selected_player):
        '''
        create a temporary board with the move, then run get_exact_moves
        to check if the king is still in check
        '''
        for row in row_index:
            for col in col_index:
                if self.board[row][col]:

                    for i, move in enumerate(self.board[row][col].moves):
                        # creates deep copy of board
                        temp_board_ = copy.deepcopy(self.board)

                        # makes move on temp board (this doesnt work for castling)
                        temp_board_[move['newPosition'][0]][move['newPosition'][1]], temp_board_[row][col] = temp_board_[row][col], None
                        if move['castle']:
                            temp_board_[move['castle']['rookEndPosition'][0]][move['castle']['rookEndPosition'][1]], temp_board_[move['castle']['rookStartPosition'][0]][move['castle']['rookStartPosition'][1]] = temp_board_[move['castle']['rookStartPosition'][0]][move['castle']['rookStartPosition'][1]], None

                        # creates new board object
                        temp_board = Board(temp_board_, self.selected_player, original=False)
                        
                        if (temp_board.is_white_check and selected_player == 'BLACK') or (temp_board.is_black_check and selected_player == 'WHITE'):
                            self.board[row][col].moves[i] = None




        
