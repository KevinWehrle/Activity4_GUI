import sqlite3

# Setup Databse
def setup_database():
    # Create file named 'company.db'
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID TEXT PRIMARY KEY,
            Password TEXT,
            Role TEXT
        )
    ''')
    
    # Insert default admin user
    cursor.execute('''
        INSERT OR IGNORE INTO Users (UserID, Password, Role) 
        VALUES ('admin', 'password123', 'Manager')
    ''')

    # Save changes and close the file
    conn.commit()
    conn.close()

# Verify Login for GUI
def check_login(user_id, password):
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    
    
    # Find the Role where the UserID and Password match what was typed
    cursor.execute("SELECT Role FROM Users WHERE UserID = ? AND Password = ?", (user_id, password))
    
    # fetchone() grabs the first matching result
    result = cursor.fetchone()
    conn.close()
    
    # If a match was found, return the Role. If not, return None.
    if result:
        return result[0] 
    else:
        return None

# Create New User
def create_user(new_id, new_password, new_role):
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    
    try:
        # Add new row to Users Table
        cursor.execute("INSERT INTO Users (UserID, Password, Role) VALUES (?, ?, ?)", (new_id, new_password, new_role))
        conn.commit()
        conn.close()
        return True # Success
    except sqlite3.IntegrityError:
        # This triggers if the UserID already exists (because UserID is a PRIMARY KEY)
        conn.close()
        return False # Failed