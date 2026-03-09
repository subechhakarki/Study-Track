import customtkinter as ctk

from database import DatabaseManager
from services.task_service import TaskService
from services.module_service import ModuleService


class TasksPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.db = DatabaseManager()
        self.task_service = TaskService(self.db)
        self.module_service = ModuleService(self.db)

        self.selected_task_id = None
        self.modules_map = {}  # name -> id

        # ── Top-level layout: sidebar | main ──────────────────────────────
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # main

        # ── Sidebar ───────────────────────────────────────────────────────
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(sidebar, text="StudyTrack", font=("Arial", 20, "bold")).grid(
            row=0, column=0, padx=16, pady=(18, 10), sticky="w"
        )
        self.welcome = ctk.CTkLabel(sidebar, text="", font=("Arial", 13), justify="left")
        self.welcome.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="w")

        ctk.CTkButton(sidebar, text="Dashboard", command=lambda: self.app.show_frame("DashboardPage")).grid(row=2, column=0, padx=16, pady=8, sticky="ew")
        ctk.CTkButton(sidebar, text="Modules",   command=lambda: self.app.show_frame("ModulesPage")).grid(row=3, column=0, padx=16, pady=8, sticky="ew")
        ctk.CTkButton(sidebar, text="Tasks",     command=lambda: self.app.show_frame("TasksPage")).grid(row=4, column=0, padx=16, pady=8, sticky="ew")
        ctk.CTkButton(sidebar, text="Profile",   command=lambda: self.app.show_frame("ProfilePage")).grid(row=5, column=0, padx=16, pady=8, sticky="ew")
        ctk.CTkButton(sidebar, text="Logout",    command=self.app.logout).grid(row=7, column=0, padx=16, pady=(8, 16), sticky="ew")

        # ── Main area ─────────────────────────────────────────────────────
        main = ctk.CTkFrame(self, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(2, weight=1)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=0)

        # Header
        header = ctk.CTkFrame(main)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=18, pady=(18, 10))
        ctk.CTkLabel(header, text="Tasks", font=("Arial", 22, "bold")).grid(row=0, column=0, sticky="w", padx=14, pady=(12, 2))
        ctk.CTkLabel(header, text="Manage your assignments", font=("Arial", 13)).grid(row=1, column=0, sticky="w", padx=14, pady=(0, 12))

        # Filters row
        filters = ctk.CTkFrame(main)
        filters.grid(row=1, column=0, columnspan=2, sticky="ew", padx=18, pady=(0, 10))
        filters.grid_columnconfigure(4, weight=1)

        ctk.CTkLabel(filters, text="Module:").grid(row=0, column=0, padx=(12, 6), pady=10, sticky="w")
        self.module_filter = ctk.CTkOptionMenu(filters, values=["All"])
        self.module_filter.grid(row=0, column=1, padx=6, pady=10, sticky="w")

        ctk.CTkLabel(filters, text="Status:").grid(row=0, column=2, padx=(12, 6), pady=10, sticky="w")
        self.status_filter = ctk.CTkOptionMenu(filters, values=["All", "Pending", "Completed"])
        self.status_filter.grid(row=0, column=3, padx=6, pady=10, sticky="w")

        self.search_entry = ctk.CTkEntry(filters, placeholder_text="Search title…")
        self.search_entry.grid(row=0, column=4, padx=(12, 6), pady=10, sticky="ew")

        ctk.CTkButton(filters, text="Apply", command=self.refresh_tasks).grid(row=0, column=5, padx=12, pady=10)

        # Task list (left)
        list_box = ctk.CTkFrame(main)
        list_box.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
        list_box.grid_rowconfigure(1, weight=1)
        list_box.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(list_box, text="Your Tasks", font=("Arial", 15, "bold")).grid(
            row=0, column=0, padx=14, pady=(12, 8), sticky="w"
        )
        self.tasks_scroll = ctk.CTkScrollableFrame(list_box)
        self.tasks_scroll.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))

        # Task form (right)
        form = ctk.CTkFrame(main, width=300)
        form.grid(row=2, column=1, sticky="nsew", padx=(0, 18), pady=(0, 18))
        form.grid_propagate(False)

        ctk.CTkLabel(form, text="Task Form", font=("Arial", 16, "bold")).pack(pady=(14, 8))

        self.title_entry = ctk.CTkEntry(form, placeholder_text="Title *")
        self.title_entry.pack(fill="x", padx=14, pady=6)

        self.desc_entry = ctk.CTkEntry(form, placeholder_text="Description (optional)")
        self.desc_entry.pack(fill="x", padx=14, pady=6)

        self.due_entry = ctk.CTkEntry(form, placeholder_text="Due date (YYYY-MM-DD)")
        self.due_entry.pack(fill="x", padx=14, pady=6)

        self.module_menu = ctk.CTkOptionMenu(form, values=["Select module"])
        self.module_menu.pack(fill="x", padx=14, pady=6)

        self.status_menu = ctk.CTkOptionMenu(form, values=["Pending", "Completed"])
        self.status_menu.pack(fill="x", padx=14, pady=6)

        self.msg = ctk.CTkLabel(form, text="")
        self.msg.pack(pady=(6, 2))

        btn_row = ctk.CTkFrame(form)
        btn_row.pack(fill="x", padx=14, pady=(10, 6))
        btn_row.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(btn_row, text="Add",    command=self.add_task).grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        ctk.CTkButton(btn_row, text="Update", command=self.update_task).grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        btn_row2 = ctk.CTkFrame(form)
        btn_row2.pack(fill="x", padx=14, pady=(0, 6))
        btn_row2.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(btn_row2, text="Mark Completed", command=self.mark_completed).grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        ctk.CTkButton(btn_row2, text="Delete", fg_color="#c0392b", hover_color="#a93226",
                      command=self.delete_task).grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        ctk.CTkButton(form, text="Clear", fg_color="transparent", border_width=1,
                      command=self.clear_form).pack(fill="x", padx=14, pady=(0, 14))

    # ── Called by App.show_frame() ─────────────────────────────────────────
    def on_show(self):
        self.welcome.configure(text=f"Hi, {self.app.current_user_name}")
        self.load_modules()
        self.refresh_tasks()

    def load_modules(self):
        user_id = self.app.current_user_id
        rows = self.module_service.get_modules(user_id)

        self.modules_map = {name: mid for (mid, name, teacher, notes) in rows}
        module_names = list(self.modules_map.keys()) or ["No modules yet"]

        self.module_menu.configure(values=module_names)
        self.module_menu.set(module_names[0])

        self.module_filter.configure(values=["All"] + module_names)
        self.module_filter.set("All")

    def refresh_tasks(self):
        user_id = self.app.current_user_id

        module_choice = self.module_filter.get()
        module_id = "All"
        if module_choice != "All" and module_choice in self.modules_map:
            module_id = self.modules_map[module_choice]

        status = self.status_filter.get()
        search = self.search_entry.get().strip()

        tasks = self.task_service.get_tasks(user_id, module_id=module_id, status=status, search=search)

        for w in self.tasks_scroll.winfo_children():
            w.destroy()

        if not tasks:
            ctk.CTkLabel(self.tasks_scroll, text="No tasks found.").pack(pady=12)
            return

        for (task_id, title, desc, due_date, status_val, module_id_val) in tasks:
            row = ctk.CTkFrame(self.tasks_scroll)
            row.pack(fill="x", pady=6)
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(row, text=title, font=("Arial", 13, "bold")).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 0))
            ctk.CTkLabel(row, text=f"Due: {due_date}   •   {status_val}").grid(row=1, column=0, sticky="w", padx=12, pady=(0, 10))

            ctk.CTkButton(row, text="Select", width=80,
                          command=lambda tid=task_id, t=title, d=desc, dd=due_date, s=status_val, mid=module_id_val:
                          self.select_task(tid, t, d, dd, s, mid)
                          ).grid(row=0, column=1, rowspan=2, padx=12, pady=12)

    def select_task(self, task_id, title, desc, due_date, status, module_id):
        self.selected_task_id = task_id
        self.title_entry.delete(0, "end");  self.title_entry.insert(0, title)
        self.desc_entry.delete(0, "end");   self.desc_entry.insert(0, desc or "")
        self.due_entry.delete(0, "end");    self.due_entry.insert(0, due_date)
        self.status_menu.set(status)

        module_name = next((n for n, mid in self.modules_map.items() if mid == module_id), None)
        if module_name:
            self.module_menu.set(module_name)
        self.msg.configure(text=f"Selected task #{task_id}")

    def clear_form(self):
        self.selected_task_id = None
        self.title_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.due_entry.delete(0, "end")
        self.status_menu.set("Pending")
        values = self.module_menu.cget("values")
        if values:
            self.module_menu.set(values[0])
        self.msg.configure(text="")

    def add_task(self):
        user_id = self.app.current_user_id
        module_name = self.module_menu.get()
        if module_name not in self.modules_map:
            self.msg.configure(text="Please create a module first.")
            return
        ok, msg = self.task_service.add_task(
            user_id, self.modules_map[module_name],
            self.title_entry.get(), self.desc_entry.get(),
            self.due_entry.get(), self.status_menu.get()
        )
        self.msg.configure(text=msg)
        if ok:
            self.clear_form()
            self.refresh_tasks()

    def update_task(self):
        if self.selected_task_id is None:
            self.msg.configure(text="Select a task first.")
            return
        module_name = self.module_menu.get()
        if module_name not in self.modules_map:
            self.msg.configure(text="Invalid module.")
            return
        ok, msg = self.task_service.update_task(
            self.selected_task_id, self.app.current_user_id,
            self.modules_map[module_name],
            self.title_entry.get(), self.desc_entry.get(),
            self.due_entry.get(), self.status_menu.get()
        )
        self.msg.configure(text=msg)
        if ok:
            self.refresh_tasks()

    def mark_completed(self):
        if self.selected_task_id is None:
            self.msg.configure(text="Select a task first.")
            return
        ok, msg = self.task_service.mark_completed(self.selected_task_id, self.app.current_user_id)
        self.msg.configure(text=msg)
        if ok:
            self.refresh_tasks()

    def delete_task(self):
        if self.selected_task_id is None:
            self.msg.configure(text="Select a task first.")
            return
        ok, msg = self.task_service.delete_task(self.selected_task_id, self.app.current_user_id)
        self.msg.configure(text=msg)
        if ok:
            self.clear_form()
            self.refresh_tasks()