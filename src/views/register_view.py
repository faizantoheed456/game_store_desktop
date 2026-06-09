import customtkinter as ctk
from PIL import Image
import os
from src.controllers.auth_controller import AuthController
from tkinter import messagebox

class RegisterView(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Register - GameVault")
        self.geometry("600x750")
        self.attributes("-topmost", True)
        
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (600 // 2)
        y = (screen_height // 2) - (750 // 2)
        self.geometry(f"600x750+{x}+{y}")

        self.configure(fg_color=("#ffffff", "#1a1a1a"))

        # Main Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both", padx=40, pady=40)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_container,
            text="Create Account",
            font=("Arial Bold", 32),
            text_color=("black", "white")
        )
        self.title_label.pack(pady=(0, 10))

        self.subtitle_label = ctk.CTkLabel(
            self.main_container,
            text="Enter your details to join GameVault",
            font=("Arial", 14),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 30))

        # Registration Fields (Shown immediately)
        self.email_entry = self._create_entry("Valid Gmail Address")
        self.username_entry = self._create_entry("Username")
        self.password_entry = self._create_entry("Password", show="*")
        self.confirm_password_entry = self._create_entry("Confirm Password", show="*")

        self.submit_button = ctk.CTkButton(
            self.main_container,
            text="Complete Registration",
            width=350,
            height=50,
            corner_radius=10,
            font=("Arial Bold", 16),
            command=self.submit_registration
        )
        self.submit_button.pack(pady=30)

        # Footer
        self.login_link = ctk.CTkLabel(
            self.main_container,
            text="Already have an account? Login",
            font=("Arial", 13),
            text_color=("blue", "#3498db"),
            cursor="hand2"
        )
        self.login_link.pack(pady=10)
        self.login_link.bind("<Button-1>", lambda e: self.destroy())

    def _create_entry(self, placeholder, show=""):
        entry = ctk.CTkEntry(
            self.main_container,
            placeholder_text=placeholder,
            width=350,
            height=50,
            corner_radius=10,
            show=show
        )
        entry.pack(pady=10)
        return entry

    def submit_registration(self):
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not email.endswith("@gmail.com"):
            messagebox.showerror("Error", "Please enter a valid Gmail address!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        success, message = AuthController.register_user(username, email, password)
        if success:
            messagebox.showinfo("Success", message)
            self.destroy()
        else:
            messagebox.showerror("Error", message)

