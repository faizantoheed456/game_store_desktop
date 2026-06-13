import customtkinter as ctk
from src.database.game_queries import GameQueries
from src.database.image_manager import ImageManager
from src.views.game_detail_view import GameDetailView
from src.views.profile_view import ProfileView
from src.views.edit_profile_view import EditProfileView
from src.views.change_password_view import ChangePasswordView
from src.views.games_hub_view import GamesHubView
from PIL import Image
import webbrowser
import os
import threading

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, user_data=None, logout_callback=None):
        super().__init__(parent, fg_color="transparent")
        
        # State
        self.current_user = user_data
        self.on_logout = logout_callback
        self.search_timer = None
        self.current_view = "store"
        
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
        self.games_hub_btn = self._create_sidebar_button("✨  Have a fun!", self.show_games_hub)
        self.profile_btn = self._create_sidebar_button("👤  Profile", self.show_profile)

        # 2. Main Content Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # A. Persistent Header (Search Bar)
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
        
        # B. Scrollable Body
        self.body_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.body_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.body_container.grid_columnconfigure(0, weight=1)
        self.body_container.grid_rowconfigure(0, weight=1)

        self.show_store()

    def show_store(self, search_query=None):
        self.current_view = "store"
        self._update_btn_states(self.store_btn)
        self.header_frame.grid()
        
        self._clear_body()

        self.scrollable_frame = ctk.CTkScrollableFrame(self.body_container, fg_color="transparent")
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")

        if search_query:
            self.clear_search_btn.place(relx=0.98, rely=0.5, anchor="e")
            self._async_render_search(search_query)
        else:
            self.clear_search_btn.place_forget()
            self._async_render_default_store()

    def _async_render_search(self, query):
        ctk.CTkLabel(self.scrollable_frame, text=f"Results for '{query}'", font=("Arial Bold", 24)).pack(anchor="w", padx=20, pady=(0, 15))
        grid_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10)
        
        def fetch_and_render():
            results = GameQueries.search_games(query)
            self.after(0, lambda: self._render_game_grid(grid_frame, results))
        
        threading.Thread(target=fetch_and_render, daemon=True).start()

    def _async_render_default_store(self):
        categories = [
            ("Trending Now", lambda: GameQueries.get_trending_games(5)),
            ("Action & FPS", lambda: GameQueries.get_games_by_genre("FPS", 5)),
            ("Horror & Survival", lambda: GameQueries.get_games_by_genre("Horror", 5)),
            ("Strategy & Simulation", lambda: GameQueries.get_games_by_genre("Strategy", 5) + GameQueries.get_games_by_genre("Sim", 5)),
            ("Racing & Sports", lambda: GameQueries.get_games_by_genre("Racing", 5) + GameQueries.get_games_by_genre("Sports", 5)),
            ("Indie Gems", lambda: GameQueries.get_games_by_genre("Indie", 5))
        ]
        
        for title, query_fn in categories:
            self._add_category_row_async(title, query_fn)

    def _add_category_row_async(self, title, query_fn):
        row_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        row_container.pack(fill="x")
        
        def fetch_and_render():
            games = query_fn()
            if games:
                self.after(0, lambda: self._render_category_row(row_container, title, games))
        
        threading.Thread(target=fetch_and_render, daemon=True).start()

    def _render_category_row(self, container, title, games):
        ctk.CTkLabel(container, text=title, font=("Arial Bold", 24)).pack(anchor="w", padx=20, pady=(40, 15))
        grid_frame = ctk.CTkFrame(container, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10)
        self._render_game_grid(grid_frame, games[:5])

    def _render_game_grid(self, container, games):
        if not games:
            ctk.CTkLabel(container, text="No matches found.", font=("Arial", 16), text_color="gray").pack(pady=40)
            return

        for i, game in enumerate(games):
            self._create_game_card(container, game).grid(row=i // 5, column=i % 5, padx=8, pady=8, sticky="nsew")
        for i in range(5): container.grid_columnconfigure(i, weight=1)

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

        card.bind("<Button-1>", lambda e, g=game: self.show_game_detail(g))
        for widget in card.winfo_children():
            widget.bind("<Button-1>", lambda e, g=game: self.show_game_detail(g))
            
        return card

    def show_game_detail(self, game):
        self.current_view = "detail"
        self.header_frame.grid_remove()
        self._clear_body()
        detail_view = GameDetailView(self.body_container, game, user_data=self.current_user, on_back_callback=self.show_store)
        detail_view.grid(row=0, column=0, sticky="nsew")

    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.show_store()

    def _on_search_key(self, event):
        if self.search_timer:
            self.after_cancel(self.search_timer)
        query = self.search_entry.get().strip()
        self.search_timer = self.after(300, lambda: self.show_store(query if query else None))

    def show_library(self, filter_query=None):
        self.current_view = "library"
        self._update_btn_states(self.library_btn)
        self.header_frame.grid_remove()
        self._clear_body()
        
        lib_header = ctk.CTkFrame(self.body_container, fg_color="transparent")
        lib_header.grid(row=0, column=0, sticky="ew", padx=40, pady=(40, 0))
        lib_header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(lib_header, text="My Collection", font=("Arial Bold", 32)).grid(row=0, column=0, sticky="w")
        
        self.lib_search = ctk.CTkEntry(lib_header, placeholder_text="Search in collection...", width=300, height=40, corner_radius=20)
        self.lib_search.grid(row=0, column=1, sticky="e")
        if filter_query: self.lib_search.insert(0, filter_query)
        self.lib_search.bind("<KeyRelease>", self._on_library_search)

        self.lib_scrollable = ctk.CTkScrollableFrame(self.body_container, fg_color="transparent")
        self.lib_scrollable.grid(row=1, column=0, sticky="nsew")
        self.body_container.grid_rowconfigure(1, weight=1)
        
        if not self.current_user:
            ctk.CTkLabel(self.lib_scrollable, text="Please login to view your collection.", font=("Arial", 16)).pack(pady=40)
            return

        self._async_render_library(filter_query)

    def _on_library_search(self, event):
        query = self.lib_search.get().strip()
        for widget in self.lib_scrollable.winfo_children(): widget.destroy()
        self._async_render_library(query if query else None)

    def _async_render_library(self, query):
        user_id = self.current_user[0]
        def fetch_and_render():
            installed = GameQueries.get_user_installed(user_id)
            favorites = GameQueries.get_user_favorites(user_id)
            self.after(0, lambda: self._render_library_content(installed, favorites, query))
        threading.Thread(target=fetch_and_render, daemon=True).start()

    def _render_library_content(self, installed, favorites, query):
        def matches_query(game):
            if not query: return True
            q = query.lower()
            return q in game[1].lower() or q in game[2].lower() or q in game[7].lower()

        filtered_installed = [g for g in installed if matches_query(g)]
        if filtered_installed:
            ctk.CTkLabel(self.lib_scrollable, text="🖥 Installed on PC", font=("Arial Bold", 24)).pack(anchor="w", padx=40, pady=(30, 15))
            grid_installed = ctk.CTkFrame(self.lib_scrollable, fg_color="transparent")
            grid_installed.pack(fill="x", padx=30)
            self._render_game_grid(grid_installed, filtered_installed)

        filtered_favs = [g for g in favorites if matches_query(g)]
        if filtered_favs:
            ctk.CTkLabel(self.lib_scrollable, text="❤ My Wishlist", font=("Arial Bold", 24)).pack(anchor="w", padx=40, pady=(30, 15))
            grid_fav = ctk.CTkFrame(self.lib_scrollable, fg_color="transparent")
            grid_fav.pack(fill="x", padx=30)
            self._render_game_grid(grid_fav, filtered_favs)

        if not filtered_installed and not filtered_favs:
            text = f"No results found for '{query}'" if query else "Your collection is empty."
            ctk.CTkLabel(self.lib_scrollable, text=text, font=("Arial", 18), text_color="gray").pack(pady=100)

    def show_profile(self):
        self.current_view = "profile"
        self._update_btn_states(self.profile_btn)
        self.header_frame.grid_remove()
        self._clear_body()
        profile_view = ProfileView(self.body_container, self.current_user, logout_callback=self.on_logout, edit_callback=self.show_edit_profile, security_callback=self.show_change_password)
        profile_view.grid(row=0, column=0, sticky="nsew")

    def show_change_password(self):
        self._clear_body()
        password_view = ChangePasswordView(self.body_container, self.current_user, on_back_callback=self.show_profile)
        password_view.grid(row=0, column=0, sticky="nsew")

    def show_edit_profile(self):
        self._clear_body()
        edit_view = EditProfileView(self.body_container, self.current_user, on_save_callback=self.on_profile_updated, on_cancel_callback=self.show_profile)
        edit_view.grid(row=0, column=0, sticky="nsew")

    def on_profile_updated(self, updated_user):
        self.current_user = updated_user
        self.show_profile()

    def show_games_hub(self):
        self.current_view = "games_hub"
        self._update_btn_states(self.games_hub_btn)
        self.header_frame.grid_remove()
        self._clear_body()
        hub_view = GamesHubView(self.body_container)
        hub_view.grid(row=0, column=0, sticky="nsew")

    def _clear_body(self):
        for widget in self.body_container.winfo_children(): 
            widget.destroy()
        self.body_container.grid_rowconfigure(0, weight=1)
        self.body_container.grid_rowconfigure(1, weight=0)
        self.body_container.grid_columnconfigure(0, weight=1)

    def _create_sidebar_button(self, text, command):
        btn = ctk.CTkButton(self.sidebar_frame, text=text, height=50, corner_radius=10, fg_color="transparent", text_color=("gray20", "gray85"), hover_color=("#ebebeb", "#2b2b2b"), anchor="w", font=("Arial", 16), command=command)
        btn.pack(fill="x", padx=20, pady=5)
        return btn

    def _update_btn_states(self, active_btn):
        for btn in [self.store_btn, self.library_btn, self.games_hub_btn, self.profile_btn]:
            btn.configure(fg_color="transparent")
        active_btn.configure(fg_color=("#ebebeb", "#2b2b2b"))
