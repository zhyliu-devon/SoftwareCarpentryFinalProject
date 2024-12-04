import tkinter as tk

def start_app():
    root = tk.Tk()
    root.title("Intelligent Calorie Tracker")

    tk.Label(root, text="Welcome to the Calorie Tracker!").pack()

    root.mainloop()
