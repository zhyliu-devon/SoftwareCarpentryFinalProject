import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from voice_recog import main as voice_recog_main
from image_recog import process_image
from data_handler import add_food_entry
import pandas as pd
from llm import process_prompt_with_llm


def start_app():
    # Create the main application window
    root = tk.Tk()
    root.title("TraLorie")
    root.geometry("1500x1200")  # Set window size
    # Main display area
    welcome_label = tk.Label(root, text="Welcome to TraLorie", font=("Helvetica", 14))
    welcome_label.pack(pady=20)
    # Scrollable display area for chat-style interaction
    chat_frame = tk.Frame(root)
    chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    chat_canvas = tk.Canvas(chat_frame)
    chat_scrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=chat_canvas.yview)
    chat_display = tk.Frame(chat_canvas)

    chat_canvas.configure(yscrollcommand=chat_scrollbar.set)
    chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    chat_canvas.create_window((0, 0), window=chat_display, anchor="nw")

    def on_canvas_configure(event):
        chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))

    chat_display.bind("<Configure>", on_canvas_configure)

    # Function to add a chat bubble
    def add_chat_bubble(message, is_user=False, image=None):
        # Align right for user input (green bubble) and left for system response (white bubble)
        align = "e" if is_user else "w"
        bubble_color = "green" if is_user else "white"
        text_color = "white" if is_user else "black"

        bubble_frame = tk.Frame(chat_display, bg=bubble_color, padx=10, pady=5)
        bubble_frame.pack(fill=tk.NONE, pady=5, padx=10, anchor=align)

        if image:
            # Display an image in the chat bubble
            img = Image.open(image)
            img.thumbnail((200, 200))  # Resize for chat bubble
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(bubble_frame, image=photo, bg=bubble_color)
            img_label.image = photo  # Keep a reference
            img_label.pack()
        else:
            # Display text in the chat bubble
            text_label = tk.Label(
                bubble_frame,
                text=message,
                wraplength=1480,
                justify="right" if is_user else "left",
                font=("Helvetica", 14),
                bg=bubble_color,
                fg=text_color,
            )
            text_label.pack()

    # Function to handle voice input
    def handle_voice_input():
        add_chat_bubble("Listening for voice input...", is_user=True)
        voice_recog_main()
        add_chat_bubble("Voice input processed.", is_user=False)

    # Function to handle image input
    def handle_image_input():
        image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")],
        )
        if image_path:
            add_chat_bubble(image_path, is_user=True, image=image_path)
            try:
                response = process_image(image_path)
                add_chat_bubble(f"Processed image:\n{response[:500]}...", is_user=False)
            except Exception as e:
                add_chat_bubble(f"Error processing image: {e}", is_user=False)

# Function to handle text input
    def handle_text_input(event=None):
        user_text = text_input.get()
        if user_text:
            add_chat_bubble(user_text, is_user=True)
            try:
                response = process_prompt_with_llm(user_text)  # Call the process_prompt_with_llm function
                if response:
                    add_chat_bubble(f"Processed data:{response}", is_user=False)
                else:
                    add_chat_bubble("Failed to process the prompt.", is_user=False)
            except Exception as e:
                add_chat_bubble(f"Error: {e}", is_user=False)
            text_input.delete(0, tk.END)
    # Input frame
    input_frame = tk.Frame(root)
    input_frame.pack(fill=tk.X, padx=10, pady=10)

    text_input = tk.Entry(input_frame, font=("Helvetica", 14), width=80)
    text_input.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
    text_input.bind("<Return>", handle_text_input)

    submit_button = tk.Button(
        input_frame, text="Submit", font=("Helvetica", 12), command=handle_text_input
    )
    submit_button.pack(side=tk.RIGHT, padx=10)

    # Button frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

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

    # Run the application
    root.mainloop()


# To test the GUI
if __name__ == "__main__":
    start_app()
