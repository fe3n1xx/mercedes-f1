import tkinter as tk
from tkinter import filedialog

# root window
root = tk.Tk()
root.withdraw()

# Open filedialog filtered to mp3
file_path = filedialog.askopenfilename(
    title="Select Song",
    filetypes=[("MP3 Audio Files", "*.mp3"), ("All Files", "*.*")]
)

# none if user cancelled
if file_path:
    print(file_path)
else:
    print("none")

root.destroy()