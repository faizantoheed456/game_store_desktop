import customtkinter as ctk
import random

class SimonSays(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back
        self.sequence = []
        self.user_sequence = []
        self.sequence_playing = False
        self.colors = ["#e74c3c", "#3498db", "#2ecc71", "#f1c40f"] 
        
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=20)
        ctk.CTkButton(header, text="← Back", width=80, command=self.on_back).pack(side="left")
        
        ctk.CTkLabel(self, text="Simon Says", font=("Arial Bold", 36)).pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Press Start to Begin!", font=("Arial", 20))
        self.status_label.pack(pady=10)

        # Game Board
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=40)
        
        self.btns = []
        for i in range(4):
            btn = ctk.CTkButton(
                self.btn_frame, text="", width=150, height=150,
                fg_color=self.colors[i], hover_color=self.colors[i],
                command=lambda i=i: self._user_press(i)
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            self.btns.append(btn)
        
        self.start_btn = ctk.CTkButton(self, text="Start Game", command=self._next_round)
        self.start_btn.pack(pady=20)

    def _next_round(self):
        self.sequence_playing = True
        self.start_btn.configure(state="disabled")
        self.sequence.append(random.randint(0, 3))
        self.user_sequence = []
        self._play_sequence()

    def _play_sequence(self):
        self.status_label.configure(text="Watch Carefully...", text_color="white")
        for i, idx in enumerate(self.sequence):
            self.after((i + 1) * 600, lambda idx=idx: self._flash(idx))
        
        # Enable input after sequence ends
        self.after((len(self.sequence) + 1) * 600, self._enable_input)

    def _enable_input(self):
        self.sequence_playing = False
        self.status_label.configure(text="Your Turn!", text_color="#3498db")

    def _flash(self, idx):
        orig_color = self.colors[idx]
        self.btns[idx].configure(fg_color="white")
        self.after(300, lambda: self.btns[idx].configure(fg_color=orig_color))

    def _user_press(self, idx):
        if self.sequence_playing: return
        
        self.user_sequence.append(idx)
        self._flash(idx)
        
        current_step = len(self.user_sequence) - 1
        
        # Safety check for race conditions
        if current_step >= len(self.sequence): return

        if self.user_sequence[current_step] != self.sequence[current_step]:
            self.status_label.configure(text="❌ WRONG! Final Score: " + str(len(self.sequence) - 1), text_color="#e74c3c")
            self.sequence = []
            self.start_btn.configure(state="normal", text="Try Again")
            self.sequence_playing = True # Block until restart
            return
            
        if len(self.user_sequence) == len(self.sequence):
            self.sequence_playing = True
            self.status_label.configure(text="✅ Correct!", text_color="#2ecc71")
            self.after(1000, self._next_round)
