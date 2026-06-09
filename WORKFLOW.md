# 🚀 GameVault — Project Workflow

This document tracks our development progress and outlines the task distribution for the team.

---

## ✅ Completed So Far (Phase 1: Foundation)
- [x] **Project Structure**: Established the MVC directory layout (`src/views`, `src/controllers`, `src/database`).
- [x] **Core Entry Point**: Created `main.py` to launch the application.
- [x] **Initial UI Background**: 
    - Fullscreen CustomTkinter window.
    - Theme Toggle (Light/Dark mode) with circular border icons.
    - Subtle background decorative elements (400pt Controller icon, varied Bubbles, and scattered Stars).
- [x] **Version Control**: Set up `.gitignore` and pushed the foundation to GitHub.

---

## 🛠️ Current Work Distribution (Today's Tasks)

### 👑 Rohan (Group Leader) — Database & Logic Layer
**Objective:** Setup the MySQL foundation so the UI can actually save and load data.
1. **Database Setup**: Run the SQL scripts from `README.md` to create the `game_store_db`.
2. **Connection Class**: Create `src/database/connection.py` to handle the MySQL connection using `mysql-connector-python`.
3. **Query Interface**: Implement `src/database/queries.py` with basic functions like `validate_user(username, password)` and `register_user(data)`.

### 🎨 Faizan (Developer) — UI Refinement
**Objective:** Design the interactive foreground elements on top of the background.
1. **Login Interface**: Create the Login Modal (Centered frame with Entry fields for Username/Password).
2. **Branding**: Add the "GameVault" title and logo in the top-left or center.
3. **Transition Logic**: Link the Login button to a placeholder function that will eventually call the controller.

### ⚙️ Usman (Developer) — Controller & Session Management
**Objective:** Bridge the gap between the UI (Faizan) and the Database (Rohan).
1. **Auth Controller**: Create `src/controllers/auth_controller.py`.
2. **Input Validation**: Write logic to check if email formats are correct and passwords meet length requirements before sending them to the database.
3. **Session State**: Implement a simple way to "remember" which user is logged in once the authentication is successful.

---

## 📌 Guidelines for the Team
- **Commit Often**: Use clear messages like `Feat: Add login validation` or `Fix: Connection timeout`.
- **Stay Decoupled**: 
    - Rohan should only touch the `database/` folder.
    - Usman should only touch the `controllers/` folder.
    - Faizan should only touch the `views/` folder.
- **Sync Regularly**: Before starting work, always run `git pull --rebase` to get the latest changes from the team.

---
*Last Updated: June 9, 2026*
