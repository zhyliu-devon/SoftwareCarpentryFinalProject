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
    
    voice_button = tk.Button(root, text="Voice Input", font=("Helvetica", 12), command=voice_input)
    voice_button.pack(pady=10)


    # Run the application
    root.mainloop()

def voice_input():
    print("voice input")

# To test the GUI
if __name__ == "__main__":
    start_app()
