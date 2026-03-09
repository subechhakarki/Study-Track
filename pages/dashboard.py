import customtkinter as ctk

from database import DatabaseManager
from services.module_service import ModuleService
from services.task_service import TaskService

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # DB + services (dashboard reads data)
        self.db = DatabaseManager()
        self.module_service = ModuleService(self.db)
        self.task_service = TaskService(self.db)

        # Layout: sidebar + main
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # main

        # -------- Sidebar --------
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(sidebar, text="StudyTrack", font=("Arial", 20, "bold")).grid(
            row=0, column=0, padx=16, pady=(18, 10), sticky="w"
        )

        self.welcome = ctk.CTkLabel(
            sidebar, text="Welcome,\n", font=("Arial", 14), justify="left"
        )
        self.welcome.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="w")

        ctk.CTkButton(sidebar, text="Dashboard", command=self.go_dashboard).grid(row=2, column=0, padx=16, pady=8, sticky="ew")
        ctk.CTkButton(sidebar, text="Modules", command=self.go_modules).grid(row=3, column=0, padx=16, pady=8, sticky="ew")
        ctk.CTkButton(sidebar, text="Tasks", command=self.go_tasks).grid(row=4, column=0, padx=16, pady=8, sticky="ew")
        ctk.CTkButton(sidebar, text="Profile", command=self.go_profile).grid(row=5, column=0, padx=16, pady=8, sticky="ew")

        ctk.CTkButton(sidebar, text="Logout", command=self.logout).grid(
            row=7, column=0, padx=16, pady=(8, 16), sticky="ew"
        )

        # -------- Main Content --------
        main = ctk.CTkFrame(self, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(2, weight=1)
        main.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(main)
        header.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 10))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(header, text="Dashboard", font=("Arial", 22, "bold")).grid(
            row=0, column=0, sticky="w", padx=14, pady=(12, 2)
        )
        ctk.CTkLabel(header, text="Your quick overview", font=("Arial", 13)).grid(
            row=1, column=0, sticky="w", padx=14, pady=(0, 12)
        )

        # Stats row (4 cards)
        stats = ctk.CTkFrame(main)
        stats.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 10))
        for i in range(4):
            stats.grid_columnconfigure(i, weight=1)

        self.modules_val = self._stat_card(stats, 0, "Total Modules")
        self.tasks_val = self._stat_card(stats, 1, "Total Tasks")
        self.due_soon_val = self._stat_card(stats, 2, "Due Soon (3 days)")
        self.completed_val = self._stat_card(stats, 3, "Completed")

        # Upcoming list
        upcoming = ctk.CTkFrame(main)
        upcoming.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
        upcoming.grid_rowconfigure(1, weight=1)
        upcoming.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(upcoming, text="Upcoming Tasks (Top 5)", font=("Arial", 16, "bold")).grid(
            row=0, column=0, sticky="w", padx=14, pady=(12, 8)
        )

        self.upcoming_list = ctk.CTkFrame(upcoming)
        self.upcoming_list.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        self.upcoming_list.grid_columnconfigure(0, weight=1)

    def _stat_card(self, parent, col, title):
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=col, padx=8, pady=10, sticky="ew")
        ctk.CTkLabel(card, text=title, font=("Arial", 12)).pack(pady=(12, 2))
        val = ctk.CTkLabel(card, text="0", font=("Arial", 22, "bold"))
        val.pack(pady=(0, 12))
        return val

    # Called automatically by App.show_frame if present
    def on_show(self):
        # Update welcome text
        self.welcome.configure(text=f"Welcome,\n{self.app.current_user_name}")

        # Must be logged in
        user_id = self.app.current_user_id
        if user_id is None:
            # App guard (4D) should prevent this, but safe fallback:
            return

        # Load stats
        total_modules = self.module_service.count_modules(user_id)
        total_tasks = self.task_service.count_tasks(user_id)
        due_soon = self.task_service.count_due_soon(user_id, days=3)
        completed = self.task_service.count_completed_tasks(user_id)

        self.modules_val.configure(text=str(total_modules))
        self.tasks_val.configure(text=str(total_tasks))
        self.due_soon_val.configure(text=str(due_soon))
        self.completed_val.configure(text=str(completed))

        # Load upcoming tasks list
        for w in self.upcoming_list.winfo_children():
            w.destroy()

        tasks = self.task_service.get_upcoming_tasks(user_id, limit=5)
        if not tasks:
            ctk.CTkLabel(self.upcoming_list, text="No upcoming tasks 🎉").pack(pady=20)
            return

        for title, due_date, status in tasks:
            row = ctk.CTkFrame(self.upcoming_list)
            row.pack(fill="x", pady=6)
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(row, text=title, font=("Arial", 13, "bold")).grid(row=0, column=0, sticky="w", padx=12, pady=10)
            ctk.CTkLabel(row, text=due_date).grid(row=0, column=1, sticky="e", padx=12)
            ctk.CTkLabel(row, text=status).grid(row=0, column=2, sticky="e", padx=12)

    # Navigation (4C)
    def go_dashboard(self): self.app.show_frame("DashboardPage")
    def go_modules(self): self.app.show_frame("ModulesPage")
    def go_tasks(self): self.app.show_frame("TasksPage")
    def go_profile(self): self.app.show_frame("ProfilePage")
    def logout(self): self.app.logout()
