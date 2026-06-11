import customtkinter as ctk
import random

class MemoryMatch(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back
        self.icons = ["🎮", "🕹️", "👾", "🎯", "🎲", "🎹", "🎸", "🎧"] * 2
        random.shuffle(self.icons)
        
        self.cards = []
        self.flipped = []
        self.matches = 0
        self.moves = 0
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=40, pady=20)
        ctk.CTkButton(header, text="← Back", width=80, command=self.on_back).pack(side="left")
        self.status_label = ctk.CTkLabel(header, text="Memory Match - Moves: 0", font=("Arial Bold", 20))
        self.status_label.pack(side="left", padx=40)

        # Board
        self.board_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.board_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)
        
        for i in range(16):
            btn = ctk.CTkButton(
                self.board_frame, text="?", font=("Arial", 32),
                width=100, height=100, corner_radius=10,
                command=lambda i=i: self._flip(i)
            )
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.cards.append(btn)
        
        self.board_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self.board_frame.grid_rowconfigure((0,1,2,3), weight=1)

    def _flip(self, i):
        if len(self.flipped) < 2 and i not in [idx for idx, _ in self.flipped] and self.cards[i].cget("state") != "disabled":
            self.cards[i].configure(text=self.icons[i], fg_color="#3498db")
            self.flipped.append((i, self.icons[i]))
            
            if len(self.flipped) == 2:
                self.moves += 1
                self.status_label.configure(text=f"Memory Match - Moves: {self.moves}")
                self.after(800, self._check_match)

    def _check_match(self):
        (i1, v1), (i2, v2) = self.flipped
        if v1 == v2:
            self.cards[i1].configure(state="disabled", fg_color="#2ecc71", text_color="white")
            self.cards[i2].configure(state="disabled", fg_color="#2ecc71", text_color="white")
            self.matches += 1
            if self.matches == 8:
                self.status_label.configure(text=f"🏆 YOU WON in {self.moves} moves!", text_color="#2ecc71")
        else:
            self.cards[i1].configure(text="?", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            self.cards[i2].configure(text="?", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        
        self.flipped = []
