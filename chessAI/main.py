import random

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
        return f"Pawn(name='{self.name}', pos={self.pos}, color='{self.color}', side='{self.board_side}')"
    
    def move(self):
        pass

    def capture(self):
        pass

    def calculate_moves(self, board):
        self.available_moves: List[Position] = []

        match self.name:
            case "king":
                curr_state = [piece.pos for piece in board.pieces]

                for i in range(2):
                    for j in range(2):
                        pos = (self.pos[0]+i, self.pos[1]+j)

                        if pos not in curr_state:
                            self.available_moves.append(pos)
            case "queen":
                curr_state = [piece.pos for piece in board.pieces]

                if self.color == 'w':
                    for i in range(1, 8-self.pos[0]):
                        pos = (self.pos[0]+i, self.pos[1])

                        if pos not in curr_state:
                            self.available_moves.append(pos)
                        else:
                            break

                    for i in range(1, 8-self.pos[0]):
                        pos = (self.pos[0]-i, self.pos[1])

                        if pos[0] < 0:
                            break

                        if pos not in curr_state:
                            self.available_moves.append(pos)
                        else:
                            break

                    for i in range(1, 8-self.pos[0]):
                        pos = (self.pos[0]+i, self.pos[1]+i)
                        if pos[0] > 7 or pos[1] > 7:
                            break

                        if pos not in curr_state:
                            self.available_moves.append(pos)
                        else:
                            break

                    for i in range(1, 8-self.pos[0]):
                        pos = (self.pos[0]+i, self.pos[1]-i)
                        if pos[0] < 0 or pos[1] < 0:
                            break

                        if pos not in curr_state:
                            self.available_moves.append(pos)
                        else:
                            break

                # elif self.board_side == 's':
                #     print("I am in s")
                #     for i in range(8-self.pos[0]):
                #         pos = (self.pos[0]-1, self.pos[1])

                #         if pos not in curr_state:
                #             self.available_moves.append(pos)
                #         else:
                #             break
            case "pawn":
                curr_state = [piece.pos for piece in board.pieces]

                if self.pos[0] == 1:
                    for i in range(1, 3):
                        pos = (self.pos[0]+i, self.pos[1])

                        if pos not in curr_state:
                                self.available_moves.append(pos)
                        else:
                            break

                elif self.pos[0] == 6:
                    for i in range(1, 3):
                        pos = (self.pos[0]-i, self.pos[1])

                        if pos not in curr_state:
                            self.available_moves.append(pos)
                        else:
                            break

                elif board.whites_side == 'n':
                    pos = (self.pos[0]+1, self.pos[1])

                    if pos not in curr_state:
                        self.available_moves.append(pos)

                elif board.whites_side == 's':
                    pos = (self.pos[0]-1, self.pos[1])

                    if pos not in curr_state:
                        self.available_moves.append(pos) 


        return self.available_moves

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
        pieces_positions = [king_positions, queen_positions, rook_positions, bishop_positions, knight_positions, ]
        __pieces_pos_map = {p_name: p_pos for p_name, p_pos in zip(__acc_names, pieces_positions)}


        # Generate pieces
        for p_name, p_pos in list(__pieces_pos_map.items()):
            for p_idx, piece_pos in enumerate(p_pos):
                if p_idx < len(p_pos)//2:
                    self.pieces.append(self.pawn_factory(name=p_name, pos=piece_pos, color="w", symbol=black_pieces[p_name]))
                else:
                    self.pieces.append(self.pawn_factory(name=p_name, pos=piece_pos, color="b", symbol=white_pieces[p_name]))

    def update_board(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]

        for piece in self.pieces:
            x, y = piece.pos
            if 0 <= x < 8 and 0 <= y < 8:
                self.board[x][y] = piece.symbol

        for row in self.board:
            print(' '.join(row))

        test_pawn = self.pieces[2]
        print(f"Available moves for {test_pawn.color} {test_pawn.name} at {test_pawn.pos} -> {test_pawn.calculate_moves(self)}")
        
if __name__ == "__main__":
    board = Board()

    board.update_board()


