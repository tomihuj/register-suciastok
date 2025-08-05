
def register_plugin(app):
    import tkinter as tk
    from tkinter import messagebox

    def edit_record(event):
        selected_item = app.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No row selected for editing.")
            return

        # Fetch the current values of the selected row
        current_values = app.tree.item(selected_item[0], "values")
        if not current_values:
            messagebox.showwarning("Warning", "No data available for the selected row.")
            return

        edit_window = tk.Toplevel(app.root)
        edit_window.title("Edit Record")

        labels = ["Typ", "Model", "Kusy", "Značka", "Pozícia"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(edit_window, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, current_values[i])
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[label] = entry

        def save_changes():
            try:
                updated_values = [entries[label].get() for label in labels]

                # Validate numerical input for "Kusy"
                if not updated_values[2].isdigit():
                    messagebox.showwarning("Warning", "Field 'Kusy' must be a number.")
                    return

                # Ensure all fields are filled
                if not all(updated_values):
                    messagebox.showwarning("Warning", "All fields must be filled.")
                    return

                # Update the database
                query = (
                    "UPDATE diely "
                    "SET Typ = ?, Model = ?, Kusy = ?, Značka = ?, Pozícia = ? "
                    "WHERE Typ = ? AND Model = ? AND Kusy = ? AND Značka = ? AND Pozícia = ?"
                )
                app.db.execute(query, updated_values + list(current_values))

                app.refresh_table()
                messagebox.showinfo("Success", "Record updated successfully.")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error updating record: {e}")

        tk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=len(labels), columnspan=2, pady=10)

    # Bind double-click event to the treeview for triggering edit
    app.tree.bind("<Double-1>", edit_record)
