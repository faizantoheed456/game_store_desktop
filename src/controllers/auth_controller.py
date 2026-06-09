import hashlib
import smtplib
from email.mime.text import MIMEText
from src.database.queries import UserQueries

class AuthController:
    @staticmethod
    def register_user(username, email, password):
        if not username or not email or not password:
            return False, "All fields are required."
        
        # Check if user already exists
        if UserQueries.get_user_by_username(username):
            return False, "Username already exists."
        
        if UserQueries.get_user_by_email(email):
            return False, "Email already exists."
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if UserQueries.create_user(username, email, hashed_password):
            # Send Thank You Email
            AuthController._send_welcome_email(username, email)
            return True, "Registration successful! A welcome email has been sent."
        else:
            return False, "An error occurred during registration."

    @staticmethod
    def _send_welcome_email(username, email):
        """Sends a formal thank you email to the newly registered user."""
        sender_email = "faizantoheed456@gmail.com" # Use your actual gmail here
        sender_password = "oqbu ycyy uooq dqzy"  # Your new 16-character App Password
        
        subject = "Welcome to GameVault!"
        body = f"""
Dear {username},

Thank you for registering with GameVault! We are thrilled to have you as part of our gaming community.

Your account has been successfully created. You can now log in to the platform using your username and password to explore our game catalog and manage your profile.

If you have any questions or need assistance, feel free to reach out to our support team.

Happy Gaming!

Best regards,
The GameVault Team
"""
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = f"GameVault <{sender_email}>"
        msg['To'] = email

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
                print(f"Success: Email sent to {email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    @staticmethod
    def login_user(username, password):
        user = UserQueries.get_user_by_username(username)
        if not user:
            return False, "Invalid username or password."
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user[3] == hashed_password: # password is at index 3
            return True, user
        else:
            return False, "Invalid username or password."
