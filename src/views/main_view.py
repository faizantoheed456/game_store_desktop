import customtkinter as ctk

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("GameVault")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.after(0, lambda: self.state('zoomed')) # Maximize window

        # Set default appearance
        ctk.set_appearance_mode("light")
        self.current_theme = "light"
        self.configure(fg_color=("#ffffff", "#1a1a1a")) # Explicitly set background colors

        # Theme Toggle Button (Top Right)
        self.theme_button = ctk.CTkButton(
            self,
            text="🌙", 
            width=45,
            height=45,
            corner_radius=22,
            border_width=2,
            border_color=("black", "white"),
            fg_color="transparent",
            text_color=("black", "white"),
            hover_color=("#ebebeb", "#2b2b2b"),
            command=self.toggle_theme
        )
        self.theme_button.place(relx=0.98, rely=0.02, anchor="ne")

        # Central Background Icon (Controller)
        self.bg_icon = ctk.CTkLabel(
            self,
            text="🎮",
            font=("Arial", 400),
            text_color=("#f0f0f0", "#252525") # Very subtle colors for light/dark
        )
        self.bg_icon.place(relx=0.5, rely=0.5, anchor="center")

        # Decorative Top Bubbles
        self._create_background_elements()

    def _create_background_elements(self):
        # Bubble configurations: (relx, rely, size)
        bubbles = [
            # Top Bubbles
            (0.10, -0.05, 120),
            (0.25, 0.05, 80),
            (0.45, -0.02, 150),
            (0.65, 0.08, 60),
            (0.85, -0.04, 100),
            # Left Side Bubbles
            (-0.02, 0.30, 90),
            (0.05, 0.55, 110),
            (-0.03, 0.80, 130),
        ]

        for x, y, size in bubbles:
            bubble = ctk.CTkFrame(
                self,
                width=size,
                height=size,
                corner_radius=size // 2,
                fg_color=("#f2f2f2", "#222222"),
                border_width=0
            )
            bubble.place(relx=x, rely=y, anchor="center")
            bubble.lower()

        # Star configurations: (relx, rely, size)
        stars = [
            (0.15, 0.20, 20),
            (0.80, 0.25, 15),
            (0.20, 0.70, 18),
            (0.90, 0.75, 22),
            (0.50, 0.15, 12),
            (0.35, 0.85, 16),
            (0.70, 0.60, 20),
        ]

        for x, y, size in stars:
            star = ctk.CTkLabel(
                self,
                text="⭐",
                font=("Arial", size),
                text_color=("#e0e0e0", "#282828") # Darkened light mode color for visibility
            )
            star.place(relx=x, rely=y, anchor="center")
            star.lower()

    def toggle_theme(self):
        if self.current_theme == "light":
            ctk.set_appearance_mode("dark")
            self.theme_button.configure(text="☀️")
            self.current_theme = "dark"
        else:
            ctk.set_appearance_mode("light")
            self.theme_button.configure(text="🌙")
            self.current_theme = "light"

if __name__ == "__main__":
    app = MainView()
    app.mainloop()
