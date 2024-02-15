# GAME MECHANICS
from datetime import datetime

global SHOW_CALCULATED_POS
SHOW_CALCULATED_POS = False

class Piece:
    def __init__(self, type, color, id, pos_num):
        self.types = {"R": "rook",
                      "N": "knight",
                      "B": "bishop",
                      "Q": "queen",
                      "K": "king",
                      "P": "pawn"}

        self.start_positions = {
            "white": {
                "R": ["A1", "H1"],
                "N": ["B1", "G1"],
                "B": ["C1", "F1"],
                "Q": ["D1"],
                "K": ["E1"],
                "P": ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"]},

            "black": {
                "R": ["A8", "H8"],
                "N": ["B8", "G8"],
                "B": ["C8", "F8"],
                "Q": ["D8"],
                "K": ["E8"],
                "P": ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"]}}
        
        self.piece_name = color + "_" + self.types[type]
        self.type = type
        self.color = color
        self.pos = self.start_positions[color][type][pos_num]
        self.status = "alive"
        self.id = id 
        self.first_move = True

    def kill(self):
        self.status = "dead"
        self.pos = "I4"

    def get_calculated_pos(self):
        for letter in self.pos:
            if letter in "ABCDEFGHI":
                x = ord(letter) - 65
            else:
                y = int(letter) - 1
        
        if SHOW_CALCULATED_POS == True:
            print(f"[PIECE CLASS] Original pos: {self.pos} || Calculated pos: {x}, {y}")

        return (x, y)

    def set_calculated_pos(self, x, y):

        if SHOW_CALCULATED_POS == True:
            print(f"[PIECE CLASS] Original pos: {x}, {y} || Calculated pos: {self.pos}")

        self.pos = chr(x + 65) + str(y + 1)

class Player: 
    def __init__(self, color, nickname):
        self.color = color
        self.pieces = self.create_pieces(color)
        self.score = 0
        self.nickname = nickname
        self.board_limits = [0, 7]
        self.score = 0

    def create_pieces(self, color):
        pieces = []
        if color == "white":
            id = 0
        else:
            id = 16
        pieces.append(Piece("R", color, 0 + id, 0))
        pieces.append(Piece("N", color, 1 + id, 0))
        pieces.append(Piece("B", color, 2 + id, 0))
        pieces.append(Piece("Q", color, 3 + id, 0))
        pieces.append(Piece("K", color, 4 + id, 0))
        pieces.append(Piece("B", color, 5 + id, 1))
        pieces.append(Piece("N", color, 6 + id, 1))
        pieces.append(Piece("R", color, 7 + id, 1))
        for i in range(8):
            pieces.append(Piece("P", color, 8 + i + id, i))

        return pieces
    
    def kill_piece(self, id):
        self.pieces[id].kill()

    #Finding piece by name, it returns piece id
    def get_piece_id(self, name):
        type = name[1]
        if len(name) == 2:
            next = 0
        else:
            next = int(name[3])

        loop = 0
        for piece in self.pieces:
            if piece.type == type:
                if loop == next:
                    return piece.id
                else:
                    loop += 1

    # Moving functions          
    def move_pawn(self, x, y, first_move):
        moves = []
        part_1 = []
        part_2 = []
        part_3 = []
        # Default move
        if abs(y + 1) <= self.board_limits[1]:
            part_1.append([abs(x), abs(y + 1)])
        # First move
        if first_move == True:
            part_1.append([abs(x), abs(y + 2)])

        moves.append(part_1)
        
        # Moves for killing        
        if abs(x + 1) <= self.board_limits[0] and abs(y + 1) <= self.board_limits[1]:
            part_2.append([abs(x + 1), abs(y + 1)])
            moves.append(part_2)
        if abs(x - 1) >= self.board_limits[0] and abs(y + 1) <= self.board_limits[1]:
            part_3.append([abs(x - 1), abs(y + 1)])
            moves.append(part_3)
        
        return moves
    
    def move_rook(self, x, y):
        moves = []
        part_1 = []
        part_2 = []
        part_3 = []
        part_4 = []

        for i in range(8):
            # Move left
            if i < x:
                part_1.append([i, y])
            # Move right
            elif i > x:
                part_2.append([i, y])
            # Move down
            if i < y:
                part_3.append([x, i])
            # Move up
            elif i > y:
                part_4.append([x, i])

        moves.append(part_1)
        moves.append(part_2)
        moves.append(part_3)
        moves.append(part_4)

        return moves
    
    def move_knight(self, x, y):
        moves = []

        # Moves right / up and down
        if abs(x + 2) <= self.board_limits[0] and abs(y + 1) <= self.board_limits[1]:
            part_1 = []
            part_1.append([abs(x + 2), abs(y + 1)])
            moves.append(part_1)
        if abs(x + 2) <= self.board_limits[0] and abs(y - 1) >= self.board_limits[0]:
            part_2 = []
            part_2.append([abs(x + 2), abs(y - 1)])    
            moves.append(part_2)

        # Moves left / up and down
        if abs(x - 2) >= self.board_limits[0] and abs(y + 1) <= self.board_limits[1]:
            part_3 = []
            part_3.append([abs(x - 2), abs(y + 1)])
            moves.append(part_3)
        if abs(x - 2) >= self.board_limits[0] and abs(y - 1) >= self.board_limits[0]:
            part_4 = []
            part_4.append([abs(x - 2), abs(y - 1)])
            moves.append(part_4)

        # Moves up / right and left
        if abs(x + 1) <= self.board_limits[0] and abs(y + 2) <= self.board_limits[1]:
            part_5 = []
            part_5.append([abs(x + 1), abs(y + 2)])
            moves.append(part_5)

        if abs(x - 1) >= self.board_limits[0] and abs(y + 2) <= self.board_limits[1]:
            part_6 = []
            part_6.append([abs(x - 1), abs(y + 2)])
            moves.append(part_6)

        # Moves down / right and left
        if abs(x + 1) <= self.board_limits[0] and abs(y - 2) >= self.board_limits[0]:
            part_7 = []
            part_7.append([abs(x + 1), abs(y - 2)])
            moves.append(part_7)

        if abs(x - 1) >= self.board_limits[0] and abs(y - 2) >= self.board_limits[0]:
            part_8 = []
            part_8.append([abs(x - 1), abs(y - 2)])
            moves.append(part_8)

        return moves   

    def move_bishop(self, x, y):
        moves = []
        part_1 = []
        part_2 = []
        part_3 = []    
        part_4 = []

        for i in range(8):
            # Move up-right
            if x + i <= self.board_limits[0] and y + i <= self.board_limits[1]:
                part_1.append([x + i, y + i])
            # Move up-left
            if x - i >= self.board_limits[0] and y + i <= self.board_limits[1]:
                part_2.append([x - i, y + i])
            # Move down-right
            if x + i <= self.board_limits[0] and y - i >= self.board_limits[0]:
                part_3.append([x + i, y - i])
            # Move down-left
            if x - i >= self.board_limits[0] and y - i >= self.board_limits[0]:
                part_4.append([x - i, y - i])

        moves.append(part_1)
        moves.append(part_2)
        moves.append(part_3)
        moves.append(part_4)

        return moves

    def move_queen(self, x, y):
        moves = []
        parts = []
        parts = self.move_rook(x, y)
        parts.extend(self.move_bishop(x, y))
        moves.append(parts)
        return moves
    
    def move_king(self, x, y):
        moves = []

        # Move up
        if abs(y + 1) <= self.board_limits[1]:
            part_1 = []
            part_1.append([abs(x), abs(y + 1)])
            moves.append(part_1)
        # Move down
        if abs(y - 1) >= self.board_limits[0]:
            part_2 = []
            part_2.append([abs(x), abs(y - 1)])
            moves.append(part_2)
        # Move right
        if abs(x + 1) <= self.board_limits[0]:
            part_3 = []
            part_3.append([abs(x + 1), abs(y)])
            moves.append(part_3)
        # Move left
        if abs(x - 1) >= self.board_limits[0]:
            part_4 = []
            part_4.append([abs(x - 1), abs(y)])
            moves.append(part_4)
        # Move right up
        if abs(x + 1) <= self.board_limits[0] and abs(y + 1) <= self.board_limits[1]:
            part_5 = []
            part_5.append([abs(x + 1), abs(y + 1)])
            moves.append(part_5)
        # Move right down
        if abs(x + 1) <= self.board_limits[0] and abs(y - 1) >= self.board_limits[0]:
            part_6 = []
            part_6.append([abs(x + 1), abs(y - 1)])
            moves.append(part_6)
        # Move left up
        if abs(x - 1) >= self.board_limits[0] and abs(y + 1) <= self.board_limits[1]:
            part_7 = []
            part_7.append([abs(x - 1), abs(y + 1)])
            moves.append(part_7)
        # Move left down
        if abs(x - 1) >= self.board_limits[0] and abs(y - 1) >= self.board_limits[0]:
            part_8 = []
            part_8.append([abs(x - 1), abs(y - 1)])
            moves.append(part_8)

        return moves

    def collect_moves(self, id):
        moves = []
        x, y = self.pieces[id].get_calculated_pos()
        if self.pieces[id].color == "black":
            x = -x
            y = -y

        if self.pieces[id].status == "alive":
            if self.pieces[id].type == "P":
                moves = self.move_pawn(x, y, self.pieces[id].first_move)
            elif self.pieces[id].type == "R":
                moves = self.move_rook(x, y)
            elif self.pieces[id].type == "N":
                moves = self.move_knight(x, y)
            elif self.pieces[id].type == "B":
                moves = self.move_bishop(x, y)
            elif self.pieces[id].type == "Q":
                moves = self.move_queen(x, y)
            elif self.pieces[id].type == "K":
                moves = self.move_king(x, y)
        else:
            print("Piece is dead")

        if self.pieces[id].first_move == True:
            self.pieces[id].first_move = False
        return moves      
    
    def get_nickname(self):
        return self.nickname
    
class ChessGame:
    def __init__(self, player1="Player 1", player2="Player 2"):
        now = datetime.now()
        self.player1 = Player("white", player1)
        self.player2 = Player("black", player2)
        self.start_data_time = now.strftime("%d-%m-%Y_%H-%M-%S")
        self.moves_counter = 0
        self.white_turn = True
        self.black_turn = False
        self.update_flags = True
        self.end_game = False
        self.pieces_values = {"P": 1,
                              "N": 3,
                              "B": 3,
                              "R": 5,
                              "Q": 9,
                              "K": 1000}

    def fix_name(self, name, names, i=1):
        if name in names:
            if len(name) == 4:
                name = name[:3] + str(i)
            else:
                name += "_" + str(i)
            name, names = self.fix_name(name, names, i + 1)
        names.append(name)
        return name, names

    def get_turn(self):
        if self.white_turn == True and self.black_turn == False:
            return "white"
        elif self.white_turn == False and self.black_turn == True:
            return "black"
        else:
            return "none"

    def pieces_pos(self):
        colors = {"white": "w", "black": "b"}
        names = []
        pieces_board = []
        for i in range(8):
            pieces_board.append(["*", "*", "*", "*", "*", "*", "*", "*"])

        for piece in self.player1.pieces:
            x, y = piece.get_calculated_pos()
            name, names = self.fix_name(colors[piece.color] + piece.type, names)
            pieces_board[y][x] = name

        for piece in self.player2.pieces:
            x, y = piece.get_calculated_pos()
            name, names = self.fix_name(colors[piece.color] + piece.type, names)
            pieces_board[y][x] = name
            
        return pieces_board
    
    def get_piece_moves(self, piece_name):
        if piece_name[0] == "w":
            id = self.player1.get_piece_id(piece_name)
            moves = self.player1.collect_moves(id)
        else:
            id = self.player2.get_piece_id(piece_name) - 16
            moves = self.player2.collect_moves(id)

        return moves

    def move(self, piece_name, move_position):
        self.updar_flags = True
        moves = self.get_piece_moves(piece_name)
        pieces_pos = self.pieces_pos()

        move_is_valid = False
        for i in range(len(moves)):
            for j in range(len(moves[i])):
                # Check if move is valid
                if moves[i][j][0] == move_position[0] and moves[i][j][1] == move_position[1]:
                    move_is_valid = True
                    if pieces_pos[move_position[1]][move_position[0]] != "*":
                        # Check if piece is the same color
                        if piece_name[0] == pieces_pos[move_position[1]][move_position[0]][0]:
                            if SHOW_CALCULATED_POS == True:
                                print(f"Invalid move - you can't kill your own piece [{move_position[0]}][{move_position[1]}] Piece you want to move {piece_name} Piece you want to kill {pieces_pos[move_position[1]][move_position[0]]}")
                                self.update_flags = False
                            else:
                                print("Invalid move - you can't kill your own piece")
                                self.update_flags = False
                            break
                        else:
                            if piece_name[0] == "w":
                                id = self.player2.get_piece_id(pieces_pos[move_position[1]][move_position[0]])
                                self.player2.kill_piece(id)
                                if self.player2.pieces[id].type == "K":
                                    print("White wins")
                                    self.end_game = True
                                    break
                                self.player1.score += self.pieces_values[self.player1.pieces[id].type]
                                self.player2.pieces[id].set_calculated_pos(move_position[0], move_position[1])
                                print(f"You killed a piece {piece_name}")
                                
                            else:
                                id = self.player1.get_piece_id(pieces_pos[move_position[1]][move_position[0]])
                                self.player1.kill_piece(id)
                                if self.player1.pieces[id].type == "K":
                                    print("Black wins")
                                    self.end_game = True
                                    break
                                self.player2.score += self.pieces_values[self.player1.pieces[id].type]
                                self.player1.pieces[id].set_calculated_pos(move_position[0], move_position[1])
                                print(f"You killed a piece {piece_name}")
                            break
                    else:
                        if piece_name[0] == "w":
                            id = self.player1.get_piece_id(piece_name)
                            self.player1.pieces[id].set_calculated_pos(move_position[0], move_position[1])
                        else:
                            id = self.player2.get_piece_id(piece_name) - 16
                            self.player2.pieces[id].set_calculated_pos(move_position[0], move_position[1])
                        break
                    break
                    

        if move_is_valid == False:
            print("Invalid move - you can't move there")
            self.update_flags = False
        else:
            self.moves_counter += 1

    def get_score(self):
        return self.player1.score, self.player2.score
    
    def get_moves_counter(self):
        return self.moves_counter

    def calculate_pos(self,pos):
        for letter in pos:
            if letter in "ABCDEFGH":
                x = ord(letter) - 65
            else:
                y = int(letter) - 1
        
        if SHOW_CALCULATED_POS == True:
            print(f"[PLAYER CLASS] Original pos: {pos} || Calculated pos: {x}, {y}")

        return (x, y)

    def get_piece_by_pos(self, pos):
        pieces_pos = self.pieces_pos()
        x, y = self.calculate_pos(pos)

        return pieces_pos[y][x]

    def white_move(self, piece_pos, move_position):
        if self.end_game == True:
            print("Game is over")
            return False
        else:
            piece_name = self.get_piece_by_pos(piece_pos)
            if piece_name == "*":
                print("There is no piece on this position")
                return False
            elif piece_name[0] == "b":
                print("It's not your piece")
                return False
            else:
                if self.white_turn == True:
                    x, y = self.calculate_pos(move_position)
                    pos_tab = [x, y]
                    self.move(piece_name, pos_tab)
                    if self.update_flags== True:
                        self.white_turn = False
                        self.black_turn = True
                    self.update_flags = True
                else:
                    print("It's not your turn")
                    return False
            
    def black_move(self, piece_pos, move_position):
        if self.end_game == True:
            print("Game is over")
            return False
        else:
            piece_name = self.get_piece_by_pos(piece_pos)
            if piece_name == "*":
                print("There is no piece on this position")
                return False
            elif piece_name[0] == "w":
                print("It's not your piece")
                return False
            else:
                if self.black_turn == True:
                    x, y = self.calculate_pos(move_position)
                    pos_tab = [x, y]
                    self.move(piece_name, pos_tab)
                    if self.update_flags == True:
                        self.black_turn = False
                        self.white_turn = True
                    self.update_flags = True
                else:
                    print("It's not your turn")
                    return False