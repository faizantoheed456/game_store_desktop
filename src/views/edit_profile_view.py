import customtkinter as ctk
from src.database.queries import UserQueries
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps
import os
import shutil
import re
import hashlib
from datetime import datetime

class EditProfileView(ctk.CTkFrame):
    def __init__(self, parent, user_data, on_save_callback, on_cancel_callback):
        super().__init__(parent, fg_color="transparent")
        
        self.user = user_data
        self.on_save = on_save_callback
        self.on_cancel = on_cancel_callback
        self.profile_pic_path = self.user[6]
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Scrollable Container
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scroll_container.grid_columnconfigure(0, weight=1)

        # Inner Container
        self.container = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=20)
        self.container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.container, text="Edit Profile & Settings", font=("Arial Bold", 32)).pack(anchor="w", pady=(0, 40))

        # --- 1. Profile Picture Section ---
        ctk.CTkLabel(self.container, text="Profile Picture", font=("Arial Bold", 18)).pack(anchor="w", pady=(0, 15))
        self.pic_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.pic_frame.pack(fill="x", pady=(0, 30))
        
        self.avatar_preview = ctk.CTkLabel(
            self.pic_frame, text="👤", font=("Arial", 80),
            width=120, height=120, fg_color=("#ebebeb", "#2b2b2b"),
            corner_radius=60
        )
        self.avatar_preview.pack(side="left", padx=(0, 20))
        
        if self.profile_pic_path and os.path.exists(self.profile_pic_path):
            self._load_avatar_preview(self.profile_pic_path)

        self.btn_subframe = ctk.CTkFrame(self.pic_frame, fg_color="transparent")
        self.btn_subframe.pack(side="left")

        self.change_pic_btn = ctk.CTkButton(
            self.btn_subframe, text="Change Photo", width=120, height=35,
            command=self._choose_profile_pic
        )
        self.change_pic_btn.pack(pady=(0, 10))

        self.remove_pic_btn = ctk.CTkButton(
            self.btn_subframe, text="Remove Photo", width=120, height=35,
            fg_color="transparent", border_width=1, border_color="#e74c3c",
            text_color="#e74c3c", hover_color=("#fee", "#311"),
            command=self._remove_profile_pic
        )
        self.remove_pic_btn.pack()

        # --- 2. Personal Info ---
        ctk.CTkLabel(self.container, text="Bio", font=("Arial Bold", 18)).pack(anchor="w", pady=(10, 5))
        self.bio_text = ctk.CTkTextbox(self.container, height=100, corner_radius=10, border_width=1)
        self.bio_text.pack(fill="x", pady=(0, 20))
        if self.user[4]:
            self.bio_text.insert("1.0", self.user[4])

        ctk.CTkLabel(self.container, text="Birthday (YYYY-MM-DD)", font=("Arial Bold", 18)).pack(anchor="w", pady=(10, 5))
        self.birthday_entry = ctk.CTkEntry(self.container, height=45, corner_radius=10, placeholder_text="e.g. 1998-12-25")
        self.birthday_entry.pack(fill="x", pady=(0, 5))
        if self.user[5]:
            self.birthday_entry.insert(0, self.user[5])
        
        self.error_label = ctk.CTkLabel(self.container, text="", text_color="#e74c3c", font=("Arial", 12))
        self.error_label.pack(anchor="w", pady=(0, 20))

        # --- 3. App Settings (Theme) ---
        ctk.CTkLabel(self.container, text="App Appearance", font=("Arial Bold", 18)).pack(anchor="w", pady=(20, 15))
        self.theme_frame = ctk.CTkFrame(self.container, fg_color=("#f9f9f9", "#1a1a1a"), corner_radius=10, border_width=1)
        self.theme_frame.pack(fill="x", pady=(0, 40))
        
        self.theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
        
        themes = [("Dark Mode", "Dark"), ("Light Mode", "Light"), ("System Default", "System")]
        for i, (label, mode) in enumerate(themes):
            rb = ctk.CTkRadioButton(
                self.theme_frame, text=label, variable=self.theme_var, 
                value=mode, command=self._change_theme
            )
            rb.pack(side="left", padx=30, pady=20)

        # --- 4. Action Buttons ---
        self.actions_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.actions_frame.pack(fill="x", pady=(20, 40))

        self.save_btn = ctk.CTkButton(
            self.actions_frame, text="Save Changes", height=50, width=180,
            corner_radius=10, fg_color="#2ecc71", hover_color="#27ae60",
            font=("Arial Bold", 16), command=self._handle_save
        )
        self.save_btn.pack(side="left", padx=(0, 20))

        self.cancel_btn = ctk.CTkButton(
            self.actions_frame, text="Cancel", height=50, width=180,
            corner_radius=10, fg_color="transparent", border_width=2,
            border_color=("#dbdbdb", "#3b3b3b"), font=("Arial Bold", 16),
            command=self.on_cancel
        )
        self.cancel_btn.pack(side="left")

    def _change_theme(self):
        mode = self.theme_var.get()
        ctk.set_appearance_mode(mode)

    def _choose_profile_pic(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp")]
        )
        if file_path:
            os.makedirs("assets/profiles", exist_ok=True)
            ext = os.path.splitext(file_path)[1]
            new_filename = f"user_{self.user[0]}{ext}"
            dest_path = os.path.join("assets", "profiles", new_filename)
            shutil.copy(file_path, dest_path)
            self.profile_pic_path = dest_path
            self._load_avatar_preview(dest_path)

    def _remove_profile_pic(self):
        self.profile_pic_path = None
        self.avatar_preview.configure(text="👤", image="")

    def _load_avatar_preview(self, path):
        try:
            pil_img = Image.open(path)
            pil_img = ImageOps.fit(pil_img, (400, 400), Image.Resampling.LANCZOS)
            # Fix DPI warning by wrapping in CTkImage
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(120, 120))
            self.avatar_preview.configure(text="", image=ctk_img)
        except Exception as e:
            print(f"Error loading avatar preview: {e}")

    def _validate_date(self, date_str):
        if not date_str: return True # Optional field
        pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
        if not re.match(pattern, date_str):
            return False
            
        # Logical check
        try:
            birth_date = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.now()
            
            if birth_date > today:
                return "Birthday cannot be in the future!"
            if birth_date.year < 1900:
                return "Year is too far in the past!"
            return True
        except ValueError:
            return False

    def _handle_save(self):
        bio = self.bio_text.get("1.0", "end-1c").strip()
        birthday = self.birthday_entry.get().strip()
        
        validation_result = self._validate_date(birthday)
        if validation_result is not True:
            error_msg = validation_result if isinstance(validation_result, str) else "Invalid date format. Use YYYY-MM-DD"
            self.error_label.configure(text=error_msg)
            return
        
        self.error_label.configure(text="")
        
        if UserQueries.update_profile(self.user[0], bio, birthday, self.profile_pic_path):
            updated_user = UserQueries.get_user_by_id(self.user[0])
            self.on_save(updated_user)
        else:
            self.error_label.configure(text="Database error. Failed to update profile.")
