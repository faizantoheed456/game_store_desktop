import customtkinter as ctk
import random

class RockPaperScissors(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back
        self.choices = ["Rock", "Paper", "Scissors"]
        self.player_score = 0
        self.bot_score = 0
        
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=20)
        ctk.CTkButton(header, text="← Back", width=80, command=self.on_back).pack(side="left")
        
        ctk.CTkLabel(self, text="Rock Paper Scissors", font=("Arial Bold", 36)).pack(pady=40)

        self.score_label = ctk.CTkLabel(self, text="Player: 0  |  Bot: 0", font=("Arial", 24))
        self.score_label.pack(pady=20)

        # Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=40)
        
        for choice in self.choices:
            ctk.CTkButton(
                self.btn_frame, text=choice, width=150, height=150,
                corner_radius=75, font=("Arial Bold", 20),
                command=lambda c=choice: self._play(c)
            ).pack(side="left", padx=20)

        self.result_label = ctk.CTkLabel(self, text="Choose your weapon!", font=("Arial", 20), text_color="gray")
        self.result_label.pack(pady=40)

    def _play(self, player_choice):
        bot_choice = random.choice(self.choices)
        
        if player_choice == bot_choice:
            result = "It's a Tie!"
            color = "gray"
        elif (player_choice == "Rock" and bot_choice == "Scissors") or \
             (player_choice == "Paper" and bot_choice == "Rock") or \
             (player_choice == "Scissors" and bot_choice == "Paper"):
            result = "You Win!"
            color = "#2ecc71"
            self.player_score += 1
        else:
            result = "Bot Wins!"
            color = "#e74c3c"
            self.bot_score += 1
            
        self.result_label.configure(text=f"You: {player_choice}  vs  Bot: {bot_choice}\n{result}", text_color=color)
        self.score_label.configure(text=f"Player: {self.player_score}  |  Bot: {self.bot_score}")
