
def register_plugin(app):
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import pandas as pd

    def export_to_csv():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            rows = app.db.fetchall("SELECT * FROM diely")
            df = pd.DataFrame(rows, columns=app.columns)
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Export", f"Data exported successfully to {file_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting data: {e}")

    tk.Button(app.plugin_frame, text="Export CSV", command=export_to_csv).pack(side=tk.LEFT, padx=5)
