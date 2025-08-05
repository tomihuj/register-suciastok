
def register_plugin(app):
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import pandas as pd
    import chardet

    def import_file():
        file_path = filedialog.askopenfilename(
            title="Import CSV/Excel",
            filetypes=(("CSV Files", "*.csv"), ("Excel Files", "*.xls;*.xlsx"))
        )
        if not file_path:
            return

        try:
            # Automatic file type detection
            if file_path.endswith(".csv"):
                # Detect encoding for CSV
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding']
                
                # Load CSV with detected encoding
                data = pd.read_csv(file_path, encoding=encoding)
            elif file_path.endswith((".xls", ".xlsx")):
                # Load Excel file
                data = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file type. Please select a CSV or Excel file.")

            # Ensure file is not empty
            if data.empty:
                raise ValueError("The selected file is empty.")

            # Open mapping window to map columns
            open_mapping_window(data)

        except pd.errors.ParserError as e:
            messagebox.showerror("Error", f"Error parsing file: {e}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error during file import: {e}")

    def open_mapping_window(data):
        mapping_window = tk.Toplevel(app.root)
        mapping_window.title("Column Mapping")

        tk.Label(mapping_window, text="Map imported columns to database columns").grid(row=0, column=0, columnspan=2)

        db_columns = app.columns
        imported_columns = list(data.columns)
        mappings = {}

        # Display dropdowns for mapping
        for i, db_col in enumerate(db_columns):
            tk.Label(mapping_window, text=db_col).grid(row=i + 1, column=0, padx=5, pady=5)
            mapping_var = tk.StringVar()

            # Preselect column if it exists in both database and imported file
            if db_col in imported_columns:
                mapping_var.set(db_col)
            else:
                mapping_var.set(imported_columns[0] if imported_columns else "")

            dropdown = tk.OptionMenu(mapping_window, mapping_var, *imported_columns)
            dropdown.grid(row=i + 1, column=1, padx=5, pady=5)
            mappings[db_col] = mapping_var

        def apply_mapping():
            try:
                # Create a new dataframe with mapped columns
                mapped_data = pd.DataFrame()
                for db_col, mapping_var in mappings.items():
                    imported_col = mapping_var.get()
                    if imported_col in data.columns:
                        mapped_data[db_col] = data[imported_col]
                    else:
                        mapped_data[db_col] = None  # Fill unmapped columns with None

                # Insert data into the database
                for _, row in mapped_data.iterrows():
                    query = f"INSERT INTO diely ({', '.join(db_columns)}) VALUES ({', '.join(['?' for _ in db_columns])})"
                    app.db.cursor.execute(query, tuple(row))
                    app.db.conn.commit()

                app.refresh_table()
                messagebox.showinfo("Success", "Data imported successfully.")
                mapping_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error applying column mapping: {e}")

        tk.Button(mapping_window, text="Apply Mapping", command=apply_mapping).grid(row=len(db_columns) + 1, columnspan=2, pady=10)

    import_button = tk.Button(app.plugin_frame, text="Import File", command=import_file)
    app.register_plugin_widget(import_button)
