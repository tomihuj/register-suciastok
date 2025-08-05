
def register_plugin(app):
    import tkinter as tk
    from tkinter import messagebox, simpledialog
    import configparser
    import os
    import glob

    config_path = "config.ini"
    config = configparser.ConfigParser()

    if not os.path.exists(config_path):
        # Initialize default configuration
        config["PLUGINS"] = {}
        config["DATABASE"] = {
            "type": "sqlite",
            "host": "",
            "user": "",
            "password": "",
            "database": "local_database.db"
        }
        with open(config_path, "w") as config_file:
            config.write(config_file)
    else:
        config.read(config_path)
        if "PLUGINS" not in config:
            config["PLUGINS"] = {}
            with open(config_path, "w") as config_file:
                config.write(config_file)

    def open_settings():
        settings_window = tk.Toplevel(app.root)
        settings_window.title("Settings")

        # Plugin Management
        tk.Label(settings_window, text="Plugin Management").grid(row=0, column=0, padx=5, pady=5)
        plugin_frame = tk.Frame(settings_window)
        plugin_frame.grid(row=1, column=0, padx=5, pady=5)

        plugins = glob.glob(os.path.join("plugins", "*.py"))

        def toggle_plugin(plugin_name, button):
            current_state = config["PLUGINS"].get(plugin_name, "enabled")
            new_state = "disabled" if current_state == "enabled" else "enabled"
            config["PLUGINS"][plugin_name] = new_state
            with open(config_path, "w") as config_file:
                config.write(config_file)
            button.config(text="Enable" if new_state == "disabled" else "Disable")
            messagebox.showinfo("Settings", f"Plugin '{plugin_name}' is now {new_state}.")

        for i, plugin_path in enumerate(plugins):
            plugin_name = os.path.basename(plugin_path)
            state = config["PLUGINS"].get(plugin_name, "enabled")
            toggle_button = tk.Button(
                plugin_frame,
                text="Disable" if state == "enabled" else "Enable"
            )
            toggle_button.config(command=lambda pn=plugin_name, btn=toggle_button: toggle_plugin(pn, btn))
            tk.Label(plugin_frame, text=plugin_name).grid(row=i, column=0, padx=5, pady=5)
            toggle_button.grid(row=i, column=1, padx=5, pady=5)

        # Database Configuration
        tk.Label(settings_window, text="Database Configuration").grid(row=2, column=0, padx=5, pady=5)
        db_frame = tk.Frame(settings_window)
        db_frame.grid(row=3, column=0, padx=5, pady=5)

        labels = ["type", "host", "user", "password", "database"]
        entries = {}
        db_types = ["sqlite", "mysql", "postgresql"]

        def update_db_fields():
            db_type = entries["type"].get()
            for label in labels[1:]:
                entries[label].config(state="normal" if db_type != "sqlite" else "disabled")

        for i, label in enumerate(labels):
            tk.Label(db_frame, text=label.capitalize()).grid(row=i, column=0, padx=5, pady=5)
            if label == "type":
                db_type_var = tk.StringVar(value=config["DATABASE"].get("type", "sqlite"))
                db_type_menu = tk.OptionMenu(db_frame, db_type_var, *db_types, command=lambda _: update_db_fields())
                db_type_menu.grid(row=i, column=1, padx=5, pady=5)
                entries[label] = db_type_var
            else:
                entry = tk.Entry(db_frame, show="*" if label == "password" else "")
                entry.insert(0, config["DATABASE"].get(label, ""))
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries[label] = entry

        update_db_fields()  # Initialize fields based on current db type

        def save_db_settings():
            for label, entry in entries.items():
                config["DATABASE"][label] = entry.get() if isinstance(entry, tk.Entry) else entry.get()
            with open(config_path, "w") as config_file:
                config.write(config_file)
            messagebox.showinfo("Settings", "Database configuration saved successfully.")

        tk.Button(db_frame, text="Save Database Settings", command=save_db_settings).grid(row=len(labels), columnspan=2, pady=10)

        # Database Structure
        tk.Label(settings_window, text="Database Structure").grid(row=4, column=0, padx=5, pady=5)
        structure_frame = tk.Frame(settings_window)
        structure_frame.grid(row=5, column=0, padx=5, pady=5)

        current_structure = app.db.fetchall("PRAGMA table_info(diely)")

        def delete_column(column_name):
            messagebox.showinfo("Info", "SQLite does not support removing columns directly.")

        def edit_column(column_name, column_type):
            edit_window = tk.Toplevel(settings_window)
            edit_window.title("Edit Column")

            tk.Label(edit_window, text="Column Name:").grid(row=0, column=0, padx=5, pady=5)
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, column_name)
            name_entry.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(edit_window, text="Column Type:").grid(row=1, column=0, padx=5, pady=5)
            type_entry = tk.Entry(edit_window)
            type_entry.insert(0, column_type)
            type_entry.grid(row=1, column=1, padx=5, pady=5)

            def save_changes():
                new_name = name_entry.get()
                new_type = type_entry.get()
                if new_name != column_name or new_type != column_type:
                    messagebox.showinfo("Info", "SQLite does not support altering column names or types directly.")
                edit_window.destroy()

            tk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=2, columnspan=2, pady=10)

        for i, column in enumerate(current_structure):
            tk.Label(structure_frame, text=column[1]).grid(row=i, column=0, padx=5, pady=5)
            tk.Label(structure_frame, text=column[2]).grid(row=i, column=1, padx=5, pady=5)
            tk.Button(
                structure_frame, text="Edit",
                command=lambda col_name=column[1], col_type=column[2]: edit_column(col_name, col_type)
            ).grid(row=i, column=2, padx=5, pady=5)
            tk.Button(
                structure_frame, text="Delete",
                command=lambda col_name=column[1]: delete_column(col_name)
            ).grid(row=i, column=3, padx=5, pady=5)

        def add_column():
            column_name = simpledialog.askstring("Add Column", "Enter new column name:")
            if not column_name:
                return
            column_type = simpledialog.askstring("Add Column", "Enter column type (e.g., TEXT, INTEGER):")
            if not column_type:
                return
            try:
                query = f"ALTER TABLE diely ADD COLUMN {column_name} {column_type}"
                app.db.execute(query)
                app.refresh_table()
                messagebox.showinfo("Success", f"Column '{column_name}' added successfully.")
                settings_window.destroy()
                open_settings()
            except Exception as e:
                messagebox.showerror("Error", f"Error adding column: {e}")

        tk.Button(settings_window, text="Add Column", command=add_column).grid(row=6, column=0, pady=10)

    settings_button = tk.Button(app.plugin_frame, text="Settings", command=open_settings)
    app.register_plugin_widget(settings_button)
