from src.database.connection import DatabaseConnection

class UserQueries:
    @staticmethod
    def create_user(username, email, password):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            db.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    @staticmethod
    def get_user_by_username(username):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

    @staticmethod
    def get_user_by_email(email):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()
