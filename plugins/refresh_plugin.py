
def register_plugin(app):
    import tkinter as tk
    tk.Button(app.plugin_frame, text="Refresh Table", command=app.refresh_table).pack(side=tk.LEFT, padx=5)
