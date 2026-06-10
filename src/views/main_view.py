import customtkinter as ctk
from src.views.register_view import RegisterView
from src.views.dashboard_view import DashboardView
from src.controllers.auth_controller import AuthController
from tkinter import messagebox

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("GameVault")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.update_idletasks() # Force geometry updates
        self.after(0, lambda: self.state('zoomed')) # Maximize window

        # Set default appearance
        ctk.set_appearance_mode("light")
        self.current_theme = "light"
        self.configure(fg_color=("#ffffff", "#1a1a1a")) # Explicitly set background colors

        # Container for main content (Dashboard)
        self.dashboard = None

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
            font=("Arial", 300),
            text_color=("#f0f0f0", "#252525")
        )
        self.bg_icon.place(relx=0.5, rely=0.5, anchor="center")

        # Decorative Top Bubbles
        self.bg_elements = []
        self._create_background_elements()

        # Login Interface (Centered Frame)
        self.login_frame = ctk.CTkFrame(
            self,
            width=650,
            height=750,
            corner_radius=30,
            border_width=3,
            border_color=("#dbdbdb", "#2b2b2b"),
            fg_color=("#ffffff", "#1f1f1f")
        )
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.login_frame.grid_propagate(False)

        # Content inside Login Frame
        self.title_label = ctk.CTkLabel(
            self.login_frame,
            text="GameVault",
            font=("Arial Bold", 40),
            text_color=("black", "white")
        )
        self.title_label.pack(pady=(80, 15))

        self.subtitle_label = ctk.CTkLabel(
            self.login_frame,
            text="Welcome back, Gamer!",
            font=("Arial", 16),
            text_color=("gray", "gray")
        )
        self.subtitle_label.pack(pady=(0, 50))

        # Input Fields Container (to help with alignment)
        self.input_container = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        self.input_container.pack(pady=20)

        self.username_entry = ctk.CTkEntry(
            self.input_container,
            placeholder_text="Username",
            width=350,
            height=50,
            corner_radius=10,
            border_width=1
        )
        self.username_entry.pack(pady=10)

        # Password Container for Entry + Eye Button
        self.pass_container = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.pass_container.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.pass_container,
            placeholder_text="Password",
            show="*",
            width=350,
            height=50,
            corner_radius=10,
            border_width=1
        )
        self.password_entry.pack()

        # Eye Icon Button (placed inside/over the entry)
        self.password_visible = False
        self.eye_button = ctk.CTkButton(
            self.pass_container,
            text="👁️",
            width=30,
            height=30,
            fg_color="transparent",
            text_color=("gray", "lightgray"),
            hover_color=("#ebebeb", "#2b2b2b"),
            command=self.toggle_password_visibility
        )
        # Position the eye button at the end of the password entry
        self.eye_button.place(relx=0.92, rely=0.5, anchor="center")

        # Login Button
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            width=350,
            height=50,
            corner_radius=10,
            font=("Arial Bold", 18),
            command=self.handle_login
        )
        self.login_button.pack(pady=(40, 10))

        # Inline Error Message Label (Hidden by default)
        self.error_label = ctk.CTkLabel(
            self.login_frame,
            text="",
            font=("Arial", 13),
            text_color="#e74c3c" # Professional red color
        )
        self.error_label.pack(pady=(0, 10))

        # Register Link
        self.register_label = ctk.CTkLabel(
            self.login_frame,
            text="Don't have an account? Register",
            font=("Arial", 13),
            text_color=("blue", "#3498db"),
            cursor="hand2"
        )
        self.register_label.pack()
        self.register_label.bind("<Button-1>", lambda e: self.open_register())

        # Bind Enter Key to handle_login
        self.bind("<Return>", lambda e: self.handle_login())

    def open_register(self):
        RegisterView(self)

    def handle_login(self):
        # Clear any previous error
        self.error_label.configure(text="")

        # Strip leading/trailing whitespace to prevent login errors from accidental spaces
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.error_label.configure(text="Please enter both username and password.")
            return

        success, result = AuthController.login_user(username, password)
        if success:
            self.animate_transition()
        else:
            self.error_label.configure(text=result)

    def animate_transition(self):
        """Animates the login frame sliding out to the left slowly."""
        try:
            current_relx = float(self.login_frame.place_info().get('relx', 0.5))
            if current_relx > -0.5:
                # Move left (decrease relx) at a slower pace
                new_relx = current_relx - 0.015 
                self.login_frame.place(relx=new_relx)
                self.after(15, self.animate_transition)
            else:
                self.login_frame.place_forget()
                # Show the sidebar/dashboard while keeping background visible
                self.show_dashboard()
        except Exception as e:
            print(f"Animation error: {e}")

    def _clear_background(self):
        """Removes decorative background elements and icons."""
        self.bg_icon.place_forget()
        for element in self.bg_elements:
            element.place_forget()

    def show_dashboard(self):
        """Initializes and displays the Dashboard view."""
        if not self.dashboard:
            self.dashboard = DashboardView(self)
            self.dashboard.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    def toggle_password_visibility(self):
        if self.password_visible:
            self.password_entry.configure(show="*")
            self.eye_button.configure(text="👁️")
            self.password_visible = False
        else:
            self.password_entry.configure(show="")
            self.eye_button.configure(text="👓")
            self.password_visible = True

    def _create_background_elements(self):
        # Bubble configurations: (relx, rely, size)
        bubbles = [
            (0.10, -0.05, 120), (0.25, 0.05, 80), (0.45, -0.02, 150),
            (0.65, 0.08, 60), (0.85, -0.04, 100), (-0.02, 0.30, 90),
            (0.05, 0.55, 110), (-0.03, 0.80, 130),
        ]
        for x, y, size in bubbles:
            bubble = ctk.CTkFrame(self, width=size, height=size, corner_radius=size // 2,
                                  fg_color=("#f2f2f2", "#222222"), border_width=0)
            bubble.place(relx=x, rely=y, anchor="center")
            bubble.lower()
            self.bg_elements.append(bubble)

        stars = [
            (0.15, 0.20, 20), (0.80, 0.25, 15), (0.20, 0.70, 18),
            (0.90, 0.75, 22), (0.50, 0.15, 12), (0.35, 0.85, 16), (0.70, 0.60, 20),
        ]
        for x, y, size in stars:
            star = ctk.CTkLabel(self, text="⭐", font=("Arial", size),
                                text_color=("#e0e0e0", "#282828"))
            star.place(relx=x, rely=y, anchor="center")
            star.lower()
            self.bg_elements.append(star)


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
