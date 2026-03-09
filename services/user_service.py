from datetime import datetime
import sqlite3
from database import DatabaseManager
import hashlib

class UserService:
    def __init__(self):
        self.db = DatabaseManager()
    
    def register_user(self, name, email, password, confirm_password):
        name=name.strip()
        email=email.strip().lower()
        
        if name == "":
            return(False, "Name is required")
        
        if '@' not in email:
            return(False, "Email must contain @")
        
        if len(password)<6:
            return(False, "Password must be atleast 6 characters")
        
        if password!=confirm_password:
            return(False, "Passwords do not match")
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = self.db.connect()
            c = conn.cursor()

            c.execute("""
                INSERT INTO users (name, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            """, (name, email, hashed_password, created_at))

            conn.commit()
            conn.close()

            return (True, "Account created")

        except sqlite3.IntegrityError:
            return (False, "Email already registered")
                
    def login_user(self, email, password):
        email = email.strip().lower()
        password = password.strip()
        
        if email=='':
            return(False, "Email is required")
        if password == '':
            return(False,"Password is required")
        conn=None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ?",(email,))
            user=c.fetchone()
            conn.close()
            
            if user is None:
                return(False,"No account found")
            #hashing the login password 
            hashed_input = hashlib.sha256(password.encode()).hexdigest()
            #getting the stored hash
            stored_hash = user[3]
            
            if hashed_input != stored_hash:
                return (False, "Incorrect password")
            
            return (True, user[0], user[1])

        except sqlite3.Error:
            return (False, "Database error. Please try again.")

        finally:
            if conn is not None:
                conn.close()
    
    def get_user_by_id(self, user_id):
        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute("SELECT id, name, email, created_at FROM users WHERE id = ?", (user_id,))
            return c.fetchone()
        except sqlite3.Error:
            return None
        finally:
            if conn:
                conn.close()

    def change_password(self, user_id, old_password, new_password, confirm_password):
        if len(new_password) < 6:
            return (False, "New password must be at least 6 characters")
        if new_password != confirm_password:
            return (False, "Passwords do not match")

        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
            row = c.fetchone()
            if row is None:
                return (False, "User not found")

            if hashlib.sha256(old_password.encode()).hexdigest() != row[0]:
                return (False, "Old password is incorrect")

            new_hash = hashlib.sha256(new_password.encode()).hexdigest()
            c.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
            conn.commit()
            return (True, "Password changed")

        except sqlite3.Error:
            return (False, "Database error")
        finally:
            if conn:
                conn.close()