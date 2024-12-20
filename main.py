import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from voice_recog import main as voice_recog_main
from image_recog import process_image
from data_handler import add_food_entry
import pandas as pd
from llm import process_prompt_with_llm, system_messages, add_food_from_prompt
import os
import json
import pyautogui


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
    
    def extract_from_data_base(food_name, database_filepath="data/food_database.csv"):
        try:
            food_database = pd.read_csv(database_filepath)
            food_row = food_database[food_database["food"].str.lower() == food_name.lower()]

            if not food_row.empty:
                nutrition_data = food_row.iloc[0].to_dict()
                return nutrition_data
            else:
                return None
        except FileNotFoundError:
            print(f"The file {database_filepath} was not found.")
            return None
        except Exception as e:
            print(f"An error occurred while accessing the database: {e}")
            return None
        
    def add_food_to_daily(response, daily_data_filepath="data/daily_data.csv"):

        try:
            # Load or initialize daily_data.csv
            if not os.path.exists(daily_data_filepath):
                daily_data = pd.DataFrame(columns=["date", "food", "quantity", "unit", "calories", "protein", "fat", "carbohydrates"])
            else:
                daily_data = pd.read_csv(daily_data_filepath)
            response = json.loads(response)
            food_name = response.get("food", "Unknown")
            if not food_name or food_name.lower() == "unknown":
                return "Food name is unknown. Entry not saved."
            # Append the new entry
            new_entry = {
                "date": response.get("date", pd.Timestamp.now().strftime('%Y-%m-%d')),
                "food": food_name,
                "quantity": response.get("quantity", 1),
                "unit": response.get("unit", "serving"),
                "calories": response.get("calories", 0),
                "protein": response.get("protein", 0),
                "fat": response.get("fat", 0),
                "carbohydrates": response.get("carbohydrates", 0),
            }

            daily_data = pd.concat([daily_data, pd.DataFrame([new_entry])], ignore_index=True)
            daily_data.to_csv(daily_data_filepath, index=False)

            return f"Added {new_entry['food']} to daily data."

        except Exception as e:
            return f"Error saving data: {e}"
        
    def show_statistics():
        # Temporarily overlay statistics on the chat
        stats_frame = tk.Frame(chat_frame, bg="white", relief=tk.RAISED, bd=2)
        stats_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        file_path = "data/daily_data.csv"  # Path to the CSV file

        try:
            # Load data from the CSV file
            data = pd.read_csv(file_path)

            # Filter today's data
            today = pd.Timestamp.now().strftime('%Y-%m-%d')
            data = data[data['date'] == today]

            # Remove rows with 'Unknown' or NaN food entries
            data = data[data['food'].notna() & (data['food'] != "Unknown")]

            if data.empty:
                tk.Label(stats_frame, text="No data available for today.", font=("Helvetica", 14), fg="red").pack()
                return

            # Generate a grouped bar chart
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots(figsize=(10, 8))

            x = range(len(data))  # Number of rows
            bar_width = 0.2

            nutrients = ["calories", "protein", "fat", "carbohydrates"]
            colors = ["blue", "green", "red", "orange"]

            for i, nutrient in enumerate(nutrients):
                ax.bar(
                    [pos + i * bar_width for pos in x],
                    data[nutrient],
                    bar_width,
                    label=nutrient.capitalize(),
                    color=colors[i],
                )

            ax.set_xticks([pos + (len(nutrients) - 1) * bar_width / 2 for pos in x])
            ax.set_xticklabels(data["food"], rotation=45, ha="right")

            ax.set_title("Daily Nutritional Intake by Food")
            ax.set_xlabel("Food")
            ax.set_ylabel("Amount")
            ax.legend(title="Nutrients")

            # Embed the plot into the Tkinter frame
            canvas = FigureCanvasTkAgg(fig, master=stats_frame)
            canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor='center', width=1200, height=960)
            canvas.draw()

            # Add a back button
            back_button = tk.Button(stats_frame, text="Back to Chat", font=("Helvetica", 12), command=stats_frame.destroy)
            back_button.place(relx=0.01, rely=0.01, anchor='nw')

        except FileNotFoundError:
            tk.Label(stats_frame, text="The file 'daily_data.csv' was not found.", font=("Helvetica", 14), fg="red").pack()
        except Exception as e:
            tk.Label(stats_frame, text=f"An error occurred: {e}", font=("Helvetica", 14), fg="red").pack()

    def handle_voice_input():
        print("Activating Windows Voice Typing (Win+H)...")
        pyautogui.hotkey('win', 'h') 

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
                add_chat_bubble(response, is_user=False)
                

            except Exception as e:
                add_chat_bubble(f"Error processing image: {e}", is_user=False)

# Function to handle text input
    def handle_text_input(event=None):
        user_text = text_input.get() 
        if user_text:
            add_chat_bubble(user_text, is_user=True)
            try:
                user_text = user_text + str(event)
                request_type = process_prompt_with_llm(user_text, system_messages["CheckReqType"])
                print(request_type)
                food_name = process_prompt_with_llm(user_text, system_messages["Extract Food Name"])
                nutrition_table = extract_from_data_base(food_name)
                if nutrition_table is not None:
                    user_text = user_text + "Nutrition Table from data base (Don't use if there are nutrition value before it):" + str(nutrition_table)
                    
                response = process_prompt_with_llm(user_text, system_messages["Estimate"])
                if "SavingDataset" in request_type:

                    _ = add_food_from_prompt(response) #Need a little change on yes or no
                    response = "Added the following information to the dataset: "+response
                if "SavingDaily" in request_type:

                        response = add_food_to_daily(response)


                if response:
                    add_chat_bubble(response, is_user=False)
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

    stats_button = tk.Button(
        button_frame,
        text="Show Statistics",
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
