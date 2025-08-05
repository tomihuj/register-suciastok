
def register_plugin(app):
    import tkinter as tk
    import os
    import sqlite3
    from tkinter import messagebox
    from datetime import datetime

    def create_backup():
        try:
            # Define backup file name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"backup_{timestamp}.sql"

            # Create backup directory if it doesn't exist
            backup_dir = os.path.join(os.getcwd(), "backups")
            os.makedirs(backup_dir, exist_ok=True)

            # Full path to the backup file
            backup_path = os.path.join(backup_dir, backup_file)

            # Execute SQLite backup
            with open(backup_path, "w") as backup:
                for line in app.db.conn.iterdump():
                    backup.write(f"{line}\n")  # Properly closed f-string

            messagebox.showinfo("Success", f"Backup created successfully: {backup_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error creating backup: {e}")

    tk.Button(app.plugin_frame, text="Create Backup", command=create_backup).pack(side=tk.LEFT, padx=5)
