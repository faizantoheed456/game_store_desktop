import customtkinter as ctk

class ChoiceAdventure(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=40, pady=20)
        ctk.CTkButton(header, text="← Back", width=80, command=self.on_back).pack(side="left")
        
        ctk.CTkLabel(self, text="The Vault Escape", font=("Arial Bold", 36)).grid(row=0, column=0, pady=40)

        # Story Area
        self.story_box = ctk.CTkTextbox(self, font=("Arial", 20), spacing3=10, corner_radius=15, border_width=2)
        self.story_box.grid(row=1, column=0, sticky="nsew", padx=100, pady=20)
        
        # Options Area
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, pady=40)

        self._start_game()

    def _start_game(self):
        self._update_story(
            "You wake up in a cold, metallic room. The only light comes from a flickering computer screen. "
            "There are two doors: one made of heavy iron, and another with a complex keypad.",
            [("Open Iron Door", self._iron_door), ("Try Keypad", self._keypad)]
        )

    def _update_story(self, text, options):
        self.story_box.configure(state="normal")
        self.story_box.delete("1.0", "end")
        self.story_box.insert("1.0", text)
        self.story_box.configure(state="disabled")
        
        for widget in self.btn_frame.winfo_children():
            widget.destroy()
            
        for text, cmd in options:
            ctk.CTkButton(self.btn_frame, text=text, width=200, height=50, command=cmd).pack(side="left", padx=10)

    def _iron_door(self):
        self._update_story(
            "The door is locked from the outside. You hear footsteps approaching... It sounds like a robotic guard.",
            [("Hide under desk", self._hide), ("Search for weapon", self._search)]
        )

    def _keypad(self):
        self._update_story(
            "The keypad requires a 4-digit code. A sticky note nearby says 'Birth of Gaming'.",
            [("Enter 1972", self._escape), ("Enter 1990", self._fail)]
        )

    def _hide(self):
        self._update_story(
            "The guard enters, looks around, and leaves. You find a ventilation duct behind the desk!",
            [("Enter Duct", self._escape), ("Wait longer", self._fail)]
        )

    def _search(self):
        self._update_story(
            "You find a heavy wrench! But the guard is already through the door and zaps you with a laser.",
            [("Try Again", self._start_game)]
        )

    def _escape(self):
        self._update_story(
            "YOU ESCAPED! You reach the surface and see the digital skyline of GameVault City. Thanks for playing!",
            [("Play Again", self._start_game)]
        )

    def _fail(self):
        self._update_story(
            "GAME OVER. The security system detected you and locked down the entire sector.",
            [("Try Again", self._start_game)]
        )
