import customtkinter as ctk
from tkinter import messagebox
from src.games.tic_tac_toe import TicTacToe
from src.games.number_guess import NumberGuess
from src.games.rock_paper_scissors import RockPaperScissors
from src.games.hangman import Hangman
from src.games.memory_match import MemoryMatch
from src.games.clicker_adventure import ClickerAdventure
from src.games.math_quiz import MathQuiz
from src.games.typing_speed import TypingSpeed
from src.games.simon_says import SimonSays
from src.games.choice_adventure import ChoiceAdventure

class GamesHubView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Game definitions with manuals
        self.game_data = [
            {
                "name": "Tic Tac Toe", 
                "desc": "Classical 3x3 grid vs Bot or Friend", 
                "icon": "❌", 
                "class": TicTacToe,
                "manual": "Objective: Get three of your marks in a horizontal, vertical, or diagonal row.\n\nModes:\n- vs Bot: Play against a random-move AI.\n- vs Human: Play with a friend on the same computer."
            },
            {
                "name": "Number Guesser", 
                "desc": "Can you guess the secret number?", 
                "icon": "🔢", 
                "class": NumberGuess,
                "manual": "Objective: Guess the hidden number between 1 and 100 in the fewest attempts possible.\n\nHow to play:\n- Type a number and press Enter.\n- The game will tell you if your guess is too high or too low."
            },
            {
                "name": "Rock Paper Scissors", 
                "desc": "The ultimate battle of luck", 
                "icon": "✂️", 
                "class": RockPaperScissors,
                "manual": "Objective: Win rounds against the bot.\n\nRules:\n- Rock beats Scissors.\n- Scissors beats Paper.\n- Paper beats Rock."
            },
            {
                "name": "Hangman", 
                "desc": "Save the man by guessing the word", 
                "icon": "🪑", 
                "class": Hangman,
                "manual": "Objective: Guess the hidden gaming-themed word before your attempts run out.\n\nRules:\n- You have 6 attempts.\n- Each wrong letter guess removes one attempt."
            },
            {
                "name": "Memory Match", 
                "desc": "Find all pairs of matching icons", 
                "icon": "🃏", 
                "class": MemoryMatch,
                "manual": "Objective: Find all 8 pairs of matching icons.\n\nHow to play:\n- Click a card to flip it.\n- Click another card to find its match.\n- If they don't match, they will flip back after a short delay."
            },
            {
                "name": "Monster Clicker", 
                "desc": "Slay monsters and upgrade power", 
                "icon": "⚔️", 
                "class": ClickerAdventure,
                "manual": "Objective: Slay monsters to earn gold and level up.\n\nMechanics:\n- Click 'ATTACK' to deal damage.\n- Use Gold to upgrade your Attack Power.\n- Each monster you kill makes the next one stronger!"
            },
            {
                "name": "Math Quiz", 
                "desc": "Test your mental calculation speed", 
                "icon": "➗", 
                "class": MathQuiz,
                "manual": "Objective: Solve as many math problems as you can.\n\nRules:\n- Correct answers give +1 point.\n- Incorrect answers give -1 point."
            },
            {
                "name": "Typing Speed", 
                "desc": "How fast can you type accurately?", 
                "icon": "⌨️", 
                "class": TypingSpeed,
                "manual": "Objective: Type the target sentence exactly as shown.\n\nHow to play:\n- Start typing in the box to begin the timer.\n- Your WPM (Words Per Minute) and Accuracy will update in real-time."
            },
            {
                "name": "Simon Says", 
                "desc": "Repeat the flashing pattern", 
                "icon": "🔴", 
                "class": SimonSays,
                "manual": "Objective: Remember and repeat a growing sequence of colors.\n\nHow to play:\n- Watch the computer flash a sequence.\n- Click the buttons in the exact same order.\n- One new color is added each round!"
            },
            {
                "name": "Vault Escape", 
                "desc": "A story-based choice adventure", 
                "icon": "🚪", 
                "class": ChoiceAdventure,
                "manual": "Objective: Escape the digital vault by making the right choices.\n\nHow to play:\n- Read the story segments.\n- Click the action buttons to decide your fate.\n- Be careful: some choices lead to a Game Over!"
            },
        ]

        self._render_hub()

    def _render_hub(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        # Header
        ctk.CTkLabel(self, text="Games Hub - Have Fun!", font=("Arial Bold", 32)).pack(anchor="w", padx=40, pady=(40, 20))
        
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=20)

        grid_frame = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=20)
        
        for i, data in enumerate(self.game_data):
            self._create_game_card(grid_frame, data).grid(
                row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew"
            )
        
        for i in range(3): grid_frame.grid_columnconfigure(i, weight=1)

    def _create_game_card(self, parent, data):
        card = ctk.CTkFrame(parent, height=250, corner_radius=15, border_width=1, border_color=("#dbdbdb", "#2b2b2b"))
        card.grid_propagate(False)
        
        # Info Button (Manual)
        info_btn = ctk.CTkButton(
            card, text="ⓘ", width=25, height=25, corner_radius=12,
            fg_color="transparent", text_color="gray", hover_color=("#dbdbdb", "#3b3b3b"),
            command=lambda d=data: messagebox.showinfo(f"How to Play: {d['name']}", d['manual'])
        )
        info_btn.place(relx=0.95, rely=0.05, anchor="ne")

        ctk.CTkLabel(card, text=data["icon"], font=("Arial", 60)).pack(pady=(25, 10))
        ctk.CTkLabel(card, text=data["name"], font=("Arial Bold", 18)).pack()
        ctk.CTkLabel(card, text=data["desc"], font=("Arial", 12), text_color="gray", wraplength=180).pack(pady=5)
        
        btn = ctk.CTkButton(
            card, text="Play Now", height=35, corner_radius=20,
            command=lambda gc=data["class"]: self._launch_game(gc)
        )
        btn.pack(side="bottom", pady=20)
        return card

    def _launch_game(self, game_class):
        # Clear hub and show game
        for widget in self.winfo_children():
            widget.destroy()
            
        game_instance = game_class(self, on_back=self._render_hub)
        game_instance.pack(fill="both", expand=True)
