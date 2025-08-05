
# Project Documentation

## Main Script (`main.py`)

### Overview
The `main.py` script is the core of the application, providing:
- A graphical user interface (GUI) built using `tkinter`.
- Database connectivity with SQLite to manage data.
- Dynamic loading and registration of plugins.

---

### Functionality
#### **1. Database Connection**
The script automatically initializes the database based on the configuration file (`config.ini`). If the database doesn’t exist, it creates one.

#### **2. Dynamic Plugin Loading**
The application dynamically loads all plugins located in the `plugins/` directory. Plugins are registered if they contain the `register_plugin` function.

#### **3. Saving Loaded Plugins**
Loaded plugins are saved in the `config.ini` file under the `[PLUGINS]` section to avoid redundant loading.

#### **4. GUI Features**
- **Data Table**: The main window displays a table populated with data from the database.
- **Plugin Buttons**: Plugins can add their buttons and functionality to the GUI.
- **Record Count**: The total number of records is displayed.

---

### Key Classes and Methods
#### **Class `Database`**
- **`__init__`**: Initializes the SQLite database connection.
- **`create_table`**: Creates the `diely` table if it does not exist.
- **`execute`**: Executes SQL commands with parameters.
- **`fetchall`**: Retrieves all records based on an SQL query.

#### **Class `App`**
- **`__init__`**: Initializes the main GUI and loads plugins.
- **`setup_ui`**: Sets up the main window and table.
- **`load_plugins`**: Dynamically loads plugins and saves their list to `config.ini`.
- **`register_plugin_widget`**: Registers widgets (e.g., buttons) from plugins.
- **`refresh_table`**: Refreshes data in the table from the database.

---

## Plugins

### Plugin Structure
Each plugin must contain a `register_plugin` function, which integrates the plugin's functionality with the main application.

#### Example Plugin
```python
def register_plugin(app):
    import tkinter as tk
    def example_function():
        print("Plugin executed!")
    tk.Button(app.plugin_frame, text="Example Plugin", command=example_function).pack(side=tk.LEFT, padx=5)
```

---

### Available Plugins
#### **1. `column_mapping_plugin.py`**
- **Purpose**: Allows importing CSV or Excel files and mapping their columns to database columns.
- **Key Functions**:
  - **`import_file`**: Loads a file and opens the column mapping window.
  - **`open_mapping_window`**: Provides a GUI for mapping columns between the file and the database.

#### **2. `validated_add_record_plugin.py`**
- **Purpose**: Adds new records to the database with input validation.
- **Key Functions**:
  - **`add_record`**: Opens a window for adding a new record.
  - **`save_record`**: Validates inputs and saves them to the database.

#### **3. `delete_plugin.py`**
- **Purpose**: Allows the user to delete a selected record from the table.
- **Key Functions**:
  - **`delete_row`**: Deletes the selected record from the database and updates the table.

#### **4. `filter_plugin.py`**
- **Purpose**: Filters the records in the table based on user input.
- **Key Functions**:
  - **`apply_filter`**: Filters the table dynamically as the user types.
  - **`clear_filter`**: Clears the filter and restores the full table.

#### **5. `integration_plugin.py`**
- **Purpose**: Manages remote database configurations and provides a basic login system.
- **Key Functions**:
  - **`configure_remote_db`**: Configures remote database settings.
  - **`login`**: Provides a simple username/password login system.

#### **6. `refresh_plugin.py`**
- **Purpose**: Refreshes the table data from the database.
- **Key Functions**:
  - **`refresh_table`**: Updates the table to reflect the latest data.

#### **7. `settings_plugin.py`**
- **Purpose**: Manages plugins and database configurations.
- **Key Functions**:
  - **`open_settings`**: Provides options to enable/disable plugins and manage database structure.

#### **8. `backup_plugin.py`**
- **Purpose**: Creates backups of the SQLite database.
- **Key Functions**:
  - **`create_backup`**: Saves a timestamped backup of the database to a file.

#### **9. `duplicates_plugin.py`**
- **Purpose**: Identifies and removes duplicate records in the table.
- **Key Functions**:
  - **`find_duplicates`**: Detects duplicates in the database.
  - **`delete_duplicates`**: Removes all duplicates, keeping one copy of each.

#### **10. `edit_on_double_click_plugin.py`**
- **Purpose**: Allows editing of records by double-clicking a row in the table.
- **Key Functions**:
  - **`edit_record`**: Opens a window to edit the selected record.

#### **11. `export_plugin.py`**
- **Purpose**: Exports table data to a CSV file.
- **Key Functions**:
  - **`export_to_csv`**: Saves the current table data to a user-specified CSV file.

---

## Installation and Usage

### Requirements
- Python 3.x
- Libraries: `tkinter`, `sqlite3`, `configparser`, `pandas` (required for `column_mapping_plugin`), `chardet`.

### Running the Application
1. Copy the entire project, including the `plugins/` directory and the `config.ini` file.
2. Run the `main.py` script:
   ```bash
   python main.py
   ```
3. Add your custom plugins to the `plugins/` directory.

---
