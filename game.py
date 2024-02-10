# GAME MECHANICS
from datetime import datetime


class Piece:
    def __init__(self, type, color, id, pos_num):
        self.types = {"R": "rook",
                      "N": "knight",
                      "B": "bishop",
                      "Q": "queen",
                      "K": "king",
                      "P": "pawn"}

        self.start_positions = {"white": {
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

    def kill(self):
        self.status = "dead"

    def calculate_pos(self):
        for letter in self.pos:
            if letter in "ABCDEFGH":
                x = ord(letter) - 65
            else:
                y = int(letter) - 1

        return (x, y)


class Player:
    def __init__(self, color, nickname):
        self.color = color
        self.pieces = self.create_pieces(color)
        self.score = 0
        self.nickname = nickname

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
    
    def find_piece(self, name):
        pass

    def move(self, piece):
        pass

class ChessGame:
    def __init__(self, player1="Player 1", player2="Player 2"):
        now = datetime.now()
        self.player1 = Player("white", player1)
        self.player2 = Player("black", player2)
        self.start_data_time = now.strftime("%d-%m-%Y_%H-%M-%S")


    def fix_name(self, name, names, i=1):
        if name in names:
            if len(name) == 4:
                name = name[:3] + str(i)
            else:
                name += "_" + str(i)
            name, names = self.fix_name(name, names, i + 1)
        names.append(name)
        return name, names

    def pieces_pos(self):
        colors = {"white": "w", "black": "b"}
        names = []
        pieces_board = []
        for i in range(8):
            pieces_board.append(["*", "*", "*", "*", "*", "*", "*", "*"])

        for piece in self.player1.pieces:
            x, y = piece.calculate_pos()
            name, names = self.fix_name(colors[piece.color] + piece.type, names)
            pieces_board[y][x] = name

        for piece in self.player2.pieces:
            x, y = piece.calculate_pos()
            name, names = self.fix_name(colors[piece.color] + piece.type, names)
            pieces_board[y][x] = name
            
        return pieces_board
            


game = ChessGame("Player 1", "Player 2")

print(game.player1.pieces[0].calculate_pos())
print(game.pieces_pos())