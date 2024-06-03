import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import parcel_calculator
from create_database import save_parcel_details  # Ensure this import matches your actual module

class ParcelCalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Parcel Calculator")
        master.configure(bg="cyan")  # Set background color

        # Define colors
        label_bg = "cyan"
        entry_bg = "#ffffff"
        button_bg = "#007BFF"
        button_fg = "#ffffff"

        # Create length input label and entry field
        self.length_label = tk.Label(master, text="Length (cm):", bg=label_bg)
        self.length_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.length_entry = tk.Entry(master, bg=entry_bg)
        self.length_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Create width input label and entry field
        self.width_label = tk.Label(master, text="Width (cm):", bg=label_bg)
        self.width_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.width_entry = tk.Entry(master, bg=entry_bg)
        self.width_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Create height input label and entry field
        self.height_label = tk.Label(master, text="Height (cm):", bg=label_bg)
        self.height_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.height_entry = tk.Entry(master, bg=entry_bg)
        self.height_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Create weight input label and entry field
        self.weight_label = tk.Label(master, text="Weight (kg):", bg=label_bg)
        self.weight_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.weight_entry = tk.Entry(master, bg=entry_bg)
        self.weight_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Create calculate button
        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate_price, bg=button_bg, fg=button_fg)
        self.calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Create price label
        self.price_label = tk.Label(master, text="", bg=label_bg)
        self.price_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Create save button
        self.save_button = tk.Button(master, text="Save Data", command=self.save_data, bg=button_bg, fg=button_fg)
        self.save_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Configure grid weights
        for i in range(7):
            master.grid_rowconfigure(i, weight=1)
        for j in range(2):
            master.grid_columnconfigure(j, weight=1)

        # Create the database and table if they don't exist
        self.create_database_and_table_if_not_exists()

    def create_database_and_table_if_not_exists(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="")
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS Lelemove_System")
            cursor.execute("USE Lelemove_System")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS parcel_data (
                    item_id INT AUTO_INCREMENT PRIMARY KEY,
                    item_height DECIMAL(10, 2),
                    item_width DECIMAL(10, 2),
                    item_length DECIMAL(10, 2),
                    item_volume DECIMAL(15, 2),
                    item_price DECIMAL(10, 2)
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            messagebox.showerror("Database Error", f"Error creating database/table: {e}")

    def calculate_price(self):
        try:
            length = float(self.length_entry.get())
            width = float(self.width_entry.get())
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            
            price = parcel_calculator.calculate_price(length, width, height, weight)
            self.price_label.config(text="The price of your parcel is: $" + str(price))
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for dimensions and weight.")

    def save_data(self):
        try:
            length = float(self.length_entry.get())
            width = float(self.width_entry.get())
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            volume = length * width * height
            price = parcel_calculator.calculate_price(length, width, height, weight)
            
            # Connect to MySQL database
            cnx = mysql.connector.connect(user='root', password='', host='localhost', database='Lelemove_System')
            cursor = cnx.cursor()

            # Insert data into database
            add_data = ("INSERT INTO parcel_data "
                        "(item_height, item_width, item_length, item_volume, item_price) "
                        "VALUES (%s, %s, %s, %s, %s)")
            data = (height, width, length, volume, price)
            cursor.execute(add_data, data)

            # Commit data to database
            cnx.commit()

            # Close cursor and connection
            cursor.close()
            cnx.close()

            save_parcel_details(length, width, height, weight, price)

            messagebox.showinfo("Success", "Data saved successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for dimensions and weight.")

# Run the GUI
root = tk.Tk()
parcel_calculator_gui = ParcelCalculatorGUI(root)
root.mainloop()
