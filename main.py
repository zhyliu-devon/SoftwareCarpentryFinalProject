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

    image_button = tk.Button(root, text="Image Input", font=("Helvetica", 12), command=image_input)
    image_button.pack(pady=10)

    stats_button = tk.Button(root, text="Statistics", font=("Helvetica", 12), command=show_statistics)
    stats_button.pack(pady=10)

    # Run the application
    root.mainloop()

def voice_input():
    print("voice input")

def image_input():
    print("2")

def show_statistics():
    print("3")

# To test the GUI
if __name__ == "__main__":
    start_app()
