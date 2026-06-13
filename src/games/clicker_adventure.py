import customtkinter as ctk
import random

class ClickerAdventure(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="transparent")
        self.on_back = on_back
        self.gold = 0
        self.power = 1
        self.monster_hp = 10
        self.monster_max_hp = 10
        self.level = 1
        
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=20)
        ctk.CTkButton(header, text="← Back", width=80, command=self.on_back).pack(side="left")
        
        ctk.CTkLabel(self, text="Monster Clicker Quest", font=("Arial Bold", 36)).pack(pady=20)

        self.stats_label = ctk.CTkLabel(self, text=f"Level: {self.level}  |  Gold: {self.gold}  |  Power: {self.power}", font=("Arial", 18))
        self.stats_label.pack(pady=10)

        # Monster UI
        self.monster_frame = ctk.CTkFrame(self, fg_color=("#f9f9f9", "#1a1a1a"), corner_radius=20, border_width=2)
        self.monster_frame.pack(pady=40, padx=100, fill="x")
        
        self.monster_icon = ctk.CTkLabel(self.monster_frame, text="👾", font=("Arial", 120))
        self.monster_icon.pack(pady=40)

        self.hp_bar = ctk.CTkProgressBar(self.monster_frame, width=400)
        self.hp_bar.set(1.0)
        self.hp_bar.pack(pady=20)

        self.hp_label = ctk.CTkLabel(self.monster_frame, text=f"HP: {self.monster_hp} / {self.monster_max_hp}", font=("Arial Bold", 16))
        self.hp_label.pack(pady=(0, 20))

        self.click_btn = ctk.CTkButton(self, text="ATTACK!", height=60, width=200, font=("Arial Bold", 24), command=self._attack)
        self.click_btn.pack(pady=20)

        # Upgrade
        self.upgrade_btn = ctk.CTkButton(
            self, text=f"Upgrade Power (Cost: 10 Gold)", 
            command=self._upgrade, fg_color="#e67e22"
        )
        self.upgrade_btn.pack(pady=20)

    def _attack(self):
        # Crit chance
        is_crit = random.random() < 0.1
        damage = self.power * 3 if is_crit else self.power
        
        self.monster_hp -= damage
        
        msg = f"CRITICAL HIT! -{damage}" if is_crit else f"-{damage}"
        color = "#f1c40f" if is_crit else "#e74c3c"
        self.hp_label.configure(text=msg, text_color=color)
        
        if self.monster_hp <= 0:
            self.gold += self.level * 2
            self.level += 1
            self.monster_max_hp = int(10 * (1.5 ** (self.level - 1)))
            self.monster_hp = self.monster_max_hp
            self._spawn_monster()
            self.hp_label.configure(text=f"DEFEATED! Level {self.level}", text_color="#2ecc71")
            
        self.after(500, self._update_ui)

    def _update_ui(self):
        self.stats_label.configure(text=f"Level: {self.level}  |  Gold: {self.gold}  |  Power: {self.power}")
        self.hp_label.configure(text=f"HP: {max(0, self.monster_hp)} / {self.monster_max_hp}", text_color="white")
        self.hp_bar.set(max(0, self.monster_hp) / self.monster_max_hp)
        self.upgrade_btn.configure(text=f"Upgrade Power (Cost: {self.power * 10} Gold)")

    def _upgrade(self):
        cost = self.power * 10
        if self.gold >= cost:
            self.gold -= cost
            self.power += 1
            self._update_ui()
        else:
            self.hp_label.configure(text="NOT ENOUGH GOLD!", text_color="#e74c3c")

    def _spawn_monster(self):
        icons = ["👾", "👹", "🤡", "🐉", "🕷️", "🧟"]
        self.monster_icon.configure(text=random.choice(icons))
