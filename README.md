# 🎮 GameVault — Desktop Digital Game Storefront

> A high-performance, dark-themed Python desktop application inspired by Steam. Engineered with a decoupled MVC architecture and optimized for responsiveness with asynchronous background processing.

---

## 👥 The Development Team

| Role           | Name              | Contribution Focus |
|----------------|-------------------|--------------------|
| **Group Leader** | M. Rohan Jabbar | Project Management & Logic |
| **Developer**    | Faizan Toheed   | Architecture, UI & Performance |
| **Developer**    | M. Usman        | Database & Integration |

**Course:** Software Construction and Development (2026)  
**Repository:** [faizantoheed456/game_store_desktop](https://github.com/faizantoheed456/game_store_desktop)

---

## 🧩 Project Overview

GameVault is a modern solution to traditional desktop application challenges. It demonstrates how professional software engineering principles—like **Separation of Concerns**, **Asynchronous Programming**, and **Relational Data Management**—can be applied to create a seamless, high-end user experience using Python.

### 1. The Core Problem
Most desktop projects suffer from "UI Freeze" when performing heavy tasks (like loading images or querying databases). They often have tightly coupled code where changing the UI breaks the database logic.

### 2. Our Solution
GameVault solves this by using:
- **MVC Architecture:** Total separation between what the user sees and how data is handled.
- **Multithreading:** Heavy tasks (Email, DB queries, Image loading) never run on the main UI thread.
- **Modern UI:** CustomTkinter provides a professional, hardware-accelerated aesthetic.

---

## ✨ Features (The "Single Thing" Detailed List)

### 👤 User Experience
- **🔐 Secure Authentication:** Full Login/Registration system with SHA-256 password hashing.
- **📧 Welcome Emails:** Automated, non-blocking emails sent via Gmail SMTP upon registration.
- **🎨 Dynamic Catalog:** A beautiful, responsive grid of games with live pricing and ratings.
- **🔍 Advanced Search:** Instant filtering of hundreds of games by title, genre, or platform.
- **📚 Personal Library:** Track which games you own ("Installed") and which are on your "Wishlist".
- **🖼️ Profile Management:** Change your bio, birthday, and upload a custom profile picture with automatic center-cropping.

### 🕹️ Games Hub (10 Integrated Mini-Games)
A dedicated entertainment sector featuring:
1.  **Tic Tac Toe:** Classic 3x3 with Bot or Human modes.
2.  **Number Guesser:** High/Low logic puzzle.
3.  **Rock Paper Scissors:** Animated weapon selection vs AI.
4.  **Hangman:** Gaming-themed word discovery.
5.  **Memory Match:** Visual pattern recognition.
6.  **Monster Clicker:** An RPG-lite clicker with upgrades and level scaling.
7.  **Math Quiz:** Mental calculation speed test.
8.  **Typing Speed:** Real-time WPM and Accuracy tracker.
9.  **Simon Says:** Sequential color memory challenge.
10. **Vault Escape:** A story-driven choice adventure.

### 🛠️ Administrative Controls
A high-visibility "Command Center" for the admin (`admin` / `@jsj3q8p`):
- **👥 User Management:** View all registered users and delete inactive/malicious accounts.
- **🎮 Game Inventory:** Full database view of every game in the system.
- **🔄 Live Refresh:** Synchronize the database state with a single click.
- **🔍 High-Visibility UI:** Specialized 18pt font and 60px row height for effortless data auditing.

---

## 🛠️ Technical Stack

| Layer          | Technology                        | Purpose |
|----------------|-----------------------------------|---------|
| **Core**       | Python 3.10+                      | Primary Language |
| **UI**         | CustomTkinter                     | Modern, Scalable GUI |
| **Database**   | SQLite 3                          | Serverless, Relational Storage |
| **Images**     | PIL (Pillow)                      | Advanced Image Processing |
| **Network**    | Requests                          | Asynchronous Asset Fetching |
| **Concurrency**| ThreadPoolExecutor                | Preventing UI Hangs |

---

## 🏗️ Architecture & Performance

### The MVC Pattern
- **Models (`src/database/`)**: Pure data logic. Handles SQLite connections and SQL queries.
- **Views (`src/views/`)**: Pure UI. No database logic lives here; they only render data received from controllers.
- **Controllers (`src/controllers/`)**: The bridge. Manages authentication rules and business flow.

### Optimization Highlights
- **Async Image Manager:** Images are downloaded or loaded from disk in background threads. They appear with a "fade-in" effect once ready, never slowing down the scroll.
- **Thread-Safe UI:** Uses `master.after()` callbacks to ensure that background data updates the GUI only through safe channels.
- **SQLite Concurrency:** Configured with `check_same_thread=False` to allow background indexing while the user browses the store.

---

## 🗄️ Database Schema

The system automatically initializes `game_store.db` with three primary tables:

1.  **`users`**: Stores IDs, hashed passwords, bios, and profile metadata.
2.  **`games`**: Stores the global catalog (titles, URLs, genres, platforms).
3.  **`user_library`**: A junction table managing many-to-many relationships (Who owns what).

---

## 🚀 Getting Started

### Prerequisites
- Python installed on your machine.
- Pip (Python Package Manager).

### Installation
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/faizantoheed456/game_store_desktop.git
    cd game_store_desktop
    ```
2.  **Install Dependencies**
    ```bash
    pip install customtkinter Pillow requests
    ```
3.  **Launch the App**
    ```bash
    python main.py
    ```

---

## 📁 Project Structure

```text
game_store_desktop/
├── main.py                  # Entry Point
├── game_store.db            # SQLite Database
├── assets/                  # Local Assets & Profiles
└── src/
    ├── controllers/         # Auth & Business Logic
    ├── database/            # SQL Queries & Image Manager
    ├── games/               # Mini-Game Implementations
    └── views/               # UI Frames (Login, Dashboard, Admin)
```

---

## 📄 License & Academic Context
This project was developed for the **Software Construction and Development** course. All rights belong to the contributors. It is intended for educational demonstration of professional Python application architecture.

---
<div align="center">
  <sub>Built with ❤️ by the GameVault Team · 2026</sub>
</div>
