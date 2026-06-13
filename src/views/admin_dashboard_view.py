import customtkinter as ctk
from src.database.queries import UserQueries
from src.database.game_queries import GameQueries
from tkinter import ttk

class AdminDashboardView(ctk.CTkFrame):
    def __init__(self, parent, logout_callback=None):
        super().__init__(parent, fg_color="transparent")
        
        self.on_logout = logout_callback
        
        # Layout: Sidebar and Main Area
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="Admin Panel", font=("Arial Bold", 20))
        self.logo.pack(pady=30)
        
        self.users_btn = ctk.CTkButton(self.sidebar, text="Registered Users", command=self.show_users)
        self.users_btn.pack(pady=10, padx=20)
        
        self.games_btn = ctk.CTkButton(self.sidebar, text="Games Database", command=self.show_games)
        self.games_btn.pack(pady=10, padx=20)
        
        self.logout_btn = ctk.CTkButton(self.sidebar, text="Logout", fg_color="#e74c3c", hover_color="#c0392b", command=self.on_logout)
        self.logout_btn.pack(side="bottom", pady=20, padx=20)
        
        # Main Area
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(self.main_area, text="Welcome, Admin", font=("Arial Bold", 24))
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        # Default view
        self.show_users()

    def _clear_main(self):
        for widget in self.main_area.winfo_children():
            if widget != self.title_label:
                widget.destroy()

    def show_users(self):
        self._clear_main()
        self.title_label.configure(text="Registered Users")
        
        users = UserQueries.get_all_users()
        
        # Create Treeview for users
        columns = ("ID", "Username", "Email", "Created At")
        tree = ttk.Treeview(self.main_area, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
            
        for user in users:
            tree.insert("", "end", values=user)
            
        tree.grid(row=1, column=0, sticky="nsew")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_area, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

    def show_games(self):
        self._clear_main()
        self.title_label.configure(text="Games Database")
        
        games = GameQueries.get_all_games()
        
        # Create Treeview for games
        columns = ("ID", "Title", "Genre", "Price", "Year", "Platform", "Rating")
        tree = ttk.Treeview(self.main_area, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        for game in games:
            # game: (id, title, genre, price, description, cover_image, release_year, platform, rating, ...)
            display_vals = (game[0], game[1], game[2], f"${game[3]}", game[6], game[7], game[8])
            tree.insert("", "end", values=display_vals)
            
        tree.grid(row=1, column=0, sticky="nsew")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_area, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")
