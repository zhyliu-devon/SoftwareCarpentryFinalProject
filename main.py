import gui
import data_handler

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def start_app():
    # Create the main application window
    root = tk.Tk()
    root.title("TraLorie")
    root.geometry("800x600")  # Set window size

    welcome_label = tk.Label(root, text="testing", font=("Helvetica", 14))
    welcome_label.pack(pady=20)

    display_frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2)
    display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    display_label = tk.Label(display_frame, text="Data will be displayed here.", font=("Helvetica", 12))
    display_label.pack(pady=10)


    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    
    voice_button = tk.Button(root, text="Voice Input", font=("Helvetica", 12), command=voice_input)
    voice_button.pack(pady=10)

    image_button = tk.Button(root, text="Image Input", font=("Helvetica", 12), command=image_input)
    image_button.pack(pady=10)

    # Function to show a random plot
    def show_statistics():
        # Clear the current display
        for widget in display_frame.winfo_children():
            widget.destroy()

        # Generate random data for the plot
        x = np.linspace(0, 10, 100)
        y = np.sin(x) + np.random.normal(0, 0.1, len(x))

        # Create the plot
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(x, y, label="Random Data")
        ax.set_title("Random Calorie Statistics")
        ax.set_xlabel("Time")
        ax.set_ylabel("Calories")
        ax.legend()

        # Embed the plot in the Tkinter GUI
        canvas = FigureCanvasTkAgg(fig, master=display_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Draw the canvas
        canvas.draw()


    # Function to update the display area with text
    def update_display(message):
        display_label.config(text=message)


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
