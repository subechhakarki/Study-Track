import sqlite3


class ModuleService:
    def __init__(self, db):
        self.db = db

    def add_module(self, user_id, module_name, teacher="", notes=""):
        module_name = (module_name or "").strip()
        teacher = (teacher or "").strip()
        notes = (notes or "").strip()

        if module_name == "":
            return (False, "Module name is required")

        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute("""
                INSERT INTO modules (user_id, module_name, teacher, notes)
                VALUES (?, ?, ?, ?)
            """, (user_id, module_name, teacher, notes))
            conn.commit()
            return (True, "Module added ✅")
        except Exception as e:
            print("MODULE ADD ERROR:", repr(e))   # <-- shows real error
            return (False, f"Database error: {e}")
        finally:
            if conn:
                conn.close()
            
    def get_modules(self, user_id):
        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute("""
                SELECT id, module_name, teacher, notes
                FROM modules
                WHERE user_id = ?
                ORDER BY module_name
            """, (user_id,))
            return c.fetchall()
        except sqlite3.Error:
            return []
        finally:
            if conn:
                conn.close()

    def update_module(self, module_id, user_id, module_name, teacher="", notes=""):
        module_name = (module_name or "").strip()
        teacher = (teacher or "").strip()
        notes = (notes or "").strip()

        if module_name == "":
            return (False, "Module name is required")

        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute("""
                UPDATE modules
                SET module_name = ?, teacher = ?, notes = ?
                WHERE id = ? AND user_id = ?
            """, (module_name, teacher, notes, module_id, user_id))
            conn.commit()
            if c.rowcount == 0:
                return (False, "Module not found (or not yours)")
            return (True, "Module updated ✅")
        except sqlite3.Error:
            return (False, "Database error while updating module")
        finally:
            if conn:
                conn.close()

    def delete_module(self, module_id, user_id):
        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute(
                "DELETE FROM modules WHERE id = ? AND user_id = ?",
                (module_id, user_id)
            )
            conn.commit()
            if c.rowcount == 0:
                return (False, "Module not found (or not yours)")
            return (True, "Module deleted ✅")
        except sqlite3.Error:
            return (False, "Database error while deleting module")
        finally:
            if conn:
                conn.close()

    def count_modules(self, user_id):
        conn = None
        try:
            conn = self.db.connect()
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM modules WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            return row[0] if row else 0
        except sqlite3.Error:
            return 0
        finally:
            if conn:
                conn.close()