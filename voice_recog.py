import tkinter as tk
import pyautogui
import time
import ctypes


def trigger_voice_typing():
    """
    Triggers Windows Voice Typing using the Win+H shortcut.
    """
    print("Activating Windows Voice Typing (Win+H)...")
    pyautogui.hotkey('win', 'h')  # Simulates Win+H key press


def create_gui():
    """
    Creates a GUI with a text area that is auto-selected for Windows Voice Typing.
    """
    def on_window_open(event):
        """
        Focus the text widget and trigger voice typing.
        """
        text_area.focus_set()
        trigger_voice_typing()

    # Initialize the Tkinter GUI
    root = tk.Tk()
    root.title("Voice Typing Interface")
    root.geometry("600x400")  # Set the window size

    # Create a text area
    text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 12))
    text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Bind the opening of the window to trigger voice typing
    root.bind("<Map>", on_window_open)

    # Start the GUI main loop
    root.mainloop()


def is_windows_active():
    """
    Checks if the system is running Windows.
    """
    return ctypes.windll.kernel32.GetVersion() < 0x80000000


def main():
    if not is_windows_active():
        print("This script only works on Windows.")
        return

    create_gui()


if __name__ == "__main__":
    main()
