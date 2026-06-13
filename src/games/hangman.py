import customtkinter as ctk
import random

class Hangman(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back
        self.words = ["PYTHON", "GAMING", "DESKTOP", "VAULT", "CUSTOMTKINTER", "DEVELOPER", "INTERFACE", "SOFTWARE", "OFFLINE", "ENGINEER"]
        self.word = ""
        self.guessed = []
        self.attempts = 6
        
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=20)
        ctk.CTkButton(header, text="← Back", width=80, command=self.on_back).pack(side="left")
        
        ctk.CTkLabel(self, text="Hangman", font=("Arial Bold", 36)).pack(pady=40)

        # Removed unsupported letter_spacing
        self.word_display = ctk.CTkLabel(self, text="", font=("Courier New Bold", 48))
        self.word_display.pack(pady=40)

        self.attempts_label = ctk.CTkLabel(self, text=f"Attempts Left: {self.attempts}", font=("Arial", 22), text_color="#e67e22")
        self.attempts_label.pack(pady=10)

        self.input_entry = ctk.CTkEntry(self, width=100, height=50, font=("Arial Bold", 24), justify="center")
        self.input_entry.pack(pady=20)
        self.input_entry.bind("<Return>", lambda e: self._guess())

        self.guess_btn = ctk.CTkButton(self, text="Guess Letter", width=150, height=45, command=self._guess)
        self.guess_btn.pack(pady=10)

        self.guessed_label = ctk.CTkLabel(self, text="Guessed: ", font=("Arial", 16), text_color="gray")
        self.guessed_label.pack(pady=20)

        self._reset()

    def _reset(self):
        self.word = random.choice(self.words)
        self.guessed = []
        self.attempts = 6
        self.attempts_label.configure(text=f"Attempts Left: {self.attempts}", text_color="#e67e22")
        self.guessed_label.configure(text="Guessed: ")
        self.guess_btn.configure(state="normal")
        self.word_display.configure(text_color=("gray10", "gray90"))
        self._update_display()

    def _update_display(self):
        display_chars = []
        for char in self.word:
            if char in self.guessed:
                display_chars.append(char)
            else:
                display_chars.append("_")
        
        # Add spaces for better readability
        display_text = " ".join(display_chars)
        self.word_display.configure(text=display_text)
        
        if "_" not in display_chars:
            self.attempts_label.configure(text="🎉 YOU SAVED HIM!", text_color="#2ecc71")
            self.guess_btn.configure(state="disabled")
        elif self.attempts <= 0:
            full_word = " ".join(list(self.word))
            self.word_display.configure(text=full_word, text_color="#e74c3c")
            self.attempts_label.configure(text="💀 GAME OVER", text_color="#e74c3c")
            self.guess_btn.configure(state="disabled")

    def _guess(self):
        char = self.input_entry.get().upper()
        self.input_entry.delete(0, 'end')
        
        if len(char) != 1 or not char.isalpha():
            return
            
        if char in self.guessed:
            return
            
        self.guessed.append(char)
        self.guessed_label.configure(text=f"Guessed: {', '.join(self.guessed)}")
        
        if char not in self.word:
            self.attempts -= 1
            self.attempts_label.configure(text=f"Attempts Left: {self.attempts}")
            
        self._update_display()
