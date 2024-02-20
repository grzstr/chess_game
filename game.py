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
            self.display_message(f"[PIECE CLASS] Original pos: {self.pos} || Calculated pos: {x}, {y}")

        return (x, y)

    def set_calculated_pos(self, x, y):

        if SHOW_CALCULATED_POS == True:
            self.display_message(f"[PIECE CLASS] Original pos: {x}, {y} || Calculated pos: {self.pos}")

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
        if abs(x + 1) <= self.board_limits[1] and abs(y + 1) <= self.board_limits[1]:
            part_2.append([abs(x + 1), abs(y + 1)])
            moves.append(part_2)
        if abs(x - 1) >= self.board_limits[0] and abs(y + 1) <= self.board_limits[1]:
            part_3.append([abs(x - 1), abs(y + 1)])
            moves.append(part_3)
        
        #print(moves)
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
                part_1.append([i, abs(y)])
            # Move right
            elif i > x:
                part_2.append([i, abs(y)])
            # Move down
            if i < y:
                part_3.append([abs(x), i])
            # Move up
            elif i > y:
                part_4.append([abs(x), i])

        if len(part_1) > 0:
            moves.append(part_1)
        if len(part_2) > 0:
            moves.append(part_2)
        if len(part_3) > 0:
            moves.append(part_3)
        if len(part_4) > 0:
            moves.append(part_4)

        return moves
    
    def move_knight(self, x, y):
        moves = []

        # Moves right / up and down
        if abs(x + 2) <= self.board_limits[1] and abs(y + 1) <= self.board_limits[1]:
            part_1 = []
            part_1.append([abs(x + 2), abs(y + 1)])
            moves.append(part_1)
        if abs(x + 2) <= self.board_limits[1] and abs(y - 1) >= self.board_limits[0]:
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
        if abs(x + 1) <= self.board_limits[1] and abs(y - 2) >= self.board_limits[0]:
            part_7 = []
            part_7.append([abs(x + 1), abs(y - 2)])
            moves.append(part_7)

        if abs(x - 1) >= self.board_limits[0] and abs(y - 2) >= self.board_limits[0]:
            part_8 = []
            part_8.append([abs(x - 1), abs(y - 2)])
            moves.append(part_8)

        if SHOW_CALCULATED_POS == True:
            self.display_message(f"Knight moves: {moves}, x: {x}, y: {y}")
        return moves   

    def move_bishop(self, x, y):
        moves = []
        part_1 = []
        part_2 = []
        part_3 = []    
        part_4 = []

        for i in range(8):
            # Move up-right
            if abs(x + i) <= self.board_limits[1] and abs(y + i) <= self.board_limits[1]:
                part_1.append([abs(x + i), abs(y + i)])
            # Move up-left
            if abs(x - i) >= self.board_limits[0] and abs(y + i) <= self.board_limits[1]:
                part_2.append([abs(x - i), abs(y + i)])
            # Move down-right
            if abs(x + i) <= self.board_limits[1] and abs(y - i) >= self.board_limits[0]:
                part_3.append([abs(x + i), abs(y - i)])
            # Move down-left
            if abs(x - i) >= self.board_limits[0] and abs(y - i) >= self.board_limits[0]:
                part_4.append([abs(x - i), abs(y - i)])

        if len(part_1) > 0:
            moves.append(part_1)
        if len(part_2) > 0:
            moves.append(part_2)
        if len(part_3) > 0:
            moves.append(part_3)
        if len(part_4) > 0:
            moves.append(part_4)

        return moves

    def move_queen(self, x, y):
        moves = []
        moves = self.move_rook(x, y)
        moves.extend(self.move_bishop(x, y))
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
        if abs(x + 1) <= self.board_limits[1]:
            part_3 = []
            part_3.append([abs(x + 1), abs(y)])
            moves.append(part_3)
        # Move left
        if abs(x - 1) >= self.board_limits[0]:
            part_4 = []
            part_4.append([abs(x - 1), abs(y)])
            moves.append(part_4)
        # Move right up
        if abs(x + 1) <= self.board_limits[1] and abs(y + 1) <= self.board_limits[1]:
            part_5 = []
            part_5.append([abs(x + 1), abs(y + 1)])
            moves.append(part_5)
        # Move right down
        if abs(x + 1) <= self.board_limits[1] and abs(y - 1) >= self.board_limits[0]:
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
            self.display_message("Piece is dead")

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
        self.message = ""
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
            if x >= 0 and x <= 7 and y >=0 and y <= 7:
                name, names = self.fix_name(colors[piece.color] + piece.type, names)
                pieces_board[y][x] = name

        for piece in self.player2.pieces:
            x, y = piece.get_calculated_pos()
            if x >= 0 and x <= 7 and y >=0 and y <= 7:
                name, names = self.fix_name(colors[piece.color] + piece.type, names)
                #print(f"Piece name: {name} || x: {x} || y: {y} || color: {piece.color} || type: {piece.type} || id: {piece.id} || pos: {piece.pos} || status: {piece.status} || first move: {piece.first_move} || nickname: {piece.piece_name}")
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

    # Usuwanie nie potrzebnych ruchów z tablicy i ustawienie ich rosnąco
    def set_begin_end_bishop(self, begin_pos, move_position):
        if begin_pos[0] < move_position[0]:
            if begin_pos[1] < move_position[1]:
                x_end = move_position[0]
                y_end = move_position[1]
                x_begin = begin_pos[0]
                y_begin = begin_pos[1]
            else:
                x_end = move_position[0]
                y_end = begin_pos[1]
                x_begin = begin_pos[0]
                y_begin = move_position[1]
        else:
            if begin_pos[1] < move_position[1]:
                x_end = begin_pos[0]
                y_end = move_position[1]
                x_begin = move_position[0]
                y_begin = begin_pos[1]
            else:
                x_end = begin_pos[0]
                y_end = begin_pos[1]
                x_begin = move_position[0]
                y_begin = move_position[1]            

        return x_begin, x_end, y_begin, y_end

    def set_begin_end_rook(self, begin_pos, move_position):
        if begin_pos[0] == move_position[0]:
            if begin_pos[1] < move_position[1]:
                x_begin = begin_pos[0]
                x_end = move_position[0]
                y_begin = begin_pos[1]
                y_end = move_position[1]
            else:
                x_begin = move_position[0]
                x_end = begin_pos[0]
                y_begin = move_position[1]
                y_end = begin_pos[1]
        elif begin_pos[1] == move_position[1]:
            if begin_pos[0] < move_position[0]:
                x_begin = begin_pos[0]
                x_end = move_position[0]
                y_begin = begin_pos[1]
                y_end = move_position[1]
            else:
                x_begin = move_position[0]
                x_end = begin_pos[0]
                y_begin = move_position[1]
                y_end = begin_pos[1]

        return x_begin, x_end, y_begin, y_end

    def set_begin_end_king(self, begin_pos, move_position):
        if begin_pos[0] < move_position[0]:
            if begin_pos[1] < move_position[1]:
                x_end = move_position[0]
                y_end = move_position[1]
                x_begin = begin_pos[0]
                y_begin = begin_pos[1]
            else:
                x_end = move_position[0]
                y_end = begin_pos[1]
                x_begin = begin_pos[0]
                y_begin = move_position[1]
        elif begin_pos[0] > move_position[0]:
            if begin_pos[1] < move_position[1]:
                x_end = begin_pos[0]
                y_end = move_position[1]
                x_begin = move_position[0]
                y_begin = begin_pos[1]
            else:
                x_end = begin_pos[0]
                y_end = begin_pos[1]
                x_begin = move_position[0]
                y_begin = move_position[1] 
        elif begin_pos[0] == move_position[0]:
            if begin_pos[1] < move_position[1]:
                x_begin = begin_pos[0]
                x_end = move_position[0]
                y_begin = begin_pos[1]
                y_end = move_position[1]
            else:
                x_begin = move_position[0]
                x_end = begin_pos[0]
                y_begin = move_position[1]
                y_end = begin_pos[1]
        elif begin_pos[1] == move_position[1]:
            if begin_pos[0] < move_position[0]:
                x_begin = begin_pos[0]
                x_end = move_position[0]
                y_begin = begin_pos[1]
                y_end = move_position[1]
            else:
                x_begin = move_position[0]
                x_end = begin_pos[0]
                y_begin = move_position[1]
                y_end = begin_pos[1]

        return x_begin, x_end, y_begin, y_end

    def filtr_moves(self, move, x_begin, x_end, y_begin, y_end):
        changed_moves = []
        for pos in move:
            if pos[0] >= x_begin and pos[0] <= x_end and pos[1] >= y_begin and pos[1] <= y_end:
                changed_moves.append(pos)
            
        return changed_moves

    def eliminate_moves(self, move, move_position, piece_name):
        if piece_name[0] == "w":
            id = self.player1.get_piece_id(piece_name)
            chosen_player = self.player1
        else:
            id = self.player2.get_piece_id(piece_name) - 16
            chosen_player = self.player2

        begin_pos = chosen_player.pieces[id].get_calculated_pos()
        if chosen_player.pieces[id].type == "N" or chosen_player.pieces[id].type == "P":
            return move
        elif chosen_player.pieces[id].type == "B":
            x_begin, x_end, y_begin, y_end = self.set_begin_end_bishop(begin_pos, move_position)
            move = self.filtr_moves(move, x_begin, x_end, y_begin, y_end)
        elif chosen_player.pieces[id].type == "R":
            x_begin, x_end, y_begin, y_end = self.set_begin_end_rook(begin_pos, move_position)
            move = self.filtr_moves(move, x_begin, x_end, y_begin, y_end)            
        elif chosen_player.pieces[id].type == "Q" or chosen_player.pieces[id].type == "K":
            x_begin, x_end, y_begin, y_end = self.set_begin_end_king(begin_pos, move_position)
            move = self.filtr_moves(move, x_begin, x_end, y_begin, y_end)

        for i in range(len(move)):
            if move[i][0] == begin_pos[0] and move[i][1] == begin_pos[1]:
                move.pop(i)
                break

        return move 

    def kill_piece(self, piece_name, move_position, pieces_pos):
        # Check if piece is the same color
        if piece_name[0] == pieces_pos[move_position[1]][move_position[0]][0]:
            if SHOW_CALCULATED_POS == True:
                self.display_message(f"Invalid move - you can't kill your own piece [{move_position[0]}][{move_position[1]}] Piece you want to move {piece_name} Piece you want to kill {pieces_pos[move_position[1]][move_position[0]]}")
                self.update_flags = False
            else:
                self.display_message(f"Invalid move - you can't kill your own piece")
                self.update_flags = False
            return False
        else:
            if pieces_pos[move_position[1]][move_position[0]] == "*":
                self.display_message("Invalid move - you can't kill nothing")
                self.update_flags = False
                return False
            else:
                if piece_name[0] == "w":
                    id = self.player2.get_piece_id(pieces_pos[move_position[1]][move_position[0]]) - 16
                    self.player2.kill_piece(id)
                    if self.player2.pieces[id].type == "K":
                        self.display_message("White wins")
                        self.end_game = True
                        return True
                    id = self.player1.get_piece_id(piece_name)
                    self.player1.score += self.pieces_values[self.player1.pieces[id].type]
                    self.player1.pieces[id].set_calculated_pos(move_position[0], move_position[1])
                    self.display_message(f"You killed a piece black {self.player2.pieces[id].piece_name}")
                    return True
                else:
                    id = self.player1.get_piece_id(pieces_pos[move_position[1]][move_position[0]])
                    self.player1.kill_piece(id)
                    if self.player1.pieces[id].type == "K":
                        self.display_message("Black wins")
                        self.end_game = True
                        return True
                    id = self.player2.get_piece_id(piece_name) - 16
                    self.player2.score += self.pieces_values[self.player1.pieces[id].type]
                    self.player2.pieces[id].set_calculated_pos(move_position[0], move_position[1])
                    self.display_message(f"You killed a piece white {self.player1.pieces[id].piece_name}")
                return True

    def move(self, piece_name, move_position):
        #self.update_flags = True
        moves = self.get_piece_moves(piece_name)
        pieces_pos = self.pieces_pos()

        move_is_valid = False
        for i in range(len(moves)):
            for j in range(len(moves[i])):
                # Check if move is valid
                if moves[i][j][0] == move_position[0] and moves[i][j][1] == move_position[1]:
                    move_is_valid = True

                    not_eliminated_moves = self.eliminate_moves(moves[i], move_position, piece_name)
                    if len(not_eliminated_moves) == 0:
                        self.display_message("Invalid move - you can't move there")
                        self.update_flags = False
                        break
                    any_piece = 0
                    for not_eliminated_move in not_eliminated_moves:
                        if pieces_pos[not_eliminated_move[1]][not_eliminated_move[0]] != "*":
                            any_piece += 1
                    if any_piece >= 2:
                        self.display_message("Invalid move - you can't move there")
                        self.update_flags = False
                        break
                    elif any_piece == 1:
                        is_killed = self.kill_piece(piece_name, move_position, pieces_pos)
                        if is_killed == True:
                            break
                        else:
                            self.display_message("Invalid move - you can't move there")
                            self.update_flags = False
                            break
                    # Check if there is a piece on the position
                    if pieces_pos[move_position[1]][move_position[0]] != "*":
                        is_killed = self.kill_piece(piece_name, move_position, pieces_pos)
                        if is_killed == True:
                            break
                    # If there is no piece on the position
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
            self.display_message("Invalid move - you can't move there")
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
            self.display_message(f"[PLAYER CLASS] Original pos: {pos} || Calculated pos: {x}, {y}")

        return (x, y)

    def get_piece_by_pos(self, pos):
        pieces_pos = self.pieces_pos()
        x, y = self.calculate_pos(pos)

        return pieces_pos[y][x]
    
    def get_message(self):
        return self.message

    def display_message(self, message):
        print(message)
        self.message = message

    def white_move(self, piece_pos, move_position):
        self.message = ""
        if self.end_game == True:
            self.display_message("Game is over")
            return False
        else:
            piece_name = self.get_piece_by_pos(piece_pos)
            if piece_name == "*":
                self.display_message("There is no piece on this position")
                return False
            elif piece_name[0] == "b":
                self.display_message("It's not your piece")
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
                    self.display_message("It's not your turn")
                    return False
            
    def black_move(self, piece_pos, move_position):
        self.message = ""
        if self.end_game == True:
            self.display_message("Game is over")
            return False
        else:
            piece_name = self.get_piece_by_pos(piece_pos)
            if piece_name == "*":
                self.display_message("There is no piece on this position")
                return False
            elif piece_name[0] == "w":
                self.display_message("It's not your piece")
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
                    self.display_message("It's not your turn")
                    return False