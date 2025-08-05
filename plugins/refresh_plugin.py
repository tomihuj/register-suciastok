
def register_plugin(app):
    import tkinter as tk
    refresh_button = tk.Button(app.plugin_frame, text="Refresh Table", command=app.refresh_table)
    app.register_plugin_widget(refresh_button)
