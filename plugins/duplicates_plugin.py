
def register_plugin(app):
    import tkinter as tk
    from tkinter import messagebox

    def find_duplicates():
        try:
            rows = app.db.fetchall("SELECT rowid, * FROM diely")
            seen = {}
            duplicates = []

            for row in rows:
                data_row = tuple(row[1:])  # Exclude rowid
                if data_row in seen:
                    duplicates.append(row[0])  # Track rowid of duplicates
                else:
                    seen[data_row] = row[0]

            duplicate_count = len(duplicates)  # Total duplicates found

            if not duplicates:
                messagebox.showinfo("Duplicates", "No duplicate rows found.")
                return

            open_duplicates_window(duplicates, duplicate_count)
        except Exception as e:
            messagebox.showerror("Error", f"Error finding duplicates: {e}")

    def open_duplicates_window(duplicates, duplicate_count):
        window = tk.Toplevel(app.root)
        window.title("Duplicates Found")

        tk.Label(window, text=f"Total duplicate rows found: {duplicate_count}").pack()
        tk.Label(window, text="Click 'Remove Duplicates' to clean up.").pack()

        def delete_duplicates():
            try:
                for rowid in duplicates:
                    query = "DELETE FROM diely WHERE rowid = ?"
                    app.db.cursor.execute(query, (rowid,))  # Corrected to use `cursor.execute`
                    app.db.conn.commit()  # Commit after executing the query

                app.refresh_table()
                messagebox.showinfo("Success", f"Removed {duplicate_count} duplicate rows, keeping one unique copy.")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting duplicates: {e}")

        tk.Button(window, text="Remove Duplicates", command=delete_duplicates).pack(pady=10)

    tk.Button(app.plugin_frame, text="Find Duplicates", command=find_duplicates).pack(side=tk.LEFT, padx=5)
