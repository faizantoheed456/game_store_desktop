# 🎮 GameVault — Desktop Digital Game Storefront

> A modern, dark-themed Python desktop application inspired by Steam. Features secure user authentication, a dynamic game catalog, and a fully decoupled MVC architecture.

---

## 👥 Team

| Role           | Name              |
|----------------|-------------------|
| **Group Leader** | M. Rohan Jabbar |
| **Developer**    | Faizan Toheed   |
| **Developer**    | Muhammad Usman        |

**Course:** Software Construction and Development  
**Repository:** [faizantoheed456/game_store_desktop](https://github.com/faizantoheed456/game_store_desktop)

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Proposed Solution](#-proposed-solution)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Recent Progress](#-recent-progress)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Database Setup](#-database-setup)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧩 Problem Statement

### 1. The Core Problem

Traditional desktop application development often suffers from **tight coupling** (spaghetti code), where the graphical user interface (GUI), business logic, and database interactions are tangled together. This makes the application difficult to scale, debug, and maintain.

Furthermore, many introductory database or desktop application projects rely on **outdated, unappealing user interfaces** (like vanilla Tkinter) that fail to replicate the user experience (UX) expected of modern digital platforms.

### 2. The Context & Scope

In the context of a **Digital Game Store** (a desktop-based Steam clone), a seamless user experience is critical. Gamers and administrators expect a highly responsive visual grid layout, immediate data rendering, and a secure gateway. Building this requires addressing three specific challenges:

- **🔐 Authentication Security** — Ensuring user credentials are encrypted, verified against a relational database management system (RDBMS), and session-managed without compromising application performance.
- **📦 Data Layer Separation** — Dynamically pulling large sets of relational data (game titles, genres, pricing, and assets) from a relational database and rendering them cleanly without freezing the user interface.
- **🏗️ Architectural Organization** — Working in a 3-member team requires a strict **Separation of Concerns** (MVC-like pattern) so multiple developers can work on the database layer, UI views, and controllers simultaneously without causing code conflicts.

---

## 💡 Proposed Solution

This project resolves these issues by developing a **modern, dark-themed Python desktop storefront application** using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) backed by a relational database system.

By enforcing a strict decoupled architecture:

- `views/` — All UI components and screen layouts
- `controllers/` — Business logic and event handling
- `database/` — SQL queries and database connection management

...the system provides a **scalable boilerplate** that brings modern UI aesthetics and professional software engineering principles to desktop-based game data management.

---

## ✨ Features

- 🔑 **Secure Login & Registration** — Password hashing (SHA-256) and credential validation.
- 📧 **Automated Email Notifications** — Automatic "Thank You" emails sent to new users via Gmail SMTP upon successful registration.
- ✅ **Gmail Validation** — Integrated validation to ensure only valid Gmail addresses are used during sign-up.
- 🗂️ **Dynamic Game Catalog** — Responsive grid layout populated from live database queries.
- 🎨 **Modern Dark UI** — Built with CustomTkinter for a Steam-like aesthetic with optimized background elements.
- 🗃️ **MVC Architecture** — Clean separation of views, controllers, and database layers.
- 👤 **User Session Management** — Persistent login sessions without performance overhead.
- 🛒 **Game Detail Views** — Title, genre, pricing, and asset display per game entry.

---

## 🛠️ Tech Stack

| Layer        | Technology                        |
|--------------|-----------------------------------|
| Language     | Python 3.10+                      |
| GUI Framework | CustomTkinter                    |
| Database     | SQLite / MySQL                    |
| Auth         | SHA-256 Hashing, Gmail SMTP       |
| Architecture | MVC (Model-View-Controller)       |
| Assets       | PNG/JPG images stored in `assets/` |

---

## 📈 Recent Progress

We have recently completed several critical milestones:

1. **UI Refinement:** Optimized the main login view, including resizing the background controller icon for better aesthetics and expanding the login frame to provide a more spacious, modern feel.
2. **Full Registration System:** Implemented a dedicated registration window with direct form inputs for Gmail, Username, and Password.
3. **Database Integration:** Set up the relational database layer with automated table creation and secure user data persistence.
4. **Email Automation:** Successfully integrated Gmail's SMTP service to send automated, professional welcome emails to new users upon registration.
5. **Security Updates:** Implemented SHA-256 password hashing to ensure user credentials are never stored in plain text.

---

## 🏛️ Architecture

The application follows a strict **MVC-like pattern** to ensure each team member could work independently on a separate layer:

```
┌─────────────────────────────────────┐
│           User Interface            │
│          (views/ — CTk Frames)      │
└──────────────┬──────────────────────┘
               │ Events / Callbacks
┌──────────────▼──────────────────────┐
│         Business Logic              │
│    (controllers/ — Python Classes)  │
└──────────────┬──────────────────────┘
               │ SQL Queries
┌──────────────▼──────────────────────┐
│          Data Layer                 │
│   (database/ — SQLite/MySQL)        │
└─────────────────────────────────────┘
```

---

## 📁 Project Structure

```
game_store_desktop/
│
├── main.py                  # Application entry point
│
├── src/
│   ├── views/               # All CustomTkinter UI screens
│   │   ├── main_view.py     # Main Login screen
│   │   ├── register_view.py # New Registration screen
│   │   ├── catalog_view.py
│   │   └── game_detail_view.py
│   │
│   ├── controllers/         # Business logic & event handling
│   │   ├── auth_controller.py # Login & Registration logic + Emailing
│   │   └── catalog_controller.py
│   │
│   └── database/            # Database connection & queries
│       ├── connection.py    # Database connection management
│       └── queries.py       # SQL query abstractions
│
├── assets/                  # Game cover images and UI assets
│   └── ...
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- Python **3.10** or higher
- `pip` package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/faizantoheed456/game_store_desktop.git
   cd game_store_desktop
   ```

2. **Install dependencies**
   ```bash
   pip install customtkinter Pillow
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

---

## 🗄️ Database Setup

The application automatically initializes the database schema upon the first run. For manual setup, use the following schema:

```sql
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT UNIQUE NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    password    TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS games (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    genre       TEXT,
    price       DECIMAL(10, 2) NOT NULL,
    description TEXT,
    cover_image TEXT,
    release_year INTEGER
);
```

---

## 📖 Usage

| Screen        | Description                                      |
|---------------|--------------------------------------------------|
| **Login**     | Authenticate with existing credentials           |
| **Register**  | Create a new account with Gmail and hashed password |
| **Catalog**   | Browse all available games in a responsive grid  |
| **Detail View** | View full game info: title, genre, price, and description |

---

## 🤝 Contributing

This project was built as a team academic submission. To contribute or extend it:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## ## 🚀 Latest Updates (June 11, 2026)

Today's development phase focused on transforming the storefront into a high-performance, visually authentic digital marketplace.

### 🎮 Advanced Storefront & Catalog
- **Massive Database Expansion:** Added 50+ legendary titles across 6 curated categories: *Trending, Action/FPS, Horror, Strategy/Sim, Racing/Sports,* and *Indie Gems*.
- **True Multi-Platform Support:** Diversified the catalog with official titles from **Epic Games, Riot Games, Battle.net, Rockstar,** and **Steam**.
- **Authentic Visuals:** Integrated official high-resolution Steam Store capsules and first-party CDN assets for 100% visual authenticity.
- **Interactive Discovery:** Every game card is clickable and opens the official game storefront directly in the user's web browser.

### ⚡ Performance & Engine Optimizations
- **High-Performance UI Refactor:** Implemented a persistent header/body architecture in `DashboardView` to eliminate input lag and UI hangs during searches.
- **Asynchronous Image Management:** Created a multithreaded `ImageManager` that fetches and caches assets in the background, keeping the main UI 100% responsive.
- **Intelligent Pre-loading:** The system now pre-fetches top category assets immediately upon login to ensure an instantaneous browsing experience.
- **Debounced Real-time Search:** Implemented a smart search engine that filters Title, Genre, and Platform as you type, with a 300ms throttle to optimize database load.

### 🛠️ UX & Workflow Refinements
- **Smooth Transition Engine:** Added a custom "Slide-to-Left" animation that elegantly moves the login interface off-screen to reveal the dashboard.
- **Robust Authentication:** 
    - Added automatic whitespace trimming for usernames.
    - Implemented **Enter Key** support for instant login.
    - Replaced disruptive popups with modern, inline red error messaging.
- **Asset Resilience:** Built a dual-CDN fallback system to handle DNS failures and ensure images always load correctly.

---

## 🛠️ Tech Stack
- **Frontend:** CustomTkinter (Python)
- **Database:** SQLite3
- **Logic:** Decoupled MVC Architecture
- **Networking:** Requests & Multithreading
- **Imaging:** PIL (Pillow)
- **Security:** SHA-256 Hashing & Google App Passwords

---

## 📦 Getting Started
1. **Configure Email:** Generate a Google App Password and update `src/controllers/auth_controller.py`.
2. **Run Application:** `python main.py`
3. **Register/Login:** Experience the smooth transition to the unified Game Store.
