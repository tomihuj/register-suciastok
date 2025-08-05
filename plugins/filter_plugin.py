
def register_plugin(app):
    import tkinter as tk

    def apply_filter(event=None):
        filter_text = app.filter_entry.get().strip()
        for row in app.tree.get_children():
            app.tree.delete(row)

        try:
            query = f"SELECT * FROM diely WHERE {' OR '.join(f'{col} LIKE ?' for col in app.columns)}"
            params = [f"%{filter_text}%"] * len(app.columns)
            rows = app.db.fetchall(query, params)
            for row in rows:
                app.tree.insert('', 'end', values=row)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Filter error: {e}")

    def clear_filter():
        app.filter_entry.delete(0, tk.END)
        app.refresh_table()

    filter_frame = tk.Frame(app.root)
    filter_frame.pack(fill=tk.X, pady=5)
    tk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=5)
    app.filter_entry = tk.Entry(filter_frame)
    app.filter_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    app.filter_entry.bind("<KeyRelease>", apply_filter)
    tk.Button(filter_frame, text="Clear Filter", command=clear_filter).pack(side=tk.LEFT, padx=5)
