import customtkinter as ctk
from src.database.queries import UserQueries
from src.database.game_queries import GameQueries
from tkinter import ttk, messagebox

class AdminDashboardView(ctk.CTkFrame):
    def __init__(self, parent, logout_callback=None):
        super().__init__(parent, fg_color="transparent")
        
        self.on_logout = logout_callback
        self.current_tab = "users"
        
        # Configure Style for Treeview
        self.style = ttk.Style()
        self.style.theme_use("clam") # 'clam' is more flexible for custom colors
        
        # Configure the Treeview colors and fonts
        self.style.configure("Treeview", 
            background="#2b2b2b", 
            foreground="white", 
            fieldbackground="#2b2b2b",
            font=("Arial", 18), # Drastically increased
            rowheight=60 # Much taller rows
        )
        self.style.configure("Treeview.Heading", 
            font=("Arial Bold", 22), # Drastically increased
            background="#1f1f1f",
            foreground="white"
        )
        self.style.map("Treeview", background=[('selected', '#1f538d')])
        
        # Layout: Sidebar and Main Area
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 1. Sidebar
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        self.logo = ctk.CTkLabel(self.sidebar, text="ADMIN PANEL", font=("Arial Bold", 28), text_color="#3498db")
        self.logo.pack(pady=50)
        
        self.users_btn = self._create_sidebar_btn("👥  Registered Users", self.show_users)
        self.games_btn = self._create_sidebar_btn("🎮  Games Database", self.show_games)
        
        self.logout_btn = ctk.CTkButton(
            self.sidebar, text="🚪  Logout Session", height=50, font=("Arial Bold", 16),
            fg_color="#e74c3c", hover_color="#c0392b", command=self.on_logout
        )
        self.logout_btn.pack(side="bottom", pady=30, padx=20, fill="x")
        
        # 2. Main Area
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)
        
        # Header with Title and Actions
        self.header_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.header_frame, text="Management", font=("Arial Bold", 32))
        self.title_label.grid(row=0, column=0, sticky="w")
        
        self.action_btn = ctk.CTkButton(
            self.header_frame, text="Delete Selected", fg_color="#e74c3c", 
            hover_color="#c0392b", width=150, height=40, font=("Arial Bold", 14),
            command=self._delete_selected
        )
        self.action_btn.grid(row=0, column=1, padx=10)

        self.refresh_btn = ctk.CTkButton(
            self.header_frame, text="🔄 Refresh", width=100, height=40, 
            font=("Arial Bold", 14), command=self._refresh
        )
        self.refresh_btn.grid(row=0, column=2)
        
        # Default view
        self.show_users()
        self.update() # Force layout calculation for scaling

    def _create_sidebar_btn(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar, text=text, height=60, font=("Arial", 18), 
            anchor="w", fg_color="transparent", text_color=("gray20", "gray85"),
            hover_color=("#ebebeb", "#2b2b2b"), command=command
        )
        btn.pack(pady=5, padx=20, fill="x")
        return btn

    def _clear_main(self):
        if hasattr(self, 'tree'):
            self.tree.destroy()
        if hasattr(self, 'scrollbar'):
            self.scrollbar.destroy()

    def show_users(self):
        self._clear_main()
        self.current_tab = "users"
        self.title_label.configure(text="Registered Users")
        self.users_btn.configure(fg_color=("#ebebeb", "#2b2b2b"))
        self.games_btn.configure(fg_color="transparent")
        
        users = UserQueries.get_all_users()
        
        columns = ("ID", "Username", "Email", "Created At")
        self.tree = ttk.Treeview(self.main_area, columns=columns, show="headings", style="Treeview")
        
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=80, anchor="center")
        self.tree.heading("Username", text="Username")
        self.tree.column("Username", width=250, anchor="w")
        self.tree.heading("Email", text="Email Address")
        self.tree.column("Email", width=400, anchor="w")
        self.tree.heading("Created At", text="Registration Date")
        self.tree.column("Created At", width=250, anchor="center")
            
        for user in users:
            self.tree.insert("", "end", values=user)
            
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.scrollbar = ttk.Scrollbar(self.main_area, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky="ns")

    def show_games(self):
        self._clear_main()
        self.current_tab = "games"
        self.title_label.configure(text="Games Database")
        self.games_btn.configure(fg_color=("#ebebeb", "#2b2b2b"))
        self.users_btn.configure(fg_color="transparent")
        
        games = GameQueries.get_all_games()
        
        columns = ("ID", "Title", "Genre", "Price", "Year", "Platform", "Rating")
        self.tree = ttk.Treeview(self.main_area, columns=columns, show="headings", style="Treeview")
        
        col_configs = {
            "ID": (80, "center"),
            "Title": (350, "w"),
            "Genre": (180, "w"),
            "Price": (100, "center"),
            "Year": (100, "center"),
            "Platform": (180, "w"),
            "Rating": (100, "center")
        }
        
        for col, config in col_configs.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=config[0], anchor=config[1])
            
        for game in games:
            display_vals = (game[0], game[1], game[2], f"${game[3]}", game[6], game[7], f"⭐ {game[8]}")
            self.tree.insert("", "end", values=display_vals)
            
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.scrollbar = ttk.Scrollbar(self.main_area, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky="ns")

    def _refresh(self):
        if self.current_tab == "users": self.show_users()
        else: self.show_games()

    def _delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select an item to delete.")
            return
        
        item_vals = self.tree.item(selected[0])['values']
        item_id = item_vals[0]
        
        if self.current_tab == "users":
            if item_id == 1: # Protect admin
                messagebox.showerror("Error", "The main admin account cannot be deleted.")
                return
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{item_vals[1]}'?"):
                if UserQueries.delete_user(item_id):
                    messagebox.showinfo("Success", "User deleted successfully.")
                    self.show_users()
        else:
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete game '{item_vals[1]}'?"):
                if GameQueries.delete_game(item_id):
                    messagebox.showinfo("Success", "Game deleted successfully.")
                    self.show_games()
