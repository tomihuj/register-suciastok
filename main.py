
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import configparser
import os
import importlib.util
import glob

# Load configuration
config_path = "config.ini"
config = configparser.ConfigParser()

if not os.path.exists(config_path):
    config['DATABASE'] = {
        'type': 'sqlite',
        'host': '',
        'user': '',
        'password': '',
        'database': 'local_database.db'
    }
    with open(config_path, 'w') as config_file:
        config.write(config_file)
else:
    config.read(config_path)

# Database class
class Database:
    def __init__(self):
        db_type = config['DATABASE']['type']
        if db_type == 'sqlite':
            self.conn = sqlite3.connect(config['DATABASE']['database'])
            self.cursor = self.conn.cursor()
            self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS diely (
            Typ TEXT,
            Model TEXT,
            Kusy INTEGER,
            Značka TEXT,
            Pozícia TEXT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

    def execute(self, query, params=None):
        if not params:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        self.conn.commit()

    def fetchall(self, query, params=None):
        if not params:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# Main App Class
class App:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Modular Application")
        self.columns = ["Typ", "Model", "Kusy", "Značka", "Pozícia"]

        self.plugin_widgets = []  # Track all plugin widgets
        self.loaded_plugins = set()  # Track names of all loaded plugins
        self.setup_ui()
        self.load_plugins()
        self.refresh_table()

    def setup_ui(self):
        # Header with count of records
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(fill=tk.X)
        self.record_count_label = tk.Label(self.header_frame, text="Records: 0")
        self.record_count_label.pack()

        # Main Treeview
        self.tree = ttk.Treeview(self.root, columns=self.columns, show="headings", selectmode="browse")
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Plugin buttons frame
        self.plugin_frame = tk.Frame(self.root)
        self.plugin_frame.pack()

        # Refresh plugins button
        refresh_button = tk.Button(self.plugin_frame, text="Refresh Plugins", command=self.load_plugins)
        refresh_button.pack(side=tk.LEFT, padx=5)
        self.plugin_widgets.append(refresh_button)

    def load_plugins(self):
        plugin_path = os.path.join(os.getcwd(), "plugins")
        os.makedirs(plugin_path, exist_ok=True)
        plugin_files = glob.glob(os.path.join(plugin_path, "*.py"))

        for plugin_file in plugin_files:
            plugin_name = os.path.basename(plugin_file)[:-3]

            # Only load the plugin if it hasn't been loaded before
            if plugin_name not in self.loaded_plugins:
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "register_plugin"):
                    module.register_plugin(self)
                    self.loaded_plugins.add(plugin_name)

    def register_plugin_widget(self, widget):
        # Register a widget created by a plugin for tracking
        self.plugin_widgets.append(widget)
        widget.pack(side=tk.LEFT, padx=5)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            rows = self.db.fetchall("SELECT * FROM diely")
            for row in rows:
                self.tree.insert('', 'end', values=row)
            self.update_record_count(len(rows))
        except Exception as e:
            messagebox.showerror("Error", f"Error loading table: {e}")

    def update_record_count(self, count):
        self.record_count_label.config(text=f"Records: {count}")

# Main Program Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
