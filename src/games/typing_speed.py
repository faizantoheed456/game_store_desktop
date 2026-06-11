import customtkinter as ctk
import random
import time

class TypingSpeed(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back
        self.sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "Python is a versatile and powerful programming language.",
            "Gaming is more than just a hobby, it's a lifestyle.",
            "Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live.",
            "Artificial intelligence is the future of digital innovation.",
            "Keep calm and carry on gaming in the vault."
        ]
        self.target_text = ""
        self.start_time = 0
        
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=20)
        ctk.CTkButton(header, text="← Back", width=80, command=self.on_back).pack(side="left")
        
        ctk.CTkLabel(self, text="Typing Speed Test", font=("Arial Bold", 36)).pack(pady=20)

        self.text_display = ctk.CTkLabel(
            self, text="", font=("Arial", 20), 
            wraplength=800, text_color="#3498db"
        )
        self.text_display.pack(pady=40, padx=60)

        self.input_text = ctk.CTkTextbox(self, height=100, font=("Arial", 16))
        self.input_text.pack(fill="x", padx=100, pady=20)
        self.input_text.bind("<KeyPress>", self._start_timer)
        self.input_text.bind("<KeyRelease>", self._check_typing)

        self.stats_label = ctk.CTkLabel(self, text="WPM: 0  |  Accuracy: 0%", font=("Arial", 18))
        self.stats_label.pack(pady=20)

        self.reset_btn = ctk.CTkButton(self, text="New Sentence", command=self._reset)
        self.reset_btn.pack(pady=20)

        self._reset()

    def _reset(self):
        self.target_text = random.choice(self.sentences)
        self.text_display.configure(text=self.target_text)
        self.input_text.delete("1.0", "end")
        self.start_time = 0
        self.stats_label.configure(text="WPM: 0  |  Accuracy: 0%")

    def _start_timer(self, event):
        if self.start_time == 0:
            self.start_time = time.time()

    def _check_typing(self, event):
        typed = self.input_text.get("1.0", "end-1c")
        if not typed: return

        # Accuracy
        correct_chars = 0
        for i in range(min(len(typed), len(self.target_text))):
            if typed[i] == self.target_text[i]:
                correct_chars += 1
        
        accuracy = (correct_chars / len(typed)) * 100 if typed else 0
        
        # WPM
        elapsed = time.time() - self.start_time
        wpm = (len(typed) / 5) / (elapsed / 60) if elapsed > 0 else 0
        
        self.stats_label.configure(text=f"WPM: {int(wpm)}  |  Accuracy: {int(accuracy)}%")
        
        if typed == self.target_text:
            self.text_display.configure(text_color="#2ecc71")
            self.input_text.configure(state="disabled")
