from services.constants import row_index, col_index

class Piece:
    def piece_type(self, is_white, piece_type):
        '''
        returns the peice type with its colour for the frontend
        '''
        if is_white:
            return piece_type+'-white'
        return piece_type+'-black'

    def add_move(self, position, is_kill, castle=None):
        '''
        appends a move that assumes false isKill. This must be overriden (or changed)
        '''
        self.moves.append(
            {
            "isKill": is_kill,
            "newPosition": position,
            "castle": castle
            }
        )

    def out(self):
        '''
        output formatting
        '''
        return {
            "type":self.piece_type(self.is_white, self.type), 
            "isWhite": self.is_white,
            "isDead": self.is_dead,
            "moves": self.moves,
            "unmoved": self.unmoved
            }

class Pawn(Piece):
    def __init__(self, is_dead, is_white, position, unmoved):
        """
        is_dead: boolean
        is_white: boolean
        """
        self.is_dead = is_dead
        self.is_white = is_white
        self.type = 'pawn'
        self.position = position
        self.unmoved = unmoved
        self.moves = []

    def __repr__(self):
        return f'Pawn({self.is_white})'

    def find_possible_moves(self):
        '''
        this method will return all moves possible assuming no other
        pieces exist on the board

        this looks messy. redo this
        '''
        new_positions = []

        row = row_index.index(self.position[0])
        col = col_index.index(self.position[1])
        if not self.is_white:
            if row+1 < len(row_index):
                new_positions.append([row_index[row+1], col_index[col]])
            # first move may move up 2 (row = 1 means second row) the third element is the position that must be empty to move 2
            if row == 1:
                new_positions.append([row_index[row+2], col_index[col], row_index[row+1]])
        elif self.is_white:
            if row-1 >= 0:
                new_positions.append([row_index[row-1], col_index[col]])
            # first move may move up 2 (row = 1 means second row)
            if row == 6:
                new_positions.append([row_index[row-2], col_index[col], row_index[row-1]])

        return new_positions

class Rook(Piece):
    def __init__(self, is_dead, is_white, position, unmoved):
        self.is_dead = is_dead
        self.is_white = is_white
        self.type = 'rook'
        self.position = position
        self.unmoved = unmoved
        self.moves = []

    def __repr__(self):
        return f'Rook({self.is_white})'

    def find_possible_moves(self):
        '''
        this method will return all moves possible assuming no other
        pieces exist on the board
        '''
        new_positions = []

        row, col = self.position
        for i in col_index:
            if i != col:
                new_positions.append([row, i])
        for j in row_index:
            if j != row:
                new_positions.append([j, col])

        return new_positions

class Knight(Piece):
    def __init__(self, is_dead, is_white, position, unmoved):
        self.is_dead = is_dead
        self.is_white = is_white
        self.type = 'knight'
        self.position = position
        self.unmoved = unmoved
        self.moves = []

    def __repr__(self):
        return f'Knight({self.is_white})'

    def find_possible_moves(self):
        '''
        this method will return all moves possible assuming no other
        pieces exist on the board

        this is hard coded in for now. Might make it cleaner later
        '''
        new_positions = []

        row, col = self.position
        row_i, col_i = row_index.index(row), col_index.index(col)
        board_range = range(0,8)
        if row_i+2 in board_range and col_i+1 in board_range:
            new_row, new_col = row_index[row_i+2], col_index[col_i+1]
            new_positions.append([new_row, new_col])
        if row_i+1 in board_range and col_i+2 in board_range:
            new_row, new_col = row_index[row_i+1], col_index[col_i+2]
            new_positions.append([new_row, new_col])

        if row_i-2 in board_range and col_i+1 in board_range:
            new_row, new_col = row_index[row_i-2], col_index[col_i+1]
            new_positions.append([new_row, new_col])
        if row_i-1 in board_range and col_i+2 in board_range:
            new_row, new_col = row_index[row_i-1], col_index[col_i+2]
            new_positions.append([new_row, new_col])

        if row_i+2 in board_range and col_i-1 in board_range:
            new_row, new_col = row_index[row_i+2], col_index[col_i-1]
            new_positions.append([new_row, new_col])
        if row_i+1 in board_range and col_i-2 in board_range:
            new_row, new_col = row_index[row_i+1], col_index[col_i-2]
            new_positions.append([new_row, new_col])

        if row_i-2 in board_range and col_i-1 in board_range:
            new_row, new_col = row_index[row_i-2], col_index[col_i-1]
            new_positions.append([new_row, new_col])
        if row_i-1 in board_range and col_i-2 in board_range:
            new_row, new_col = row_index[row_i-1], col_index[col_i-2]
            new_positions.append([new_row, new_col])

        return new_positions  

class Bishop(Piece):
    def __init__(self, is_dead, is_white, position, unmoved):
        self.is_dead = is_dead
        self.is_white = is_white
        self.type = 'bishop'
        self.position = position
        self.unmoved = unmoved
        self.moves = []

    def __repr__(self):
        return f'Bishop({self.is_white})'

    def find_possible_moves(self):
        '''
        this method will return all moves possible assuming no other
        pieces exist on the board
        '''
        new_positions = []

        row, col = self.position
        row_i, col_i = row_index.index(row), col_index.index(col)
        board_range = range(0,8)
        for i in board_range:
            if row_i+i in board_range and col_i+i in board_range:
                new_row, new_col = row_index[row_i+i], col_index[col_i+i]
                if (new_row, new_col) != (row, col):
                    new_positions.append([new_row, new_col])
            if row_i-i in board_range and col_i+i in board_range:
                new_row, new_col = row_index[row_i-i], col_index[col_i+i]
                if (new_row, new_col) != (row, col):
                    new_positions.append([new_row, new_col])
            if row_i+i in board_range and col_i-i in board_range:
                new_row, new_col = row_index[row_i+i], col_index[col_i-i]
                if (new_row, new_col) != (row, col):
                    new_positions.append([new_row, new_col])
            if row_i-i in board_range and col_i-i in board_range:
                new_row, new_col = row_index[row_i-i], col_index[col_i-i]
                if (new_row, new_col) != (row, col):
                    new_positions.append([new_row, new_col])
            
        return new_positions

class Queen(Piece):
    def __init__(self, is_dead, is_white, position, unmoved):
        self.is_dead = is_dead
        self.is_white = is_white
        self.type = 'queen'
        self.position = position
        self.unmoved = unmoved
        self.moves = []
    
    def __repr__(self):
        return f'Queen({self.is_white})'

    def find_possible_moves(self):
        '''
        this method will return all moves possible assuming no other
        pieces exist on the board
        '''
        new_positions = []

        row, col = self.position
        row_i, col_i = row_index.index(row), col_index.index(col)
        board_range = range(0,8)

        for i in col_index:
            if i != col:
                new_positions.append([row, i])
        for j in row_index:
            if j != row:
                new_positions.append([j, col])

        for i in board_range:
            if row_i+i in board_range and col_i+i in board_range:
                new_row, new_col = row_index[row_i+i], col_index[col_i+i]
                if (new_row, new_col) != (row, col):
                    new_positions.append([new_row, new_col])
            if row_i-i in board_range and col_i+i in board_range:
                new_row, new_col = row_index[row_i-i], col_index[col_i+i]
                if (new_row, new_col) != (row, col):
                    new_positions.append([new_row, new_col])
            if row_i+i in board_range and col_i-i in board_range:
                new_row, new_col = row_index[row_i+i], col_index[col_i-i]
                if (new_row, new_col) != (row, col):
                    new_positions.append([new_row, new_col])
            if row_i-i in board_range and col_i-i in board_range:
                new_row, new_col = row_index[row_i-i], col_index[col_i-i]
                if (new_row, new_col) != (row, col):
                    new_positions.append([new_row, new_col])
        
        return new_positions

class King(Piece):
    def __init__(self, is_dead, is_white, position, unmoved):
        self.is_dead = is_dead
        self.is_white = is_white
        self.type = 'king'
        self.position = position
        self.unmoved = unmoved
        self.moves = []

    def __repr__(self):
        return f'King({self.is_white})'

    def find_possible_moves(self):
        '''
        this method will return all moves possible assuming no other
        pieces exist on the board
        '''
        new_positions = []

        row, col = self.position
        row_i, col_i = row_index.index(row), col_index.index(col)
        board_range = range(0,8)

        if row_i+1 in board_range and col_i+1 in board_range:
            new_positions.append([row_index[row_i+1], col_index[col_i+1]])
        if row_i+1 in board_range and col_i in board_range:
            new_positions.append([row_index[row_i+1], col_index[col_i]])
        if row_i+1 in board_range and col_i-1 in board_range:
            new_positions.append([row_index[row_i+1], col_index[col_i-1]])

        if row_i in board_range and col_i+1 in board_range:
            new_positions.append([row_index[row_i], col_index[col_i+1]])
        if row_i in board_range and col_i-1 in board_range:
            new_positions.append([row_index[row_i], col_index[col_i-1]])

        if row_i-1 in board_range and col_i+1 in board_range:
            new_positions.append([row_index[row_i-1], col_index[col_i+1]])
        if row_i-1 in board_range and col_i in board_range:
            new_positions.append([row_index[row_i-1], col_index[col_i]])
        if row_i-1 in board_range and col_i-1 in board_range:
            new_positions.append([row_index[row_i-1], col_index[col_i-1]])

        return new_positions

