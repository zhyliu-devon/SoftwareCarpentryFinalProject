import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from voice_recog import trigger_voice_typing
from image_recog import encode_image
from data_handler import add_food_entry
import pandas as pd
from llm import add_food_from_prompt

def start_app():
    # Create the main application window
    root = tk.Tk()
    root.title("TraLorie")
    root.geometry("1500x1200")  # Set window size

    welcome_label = tk.Label(root, text="testing", font=("Helvetica", 14))
    welcome_label.pack(pady=20)

    display_frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2)
    display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    display_label = tk.Label(display_frame, text="Data will be displayed here.", font=("Helvetica", 12))
    display_label.pack(pady=10)


    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    

    # Function to show a random plot
    def show_statistics():
        for widget in display_frame.winfo_children():
            widget.destroy()

        try:
            data = pd.read_csv("data/food_database.csv")
            if not data.empty:
                plt.figure(figsize=(8, 4))
                data.plot(kind="bar", x="food", y="calories", legend=False, ax=plt.gca())
                plt.title("Calories by Food")
                plt.xlabel("Food")
                plt.ylabel("Calories")
                canvas = FigureCanvasTkAgg(plt.gcf(), master=display_frame)
                canvas.get_tk_widget().pack()
                canvas.draw()
            else:
                update_display("No data available for visualization!", bg_color="lightyellow")
        except Exception as e:
            update_display(f"Error displaying statistics: {e}", bg_color="lightcoral")

    # Function to update the display area with text
    def update_display(message):
        # Clear the current display
        for widget in display_frame.winfo_children():
            widget.destroy()

        # Display the message
        display_label = tk.Label(display_frame, text=message, font=("Helvetica", 14), bg="white")
        display_label.pack(pady=20)


    def handle_voice_input():
        update_display("Listening for voice input...")
        trigger_voice_typing()

    # Function to handle image input
    def handle_image_input():
        image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if image_path:
            update_display(f"Processing image: {image_path}")
            try:
                encoded_image = encode_image(image_path)
                update_display(f"Image processed successfully: {encoded_image[:50]}...")
            except Exception as e:
                update_display(f"Error processing image: {e}", bg_color="lightcoral")



    voice_button = tk.Button(button_frame, text="Voice Input", font=("Helvetica", 12), width=15, command=handle_voice_input)
    voice_button.grid(row=0, column=0, padx=10, pady=5)

    image_button = tk.Button(button_frame, text="Image Input", font=("Helvetica", 12), width=15, command=handle_image_input)
    image_button.grid(row=0, column=1, padx=10, pady=5)



    stats_button = tk.Button(button_frame, text="Statistics", font=("Helvetica", 12), width=15, command=show_statistics)
    stats_button.grid(row=0, column=2, padx=10, pady=5)

    # Run the application
    root.mainloop()

# To test the GUI
if __name__ == "__main__":
    start_app()