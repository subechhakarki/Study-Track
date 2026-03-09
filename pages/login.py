import customtkinter as ctk
from services.user_service import UserService  # adjust name if your file is different

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.user_service = UserService()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Login", font=("Arial", 24, "bold")).grid(pady=(40, 20), row=0, column=0)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.grid(padx=60, pady=10, row=1, column=0, sticky="ew")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.grid(padx=60, pady=10, row=2, column=0, sticky="ew")

        self.msg_label = ctk.CTkLabel(self, text="")
        self.msg_label.grid(pady=(10, 0), row=3, column=0)

        ctk.CTkButton(self, text="Login", command=self.handle_login).grid(pady=20, row=4, column=0)
        
        ctk.CTkButton(self, text="Create an account", fg_color="transparent", border_width=1, command=self.go_register).grid(padx=60, pady=(0, 30), row=6, column=0, sticky="ew")


    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        result = self.user_service.login_user(email, password)

        # result should be: (True, user_id, name) OR (False, "message")
        if result[0] is True:
            user_id = result[1]
            name = result[2]
            self.msg_label.configure(text="")
            self.password_entry.delete(0, "end")
            self.app.login_success(user_id, name)  # ✅ THIS IS 4C.5
        else:
            self.msg_label.configure(text=result[1])
    def go_register(self):
        self.msg_label.configure(text="")
        self.app.show_frame("RegisterPage")
    
