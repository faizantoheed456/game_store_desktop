import customtkinter as ctk
import random
from tkinter import messagebox

class TicTacToe(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back
        self.current_player = "X"
        self.board = [""] * 9
        self.game_mode = "bot" # "bot" or "human"
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=40, pady=20)
        
        ctk.CTkButton(header, text="← Back", width=80, command=self.on_back).pack(side="left")
        self.status_label = ctk.CTkLabel(header, text="Tic Tac Toe - Player X's Turn", font=("Arial Bold", 20))
        self.status_label.pack(side="left", padx=40)
        
        self.mode_btn = ctk.CTkButton(header, text="Mode: vs Bot", width=120, command=self._toggle_mode)
        self.mode_btn.pack(side="right")

        # Board
        self.board_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.board_frame.grid(row=1, column=0, sticky="nsew")
        
        self.buttons = []
        for i in range(9):
            btn = ctk.CTkButton(
                self.board_frame, text="", font=("Arial Bold", 40),
                width=120, height=120, corner_radius=10,
                command=lambda i=i: self._make_move(i)
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)
        
        self.board_frame.grid_columnconfigure((0,1,2), weight=1)
        self.board_frame.grid_rowconfigure((0,1,2), weight=1)

        # Reset
        ctk.CTkButton(self, text="Reset Game", command=self._reset).grid(row=2, column=0, pady=20)

    def _toggle_mode(self):
        self.game_mode = "human" if self.game_mode == "bot" else "bot"
        self.mode_btn.configure(text=f"Mode: vs {'Bot' if self.game_mode == 'bot' else 'Human'}")
        self._reset()

    def _make_move(self, i):
        if self.board[i] == "" and not self._check_winner():
            self.board[i] = self.current_player
            color = "#3498db" if self.current_player == "X" else "#e74c3c"
            self.buttons[i].configure(text=self.current_player, state="disabled", text_color_disabled=color)
            
            if self._check_winner():
                self.status_label.configure(text=f"🎉 Player {self.current_player} Wins!", text_color="#2ecc71")
                return
            
            if "" not in self.board:
                self.status_label.configure(text="🤝 It's a Draw!", text_color="gray")
                return
                
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.configure(text=f"Player {self.current_player}'s Turn", text_color="white")
            
            if self.game_mode == "bot" and self.current_player == "O":
                self.after(500, self._bot_move)

    def _bot_move(self):
        empty_cells = [i for i, v in enumerate(self.board) if v == ""]
        if empty_cells:
            move = random.choice(empty_cells)
            self._make_move(move)

    def _check_winner(self):
        win_coords = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in win_coords:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return True
        return False

    def _reset(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.status_label.configure(text="Tic Tac Toe - Player X's Turn")
        for btn in self.buttons:
            btn.configure(text="", state="normal")
