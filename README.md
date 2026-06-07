# 🎮 GameVault — Desktop Digital Game Storefront

> A modern, dark-themed Python desktop application inspired by Steam. Features secure user authentication, a dynamic game catalog, and a fully decoupled MVC architecture backed by a MySQL database.

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
- **📦 Data Layer Separation** — Dynamically pulling large sets of relational data (game titles, genres, pricing, and assets) from a MySQL database and rendering them cleanly without freezing the user interface.
- **🏗️ Architectural Organization** — Working in a 3-member team requires a strict **Separation of Concerns** (MVC-like pattern) so multiple developers can work on the database layer, UI views, and controllers simultaneously without causing code conflicts.

---

## 💡 Proposed Solution

This project resolves these issues by developing a **modern, dark-themed Python desktop storefront application** using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) backed by a **MySQL database**.

By enforcing a strict decoupled architecture:

- `views/` — All UI components and screen layouts
- `controllers/` — Business logic and event handling
- `database/` — SQL queries and database connection management

...the system provides a **scalable boilerplate** that brings modern UI aesthetics and professional software engineering principles to desktop-based game data management.

---

## ✨ Features

- 🔑 **Secure Login & Registration** — Password hashing and credential validation against MySQL
- 🗂️ **Dynamic Game Catalog** — Responsive grid layout populated from live database queries
- 🎨 **Modern Dark UI** — Built with CustomTkinter for a Steam-like aesthetic
- 🗃️ **MVC Architecture** — Clean separation of views, controllers, and database layers
- 👤 **User Session Management** — Persistent login sessions without performance overhead
- 🛒 **Game Detail Views** — Title, genre, pricing, and asset display per game entry
- 🔍 **Browsing & Filtering** — Navigate catalog by genre or search parameters

---

## 🛠️ Tech Stack

| Layer        | Technology                        |
|--------------|-----------------------------------|
| Language     | Python 3.10+                      |
| GUI Framework | CustomTkinter                    |
| Database     | MySQL (via `mysql-connector-python`) |
| Architecture | MVC (Model-View-Controller)       |
| Assets       | PNG/JPG images stored in `assets/` |

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
│   (database/ — MySQL Connector)     │
└─────────────────────────────────────┘
```

This architecture means:
- **UI changes** in `views/` never break database logic
- **Business rules** in `controllers/` remain independent of how data is stored or displayed
- **Database queries** in `database/` can be swapped or extended without touching the UI

---

## 📁 Project Structure

```
game_store_desktop/
│
├── main.py                  # Application entry point
│
├── src/
│   ├── views/               # All CustomTkinter UI screens
│   │   ├── login_view.py
│   │   ├── register_view.py
│   │   ├── catalog_view.py
│   │   └── game_detail_view.py
│   │
│   ├── controllers/         # Business logic & event handling
│   │   ├── auth_controller.py
│   │   └── catalog_controller.py
│   │
│   └── database/            # Database connection & queries
│       ├── connection.py
│       └── queries.py
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
- MySQL Server **8.0** or higher
- `pip` package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/faizantoheed456/game_store_desktop.git
   cd game_store_desktop
   ```

2. **Install dependencies**
   ```bash
   pip install customtkinter mysql-connector-python Pillow
   ```

3. **Configure the database connection**

   Open `src/database/connection.py` and update the credentials:
   ```python
   DB_CONFIG = {
       "host": "localhost",
       "user": "your_mysql_user",
       "password": "your_mysql_password",
       "database": "game_store_db"
   }
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

---

## 🗄️ Database Setup

Run the following SQL script to initialize the database schema:

```sql
CREATE DATABASE IF NOT EXISTS game_store_db;
USE game_store_db;

CREATE TABLE users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  UNIQUE NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,   -- store hashed passwords
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE games (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(100) NOT NULL,
    genre       VARCHAR(50),
    price       DECIMAL(10, 2) NOT NULL,
    description TEXT,
    cover_image VARCHAR(255),            -- relative path to assets/
    release_year YEAR
);
```

Populate the `games` table with sample data to see the catalog in action.

---

## 📖 Usage

| Screen        | Description                                      |
|---------------|--------------------------------------------------|
| **Login**     | Authenticate with existing credentials           |
| **Register**  | Create a new account with hashed password storage |
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

Please follow the existing MVC structure — new features should maintain the separation between `views/`, `controllers/`, and `database/`.

---

## 📄 License

This project is intended for academic and educational purposes. All rights belong to the respective contributors.

---

<div align="center">
  <sub>Built with ❤️ for Software Construction and Development · 2025</sub>
</div>