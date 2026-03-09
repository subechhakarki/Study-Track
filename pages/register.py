from datetime import datetime
import customtkinter as ctk
from database import DatabaseManager
from services.user_service import UserService

class RegisterPage(ctk.CTkFrame):
    def __init__(self,parent, app):
        super().__init__(parent)
        self.app= app
        self.user_service= UserService()
        self.db=DatabaseManager()
        
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="StudyTrack", font=("Arial", 26, "bold")).grid(
            row=0, column=0, pady=(40, 4)
        )
        ctk.CTkLabel(self, text="Create your account", font=("Arial", 14)).grid(
            row=1, column=0, pady=(0, 20)
        )
        
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Full Name", width=300)
        self.name_entry.grid(row=2, column=0, padx=60, pady=8, sticky="ew")

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", width=300)
        self.email_entry.grid(row=3, column=0, padx=60, pady=8, sticky="ew")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password (min 6 chars)", show="*", width=300)
        self.password_entry.grid(row=4, column=0, padx=60, pady=8, sticky="ew")

        self.confirm_entry = ctk.CTkEntry(self, placeholder_text="Confirm Password", show="*", width=300)
        self.confirm_entry.grid(row=5, column=0, padx=60, pady=8, sticky="ew")

        self.msg_label = ctk.CTkLabel(self, text="", text_color="red")
        self.msg_label.grid(row=6, column=0, pady=(8, 0))
        
        ctk.CTkButton(self, text="Create Account", command=self.handle_register).grid(
            row=7, column=0, padx=60, pady=(14, 8), sticky="ew"
        )

        ctk.CTkButton(
            self, text="Back to Login",
            fg_color="transparent", border_width=1,
            command=self.go_login
        ).grid(row=8, column=0, padx=60, pady=(0, 30), sticky="ew")
        
    def handle_register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        ok, msg = self.user_service.register_user(name, email, password, confirm)

        if ok:
            self.msg_label.configure(text="Account created ✅", text_color="green")
            self.clear_form()
            # Redirect to login after short delay
            self.after(1200, self.go_login)
        else:
            self.msg_label.configure(text=msg, text_color="red")

    def clear_form(self):
        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.confirm_entry.delete(0, "end")

    def go_login(self):
        self.msg_label.configure(text="")
        self.app.show_frame("LoginPage")

        
        

