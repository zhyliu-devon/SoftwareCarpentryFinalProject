import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from voice_recog import main as voice_recog_main
from image_recog import process_image
from data_handler import add_food_entry
import pandas as pd
from llm import add_food_from_prompt
from PIL import Image, ImageTk


def start_app():
    # Create the main application window
    root = tk.Tk()
    root.title("TraLorie")
    root.geometry("1500x1200")  # Set window size

    # Main display area
    welcome_label = tk.Label(root, text="Welcome to TraLorie", font=("Helvetica", 14))
    welcome_label.pack(pady=20)

    display_frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2)
    display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Scrollable text display for output
    scrollable_text_frame = tk.Frame(display_frame)
    scrollable_text_frame.pack(fill=tk.BOTH, expand=True)

    output_scrollbar = tk.Scrollbar(scrollable_text_frame)
    output_text_widget = tk.Text(
        scrollable_text_frame,
        wrap=tk.WORD,
        font=("Helvetica", 14),
        yscrollcommand=output_scrollbar.set,
    )
    output_scrollbar.config(command=output_text_widget.yview)
    output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Clear text in the output widget
    def clear_text_widget():
        output_text_widget.config(state=tk.NORMAL)
        output_text_widget.delete("1.0", tk.END)

    # Add text to the output widget
    def add_text_to_output(message, bg_color="white"):
        output_text_widget.config(state=tk.NORMAL, bg=bg_color)
        output_text_widget.insert(tk.END, message + "\n")
        output_text_widget.config(state=tk.DISABLED)

    # Display the image in the output area
    def display_image(image_path):
        # Clear current display
        clear_text_widget()

        # Load the image and resize it
        img = Image.open(image_path)
        img.thumbnail((800, 800))  # Resize to fit within 800x800
        photo = ImageTk.PhotoImage(img)

        # Display the image
        img_label = tk.Label(display_frame, image=photo)
        img_label.image = photo  # Keep a reference to avoid garbage collection
        img_label.pack(pady=10)

    # Function to handle voice input
    def handle_voice_input():
        add_text_to_output("Listening for voice input...")
        voice_recog_main()

    # Function to handle image input
    def handle_image_input():
        image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")],
        )
        if image_path:
            display_image(image_path)  # Display the selected image
            try:
                encoded_image = process_image(image_path)
                add_text_to_output(
                    f"Image processed successfully:\n{encoded_image[:500]}...\n(Truncated Base64 String)"
                )
            except Exception as e:
                add_text_to_output(f"Error processing image: {e}", bg_color="lightcoral")

    # Function to handle text input
    def handle_text_input(event=None):
        user_text = text_input.get()
        if user_text:
            add_text_to_output(f"Processing: {user_text}")
            try:
                add_food_from_prompt(user_text)
                add_text_to_output(f"Food entry added successfully: {user_text}")
            except Exception as e:
                add_text_to_output(f"Error: {e}", bg_color="lightcoral")
            text_input.delete(0, tk.END)

    # Function to show statistics
    def show_statistics():
        # Clear the current display area
        for widget in display_frame.winfo_children():
            widget.destroy()

        try:
            # Load data from the CSV
            data = pd.read_csv("data/food_database.csv")
            if not data.empty:
                # Create a bar plot
                fig, ax = plt.subplots(figsize=(8, 6))
                data.plot(kind="bar", x="food", y="calories", legend=False, ax=ax)
                ax.set_title("Calories by Food")
                ax.set_xlabel("Food")
                ax.set_ylabel("Calories")

                # Display the plot in the GUI
                canvas = FigureCanvasTkAgg(fig, master=display_frame)
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                canvas.draw()
            else:
                add_text_to_output("No data available for visualization!", bg_color="lightyellow")
        except Exception as e:
            add_text_to_output(f"Error displaying statistics: {e}", bg_color="lightcoral")

    # Button frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Text input field
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    text_input = tk.Entry(input_frame, font=("Helvetica", 14), width=50)
    text_input.pack(side=tk.LEFT, padx=10)
    text_input.bind("<Return>", handle_text_input)  # Bind Enter key to submission

    submit_button = tk.Button(
        input_frame, text="Submit", font=("Helvetica", 12), command=handle_text_input
    )
    submit_button.pack(side=tk.RIGHT, padx=10)

    # Buttons
    voice_button = tk.Button(
        button_frame,
        text="Voice Input",
        font=("Helvetica", 12),
        width=15,
        command=handle_voice_input,
    )
    voice_button.grid(row=0, column=0, padx=10, pady=5)

    image_button = tk.Button(
        button_frame,
        text="Image Input",
        font=("Helvetica", 12),
        width=15,
        command=handle_image_input,
    )
    image_button.grid(row=0, column=1, padx=10, pady=5)

    stats_button = tk.Button(
        button_frame,
        text="Statistics",
        font=("Helvetica", 12),
        width=15,
        command=show_statistics,
    )
    stats_button.grid(row=0, column=2, padx=10, pady=5)

    # Run the application
    root.mainloop()


# To test the GUI
if __name__ == "__main__":
    start_app()
