# 🎮 GameVault — Desktop Digital Game Storefront

> A modern, dark-themed Python desktop application inspired by Steam. Features secure user authentication, a dynamic game catalog, a personalized collection system, and a built-in interactive Games Hub.

---

## ✨ Key Features

### 🛒 Digital Storefront
- **Dynamic Catalog**: Browse 50+ games categorized by genre (FPS, RPG, Indie, etc.).
- **Smart Search**: Real-time filtering by title, platform, or genre.
- **Detailed Game Views**: High-res covers, immersive descriptions, and direct links to official stores.
- **Asynchronous Assets**: Multithreaded image downloading and caching for a buttery-smooth UI.

### 📚 Collection Management
- **Dual Tracking**: Separate your "Wishlist" from games actually "Installed on PC".
- **Local Library Search**: Quickly filter through your personal collection.
- **Persistence**: All collection data is saved securely in a local SQLite database.

### ✨ Games Hub ("Have a fun!")
A built-in suite of 10 interactive games to play directly within the app:
1.  **Tic Tac Toe**: vs Bot or Local Friend.
2.  **Number Guesser**: Logical deduction challenge.
3.  **Rock Paper Scissors**: Battle for luck.
4.  **Hangman**: Gaming-themed word puzzles.
5.  **Memory Match**: Concentration training with gaming icons.
6.  **Monster Clicker**: RPG-lite progression with critical hits.
7.  **Math Quiz**: Mental calculation speed test.
8.  **Typing Speed**: Real-time WPM and accuracy tracker.
9.  **Simon Says**: Color-pattern memory challenge.
10. **Vault Escape**: A text-based choice adventure story.

### 👤 User Personalization
- **Custom Profiles**: Upload and center-crop avatars, write a bio, and set your birthday.
- **Security**: Dedicated "Security Settings" for hashed password management.
- **App Themes**: Switch between Dark Mode, Light Mode, or System Default on the fly.
- **Statistics**: Visual overview of your gaming collection and history.

---

## 🏗️ Architecture (MVC)

- **`src/views/`**: Decoupled UI components built with `CustomTkinter`.
- **`src/controllers/`**: Business logic, authentication, and session management.
- **`src/database/`**: Singleton connection handling and complex SQL queries.
- **`src/games/`**: Modular built-in game implementations.

---

## 🚀 Getting Started

1. **Install Dependencies:**
   ```bash
   pip install customtkinter pillow requests
   ```
2. **Configure Email (Optional):** Update `src/controllers/auth_controller.py` with your SMTP details for registration emails.
3. **Run Application:**
   ```bash
   python main.py
   ```

---

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **GUI**: CustomTkinter & Pillow (PIL)
- **Database**: SQLite3
- **Networking**: Requests
- **Security**: SHA-256 Hashing
