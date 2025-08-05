
def register_plugin(app):
    import tkinter as tk
    from tkinter import messagebox

    def delete_row():
        selected_item = app.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select a row to delete.")
            return

        values = app.tree.item(selected_item, "values")
        try:
            query = f"DELETE FROM diely WHERE {app.columns[0]} = ?"
            app.db.cursor.execute(query, [values[0]])  # Corrected to use `cursor.execute`
            app.db.conn.commit()  # Commit the changes to the database
            app.refresh_table()
            messagebox.showinfo("Success", "Row deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting row: {e}")

    tk.Button(app.plugin_frame, text="Delete Row", command=delete_row).pack(side=tk.LEFT, padx=5)
