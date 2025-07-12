import time
import os, random
# from IPython.display import clear_output
from typing import Optional, Tuple, List, AnyStr

Position = Tuple[int, int]

class Piece:
    def __init__(self, name: AnyStr, pos: Position, color: AnyStr, symbol: AnyStr):
        __acc_names = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
        __acc_colors = ['b', 'w']
        __acc_sides = ['n', 's']

        assert name in __acc_names, f"Invalid piece name, you provided {name}"
        assert color in __acc_colors, f"Invalid piece color, you provided {color}"

        self.name: AnyStr = name
        self.pos: Position = pos
        self.color: AnyStr = color
        self.symbol: AnyStr = symbol

        self.available_moves: List[Position] = []

    def __repr__(self):
        return f"Pawn(name={self.name}, pos={self.pos}, color={self.color})"

    def move(self):
        pass

    def capture(self):
        pass

    def find_by_pos(self, pos, boar):
        for piece in board.pieces:      
            if piece.pos == pos:
                return piece

        return False

    def calculate_moves(self, board):
        self.available_moves: List[Position] = []

        match self.name:
            case "king":
                curr_state = [piece.pos for piece in board.pieces]
                pawn_dir = 1 if self.color == 'w' else -1

                for i in range(-1, 2):
                    for j in range(-1, 2):
                        pos = (self.pos[0]+(i*pawn_dir), self.pos[1]+j)

                        if pos[0] > 7 or pos[1] > 7 or pos[0] < 0 or pos[1] < 0:
                            continue

                        if pos not in curr_state:
                            self.available_moves.append(pos)
                        else:
                            unknown_piece = self.find_by_pos(pos, board)

                            if unknown_piece.color != self.color:
                                self.available_moves.append(pos)
                            break

            case "queen":
                curr_state = [piece.pos for piece in board.pieces]

                # Queen forward move
                for i in range(1, 8):
                    pos = (self.pos[0]+i, self.pos[1])

                    # Don't get out of the board
                    if pos[0] > 7:
                        break
                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:             
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Queen backwards move
                for i in range(1, 8):
                    pos = (self.pos[0]-i, self.pos[1])

                    # Don't get out of the board
                    if pos[0] < 0:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Queen right move
                for i in range(1, 8):
                    pos = (self.pos[0], self.pos[1]+i)

                    # Don't get out of the board
                    if pos[1] > 7:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Queen left move
                for i in range(1, 8):
                    pos = (self.pos[0], self.pos[1]-i)

                    # Don't get out of the board
                    if pos[1] < 0:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Queen diagonal forward right move
                for i in range(1, 8):
                    pos = (self.pos[0]+i, self.pos[1]+i)

                    # Don't get out of the board
                    if pos[0] > 7 or pos[1] > 7:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Queen diagonal forward left move
                for i in range(1, 8):
                    pos = (self.pos[0]+i, self.pos[1]-i)

                    # Don't get out of the board
                    if pos[0] > 7 or pos[1] < 0:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Queen diagonal backwards right move
                for i in range(1, 8):
                    pos = (self.pos[0]-i, self.pos[1]+i)

                    # Don't get out of the board
                    if pos[0] < 0 or pos[1] > 7:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Queen diagonal backwards left move
                for i in range(1, 8):
                    pos = (self.pos[0]-i, self.pos[1]-i)

                    # Don't get out of the board
                    if pos[0] < 0 or pos[1] < 0:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

            case "rook":
                curr_state = [piece.pos for piece in board.pieces]

                # Rook forward move
                for i in range(1, 8):
                    pos = (self.pos[0]+i, self.pos[1])

                    # Don't get out of the board
                    if pos[0] > 7:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Rook backward move
                for i in range(1, 8):
                    pos = (self.pos[0]-i, self.pos[1])

                    # Don't get out of the board
                    if pos[0] < 0:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Rook right move
                for i in range(1, 8):
                    pos = (self.pos[0], self.pos[1]+i)

                    # Don't get out of the board
                    if pos[1] > 7:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break


                # Rook left move
                for i in range(1, 8):
                    pos = (self.pos[0], self.pos[1]-i)

                    # Don't get out of the board
                    if pos[1] < 0:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

            case "knight":
                curr_state = [piece.pos for piece in board.pieces]

                directions = [(2, 1), (2, -1), (1, -2), (1, 2), (-2, 1), (-2, -1), (-1, -2), (-1, 2)]
                for d in directions:
                    pos = (self.pos[0] + d[0], self.pos[1] + d[1])

                    if pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0:
                        continue

                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

            case "bishop":
                curr_state = [piece.pos for piece in board.pieces]


                # Bishop diagonal forward right move
                for i in range(1, 8):
                    pos = (self.pos[0]+i, self.pos[1]+i)

                    # Don't get out of the board
                    if pos[0] > 7 or pos[1] > 7:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Bishop diagonal forward left move
                for i in range(1, 8):
                    pos = (self.pos[0]+i, self.pos[1]-i)

                    # Don't get out of the board
                    if pos[0] > 7 or pos[1] < 0:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Bishop diagonal backwards right move
                for i in range(1, 8):
                    pos = (self.pos[0]-i, self.pos[1]+i)

                    # Don't get out of the board
                    if pos[0] < 0 or pos[1] > 7:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

                # Bishop diagonal backwards left move
                for i in range(1, 8):
                    pos = (self.pos[0]-i, self.pos[1]-i)

                    # Don't get out of the board
                    if pos[0] < 0 or pos[1] < 0:
                        break

                    # Check if pos is held by another piece
                    if pos not in curr_state:
                        self.available_moves.append(pos)
                    else:
                        unknown_piece = self.find_by_pos(pos, board)

                        if unknown_piece.color != self.color:
                            self.available_moves.append(pos)
                        break

            case "pawn":
                curr_state = [piece.pos for piece in board.pieces]
                pawn_dir = 1 if self.color == 'w' else -1

                # Special case where pawn can make 2 moves forward
                if self.pos[0] == 1:
                    for i in range(1, 3):
                        pos = (self.pos[0]+(i*pawn_dir), self.pos[1])

                        if pos[0] > 7:
                            break

                        if pos not in curr_state:
                            self.available_moves.append(pos)
                        else:
                            unknown_piece = self.find_by_pos(pos, board)

                            if unknown_piece.color != self.color:
                                self.available_moves.append(pos)
                            break

                # Special case where pawn can make 2 moves forward
                elif self.pos[0] == 6:
                    for i in range(1, 3):
                        pos = (self.pos[0]+(i*pawn_dir), self.pos[1])

                        if pos[0] < 0:
                            break

                        if pos not in curr_state:
                            self.available_moves.append(pos)
                        else:
                            unknown_piece = self.find_by_pos(pos, board)

                            if unknown_piece.color != self.color:
                                self.available_moves.append(pos)
                            break
                else:
                    cap_dir = [(pawn_dir, 0), (pawn_dir, 1), (pawn_dir, -1)]
                    for idx, cp_d in enumerate(cap_dir):
                        pos = (self.pos[0] + cp_d[0], self.pos[1] + cp_d[1])

                        # if position has any piece
                        if pos in curr_state and idx > 0:
                            # find the piece by position
                            unknown_piece = self.find_by_pos(pos, board)

                            if unknown_piece and unknown_piece.color != self.color:
                                self.available_moves.append(pos)

                        if pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0:
                            continue

                        if pos not in curr_state:
                            self.available_moves.append(pos)

        return list(set(self.available_moves))

class PieceFactory:
    def __call__(self, name: AnyStr, pos: Position, color: AnyStr, symbol: AnyStr):
        self.piece = Piece(name=name, pos=pos, color=color, symbol=symbol)

        return self.piece

class Board:
    def __init__(self):
        __acc_names = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
        __piece_nums = [1, 1, 2, 2, 2, 8]
        __pieces_num_map = {p_name: p_num for p_name, p_num in zip(__acc_names, __piece_nums)}

        __acc_colors = ['b', 'w']

        white_pieces = {
            'king': '\u2654',
            'queen': '\u2655',
            'rook': '\u2656',
            'bishop': '\u2657',
            'knight': '\u2658',
            'pawn': '\u2659'
        }

        black_pieces = {
            'king': '\u265A',
            'queen': '\u265B',
            'rook': '\u265C',
            'bishop': '\u265D',
            'knight': '\u265E',
            'pawn': '\u265F'
        }

        self.pawn_factory = PieceFactory()
        self.pieces: List[Piece] = []

        king_positions = [(0, 3), (7, 4)]
        queen_positions = [(0, 4), (7, 3)]
        rook_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]
        bishop_positions = [(0, 2), (0, 5), (7, 2), (7, 5)]
        knight_positions = [(0, 1), (0, 6), (7, 1), (7, 6)]
        pawn_positions = [(i, j) for i in [1, 6] for j in range(8)]     
        pieces_positions = [king_positions, queen_positions, rook_positions, bishop_positions, knight_positions, pawn_positions]
        __pieces_pos_map = {p_name: p_pos for p_name, p_pos in zip(__acc_names, pieces_positions)}

        self.board = [['\u2022 ' for _ in range(8)] for _ in range(8)]

        # Generate pieces
        for p_name, p_pos in list(__pieces_pos_map.items()):
            for p_idx, piece_pos in enumerate(p_pos):
                if p_idx < len(p_pos)//2:
                    self.pieces.append(self.pawn_factory(name=p_name, pos=piece_pos, color="w", symbol=white_pieces[p_name]))
                else:
                    self.pieces.append(self.pawn_factory(name=p_name, pos=piece_pos, color="b", symbol=black_pieces[p_name]))
        
        # Assign each piece to the board
        for piece in self.pieces:
            x, y = piece.pos

            if 0 <= x < 8 and 0 <= y < 8:
                self.board[x][y] = piece.symbol + " "

    def print_board(self):        
        # This is for colab, use self.clear() for terminal
        # clear_output(wait=True)
        # self.clear()

        for row in self.board:
            print(' '.join(row))

    def check_piece(self, piece: Piece):
        self.clear_board()
        x, y = piece.pos

        self.board[x][y] = "\033[31m" + piece.symbol + " \033[0m"
        av_moves = piece.calculate_moves(self)

        for mv in av_moves:
            x, y = mv

            self.board[x][y] = "\033[31m" + '\u2022 ' + "\033[0m"

        # TODO: remove printing the board each time you check for available moves
        self.print_board()

        return av_moves

    def get_pieces_for_player(self, player: AnyStr):
        return [piece for piece in self.pieces if piece.color == player]


    def apply_move(self, pos: Position, symb: AnyStr):
        x, y = pos

        self.board[x][y] = symb + " "
        self.print_board()

    def clear_board(self):
        self.board = [['\u2022 ' for _ in range(8)] for _ in range(8)]

        for piece in self.pieces:   
            x, y = piece.pos

            if 0 <= x < 8 and 0 <= y < 8:
                self.board[x][y] = piece.symbol + " "

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')



if __name__ == "__main__":
    board = Board()

    white_pieces = board.get_pieces_for_player('w')
    black_pieces = board.get_pieces_for_player('b')

