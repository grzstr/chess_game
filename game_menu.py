
import game
from tkinter import *

class GameMenu:

    def __init__(self):
        self.pieces_dict = {"P": "pawn", "R": "rook", "N": "knight", "B": "bishop", "Q": "queen", "K": "king"}

        self.window = Tk()
        self.window.title("Chess Game")
        #self.window.geometry("400x300")
        self.game = None
        self.piece_pos = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", 
                          "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",
                          "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", 
                          "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8",
                          "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", 
                          "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8",
                          "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", 
                          "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8"]
        
        self.label = Label(self.window, text="Chess Game", font=("Arial", 24)).grid(row=0, column=0)

        self.start_button = Button(self.window, text="Start Game", command=self.start_game).grid(row=1, column=0)
        self.end_button = Button(self.window, text="End Game", command=self.end_game).grid(row=10, column=0)

        self.window.mainloop()

# BUTTON COMMANDS
    def button_white_move(self, piece_pos, move_pos):
        self.game.white_move(piece_pos, move_pos)
        self.board_update()

    def button_black_move(self, piece_pos, move_pos):
        self.game.black_move(piece_pos, move_pos)
        self.board_update()
# GUI

    def img_piece_name(self, piece_name, x, y):
        if piece_name[0] == "w":
            color = "white"
        else:
            color = "black"

        piece = self.pieces_dict[piece_name[1]]

        if (x+y)%2==0:
            bg = "w"
        else:
            bg = "b"

        return f"{color}_{piece}_{bg}.png"

    def board_update(self):

        self.communicates_panel()

        w_empty = "empty_white.png"
        b_empty = "empty_black.png"

        corner_img = PhotoImage(file="board/corner.png")
        label_corner_1 = Label(self.window, image=corner_img, borderwidth=0, highlightthickness=0)
        label_corner_1.image = corner_img
        label_corner_1.grid(row=0, column=0)

        label_corner_1 = Label(self.window, image=corner_img, borderwidth=0, highlightthickness=0)
        label_corner_1.image = corner_img
        label_corner_1.grid(row=9, column=0)

        label_corner_1 = Label(self.window, image=corner_img, borderwidth=0, highlightthickness=0)
        label_corner_1.image = corner_img
        label_corner_1.grid(row=0, column=9)

        label_corner_1 = Label(self.window, image=corner_img, borderwidth=0, highlightthickness=0)
        label_corner_1.image = corner_img
        label_corner_1.grid(row=9, column=9)

        letters = "ABCDEFGH"        
        for i in range(8):
            img = PhotoImage(file=f"board/{i+1}.png")
            label_left = Label(self.window, image=img, borderwidth=0, highlightthickness=0)
            label_left.image = img
            label_left.grid(row=i+1, column=0)
            
            label_right = Label(self.window, image=img, borderwidth=0, highlightthickness=0)
            label_right.image = img
            label_right.grid(row=i+1, column=9)

            img = PhotoImage(file=f"board/{letters[i]}.png")
            label_up = Label(self.window, image=img, borderwidth=0, highlightthickness=0)
            label_up.image = img
            label_up.grid(row=0, column=i+1)

            label_down = Label(self.window, image=img, borderwidth=0, highlightthickness=0)
            label_down.image = img
            label_down.grid(row=9, column=i+1)

        pieces = self.game.pieces_pos()
        
        for i in range(8):
            for j in range(8):
                piece = pieces[i][j]
                
                if piece != "*":
                    piece_name = self.img_piece_name(piece, j, i)
                    path = f"pieces/{piece_name}"

                    img = PhotoImage(file=path)
                    label = Label(self.window, image=img, borderwidth=0, highlightthickness=0)
                    label.image = img
                    label.grid(row=i+1, column=j+1)
                else:
                    if (i+j)%2==0:
                        img = PhotoImage(file=f"pieces/{w_empty}")
                    else:
                        img = PhotoImage(file=f"pieces/{b_empty}")
                    label = Label(self.window, image=img, borderwidth=0, highlightthickness=0)
                    label.image = img
                    label.grid(row=i+1, column=j+1)
         
    def communicates_panel(self):
        turn = self.game.get_turn()
        if turn == "white":
            turn = turn[0].upper() + turn[1:]
            which_turn_label = Label(self.window, text=f"{turn} turn", fg="black", bg="white")
        elif turn == "black":
            turn = turn[0].upper() + turn[1:]
            which_turn_label = Label(self.window, text=f"{turn} turn", fg="white", bg="black")
        which_turn_label.grid(row=3, column=10)

    def side_panel(self):
        #WHITE PIECE MOVE
        piece_pos = StringVar()
        piece_pos.set(self.piece_pos[0])
        piece_pos_label = Label(self.window, text = "Chosen piece: ").grid(row=5, column=11, sticky=E, padx = 5)
        choose_piece = OptionMenu(self.window, piece_pos, *self.piece_pos)
        choose_piece.grid(row=5, column=12, sticky=W, padx = 5)

        move_pos = StringVar()
        move_pos.set(self.piece_pos[0])
        move_pos_label = Label(self.window, text = "Move to: ").grid(row=5, column=13, sticky=E, padx = 5)
        move_piece = OptionMenu(self.window, move_pos, *self.piece_pos)
        move_piece.grid(row=5, column=14, sticky=W, padx = 5)

        #BLACK PIECE MOVE
        black_piece_pos = StringVar()
        black_piece_pos.set(self.piece_pos[0])
        black_piece_pos_label = Label(self.window, text = "Chosen piece: ").grid(row=6, column=11, sticky=E, padx = 5)
        black_choose_piece = OptionMenu(self.window, black_piece_pos, *self.piece_pos)
        black_choose_piece.grid(row=6, column=12, sticky=W, padx = 5)

        black_move_pos = StringVar()
        black_move_pos.set(self.piece_pos[0])
        black_move_pos_label = Label(self.window, text = "Move to: ").grid(row=6, column=13, sticky=E, padx = 5)
        black_move_piece = OptionMenu(self.window, black_move_pos, *self.piece_pos)
        black_move_piece.grid(row=6, column=14, sticky=W, padx = 5)

        self.white_button = Button(self.window, text="Move White piece", command=lambda:self.button_white_move(piece_pos.get(), move_pos.get())).grid(row=5, column=10)
        self.black_button = Button(self.window, text="Move Black piece", command=lambda:self.button_black_move(black_piece_pos.get(), black_move_pos.get())).grid(row=6, column=10)

    def start_game(self):
        self.window.destroy()
        self.window = Tk()
        self.window.title("Chess Game")
        self.game = game.ChessGame()
        self.board_update()
        self.side_panel()

    def end_game(self):
        self.window.destroy()


GameMenu()




