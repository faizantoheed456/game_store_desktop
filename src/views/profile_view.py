import customtkinter as ctk
from src.database.game_queries import GameQueries
from PIL import Image, ImageOps
import os
import threading

class ProfileView(ctk.CTkFrame):
    def __init__(self, parent, user_data, logout_callback, edit_callback, security_callback):
        super().__init__(parent, fg_color="transparent")
        
        self.user = user_data
        self.on_logout = logout_callback
        self.on_edit = edit_callback
        self.on_security = security_callback
        
        # Initial Stats (Placeholder)
        self.stats = {"wishlist": 0, "installed": 0}
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Scrollable Container
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scroll_container.grid_columnconfigure(0, weight=1)

        # Inner Container for centered content
        self.container = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=20)
        self.container.grid_columnconfigure(0, weight=1)

        # --- 1. User Header ---
        self.header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 40))
        
        # Avatar
        self.avatar_label = ctk.CTkLabel(
            self.header_frame, text="👤", font=("Arial", 120),
            width=180, height=180, fg_color=("#ebebeb", "#2b2b2b"),
            corner_radius=90
        )
        self.avatar_label.pack(side="left", padx=(0, 30))
        
        # Load profile picture async
        if self.user[6] and os.path.exists(self.user[6]):
            threading.Thread(target=self._load_avatar_async, daemon=True).start()

        self.user_info = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.user_info.pack(side="left", fill="y")
        
        ctk.CTkLabel(
            self.user_info, text=self.user[1], # Username
            font=("Arial Bold", 48), anchor="w"
        ).pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(
            self.user_info, text=self.user[2], # Email
            font=("Arial", 18), text_color="gray", anchor="w"
        ).pack(fill="x")
        
        # Birthday Display
        if self.user[5]:
            ctk.CTkLabel(
                self.user_info, text=f"🎂 Birthday: {self.user[5]}",
                font=("Arial", 14), text_color="gray", anchor="w"
            ).pack(fill="x", pady=(5, 0))
        
        ctk.CTkLabel(
            self.user_info, text=f"📅 Member since: {self.user[7][:10]}", # created_at
            font=("Arial Italic", 14), text_color="gray", anchor="w"
        ).pack(fill="x", pady=(5, 0))

        # --- Bio Section ---
        if self.user[4]:
            ctk.CTkLabel(self.container, text="About Me", font=("Arial Bold", 20)).pack(anchor="w", pady=(20, 10))
            bio_box = ctk.CTkTextbox(self.container, height=100, fg_color=("#f9f9f9", "#1a1a1a"), font=("Arial", 15), border_width=1)
            bio_box.pack(fill="x")
            bio_box.insert("1.0", self.user[4])
            bio_box.configure(state="disabled")

        # --- 2. Stats Grid ---
        ctk.CTkLabel(self.container, text="Collection Overview", font=("Arial Bold", 24)).pack(anchor="w", pady=(40, 20))
        
        self.stats_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.stats_frame.pack(fill="x")
        self.stats_frame.grid_columnconfigure((0, 1), weight=1)

        self.wishlist_card = self._create_stat_card(self.stats_frame, "Games in Wishlist", "0", "❤", 0)
        self.installed_card = self._create_stat_card(self.stats_frame, "Installed on PC", "0", "🖥", 1)

        # Load Stats Async
        threading.Thread(target=self._load_stats_async, daemon=True).start()

        # --- 3. Account Actions ---
        ctk.CTkLabel(self.container, text="Account Actions", font=("Arial Bold", 24)).pack(anchor="w", pady=(60, 20))
        
        self.actions_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.actions_frame.pack(fill="x", pady=(0, 40))

        self.logout_btn = ctk.CTkButton(
            self.actions_frame, text="Logout Session", height=50, width=200,
            corner_radius=10, fg_color="#e74c3c", hover_color="#c0392b",
            font=("Arial Bold", 16), command=self.on_logout
        )
        self.logout_btn.pack(side="left")

        self.edit_btn = ctk.CTkButton(
            self.actions_frame, text="Edit Profile", height=50, width=200,
            corner_radius=10, fg_color="transparent", border_width=2,
            border_color=("#dbdbdb", "#3b3b3b"), font=("Arial Bold", 16),
            command=self.on_edit
        )
        self.edit_btn.pack(side="left", padx=20)

        self.security_btn = ctk.CTkButton(
            self.actions_frame, text="Security Settings", height=50, width=200,
            corner_radius=10, fg_color="transparent", border_width=2,
            border_color=("#dbdbdb", "#3b3b3b"), font=("Arial Bold", 16),
            command=self.on_security
        )
        self.security_btn.pack(side="left")

    def _load_avatar_async(self):
        try:
            pil_img = Image.open(self.user[6])
            pil_img = ImageOps.fit(pil_img, (400, 400), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(180, 180))
            self.after(0, lambda: self.avatar_label.configure(text="", image=ctk_img))
        except Exception as e:
            print(f"Error loading profile picture: {e}")

    def _load_stats_async(self):
        self.stats = GameQueries.get_user_stats(self.user[0])
        self.after(0, self._update_stats_display)

    def _update_stats_display(self):
        # Update labels within cards (we need references)
        self.wishlist_val_label.configure(text=str(self.stats["wishlist"]))
        self.installed_val_label.configure(text=str(self.stats["installed"]))

    def _create_stat_card(self, parent, title, value, icon, col):
        card = ctk.CTkFrame(
            parent, height=150, corner_radius=20,
            fg_color=("#f9f9f9", "#151515"),
            border_width=1, border_color=("#dbdbdb", "#2b2b2b")
        )
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        card.grid_propagate(False)
        
        ctk.CTkLabel(card, text=icon, font=("Arial", 40)).pack(pady=(20, 5))
        val_label = ctk.CTkLabel(card, text=value, font=("Arial Bold", 32))
        val_label.pack()
        ctk.CTkLabel(card, text=title, font=("Arial", 14), text_color="gray").pack()
        
        # Save reference for async update
        if col == 0: self.wishlist_val_label = val_label
        else: self.installed_val_label = val_label
        
        return card
