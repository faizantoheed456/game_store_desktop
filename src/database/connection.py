import sqlite3
import os

class DatabaseConnection:
    _instance = None
    _db_path = "game_store.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect(cls._db_path)
            # Enable foreign keys
            cls._instance.connection.execute("PRAGMA foreign_keys = ON")
            cls._instance._create_tables()
        return cls._instance

    def _create_tables(self):
        cursor = self.connection.cursor()
        
        # Users Table (matching the schema in README but for SQLite)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                bio TEXT,
                birthday DATE,
                profile_picture TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Games Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT,
                price DECIMAL(10, 2) NOT NULL,
                description TEXT,
                cover_image TEXT,
                release_year INTEGER,
                platform TEXT,
                rating REAL DEFAULT 0.0,
                is_trending INTEGER DEFAULT 0,
                website_url TEXT,
                remote_image_url TEXT
            )
        ''')

        # User Library Table (Now acts as a General Collection Table)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_library (
                user_id INTEGER,
                game_id INTEGER,
                is_favorite INTEGER DEFAULT 1,
                is_installed INTEGER DEFAULT 0,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, game_id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (game_id) REFERENCES games(id)
            )
        ''')
        
        self.connection.commit()

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
            DatabaseConnection._instance = None
