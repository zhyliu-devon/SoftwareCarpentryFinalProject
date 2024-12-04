import gui
import data_handler

import tkinter as tk

def start_app():
    # Create the main application window
    root = tk.Tk()
    root.title("TraLorie")
    root.geometry("400x300")  # Set window size

    # Add a welcome label
    welcome_label = tk.Label(root, text="testing", font=("Helvetica", 14))
    welcome_label.pack(pady=20)

    # Run the application
    root.mainloop()

# To test the GUI
if __name__ == "__main__":
    start_app()
