import customtkinter as ctk

from pages.dashboard import DashboardPage
from pages.modules import ModulesPage
from pages.tasks import TasksPage
from pages.profile import ProfilePage
from pages.login import LoginPage
from pages.register import RegisterPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("StudyTrack")
        self.geometry("900x600")

        # Session values (set after login)
        self.current_user_id = None
        self.current_user_name = ""

        # Container holds all pages
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create all pages once
        self.frames = {}
        for Page in (LoginPage, DashboardPage, ModulesPage, TasksPage, ProfilePage, RegisterPage):
            frame = Page(container, app=self)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start at login
        self.show_frame("LoginPage")

    def show_frame(self, page_name: str):
        # Pages that require login
        protected = {"DashboardPage", "ModulesPage", "TasksPage", "ProfilePage"}

        # If user is not logged in and tries to open protected pages → send to login
        if page_name in protected and self.current_user_id is None:
            page_name = "LoginPage"

        frame = self.frames[page_name]

        if hasattr(frame, "on_show"):
            frame.on_show()

        frame.tkraise()


    def login_success(self, user_id: int, name: str):
        self.current_user_id = user_id
        self.current_user_name = name
        self.show_frame("DashboardPage")

    def logout(self):
        self.current_user_id = None
        self.current_user_name = ""
        self.show_frame("LoginPage")

