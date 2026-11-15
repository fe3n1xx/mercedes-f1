import tkinter as tk
from tkinter import ttk
import os

# Create Window
root = tk.Tk()
root.title("Mercedes F1")
root.geometry("400x300")

# Set background colour
bg_colour = "#004146"
root.configure(bg=bg_colour)

current_song = "none"

def change_song():
    #
    return "change"

# SELECT SONG
change_song = tk.Button(root, text="Change Song", command=change_song, bg="#018076", fg="#03BFB5")
change_song.place(relx=0.1, rely=0.05, anchor="center")

# FUNCTIONS
def next_song():
    #
    print("Next Song")

def prev_song():
    #
    print("Previous Song")

def pause_song():
    #
    print("Song paused")

def get_current_song():
    #
    return "Song Name Unknown"

def get_artist_name():
    #
    return "Artist Unknown"

def get_album_name():
    #
    return "Album Unknown"

def get_album_cover():
    #
    app_dir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(app_dir, "..", "img", "unknown.png"))
# App


# Album Cover
album_frame = tk.Frame(root, bg="lightgray", bd=2, relief="sunken")
album_frame.place(relx=0.5, rely=0.38, anchor="center")

album_cover = tk.PhotoImage(file=get_album_cover())
album_cover = album_cover.zoom(3,3).subsample(2,2)

album_label = tk.Label(album_frame, image=album_cover)
album_label.pack()

# Progress bar
style = ttk.Style()
style.theme_use("default")
style.configure(
    "F1.Horizontal.TProgressbar",
    troughcolor="#018076",
    background="#03BFB5",
    bordercolor="#004146",
    lightcolor="#03BFB5",
    darkcolor="#03BFB5",
    thickness=6
)

progress_bar = ttk.Progressbar(
    root,
    style="F1.Horizontal.TProgressbar",
    orient="horizontal",
    mode="determinate",
    maximum=100,
    value=0 # Starting pctge
)

progress_bar.place(relx=0.5, rely=0.69, relwidth=0.6, anchor="center")
# Previous song button
prev_button = tk.Button(root, text="<<", command=prev_song, bg="#018076",fg="#03BFB5")
prev_button.place(relx=0.25, rely=0.85, anchor="center")
# Pause button
pause_button = tk.Button(root, text="||", command=pause_song, bg="#018076", fg="#03BFB5")
pause_button.place(relx=0.5, rely=0.85, anchor="center")
# Next button
next_button = tk.Button(root, text=">>", command=next_song, bg="#018076",fg="#03BFB5")
next_button.place(relx=0.75, rely=0.85, anchor="center")

# SONG INFORMATION TICKER: NAME, ARTIST NAME, ALBUM NAME
# Song title
song_title_label = tk.Label(root, text=get_current_song(), bg="#004146",fg="#03BFB5")
song_title_label.place(relx=0.5, rely=0.75, anchor="center")
# Artist name
artist_name_label = tk.Label(root, text=get_artist_name(), bg="#004146", fg="#03BFB5")
artist_name_label.place(relx=0.5, rely=0.775, anchor="center")
# Album name
album_name_label = tk.Label(root, text=get_album_name(), bg="#004146", fg="#03BFB5")
album_name_label.place(relx=0.5, rely=0.8, anchor="center")

# VOLUME SLIDER
# Keep window open
root.mainloop()