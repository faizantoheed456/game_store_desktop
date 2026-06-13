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
        cursor.execute("SELECT id, username, email, password, bio, birthday, profile_picture, created_at FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

    @staticmethod
    def get_user_by_email(email):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("SELECT id, username, email, password, bio, birthday, profile_picture, created_at FROM users WHERE email = ?", (email,))
        return cursor.fetchone()

    @staticmethod
    def update_profile(user_id, bio, birthday, profile_picture):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        try:
            cursor.execute("""
                UPDATE users 
                SET bio = ?, birthday = ?, profile_picture = ?
                WHERE id = ?
            """, (bio, birthday, profile_picture, user_id))
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False

    @staticmethod
    def update_password(user_id, hashed_password):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        try:
            cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
            
    @staticmethod
    def get_user_by_id(user_id):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("SELECT id, username, email, password, bio, birthday, profile_picture, created_at FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

    @staticmethod
    def get_all_users():
        db = DatabaseConnection()
        cursor = db.get_cursor()
        cursor.execute("SELECT id, username, email, created_at FROM users")
        return cursor.fetchall()

    @staticmethod
    def delete_user(user_id):
        db = DatabaseConnection()
        cursor = db.get_cursor()
        try:
            cursor.execute("DELETE FROM user_library WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            db.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
