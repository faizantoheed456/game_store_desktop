import sqlite3
import os

class DatabaseConnection:
    _instance = None
    _db_path = "game_store.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect(cls._db_path)
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
                website_url TEXT
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
