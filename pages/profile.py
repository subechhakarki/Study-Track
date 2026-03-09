import customtkinter as ctk
from services.user_service import UserService


class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.user_service = UserService()

        # ── Top-level layout: sidebar | main ──────────────────────────────
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

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
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Scrollable so it works on smaller screens
        scroll = ctk.CTkScrollableFrame(main)
        scroll.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        scroll.grid_columnconfigure(0, weight=1)

        # ── Account Info card ─────────────────────────────────────────────
        ctk.CTkLabel(scroll, text="Profile", font=("Arial", 22, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 12)
        )

        info_card = ctk.CTkFrame(scroll)
        info_card.grid(row=1, column=0, sticky="ew", pady=(0, 24))
        info_card.grid_columnconfigure(1, weight=1)

        fields = [("Name", "name_label"), ("Email", "email_label"), ("Member since", "joined_label")]
        for i, (label_text, attr) in enumerate(fields):
            ctk.CTkLabel(info_card, text=label_text, font=("Arial", 13, "bold")).grid(
                row=i, column=0, sticky="w", padx=16, pady=(14 if i == 0 else 6, 14 if i == 2 else 6)
            )
            lbl = ctk.CTkLabel(info_card, text="—", font=("Arial", 13))
            lbl.grid(row=i, column=1, sticky="w", padx=8,
                     pady=(14 if i == 0 else 6, 14 if i == 2 else 6))
            setattr(self, attr, lbl)

        # ── Change Password card ──────────────────────────────────────────
        ctk.CTkLabel(scroll, text="Change Password", font=("Arial", 18, "bold")).grid(
            row=2, column=0, sticky="w", pady=(0, 10)
        )

        pw_card = ctk.CTkFrame(scroll)
        pw_card.grid(row=3, column=0, sticky="ew")
        pw_card.grid_columnconfigure(0, weight=1)

        # Current password
        ctk.CTkLabel(pw_card, text="Current Password", font=("Arial", 13)).grid(
            row=0, column=0, sticky="w", padx=16, pady=(16, 2)
        )
        self.old_pw = ctk.CTkEntry(pw_card, show="*")
        self.old_pw.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 10))

        # New password
        ctk.CTkLabel(pw_card, text="New Password", font=("Arial", 13)).grid(
            row=2, column=0, sticky="w", padx=16, pady=(4, 2)
        )
        self.new_pw = ctk.CTkEntry(pw_card, show="*")
        self.new_pw.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 10))

        # Confirm new password
        ctk.CTkLabel(pw_card, text="Confirm New Password", font=("Arial", 13)).grid(
            row=4, column=0, sticky="w", padx=16, pady=(4, 2)
        )
        self.confirm_pw = ctk.CTkEntry(pw_card, show="*")
        self.confirm_pw.grid(row=5, column=0, sticky="ew", padx=16, pady=(0, 10))

        self.pw_msg = ctk.CTkLabel(pw_card, text="")
        self.pw_msg.grid(row=6, column=0, pady=(2, 4))

        ctk.CTkButton(pw_card, text="Change Password", command=self.handle_change_password).grid(
            row=7, column=0, sticky="ew", padx=16, pady=(4, 16)
        )

    # ── Called by App.show_frame() ─────────────────────────────────────────
    def on_show(self):
        self.welcome.configure(text=f"Hi, {self.app.current_user_name}")
        self.pw_msg.configure(text="")
        self.old_pw.delete(0, "end")
        self.new_pw.delete(0, "end")
        self.confirm_pw.delete(0, "end")

        user = self.user_service.get_user_by_id(self.app.current_user_id)
        if user:
            # user = (id, name, email, created_at)
            self.name_label.configure(text=user[1])
            self.email_label.configure(text=user[2])
            self.joined_label.configure(text=user[3][:10] if user[3] else "—")

    def handle_change_password(self):
        ok, msg = self.user_service.change_password(
            self.app.current_user_id,
            self.old_pw.get(),
            self.new_pw.get(),
            self.confirm_pw.get()
        )
        self.pw_msg.configure(text=msg, text_color="green" if ok else "red")
        if ok:
            self.old_pw.delete(0, "end")
            self.new_pw.delete(0, "end")
            self.confirm_pw.delete(0, "end")