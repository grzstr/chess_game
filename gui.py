
import game
from tkinter import *
from tkinter import messagebox

class GameMenu:

    def __init__(self):
        self.window = Tk()
        self.window.title("Chess Game")
        self.window.protocol("WM_DELETE_WINDOW", self.button_end_game)
        self.window.iconbitmap("icon.ico")
        #self.window.geometry("200x300")      
        self.game = None

        #Status variables
        self.status_white = NORMAL
        self.status_black = DISABLED

        self.pieces_dict = {"P": "pawn", "R": "rook", "N": "knight", "B": "bishop", "Q": "queen", "K": "king"}
        self.piece_pos = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", 
                          "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",
                          "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", 
                          "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8",
                          "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", 
                          "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8",
                          "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", 
                          "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8"]
        
        self.label = Label(self.window, text="Chess Game", font=("Arial", 24)).grid(row=0, column=0)

        # Buttons
        self.start_button = Button(self.window, text="Start Game", command=self.button_start_game).grid(row=5, column=0, pady=5)
        self.end_button = Button(self.window, text="Quit Game", command=self.button_end_game).grid(row=10, column=0, pady=5)

        self.window.mainloop()

# BUTTON COMMANDS
        
    def button_white_move(self, piece_pos, move_pos):
        self.game.white_move(piece_pos, move_pos)
        self.board_update()

    def button_black_move(self, piece_pos, move_pos):
        self.game.black_move(piece_pos, move_pos)
        self.board_update()

    def button_end_game(self):
        response = messagebox.askyesno("Quit Game", "Do you want to quit the game?")
        if response == 1:
            self.window.destroy()
            self.window.quit()

    def button_start_game(self):
        self.window.destroy()
        self.window = Tk()
        self.window.title("Chess Game")
        self.window.iconbitmap("icon.ico")
        self.window.protocol("WM_DELETE_WINDOW", self.button_end_game)
        self.game = game.ChessGame()
        self.board_update()

# REDUCING THE OPTIONS IN OPTIONS MENU

    def find_empty(self):
        empty_options = []
        pieces_pos = self.game.pieces_pos()
        for i in range(8):
            for j in range(8):
                if pieces_pos[i][j] == "*":
                    empty_options.append(chr(j + 65) + str(i + 1))
        return empty_options

    def find_my_pieces(self):
        my_pieces = []
        pieces_pos = self.game.pieces_pos()
        turn = self.game.get_turn()
        
        for i in range(8):
            for j in range(8):
                if turn == "white":
                    if pieces_pos[i][j][0] == "w":
                        my_pieces.append(chr(j + 65) + str(i + 1))
                else:
                    if pieces_pos[i][j][0] == "b":
                        my_pieces.append(chr(j + 65) + str(i + 1))
        return my_pieces        

    def find_enemy_pieces(self):
        enemy_pieces = []
        pieces_pos = self.game.pieces_pos()
        turn = self.game.get_turn()
        for i in range(8):
            for j in range(8):
                if turn == "black":
                    if pieces_pos[i][j][0] == "w":
                        enemy_pieces.append(chr(j + 65) + str(i + 1))
                else:
                    if pieces_pos[i][j][0] == "b":
                        enemy_pieces.append(chr(j + 65) + str(i + 1))
        return enemy_pieces 

    def make_move_list(self):
        move_list = self.find_empty()
        move_list.extend(self.find_enemy_pieces())
        return move_list
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
            which_turn_label = Label(self.window, text=f"TURN: {turn}", fg="black", bg="white")
            self.status_black = DISABLED
            self.status_white = NORMAL
        elif turn == "black":
            turn = turn[0].upper() + turn[1:]
            which_turn_label = Label(self.window, text=f"TURN: {turn}", fg="white", bg="black")
            self.status_white = DISABLED
            self.status_black = NORMAL
        which_turn_label.grid(row=3, column=10)

        white_score, black_score = self.game.get_score()
        score_label = Label(self.window, text=f"SCORE: White: {white_score} - Black: {black_score}").grid(row=4, column=10)

        text_message = self.game.get_message()
        if text_message == "":
            text_message = "                                                                        "
        message_label = Label(self.window, text=text_message).grid(row=7, column=10)

        self.side_panel()

    def side_panel(self):
        chosen_list = self.find_my_pieces()
        move_list = self.make_move_list()

        logo_img = PhotoImage(file="logo.png")
        label_corner_1 = Label(self.window, image=logo_img, borderwidth=0, highlightthickness=0)
        label_corner_1.image = logo_img
        label_corner_1.grid(row=1, column=10, columnspan=8)

        #WHITE PIECE MOVE
        piece_pos = StringVar()
        piece_pos.set(chosen_list[0])
        piece_pos_label = Label(self.window, text = "Chosen piece: ").grid(row=5, column=11, sticky=E, padx = 5)
        choose_piece = OptionMenu(self.window, piece_pos, *chosen_list)
        choose_piece.configure(state=self.status_white)
        choose_piece.grid(row=5, column=12, sticky=W, padx = 5)

        move_pos = StringVar()
        move_pos.set(move_list[0])
        move_pos_label = Label(self.window, text = "Move to: ").grid(row=5, column=13, sticky=E, padx = 5)
        move_piece = OptionMenu(self.window, move_pos, *move_list)
        move_piece.configure(state=self.status_white)
        move_piece.grid(row=5, column=14, sticky=W, padx = 5)

        #BLACK PIECE MOVE
        black_piece_pos = StringVar()
        black_piece_pos.set(chosen_list[0])
        black_piece_pos_label = Label(self.window, text = "Chosen piece: ").grid(row=6, column=11, sticky=E, padx = 5)
        black_choose_piece = OptionMenu(self.window, black_piece_pos, *chosen_list)
        black_choose_piece.configure(state=self.status_black)
        black_choose_piece.grid(row=6, column=12, sticky=W, padx = 5)

        black_move_pos = StringVar()
        black_move_pos.set(move_list[0])
        black_move_pos_label = Label(self.window, text = "Move to: ").grid(row=6, column=13, sticky=E, padx = 5)
        black_move_piece = OptionMenu(self.window, black_move_pos, *move_list)
        black_move_piece.configure(state=self.status_black)
        black_move_piece.grid(row=6, column=14, sticky=W, padx = 5)

        self.white_button = Button(self.window, text="Move White piece", command=lambda:self.button_white_move(piece_pos.get(), move_pos.get()), state=self.status_white).grid(row=5, column=10)
        self.black_button = Button(self.window, text="Move Black piece", command=lambda:self.button_black_move(black_piece_pos.get(), black_move_pos.get()), state=self.status_black).grid(row=6, column=10)
        self.end_button = Button(self.window, text="Quit Game", command=self.button_end_game).grid(row=8, column=13)

GameMenu()




