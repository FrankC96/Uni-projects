import time
import copy
import itertools
import os, random
from IPython.display import display, HTML, clear_output
from typing import Optional, Tuple, List, AnyStr, Union

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

        self.move_factory = MoveFactory() 

    def __repr__(self):
        return f"Piece {self.name} in team {self.color} with pos {self.pos}"

    def colored_piece(self, color):
        return f"<span style='color:{color}; font-size:24px;'>{self.symbol}</span>"

    def move(self, board, move):
        end_pos = move.end_pos

        assert  0 <= end_pos[0] < 8, f"Wrong move provided {self} to {end_pos}"
        assert  0 <= end_pos[1] < 8, f"Wrong move provided {self} to {end_pos}"

        # Starting position set to empty
        x_st, y_st = self.pos
        board.board[x_st][y_st] = "\u2022"

        # Check if the resulting position is occupied by another piece
        # Set the other piece to empty
        unknown_piece = self.find_by_pos(end_pos, board)
        if unknown_piece:
            if unknown_piece.name == "king":
                board.game_over = True

            board.captured_pieces.append(unknown_piece)
            board.pieces.remove(unknown_piece)

            x, y = end_pos
            self.pos = (x, y)
        else:
            x, y = end_pos
            self.pos = (x, y)

    def can_move(self, pos: Position, state: List[Position]):
        can_move = False
        if pos not in state:
            self.available_moves.append(pos)
            can_move = True

        return can_move

    def find_by_pos(self, pos, board):
        # REMINDME: Make it static or a Board method (prob)
        for piece in board.pieces:
            if piece.pos == pos:
                return piece

        return False

    def _check_position_bounds(self, pos: Position) -> Union[Position, None]:
        in_bounds = pos
        if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
            in_bounds = None

        return in_bounds

    def calculate_moves(self, board):
        self.available_moves: List[Position] = []

        white_pieces = [piece.pos for piece in board.pieces if piece.color == 'w']
        black_pieces = [piece.pos for piece in board.pieces if piece.color == 'b']

        map = board.board
        curr_player = self.color

        match self.name:
            case "king":
                start_pos = self.pos
                # directions=[forward, backward, left, right, forward diagonal right, forward diagonal left, backward diagonal right, backward diagonal left]
                directions = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                for dir in directions:
                    end_pos = self._check_position_bounds((start_pos[0] + dir[0], start_pos[1] + dir[1]))

                    if not end_pos:
                        continue

                    unknown_piece = self.find_by_pos(end_pos, board)
                    # There are 3 states a board cell can be in.
                    # 1. empty  2. Occupied by same team    3. Occupied by enemy team
                    if end_pos and unknown_piece and self.color != unknown_piece.color:
                        # Cell is occupied by enemy team, capture is registered as a valid move
                        self.available_moves.append(
                            self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=10000.0, is_capture=True, captured_piece=unknown_piece)
                        )

                    elif not unknown_piece:
                        # Cell is unoccupied, move
                        self.available_moves.append(
                            self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=1000.0, is_capture=False, captured_piece=None)
                        )
                    if end_pos and unknown_piece and self.color == unknown_piece.color:
                        # Cell occupied by same team, check next move
                        continue

            case "queen":
                start_pos = self.pos

                # directions=[forward, backward, left, right, left_forward, right_forward, left_backward, right_backward]
                directions = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 1), (-1, -1), (-1, 1)]
                for dir in directions:
                    for i in range(8):
                        end_pos = self._check_position_bounds((start_pos[0] + i*dir[0], start_pos[1] + i*dir[1]))

                        if not end_pos:
                            continue

                        unknown_piece = self.find_by_pos(end_pos, board)
                        # There are 3 states a board cell can be in.
                        # 1. empty  2. Occupied by same team    3. Occupied by enemy team
                        if end_pos and unknown_piece and self.color != unknown_piece.color:
                            # Cell is occupied by enemy team, capture is registered as a valid move
                            self.available_moves.append(
                                self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=600.0, is_capture=True, captured_piece=unknown_piece)
                            )
                            break

                        elif not unknown_piece:
                            # Cell is unoccupied, move
                            self.available_moves.append(
                                self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=300.0, is_capture=False, captured_piece=None)
                            )
                        if end_pos and unknown_piece and self.color == unknown_piece.color:
                            # Cell occupied by same team, check next move
                            break


            case "rook":
                start_pos = self.pos

                # directions=[forward, backward, left, right]
                directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
                for dir in directions:
                    for i in range(8):
                        end_pos = self._check_position_bounds((start_pos[0] + i*dir[0], start_pos[1] + i*dir[1]))

                        if not end_pos:
                            continue

                        unknown_piece = self.find_by_pos(end_pos, board)
                        # There are 3 states a board cell can be in.
                        # 1. empty  2. Occupied by same team    3. Occupied by enemy team
                        if end_pos and unknown_piece and self.color != unknown_piece.color:
                            # Cell is occupied by enemy team, capture is registered as a valid move
                            self.available_moves.append(
                                self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=200.0, is_capture=True, captured_piece=unknown_piece)
                            )
                            break

                        elif not unknown_piece:
                            # Cell is unoccupied, move
                            self.available_moves.append(
                                self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=100.0, is_capture=False, captured_piece=None)
                            )

                        if end_pos and unknown_piece and self.color == unknown_piece.color:
                            # Cell occupied by same team, check next move
                            break

            case "bishop":
                start_pos = self.pos

                # directions=[left_forward, right_forward, left_backward, right_backward]
                directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]
                for dir in directions:
                    for i in range(8):
                        end_pos = self._check_position_bounds((start_pos[0] + i*dir[0], start_pos[1] + i*dir[1]))

                        if not end_pos:
                            continue

                        unknown_piece = self.find_by_pos(end_pos, board)
                        # There are 3 states a board cell can be in.
                        # 1. empty  2. Occupied by same team    3. Occupied by enemy team
                        if end_pos and unknown_piece and self.color != unknown_piece.color:
                            # Cell is occupied by enemy team, capture is registered as a valid move
                            self.available_moves.append(
                                self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=100.0, is_capture=True, captured_piece=unknown_piece)
                            )
                            break

                        elif not unknown_piece:
                            # Cell is unoccupied, move
                            self.available_moves.append(
                                self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=50.0, is_capture=False, captured_piece=None)
                            )

                        if end_pos and unknown_piece and self.color == unknown_piece.color:
                            # Cell occupied by same team, check next move
                            break

            case "knight":
                start_pos = self.pos

                directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
                for dir in directions:
                    end_pos = self._check_position_bounds((start_pos[0] + dir[0], start_pos[1] + dir[1]))

                    if not end_pos:
                        continue

                    unknown_piece = self.find_by_pos(end_pos, board)
                    # There are 3 states a board cell can be in.
                    # 1. empty  2. Occupied by same team    3. Occupied by enemy team
                    if end_pos and unknown_piece and self.color != unknown_piece.color:
                        # Cell is occupied by enemy team, capture is registered as a valid move
                        self.available_moves.append(
                            self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=100.0, is_capture=True, captured_piece=unknown_piece)
                        )

                    elif not unknown_piece:
                        # Cell is unoccupied, move
                        self.available_moves.append(
                            self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=0.0, is_capture=False, captured_piece=None)
                        )

                    if end_pos and unknown_piece and self.color == unknown_piece.color:
                        # Cell occupied by same team, check next move
                        continue

            case "pawn":
                start_pos = self.pos
                home_pos = 2 if start_pos[0] == 1 or start_pos[0] == 6 else 1
                pawn_dir = 1 if curr_player == 'w' else -1

                #directions=[forward, forward_right, forward_left]
                directions = [(pawn_dir*home_pos, 0), (pawn_dir, 1), (pawn_dir, -1)]
                for dir in directions:
                    end_pos = self._check_position_bounds((start_pos[0] + dir[0], start_pos[1] + dir[1]))

                    if not end_pos:
                        continue

                    # REMINDME: Put condition for reaching final rank and promoting to queen

                    unknown_piece = self.find_by_pos(end_pos, board)
                    # There are 3 states a board cell can be in.
                    # 1. empty  2. Occupied by same team    3. Occupied by enemy team
                    if end_pos and unknown_piece and self.color != unknown_piece.color and dir != (pawn_dir*home_pos, 0):
                        # Cell is occupied by enemy team, capture is registered as a valid move
                        self.available_moves.append(
                            self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=20.0, is_capture=True, captured_piece=unknown_piece)
                        )

                    elif not unknown_piece and dir == (pawn_dir*home_pos, 0):
                        # Since the first move examined is the +2 forward
                        # We need to also examing the +1 forward if there is any pawn and not hover above it
                        inter_piece = self.find_by_pos((end_pos[0]-pawn_dir, end_pos[1]), board)
                        if inter_piece:
                            break
                        else:
                            # Cell is unoccupied, move
                            self.available_moves.append(
                                self.move_factory(piece=self, start_pos=start_pos, end_pos=end_pos, score=0.0, is_capture=False, captured_piece=None)
                            )
                        if home_pos == 2:
                            if not inter_piece:
                                self.available_moves.append(
                                    self.move_factory(piece=self, start_pos=start_pos, end_pos=(end_pos[0]-pawn_dir, end_pos[1]), score=0.0, is_capture=False, captured_piece=None)
                                )

                    if end_pos and unknown_piece and self.color == unknown_piece.color:
                        # Cell occupied by same team, check next move
                        break
        
        return list(set(self.available_moves))

class PieceFactory:
    def __call__(self, name: AnyStr, pos: Position, color: AnyStr, symbol: AnyStr):
        self.piece = Piece(name=name, pos=pos, color=color, symbol=symbol)

        return self.piece

class Move:
    def __init__(self, piece: Piece, start_pos: Position, end_pos: Position, score: float, is_capture: bool, captured_piece: Piece=None):
        self.piece = piece
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.score = score
        self.is_capture = is_capture
        self.captured_piece = captured_piece

    def __lt__(self, other):
        # just an overloaded operator for comparison
        return self.score < other.score

class MoveFactory:
    def __call__(self, piece: Piece, start_pos: Position, end_pos: Position, score: float, is_capture: bool, captured_piece: Piece=None):
        self.move = Move(piece=piece, start_pos=start_pos, end_pos=end_pos, score=score, is_capture=is_capture, captured_piece=captured_piece)

        return self.move

class Board:
    def __init__(self):
        __acc_names = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
        __piece_nums = [1, 1, 2, 2, 2, 8]
        __pieces_num_map = {p_name: p_num for p_name, p_num in zip(__acc_names, __piece_nums)}

        self.__acc_colors = ['b', 'w']

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
        self.captured_pieces: List[Piece] = []

        self.game_over: bool = False

        self.move_history: List[dict] = []

        king_positions = [(0, 3), (7, 4)]
        queen_positions = [(0, 4), (7, 3)]
        rook_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]
        bishop_positions = [(0, 2), (0, 5), (7, 2), (7, 5)]
        knight_positions = [(0, 1), (0, 6), (7, 1), (7, 6)]
        pawn_positions = [(i, j) for i in [1, 6] for j in range(8)]
        pieces_positions = [king_positions, queen_positions, rook_positions, bishop_positions, knight_positions, pawn_positions]
        __pieces_pos_map = {p_name: p_pos for p_name, p_pos in zip(__acc_names, pieces_positions)}

        self.board = [['\u2022' for _ in range(8)] for _ in range(8)]

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
                self.board[x][y] = piece.symbol

    def show(self, player: str=None, score: float=None, time: float=None):
        # This is for colab, use self.clear() for terminal
        # clear_output(wait=True)
        # self.clear()

        # self.board = [['\u2022' for _ in range(8)] for _ in range(8)]

        # Assign each piece to the board
        for piece in self.pieces:
            x, y = piece.pos

            if 0 <= x < 8 and 0 <= y < 8:
                self.board[x][y] = piece.symbol

        white_pieces = len([piece for piece in self.pieces if piece.color == 'w' and piece.symbol != "\u2022"])
        black_pieces = len([piece for piece in self.pieces if piece.color == 'b' and piece.symbol != "\u2022"])

        print(f"WHITE PIECES {white_pieces} | BLACK PIECES {black_pieces} | Player {player} | Score {score} | Time elapsed {time}")
        html = "<table style='font-size:24px; font-family:Arial; border-collapse: collapse;'>"
        for row in self.board:
            html += "<tr>"
            for cell in row:
                html += f"<td style='width:30px; height:30px; text-align:center;'>{cell}</td>"
            html += "</tr>"
        html += "</table>"
        display(HTML(html))

    def format_piece(self, piece):
        return piece.center(3)

    def get_pieces_for_player(self, player: AnyStr):
        return [piece for piece in self.pieces if piece.color == player]

    def count_pieces(self, team: str):
        p_idx = 0
        for p in self.pieces:
            if p.color == team:
                p_idx += 1

        return p_idx

    def score_board(self, player: AnyStr):
        assert player in self.__acc_colors, f"Valid players are 'w' and 'b', you provided {player}"

        PIECE_VALUES = {
        "king": 1000,
        "queen": 9,
        "rook": 5,
        "bishop": 3,
        "knight": 3,
        "pawn": 1
    }
        player_score = 0
        opponent_score = 0
        player_valid_moves = 0
        opponent_valid_moves = 0

        empty_cells  = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == '\u2022':
                    empty_cells += 1

        for piece in self.pieces:
            value = PIECE_VALUES.get(piece.name, 0)

            if piece.color == player:
                player_score += value
                player_valid_moves += len(piece.calculate_moves(self))
            else:
                opponent_score += value
                opponent_valid_moves += len(piece.calculate_moves(self))

        return (player_score - opponent_score) + (empty_cells-32)

    def clone(self):
        return copy.deepcopy(self)

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

def check_minimax():
    for i in range(1):
        curr_player = next(PLAYERS)

        if board.pieces:
            v, p, m = minimax(board, 2, True)

            print(f"[{v}] Moving piece {p.name + ' ' + p.color} from {p.pos} -> {m}")
            p.move(board, m)

            board.show()

def check_pawn_movement(board):
    for i in range(10):

        piece = black_pieces[-8]
        av_moves = piece.calculate_moves(board)

        if av_moves:
            piece.move(board, av_moves[0])
        else:
            board.undo_move()

        board.show()

def check_queen_movement(board, piece):
    av_moves = piece.calculate_moves(board)
    print(piece, av_moves)
    for move in av_moves:
        x, y = move.end_pos

        board.board[x][y] = f"<span style='color:{'red'}; font-size:24px;'>&#8226</span>"

    board.show()

def minimax(board, depth, is_maximizing_player, a, b):
    if depth == 0 or board.game_over:
        player = 'w' if is_maximizing_player else 'b'
        return board.score_board(player), None, None

    if is_maximizing_player:
        max_score = -float('inf')
        best_piece = None
        best_move = None
        for piece in board.get_pieces_for_player('w'):
            moves = piece.calculate_moves(board)
            sorted_moves = sorted(moves, key=lambda x: x.score, reverse=True)
            for move in sorted_moves:
                new_board = board.clone()
                new_piece = piece.find_by_pos(piece.pos, new_board)
                new_piece.move(new_board, move)
                score, _, _ = minimax(new_board, depth - 1, False, a, b)
                if score > max_score:
                    max_score = score
                    best_piece = piece
                    best_move = move

                if max_score >= b:
                    break

                a = max(a, max_score)
                if max_score >= b:
                    break
            if max_score >= b:
                break

        return (max_score, best_piece, best_move)
    else:
        min_score = float('inf')
        best_piece = None
        best_move = None
        for piece in board.get_pieces_for_player('b'):
            moves = piece.calculate_moves(board)
            sorted_moves = sorted(moves, key=lambda x: x.score, reverse=True)
            for move in sorted_moves:
                new_board = board.clone()
                new_piece = piece.find_by_pos(piece.pos, new_board)
                new_piece.move(new_board, move)
                score, _, _ = minimax(new_board, depth - 1, True, a, b)
                if score < min_score:
                    min_score = score
                    best_piece = piece
                    best_move = move

                b = min(b, min_score)
                if min_score <= a:
                    break
            if min_score <= a:
                break


        return (min_score, best_piece, best_move)

if __name__ == "__main__":
    board = Board()

    PLAYERS = itertools.cycle(['w', 'b'])

    white_pieces = [piece for piece in board.pieces if piece.color == 'w']
    black_pieces = [piece for piece in board.pieces if piece.color == 'b']
 
    # check_queen_movement(board, black_pieces[-1])

    for _ in range(50):
        curr_player = next(PLAYERS)

        alpha = -float('inf')
        beta = float('inf')

        start_time = time.time()
        score, piece, move = minimax(board, 3, curr_player == 'w', a=alpha, b=beta)
        end_time = time.time()

        if piece:
            piece.move(board, move)
        else:
            print(f"Player {curr_player} won!")
            break
        board.show(curr_player, score, end_time - start_time)

