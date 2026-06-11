import customtkinter as ctk
from src.database.image_manager import ImageManager
from src.database.game_queries import GameQueries
from PIL import Image
import webbrowser

class GameDetailView(ctk.CTkFrame):
    def __init__(self, parent, game_data, user_data=None, on_back_callback=None):
        super().__init__(parent, fg_color="transparent")
        
        self.game = game_data
        self.user = user_data
        self.on_back = on_back_callback
        
        # Get Collection Status
        self.is_favorite = 0
        self.is_installed = 0
        if self.user:
            self.is_favorite, self.is_installed = GameQueries.get_collection_status(self.user[0], self.game[0])
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Scrollable Container
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scroll_container.grid_columnconfigure(0, weight=1)

        # --- 1. Header & Back Button ---
        self.header_nav = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.header_nav.pack(fill="x", pady=(0, 20))
        
        self.back_btn = ctk.CTkButton(
            self.header_nav, text="← Back to Store", width=120, height=35,
            corner_radius=20, fg_color=("#ebebeb", "#2b2b2b"),
            text_color=("gray20", "gray85"), hover_color=("#dbdbdb", "#3b3b3b"),
            command=self.on_back
        )
        self.back_btn.pack(side="left")

        # --- 2. Hero Section (Image + Quick Info) ---
        self.hero_frame = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.hero_frame.pack(fill="x")
        self.hero_frame.grid_columnconfigure(1, weight=1)

        # Game Image
        self.img_label = ctk.CTkLabel(
            self.hero_frame, text="⌛", width=460, height=215, 
            fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=15
        )
        self.img_label.grid(row=0, column=0, padx=(0, 30), sticky="nw")

        def update_image(ctk_img):
            if self.img_label.winfo_exists():
                self.img_label.configure(text="", image=ctk_img)

        # Use ImageManager to load
        local_name = self.game[5]
        remote_url = self.game[11]
        loaded_img = ImageManager.get_image(remote_url, local_name, callback=update_image)
        if loaded_img:
            self.img_label.configure(text="", image=loaded_img)

        # Quick Info (Right Side)
        self.info_frame = ctk.CTkFrame(self.hero_frame, fg_color="transparent")
        self.info_frame.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(self.info_frame, text=self.game[1], font=("Arial Bold", 36), anchor="w").pack(fill="x")
        
        # Rating & Genre
        meta_text = f"⭐ {self.game[8]}  •  {self.game[2]}  •  {self.game[6]}"
        ctk.CTkLabel(self.info_frame, text=meta_text, font=("Arial", 16), text_color="gray", anchor="w").pack(fill="x", pady=(5, 20))

        # Price
        price_val = "Free" if self.game[3] == 0 else f"${self.game[3]}"
        self.price_label = ctk.CTkLabel(
            self.info_frame, text=price_val, font=("Arial Bold", 28), 
            text_color="#2ecc71", anchor="w"
        )
        self.price_label.pack(fill="x", pady=(0, 20))

        # Buttons
        self.btn_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.btn_frame.pack(fill="x", side="bottom")

        # 1. Favorites Button (Wishlist)
        self.fav_btn = ctk.CTkButton(
            self.btn_frame, text="❤ Add to Wishlist", height=45, corner_radius=10,
            font=("Arial Bold", 14), command=self.toggle_favorite
        )
        self.fav_btn.pack(side="left", padx=(0, 10), expand=True, fill="x")

        # 2. Installed Button (PC)
        self.install_btn = ctk.CTkButton(
            self.btn_frame, text="🖥 Mark as Installed", height=45, corner_radius=10,
            font=("Arial Bold", 14), command=self.toggle_installed
        )
        self.install_btn.pack(side="left", padx=(0, 10), expand=True, fill="x")

        self._update_button_states()

        self.store_btn = ctk.CTkButton(
            self.btn_frame, text="🌐 Store", height=45, width=100, corner_radius=10,
            font=("Arial Bold", 14), fg_color="transparent", border_width=2,
            border_color=("#dbdbdb", "#3b3b3b"), command=lambda: webbrowser.open(self.game[10])
        )
        self.store_btn.pack(side="left")

        # --- 3. Description Section ---
        ctk.CTkLabel(self.scroll_container, text="About This Game", font=("Arial Bold", 22)).pack(anchor="w", pady=(40, 15))
        
        description = self.game[4] if self.game[4] else "No description available for this title."
        # If it's the short placeholder, let's make it look better
        if len(description) < 50:
            description = f"{description}\n\nExperience high-octane gameplay and immersive storytelling in this top-rated {self.game[2]} title. Available now on {self.game[7]}."

        self.desc_label = ctk.CTkLabel(
            self.scroll_container, text=description, font=("Arial", 15),
            wraplength=800, justify="left", anchor="w"
        )
        self.desc_label.pack(fill="x", padx=5)

        # Platform Info
        platform_frame = ctk.CTkFrame(self.scroll_container, fg_color=("#f9f9f9", "#151515"), corner_radius=10)
        platform_frame.pack(fill="x", pady=40, padx=5)
        
        ctk.CTkLabel(
            platform_frame, text=f"Platform: {self.game[7]}  |  Released: {self.game[6]}", 
            font=("Arial Italic", 13), text_color="gray"
        ).pack(pady=15)

    def toggle_favorite(self):
        if not self.user: return
        self.is_favorite = 1 if not self.is_favorite else 0
        GameQueries.update_collection_status(self.user[0], self.game[0], self.is_favorite, self.is_installed)
        self._update_button_states()

    def toggle_installed(self):
        if not self.user: return
        self.is_installed = 1 if not self.is_installed else 0
        GameQueries.update_collection_status(self.user[0], self.game[0], self.is_favorite, self.is_installed)
        self._update_button_states()

    def _update_button_states(self):
        # Update Favorite Button
        if self.is_favorite:
            self.fav_btn.configure(text="❤ In Wishlist", fg_color=("#f9f9f9", "#333333"), text_color=("#e74c3c", "#ff4757"))
        else:
            self.fav_btn.configure(text="❤ Add to Wishlist", fg_color="#3498db", text_color="white")

        # Update Installed Button
        if self.is_installed:
            self.install_btn.configure(text="🖥 Installed on PC", fg_color=("#2ecc71", "#27ae60"), text_color="white")
        else:
            self.install_btn.configure(text="🖥 Mark as Installed", fg_color=("#ebebeb", "#2b2b2b"), text_color=("gray20", "gray85"))
