# 🎮 GameVault — Desktop Digital Game Storefront

> A modern, dark-themed Python desktop application inspired by Steam. Features secure user authentication, a dynamic game catalog, and a fully decoupled MVC architecture backed by a high-performance SQLite database.

---

## 👥 Team

| Role           | Name              |
|----------------|-------------------|
| **Group Leader** | M. Rohan Jabbar |
| **Developer**    | Faizan Toheed   |
| **Developer**    | M. Usman        |

**Course:** Software Construction and Development  
**Repository:** [faizantoheed456/game_store_desktop](https://github.com/faizantoheed456/game_store_desktop)

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Proposed Solution](#-proposed-solution)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Performance Optimizations](#-performance-optimizations)
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
- **📦 Data Layer Separation** — Dynamically pulling large sets of relational data (game titles, genres, pricing, and assets) from a database and rendering them cleanly without freezing the user interface.
- **🏗️ Architectural Organization** — Working in a 3-member team requires a strict **Separation of Concerns** (MVC-like pattern) so multiple developers can work on the database layer, UI views, and controllers simultaneously without causing code conflicts.

---

## 💡 Proposed Solution

This project resolves these issues by developing a **modern, dark-themed Python desktop storefront application** using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) backed by a **SQLite database**.

By enforcing a strict decoupled architecture:

- `views/` — All UI components and screen layouts
- `controllers/` — Business logic and event handling
- `database/` — SQL queries and database connection management

...the system provides a **scalable boilerplate** that brings modern UI aesthetics and professional software engineering principles to desktop-based game data management.

---

## ✨ Features

- 🔑 **Secure Login & Registration** — Password hashing and credential validation.
- 📧 **Email Automation** — Automated welcome emails sent via Gmail SMTP on registration.
- 🗂️ **Dynamic Game Catalog** — Responsive grid layout with asynchronous image loading.
- 🎨 **Modern Dark UI** — Built with CustomTkinter for a Steam-like aesthetic.
- 🗃️ **MVC Architecture** — Clean separation of views, controllers, and database layers.
- 👤 **Personalized Profiles** — User bio, birthday, and profile picture management.
- 📚 **My Library** — Track wishlisted games and games marked as installed.
- ✨ **Games Hub** — Built-in mini-games (Tic Tac Toe, Hangman, etc.) for extra fun!
- 🔍 **Advanced Search** — Real-time filtering by title, genre, or platform.

---

## 🛠️ Tech Stack

| Layer        | Technology                        |
|--------------|-----------------------------------|
| Language     | Python 3.10+                      |
| GUI Framework | CustomTkinter                    |
| Database     | SQLite 3                          |
| Architecture | MVC (Model-View-Controller)       |
| Assets       | PIL (Pillow) for Image Handling   |

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
│   (database/ — SQLite Connection)   │
└─────────────────────────────────────┘
```

---

## ⚡ Performance Optimizations

To ensure a "lag-free" experience similar to modern digital storefronts, we implemented several key optimizations:

- **Asynchronous Image Manager** — Images are fetched, resized, and cached in background threads using a `ThreadPoolExecutor`. This prevents the UI from "stuttering" while loading game covers.
- **Background Database Tasks** — All SQL queries are offloaded to background threads. The UI remains responsive while data is being fetched.
- **Multi-threaded SQLite** — Enabled `check_same_thread=False` to allow concurrent data access across background tasks.
- **Smart Preloading** — Trending games and assets are pre-cached on application startup to ensure instant navigation.

---

## 📁 Project Structure

```
game_store_desktop/
│
├── main.py                  # Application entry point
│
├── src/
│   ├── views/               # CustomTkinter UI screens
│   ├── controllers/         # Business logic & authentication
│   ├── database/            # SQLite connection, queries, and image management
│   └── games/               # Mini-games for the Games Hub
│
├── assets/                  # Local game images and UI assets
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

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
   pip install customtkinter Pillow requests
   ```

3. **Run the application**
   ```bash
   python main.py
   ```
   *Note: On first run, the application automatically initializes the SQLite database and populates it with sample games.*

---

## 🗄️ Database Setup

The project uses **SQLite**, which is serverless. The database file (`game_store.db`) is automatically created and initialized by `src/database/connection.py`.

---

## 🤝 Contributing

This project was built as a team academic submission. To contribute or extend it:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is intended for academic and educational purposes. All rights belong to the respective contributors.

---

<div align="center">
  <sub>Built with ❤️ for Software Construction and Development · 2026</sub>
</div>