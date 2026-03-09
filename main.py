from database import DatabaseManager

db = DatabaseManager()

from app import App

if __name__ == "__main__":
    App().mainloop()

