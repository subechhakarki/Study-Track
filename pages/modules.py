import customtkinter as ctk
from database import DatabaseManager
from services.module_service import ModuleService


class ModulesPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.db = DatabaseManager()
        self.module_service = ModuleService(self.db)
        
        self.selected_module_id =None
        
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

        self.welcome = ctk.CTkLabel(sidebar, text="", font=("Arial", 13), justify="left")
        self.welcome.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="w")

        ctk.CTkButton(sidebar, text="Dashboard", command=lambda: self.app.show_frame("DashboardPage")).grid(row=2, column=0, padx=16, pady=8, sticky="ew")
        ctk.CTkButton(sidebar, text="Modules",   command=lambda: self.app.show_frame("ModulesPage")).grid(row=3, column=0, padx=16, pady=8, sticky="ew")
        ctk.CTkButton(sidebar, text="Tasks",     command=lambda: self.app.show_frame("TasksPage")).grid(row=4, column=0, padx=16, pady=8, sticky="ew")
        ctk.CTkButton(sidebar, text="Profile",   command=lambda: self.app.show_frame("ProfilePage")).grid(row=5, column=0, padx=16, pady=8, sticky="ew")
        ctk.CTkButton(sidebar, text="Logout",    command=self.app.logout).grid(row=7, column=0, padx=16, pady=(8, 16), sticky="ew")

        # -------- Main Content --------
        main = ctk.CTkFrame(self, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=0)

        # Header
        header = ctk.CTkFrame(main)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=18, pady=(18, 10))
        ctk.CTkLabel(header, text="Modules", font=("Arial", 22, "bold")).grid(row=0, column=0, sticky="w", padx=14, pady=(12, 2))
        ctk.CTkLabel(header, text="Manage your subjects", font=("Arial", 13)).grid(row=1, column=0, sticky="w", padx=14, pady=(0, 12))

        # Module list (left)
        list_box = ctk.CTkFrame(main)
        list_box.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        list_box.grid_rowconfigure(1, weight=1)
        list_box.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(list_box, text="Your Modules", font=("Arial", 15, "bold")).grid(
            row=0, column=0, sticky="w", padx=14, pady=(12, 8)
        )

        self.modules_scroll = ctk.CTkScrollableFrame(list_box)
        self.modules_scroll.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        self.modules_scroll.grid_columnconfigure(0, weight=1)

        # Module form (right)
        form = ctk.CTkFrame(main, width=300)
        form.grid(row=1, column=1, sticky="nsew", padx=(0, 18), pady=(0, 18))
        form.grid_propagate(False)

        ctk.CTkLabel(form, text="Module Form", font=("Arial", 16, "bold")).pack(pady=(14, 8))

        self.name_entry = ctk.CTkEntry(form, placeholder_text="Module Name *")
        self.name_entry.pack(fill="x", padx=14, pady=6)

        self.teacher_entry = ctk.CTkEntry(form, placeholder_text="Teacher (optional)")
        self.teacher_entry.pack(fill="x", padx=14, pady=6)

        self.notes_entry = ctk.CTkEntry(form, placeholder_text="Notes (optional)")
        self.notes_entry.pack(fill="x", padx=14, pady=6)

        self.msg = ctk.CTkLabel(form, text="")
        self.msg.pack(pady=(6, 2))

        btn_row1 = ctk.CTkFrame(form)
        btn_row1.pack(fill="x", padx=14, pady=(10, 4))
        btn_row1.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_row1, text="Add",    command=self.add_module).grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        ctk.CTkButton(btn_row1, text="Update", command=self.update_module).grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        btn_row2 = ctk.CTkFrame(form)
        btn_row2.pack(fill="x", padx=14, pady=(0, 4))
        btn_row2.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_row2, text="Delete", fg_color="#c0392b", hover_color="#a93226",
                      command=self.delete_module).grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        ctk.CTkButton(btn_row2, text="Clear",  fg_color="transparent", border_width=1,
                      command=self.clear_form).grid(row=0, column=1, padx=4, pady=4, sticky="ew")

    # Called by App.show_frame()
    def on_show(self):
        self.welcome.configure(text=f"Hi, {self.app.current_user_name}")
        self.refresh_modules()

    def refresh_modules(self):
        for w in self.modules_scroll.winfo_children():
            w.destroy()

        user_id = self.app.current_user_id
        rows = self.module_service.get_modules(user_id)

        if not rows:
            ctk.CTkLabel(self.modules_scroll, text="No modules yet. Add one →").pack(pady=20)
            return

        for (mid, mname, teacher, notes) in rows:
            row = ctk.CTkFrame(self.modules_scroll)
            row.pack(fill="x", pady=5)
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(row, text=mname, font=("Arial", 13, "bold")).grid(
                row=0, column=0, sticky="w", padx=12, pady=(10, 0)
            )
            detail = f"Teacher: {teacher}" if teacher else "No teacher listed"
            ctk.CTkLabel(row, text=detail, font=("Arial", 11)).grid(
                row=1, column=0, sticky="w", padx=12, pady=(0, 10)
            )
            ctk.CTkButton(
                row, text="Select", width=80,
                command=lambda m=mid, n=mname, t=teacher, no=notes:
                    self.select_module(m, n, t, no)
            ).grid(row=0, column=1, rowspan=2, padx=12, pady=10)

    def select_module(self, module_id, name, teacher, notes):
        self.selected_module_id = module_id
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, name)
        self.teacher_entry.delete(0, "end")
        self.teacher_entry.insert(0, teacher or "")
        self.notes_entry.delete(0, "end")
        self.notes_entry.insert(0, notes or "")
        self.msg.configure(text=f"Selected: {name}")

    def clear_form(self):
        self.selected_module_id = None
        self.name_entry.delete(0, "end")
        self.teacher_entry.delete(0, "end")
        self.notes_entry.delete(0, "end")
        self.msg.configure(text="")

    def add_module(self):
        user_id = self.app.current_user_id
        ok, msg = self.module_service.add_module(
            user_id,
            self.name_entry.get(),
            self.teacher_entry.get(),
            self.notes_entry.get()
        )
        self.msg.configure(text=msg)
        if ok:
            self.clear_form()
            self.refresh_modules()

    def update_module(self):
        if self.selected_module_id is None:
            self.msg.configure(text="Select a module first.")
            return
        user_id = self.app.current_user_id
        ok, msg = self.module_service.update_module(
            self.selected_module_id, user_id,
            self.name_entry.get(),
            self.teacher_entry.get(),
            self.notes_entry.get()
        )
        self.msg.configure(text=msg)
        if ok:
            self.refresh_modules()

    def delete_module(self):
        if self.selected_module_id is None:
            self.msg.configure(text="Select a module first.")
            return
        user_id = self.app.current_user_id
        ok, msg = self.module_service.delete_module(self.selected_module_id, user_id)
        self.msg.configure(text=msg)
        if ok:
            self.clear_form()
            self.refresh_modules()
        