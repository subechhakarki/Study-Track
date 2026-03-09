import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="app.db"):
        self.db_name= db_name
        self.create_users_table()
        self.create_modules_table()
        self.create_tasks_table()
        
    def connect(self):
        return sqlite3.connect(self.db_name)
    
    def create_users_table(self):
        conn=self.connect()
        #create a cursor
        c = conn.cursor()
        #create a table 
        c.execute("""
          CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL,
              password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
          )
          """)
        conn.commit()
        conn.close()
    
    def create_modules_table(self):
        conn = self.connect()
        c= conn.cursor()
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS modules(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER NOT NULL,
                  module_name TEXT NOT NULL,
                  teacher TEXT,
                  notes TEXT  
            )  
            """)
        conn.commit()
        conn.close()
        
    def create_tasks_table(self):
        conn= self.connect()
        c= conn.cursor()
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER NOT NULL,
                      module_id INTEGER NOT NULL,
                      title TEXT NOT NULL,
                      description TEXT,
                      due_date TEXT NOT NULL,
                      status TEXT NOT NULL
                )
                """)
        conn.commit()
        conn.close()

    