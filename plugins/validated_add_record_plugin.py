
def register_plugin(app):
    import tkinter as tk
    from tkinter import messagebox

    def add_record():
        add_window = tk.Toplevel(app.root)
        add_window.title("Add New Record")

        labels = ["Typ", "Model", "Kusy", "Značka", "Pozícia"]
        entries = {}

        # Default values
        defaults = {
            "Kusy": "1",
            "Pozícia": "Sklad"
        }

        for i, label in enumerate(labels):
            tk.Label(add_window, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1, padx=5, pady=5)

            # Set default values if available
            if label in defaults:
                entry.insert(0, defaults[label])

            entries[label] = entry

        def save_record():
            try:
                values = [entries[label].get() for label in labels]

                # Validate numerical input for "Kusy"
                if not values[2].isdigit():
                    messagebox.showwarning("Warning", "Field 'Kusy' must be a number.")
                    return

                # Ensure all fields are filled
                if not all(values):
                    messagebox.showwarning("Warning", "All fields must be filled.")
                    return

                query = f"INSERT INTO diely ({', '.join(labels)}) VALUES (?, ?, ?, ?, ?)"
                app.db.cursor.execute(query, values)  # Corrected to use `cursor.execute`
                app.db.conn.commit()  # Commit the changes to the database
                app.refresh_table()
                messagebox.showinfo("Success", "Record added successfully.")
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error adding record: {e}")

        tk.Button(add_window, text="Save Record", command=save_record).grid(row=len(labels), columnspan=2, pady=10)

    tk.Button(app.plugin_frame, text="Add Record", command=add_record).pack(side=tk.LEFT, padx=5)
