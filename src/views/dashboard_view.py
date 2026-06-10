import customtkinter as ctk
from src.database.game_queries import GameQueries
from src.database.image_manager import ImageManager
from PIL import Image
import webbrowser
import os

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # State
        self.search_timer = None
        self.current_view = "store"
        
        # Add sample games and Pre-load images in background
        GameQueries.add_sample_games()
        all_games = GameQueries.get_trending_games(10) + GameQueries.get_games_by_genre("FPS")
        ImageManager.preload_images(all_games)

        # Layout: [Sidebar] [Content(Header + Body)]
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 1. Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(
            self, width=280, corner_radius=0, 
            fg_color=("#f9f9f9", "#151515"),
            border_width=1, border_color=("#dbdbdb", "#2b2b2b")
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="GameVault", font=("Arial Bold", 24))
        self.logo_label.pack(pady=(40, 40))

        self.store_btn = self._create_sidebar_button("🎮  Game Store", self.show_store)
        self.library_btn = self._create_sidebar_button("📚  My Library", self.show_library)
        self.profile_btn = self._create_sidebar_button("👤  Profile", self.show_profile)

        # 2. Main Content Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # A. Persistent Header (Search Bar) - Never destroyed during store browsing
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", height=80)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 0))
        self.header_frame.grid_propagate(False)
        
        self.search_entry = ctk.CTkEntry(
            self.header_frame, 
            placeholder_text="Search games, genres, or platforms...",
            height=50, corner_radius=25, border_width=2,
            font=("Arial", 15)
        )
        self.search_entry.pack(fill="x", side="left", expand=True)
        self.search_entry.bind("<KeyRelease>", self._on_search_key)

        self.clear_search_btn = ctk.CTkButton(
            self.header_frame, text="✕", width=40, height=40, 
            corner_radius=20, fg_color="transparent", 
            text_color="gray", hover_color=("#dbdbdb", "#2b2b2b"),
            command=self.clear_search
        )
        # Initially hidden
        
        # B. Scrollable Body
        self.body_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.body_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.body_container.grid_columnconfigure(0, weight=1)
        self.body_container.grid_rowconfigure(0, weight=1)

        self.show_store()

    def show_store(self, search_query=None):
        self.current_view = "store"
        self._update_btn_states(self.store_btn)
        self.header_frame.grid() # Ensure search is visible
        
        # Clear body only
        for widget in self.body_container.winfo_children():
            widget.destroy()

        scrollable_frame = ctk.CTkScrollableFrame(self.body_container, fg_color="transparent")
        scrollable_frame.grid(row=0, column=0, sticky="nsew")

        if search_query:
            self.clear_search_btn.place(relx=0.98, rely=0.5, anchor="e")
            self._render_search_results(scrollable_frame, search_query)
        else:
            self.clear_search_btn.place_forget()
            self._render_default_store(scrollable_frame)

    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.show_store()

    def _on_search_key(self, event):
        if self.search_timer:
            self.after_cancel(self.search_timer)
        
        query = self.search_entry.get().strip()
        self.search_timer = self.after(300, lambda: self.show_store(query if query else None))

    def _render_search_results(self, parent, query):
        ctk.CTkLabel(parent, text=f"Results for '{query}'", font=("Arial Bold", 24)).pack(anchor="w", padx=20, pady=(0, 15))
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10)
        
        results = GameQueries.search_games(query)
        if not results:
            ctk.CTkLabel(grid_frame, text="No matches found. Try 'FPS' or 'RPG'!", font=("Arial", 16), text_color="gray").pack(pady=40)
        else:
            for i, game in enumerate(results):
                self._create_game_card(grid_frame, game).grid(row=i // 5, column=i % 5, padx=8, pady=8, sticky="nsew")
            for i in range(5): grid_frame.grid_columnconfigure(i, weight=1)

    def _render_default_store(self, parent):
        # 1. Trending Now
        self._add_category_row(parent, "Trending Now", GameQueries.get_trending_games(5))

        # 2. Action & FPS
        self._add_category_row(parent, "Action & FPS", GameQueries.get_games_by_genre("FPS", 5))

        # 3. Horror & Survival
        self._add_category_row(parent, "Horror & Survival", GameQueries.get_games_by_genre("Horror", 5))

        # 4. Strategy & Simulation
        self._add_category_row(parent, "Strategy & Simulation", GameQueries.get_games_by_genre("Strategy", 5) + GameQueries.get_games_by_genre("Sim", 5))

        # 5. Racing & Sports
        self._add_category_row(parent, "Racing & Sports", GameQueries.get_games_by_genre("Racing", 5) + GameQueries.get_games_by_genre("Sports", 5))

        # 6. Indie Gems
        self._add_category_row(parent, "Indie Gems", GameQueries.get_games_by_genre("Indie", 5))

    def _add_category_row(self, parent, title, games):
        if not games: return
        
        ctk.CTkLabel(parent, text=title, font=("Arial Bold", 24)).pack(anchor="w", padx=20, pady=(40, 15))
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", padx=10)
        
        # Limit to 5 per row for clean grid
        for i, game in enumerate(games[:5]):
            self._create_game_card(row_frame, game).grid(row=0, column=i, padx=8, pady=8, sticky="nsew")
        for i in range(5): row_frame.grid_columnconfigure(i, weight=1)

    def _create_game_card(self, parent, game):
        card = ctk.CTkFrame(parent, height=320, corner_radius=15, border_width=1, border_color=("#dbdbdb", "#2b2b2b"), cursor="hand2")
        card.grid_propagate(False)
        
        local_name = game[5]
        remote_url = game[11]
        
        img_label = ctk.CTkLabel(card, text="⌛", font=("Arial", 40), height=160, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        img_label.pack(fill="x", padx=10, pady=10)
        
        def on_img_loaded(ctk_img):
            if img_label.winfo_exists():
                img_label.configure(text="", image=ctk_img)

        loaded_img = ImageManager.get_image(remote_url, local_name, callback=on_img_loaded)
        if loaded_img:
            img_label.configure(text="", image=loaded_img)

        ctk.CTkLabel(card, text=game[1], font=("Arial Bold", 15), anchor="w").pack(fill="x", padx=12)
        ctk.CTkLabel(card, text=game[7], font=("Arial", 11), text_color="gray", anchor="w").pack(fill="x", padx=12)
        
        price = "Free" if game[3] == 0 else f"${game[3]}"
        ctk.CTkLabel(card, text=price, font=("Arial Bold", 14), text_color="#2ecc71").pack(side="bottom", anchor="e", padx=12, pady=12)

        url = game[10]
        card.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
        return card

    def show_library(self):
        self.current_view = "library"
        self._update_btn_states(self.library_btn)
        self.header_frame.grid_remove() # Hide search in library
        for widget in self.body_container.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.body_container, text="My Collection", font=("Arial Bold", 32)).pack(pady=40)

    def show_profile(self):
        self.current_view = "profile"
        self._update_btn_states(self.profile_btn)
        self.header_frame.grid_remove() # Hide search in profile
        for widget in self.body_container.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.body_container, text="Account Settings", font=("Arial Bold", 32)).pack(pady=40)

    def _create_sidebar_button(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar_frame, text=text, height=50, corner_radius=10, 
            fg_color="transparent", text_color=("gray20", "gray85"),
            hover_color=("#ebebeb", "#2b2b2b"), anchor="w", font=("Arial", 16), command=command
        )
        btn.pack(fill="x", padx=20, pady=5)
        return btn

    def _update_btn_states(self, active_btn):
        for btn in [self.store_btn, self.library_btn, self.profile_btn]:
            btn.configure(fg_color="transparent")
        active_btn.configure(fg_color=("#ebebeb", "#2b2b2b"))
