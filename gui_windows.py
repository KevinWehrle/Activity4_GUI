import tkinter as tk
from tkinter import ttk, messagebox
import database_ops # Connects to the database_ops.py file made for SQL stuff

class CompanyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Company Portal")
        self.root.geometry("500x400")
        
        # This runs our database setup so the table exists
        database_ops.setup_database()
        
        # Inactivity TimeOut
        self.timeout_timer = None
        # Anytime the mouse moves or a key is pressed, reset the timer
        self.root.bind("<Motion>", self.reset_timer)
        self.root.bind("<Key>", self.reset_timer)
        
        self.show_login()

    def reset_timer(self, event=None):
        # If there's an existing timer, cancel it
        if self.timeout_timer is not None:
            self.root.after_cancel(self.timeout_timer)
        # Set timeer to 1 min (60,000ms)
        self.timeout_timer = self.root.after(60000, self.auto_logout)

    def auto_logout(self):
        messagebox.showwarning("Timeout", "Logged out due to inactivity.")
        self.show_login()

    # Clear the Screen
    def clear_screen(self):
        # This deletes all buttons/labels currently on the screen
        for widget in self.root.winfo_children():
            widget.destroy()

    # Login Screen
    def show_login(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Login", font=("Arial", 20)).pack(pady=20)
        
        tk.Label(self.root, text="User ID:").pack()
        
        # Auto Suggest Feature
        # Try to read the text file of saved usernames
        saved_users = []
        try:
            with open("recent_logins.txt", "r") as file:
                # Read lines, strip out extra spaces/newlines
                saved_users = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            pass # If the file doesn't exist yet, do nothing

        # Create dropdown box instead of a normal text entry for auto-suggest
        self.entry_user = ttk.Combobox(self.root, values=saved_users)
        self.entry_user.pack()
        
        tk.Label(self.root, text="Password:").pack()
        self.entry_pass = tk.Entry(self.root, show="*") # Stars out the password
        self.entry_pass.pack()
        
        tk.Button(self.root, text="Submit", command=self.process_login).pack(pady=20)

    # Login Logic
    def process_login(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
        
        # Input Validation
        if user == "" or password == "":
            messagebox.showerror("Error", "Fields cannot be blank!")
            return
            
        # Check the Database
        role = database_ops.check_login(user, password)
        
        if role:
            # Save username for future auto-suggest
            with open("recent_logins.txt", "a") as file:
                file.write(user + "\n")
                
            # Role-Based Routing
            if role == "Manager":
                self.show_manager_dashboard()
            elif role == "Employee":
                self.show_employee_dashboard()
            elif role == "Owner":
                self.show_owner_dashboard()
        else:
            messagebox.showerror("Error", "Wrong ID or Password")

    # Dashboards
    def show_manager_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="Manager Dashboard", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Welcome, Manager!").pack()
        
        # ONLY managers get the "Create Account" button
        tk.Button(self.root, text="Create New Account", command=self.create_account_window).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.show_login).pack(pady=10)

    def show_employee_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="Employee Dashboard", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Welcome, Employee!").pack()

        tk.Button(self.root, text="Logout", command=self.show_login).pack(pady=10)

    def show_owner_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="Owner Dashboard", font=("Arial", 20)).pack(pady=20)

        tk.Button(self.root, text="Logout", command=self.show_login).pack(pady=10)

    # Create Account PopUp
    def create_account_window(self):
        # Creates a new mini-window
        top = tk.Toplevel(self.root)
        top.title("Create Account")
        top.geometry("300x250")
        
        tk.Label(top, text="New User ID:").pack()
        new_user = tk.Entry(top)
        new_user.pack()
        
        tk.Label(top, text="New Password:").pack()
        new_pass = tk.Entry(top)
        new_pass.pack()
        
        tk.Label(top, text="Role:").pack()
        role_combo = ttk.Combobox(top, values=["Employee", "Manager", "Owner"])
        role_combo.pack()
        
        def save_to_db():
            u = new_user.get()
            p = new_pass.get()
            r = role_combo.get()
            
            # Validation
            if not u or not p or not r:
                messagebox.showerror("Error", "All fields required")
                return
                
            # Send to SQL file
            success = database_ops.create_user(u, p, r)
            if success:
                messagebox.showinfo("Success", "Account Created!")
                top.destroy() # Close the popup
            else:
                messagebox.showerror("Error", "User ID already exists!")

        tk.Button(top, text="Save Account", command=save_to_db).pack(pady=20)