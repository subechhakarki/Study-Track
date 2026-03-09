import sqlite3
from datetime import datetime, timedelta

class TaskService:
    def __init__(self, db):
        self.db = db

    def add_task(self, user_id, module_id, title, description, due_date, status="Pending"):
        title = (title or "").strip()
        description = (description or "").strip()
        due_date = (due_date or "").strip()
        status = (status or "Pending").strip()

        if title == "":
            return (False, "Title is required")
        if due_date == "":
            return (False, "Due date is required (YYYY-MM-DD)")
        if status not in ("Pending", "Completed"):
            return (False, "Status must be Pending or Completed")

        # Simple due date format check (YYYY-MM-DD)
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return (False, "Due date must be in YYYY-MM-DD format")

        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute(
                """
                INSERT INTO tasks (user_id, module_id, title, description, due_date, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, module_id, title, description, due_date, status)
            )
            conn.commit()
            return (True, "Task added")
        except sqlite3.Error:
            return (False, "Database error while adding task")
        finally:
            if conn:
                conn.close()

    def get_tasks(self, user_id, module_id=None, status=None, search=None):
        # Build query dynamically (filters)
        query = """
            SELECT id, title, description, due_date, status, module_id
            FROM tasks
            WHERE user_id = ?
        """
        params = [user_id]

        if module_id and module_id != "All":
            query += " AND module_id = ?"
            params.append(int(module_id))

        if status and status != "All":
            query += " AND status = ?"
            params.append(status)

        if search:
            query += " AND title LIKE ?"
            params.append(f"%{search}%")

        query += " ORDER BY due_date ASC"

        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute(query, params)
            return c.fetchall()
        except sqlite3.Error:
            return []
        finally:
            if conn:
                conn.close()

    def update_task(self, task_id, user_id, module_id, title, description, due_date, status):
        title = (title or "").strip()
        description = (description or "").strip()
        due_date = (due_date or "").strip()
        status = (status or "").strip()

        if title == "":
            return (False, "Title is required")
        if due_date == "":
            return (False, "Due date is required (YYYY-MM-DD)")
        if status not in ("Pending", "Completed"):
            return (False, "Status must be Pending or Completed")

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return (False, "Due date must be in YYYY-MM-DD format")

        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute(
                """
                UPDATE tasks
                SET module_id = ?, title = ?, description = ?, due_date = ?, status = ?
                WHERE id = ? AND user_id = ?
                """,
                (module_id, title, description, due_date, status, task_id, user_id)
            )
            conn.commit()
            if c.rowcount == 0:
                return (False, "Task not found (or not yours)")
            return (True, "Task updated")
        except sqlite3.Error:
            return (False, "Database error while updating task")
        finally:
            if conn:
                conn.close()

    def mark_completed(self, task_id, user_id):
        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute(
                """
                UPDATE tasks
                SET status = 'Completed'
                WHERE id = ? AND user_id = ?
                """,
                (task_id, user_id)
            )
            conn.commit()
            if c.rowcount == 0:
                return (False, "Task not found (or not yours)")
            return (True, "Marked completed")
        except sqlite3.Error:
            return (False, "Database error while marking completed")
        finally:
            if conn:
                conn.close()

    def delete_task(self, task_id, user_id):
        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute(
                "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            )
            conn.commit()
            if c.rowcount == 0:
                return (False, "Task not found (or not yours)")
            return (True, "Task deleted")
        except sqlite3.Error:
            return (False, "Database error while deleting task")
        finally:
            if conn:
                conn.close()
                
    def count_tasks(self, user_id):
        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            return row[0] if row else 0
        except sqlite3.Error:
            return 0
        finally:
            if conn:
                conn.close()

    def count_completed_tasks(self, user_id):
        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute(
                "SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 'Completed'",
                (user_id,)
            )
            row = c.fetchone()
            return row[0] if row else 0
        except sqlite3.Error:
            return 0
        finally:
            if conn:
                conn.close()

    def count_due_soon(self, user_id, days=3):
        today = datetime.now().date()
        cutoff = today + timedelta(days=days)
        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute("""
                SELECT COUNT(*) FROM tasks
                WHERE user_id = ?
                  AND status = 'Pending'
                  AND due_date BETWEEN ? AND ?
            """, (user_id, today.isoformat(), cutoff.isoformat()))
            row = c.fetchone()
            return row[0] if row else 0
        except sqlite3.Error:
            return 0
        finally:
            if conn:
                conn.close()

    def get_upcoming_tasks(self, user_id, limit=5):
        today = datetime.now().date().isoformat()
        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute("""
                SELECT title, due_date, status FROM tasks
                WHERE user_id = ?
                  AND status = 'Pending'
                  AND due_date >= ?
                ORDER BY due_date ASC
                LIMIT ?
            """, (user_id, today, limit))
            return c.fetchall()
        except sqlite3.Error:
            return []
        finally:
            if conn:
                conn.close()
