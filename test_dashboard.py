import customtkinter as ctk
from pages.dashboard import DashboardPage

ctk.set_appearance_mode("System")

root = ctk.CTk()
root.geometry("500x500")

page = DashboardPage(root, app=None, user_name="Test User")
page.pack(fill="both", expand=True)

root.mainloop()
