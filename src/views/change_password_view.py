import customtkinter as ctk
from src.database.queries import UserQueries
from tkinter import messagebox
import hashlib

class ChangePasswordView(ctk.CTkFrame):
    def __init__(self, parent, user_data, on_back_callback):
        super().__init__(parent, fg_color="transparent")
        
        self.user = user_data
        self.on_back = on_back_callback
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Scrollable Container (Consistent with other views)
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scroll_container.grid_columnconfigure(0, weight=1)

        # Inner Container
        self.container = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=20)
        self.container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.container, text="Security & Password", font=("Arial Bold", 32)).pack(anchor="w", pady=(0, 40))

        # --- Password Change Section ---
        self.pass_frame = ctk.CTkFrame(self.container, fg_color=("#f9f9f9", "#1a1a1a"), corner_radius=15, border_width=1)
        self.pass_frame.pack(fill="x", pady=(0, 30))
        
        inner_pass = ctk.CTkFrame(self.pass_frame, fg_color="transparent")
        inner_pass.pack(padx=30, pady=30, fill="x")

        ctk.CTkLabel(inner_pass, text="Update your login credentials", font=("Arial", 14), text_color="gray").pack(anchor="w", pady=(0, 20))

        self.old_pass = ctk.CTkEntry(inner_pass, placeholder_text="Current Password", show="*", height=50, corner_radius=10)
        self.old_pass.pack(fill="x", pady=10)
        
        self.new_pass = ctk.CTkEntry(inner_pass, placeholder_text="New Password", show="*", height=50, corner_radius=10)
        self.new_pass.pack(fill="x", pady=10)

        self.confirm_pass = ctk.CTkEntry(inner_pass, placeholder_text="Confirm New Password", show="*", height=50, corner_radius=10)
        self.confirm_pass.pack(fill="x", pady=10)

        self.update_pass_btn = ctk.CTkButton(
            inner_pass, text="Confirm Password Change", height=50,
            fg_color="#3498db", hover_color="#2980b9", font=("Arial Bold", 16),
            command=self._handle_password_change
        )
        self.update_pass_btn.pack(pady=(20, 0), fill="x")

        # --- Footer Actions ---
        self.back_btn = ctk.CTkButton(
            self.container, text="← Back to Profile", width=150, height=40,
            fg_color="transparent", border_width=1, border_color=("#dbdbdb", "#3b3b3b"),
            command=self.on_back
        )
        self.back_btn.pack(pady=20, anchor="w")

    def _handle_password_change(self):
        old = self.old_pass.get()
        new = self.new_pass.get()
        confirm = self.confirm_pass.get()

        if not old or not new or not confirm:
            messagebox.showerror("Error", "Please fill all password fields.")
            return

        # Check current password (user[3] is password)
        old_hashed = hashlib.sha256(old.encode()).hexdigest()
        if old_hashed != self.user[3]:
            messagebox.showerror("Error", "Current password is incorrect.")
            return

        if new != confirm:
            messagebox.showerror("Error", "New passwords do not match.")
            return
        
        if len(new) < 6:
            messagebox.showerror("Error", "New password must be at least 6 characters long.")
            return

        new_hashed = hashlib.sha256(new.encode()).hexdigest()
        if UserQueries.update_password(self.user[0], new_hashed):
            # Update parent user data via a sneaky way or just force re-login? 
            # Better to show success and go back.
            messagebox.showinfo("Success", "Password updated successfully.")
            self.on_back()
        else:
            messagebox.showerror("Error", "Failed to update password.")
