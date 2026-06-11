import customtkinter as ctk
import random

class NumberGuess(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back
        self.target = random.randint(1, 100)
        self.attempts = 0
        
        self.grid_columnconfigure(0, weight=1)
        self.pack_propagate(False)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=20)
        ctk.CTkButton(header, text="← Back", width=80, command=self.on_back).pack(side="left")
        
        # Game UI
        ctk.CTkLabel(self, text="Guess a Number (1-100)", font=("Arial Bold", 32)).pack(pady=(100, 20))
        
        self.guess_entry = ctk.CTkEntry(self, width=200, height=50, font=("Arial", 20), placeholder_text="Enter number...")
        self.guess_entry.pack(pady=20)
        self.guess_entry.bind("<Return>", lambda e: self._check_guess())

        self.submit_btn = ctk.CTkButton(self, text="Submit Guess", width=200, height=50, command=self._check_guess)
        self.submit_btn.pack(pady=20)

        self.feedback_label = ctk.CTkLabel(self, text="Good luck!", font=("Arial", 18), text_color="gray")
        self.feedback_label.pack(pady=20)

        self.reset_btn = ctk.CTkButton(self, text="Play Again", width=150, command=self._reset, fg_color="transparent", border_width=1)
        self.reset_btn.pack(pady=40)

    def _check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1
            self.guess_entry.delete(0, 'end')

            if guess < self.target:
                self.feedback_label.configure(text=f"Too low! Try again. (Attempts: {self.attempts})", text_color="#e67e22")
            elif guess > self.target:
                self.feedback_label.configure(text=f"Too high! Try again. (Attempts: {self.attempts})", text_color="#e67e22")
            else:
                self.feedback_label.configure(text=f"Correct! You got it in {self.attempts} attempts!", text_color="#2ecc71")
                self.submit_btn.configure(state="disabled")
        except ValueError:
            self.feedback_label.configure(text="Please enter a valid number!", text_color="#e74c3c")

    def _reset(self):
        self.target = random.randint(1, 100)
        self.attempts = 0
        self.feedback_label.configure(text="New number generated. Good luck!", text_color="gray")
        self.submit_btn.configure(state="normal")
