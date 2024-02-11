
import game
from tkinter import *

class GameMenu:

    def __init__(self):
        self.pieces_dict = {"P": "pawn", "R": "rook", "N": "knight", "B": "bishop", "Q": "queen", "K": "king"}

        self.window = Tk()
        self.window.title("Chess Game")
        #self.window.geometry("400x300")
        self.game = None

        self.label = Label(self.window, text="Chess Game", font=("Arial", 24)).grid(row=0, column=0)

        self.start_button = Button(self.window, text="Start Game", command=self.start_game).grid(row=1, column=0)
        self.end_button = Button(self.window, text="End Game", command=self.end_game).grid(row=10, column=0)

        self.window.mainloop()

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
        self.window = Tk()
        self.window.title("Chess Game")

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
         


    def start_game(self):
        self.window.destroy()
        self.game = game.ChessGame()
        self.board_update()
    
    def end_game(self):
        self.window.destroy()


GameMenu()




