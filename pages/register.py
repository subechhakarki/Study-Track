import tkinter as tk
import customtkinter as ctk
from services.user_service import UserService


class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.user_service = UserService()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.grid(row=0, column=0, sticky="nsew")

        # ── Card ──────────────────────────────────────────────────────────
        card = ctk.CTkFrame(outer, width=500, corner_radius=16)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.grid_columnconfigure(0, weight=1)

        # ── Branding ──────────────────────────────────────────────────────
        brand = ctk.CTkFrame(card, fg_color="transparent")
        brand.grid(row=0, column=0, pady=(26, 0), padx=44, sticky="ew")
        brand.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            brand, text="StudyTrack",
            font=("Georgia", 28, "bold"),
        ).grid(row=0, column=0)

        ctk.CTkLabel(
            brand, text="Create your free account",
            font=("Arial", 13), text_color="gray"
        ).grid(row=1, column=0, pady=(4, 0))

        # ── Divider ───────────────────────────────────────────────────────
        div1 = tk.Canvas(card, height=1, highlightthickness=0, bg="gray50")
        div1.grid(row=1, column=0, sticky="ew", padx=44, pady=(18, 20))

        # ── Fields ────────────────────────────────────────────────────────
        fields = ctk.CTkFrame(card, fg_color="transparent")
        fields.grid(row=2, column=0, sticky="ew", padx=44)
        fields.grid_columnconfigure(0, weight=1)

        # Full Name
        ctk.CTkLabel(
            fields, text="Full Name",
            font=("Arial", 12, "bold"), anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.name_entry = ctk.CTkEntry(
            fields, height=38, font=("Arial", 13),
            corner_radius=8
        )
        self.name_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Email
        ctk.CTkLabel(
            fields, text="Email address",
            font=("Arial", 12, "bold"), anchor="w"
        ).grid(row=2, column=0, sticky="w", pady=(0, 4))

        self.email_entry = ctk.CTkEntry(
            fields, height=38, font=("Arial", 13),
            corner_radius=8
        )
        self.email_entry.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        # Password
        ctk.CTkLabel(
            fields, text="Password",
            font=("Arial", 12, "bold"), anchor="w"
        ).grid(row=4, column=0, sticky="w", pady=(0, 4))

        self.password_entry = ctk.CTkEntry(
            fields, height=38, show="*", font=("Arial", 13),
            corner_radius=8
        )
        self.password_entry.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        # Confirm Password
        ctk.CTkLabel(
            fields, text="Confirm Password",
            font=("Arial", 12, "bold"), anchor="w"
        ).grid(row=6, column=0, sticky="w", pady=(0, 4))

        self.confirm_entry = ctk.CTkEntry(
            fields, height=38, show="*", font=("Arial", 13),
            corner_radius=8
        )
        self.confirm_entry.grid(row=7, column=0, sticky="ew", pady=(0, 4))
        self.confirm_entry.bind("<Return>", lambda e: self.handle_register())

        # Message
        self.msg_label = ctk.CTkLabel(
            fields, text="", font=("Arial", 11),
            text_color="#e74c3c", anchor="w"
        )
        self.msg_label.grid(row=8, column=0, sticky="w", pady=(2, 18))

        # Create Account button
        ctk.CTkButton(
            fields, text="Create Account", height=40,
            font=("Arial", 14, "bold"), corner_radius=8,
            command=self.handle_register
        ).grid(row=9, column=0, sticky="ew")

        # ── Footer ────────────────────────────────────────────────────────
        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.grid(row=3, column=0, pady=(14, 22), padx=44, sticky="ew")
        footer.grid_columnconfigure(0, weight=1)

        div2 = tk.Canvas(footer, height=1, highlightthickness=0, bg="gray50")
        div2.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        ctk.CTkLabel(
            footer, text="Already have an account?",
            font=("Arial", 12), text_color="gray"
        ).grid(row=1, column=0, pady=(0, 6))

        ctk.CTkButton(
            footer, text="Sign in instead", height=36,
            font=("Arial", 13), fg_color="transparent",
            border_width=1, corner_radius=8,
            text_color=("gray20", "gray80"),
            hover_color=("gray90", "gray25"),
            command=self.go_login
        ).grid(row=2, column=0, sticky="ew")

    def handle_register(self):
        ok, msg = self.user_service.register_user(
            self.name_entry.get(),
            self.email_entry.get(),
            self.password_entry.get(),
            self.confirm_entry.get()
        )
        if ok:
            self.msg_label.configure(text="✅  Account created! Redirecting…", text_color="#27ae60")
            self.clear_form()
            self.after(1200, self.go_login)
        else:
            self.msg_label.configure(text="⚠  " + msg, text_color="#e74c3c")

    def clear_form(self):
        for entry in (self.name_entry, self.email_entry,
                      self.password_entry, self.confirm_entry):
            entry.delete(0, "end")

    def go_login(self):
        self.msg_label.configure(text="")
        self.app.show_frame("LoginPage")