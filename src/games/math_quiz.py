import customtkinter as ctk
import random

class MathQuiz(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back
        self.score = 0
        self.current_answer = 0
        
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=20)
        ctk.CTkButton(header, text="← Back", width=80, command=self.on_back).pack(side="left")
        
        ctk.CTkLabel(self, text="Math Genius Quiz", font=("Arial Bold", 36)).pack(pady=40)

        self.score_label = ctk.CTkLabel(self, text="Score: 0", font=("Arial", 24), text_color="#3498db")
        self.score_label.pack(pady=20)

        self.question_label = ctk.CTkLabel(self, text="", font=("Arial Bold", 48))
        self.question_label.pack(pady=40)

        self.answer_entry = ctk.CTkEntry(self, width=200, height=50, font=("Arial", 24), justify="center")
        self.answer_entry.pack(pady=20)
        self.answer_entry.bind("<Return>", lambda e: self._check_answer())

        self.submit_btn = ctk.CTkButton(self, text="Check Answer", width=200, height=45, command=self._check_answer)
        self.submit_btn.pack(pady=20)

        self.feedback_label = ctk.CTkLabel(self, text="", font=("Arial", 18))
        self.feedback_label.pack(pady=20)

        self._next_question()

    def _next_question(self):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(["+", "-", "*"])
        
        if op == "+": self.current_answer = a + b
        elif op == "-": self.current_answer = a - b
        else: self.current_answer = a * b
        
        self.question_label.configure(text=f"{a} {op} {b} = ?")
        self.answer_entry.delete(0, 'end')

    def _check_answer(self):
        try:
            user_ans = int(self.answer_entry.get())
            if user_ans == self.current_answer:
                self.score += 1
                self.feedback_label.configure(text="Correct!", text_color="#2ecc71")
            else:
                self.feedback_label.configure(text=f"Wrong! Answer was {self.current_answer}", text_color="#e74c3c")
                self.score = max(0, self.score - 1)
                
            self.score_label.configure(text=f"Score: {self.score}")
            self._next_question()
        except ValueError:
            pass
