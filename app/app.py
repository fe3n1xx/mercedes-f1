import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys
import pygame
import time
from mutagen.mp3 import MP3
import io
from mutagen.id3 import ID3
from PIL import Image, ImageTk

song_length = 0 # tot duration in sec
is_playing = False
is_paused = False
start_time = 0
pause_start = 0
current_cover_img = None

pygame.mixer.init()
# Create Window
root = tk.Tk()
root.title("Mercedes F1")
root.geometry("400x300")

# Set background colour
bg_colour = "#004146"
root.configure(bg=bg_colour)

# GET ALBUM COVER
def get_album_cover(file_path, size=(370,370)):
    global current_cover_img
    if file_path and file_path != "none":
        try:
            tags = ID3(file_path)
            # search for any APIC in the mp3 metadata
            for key in tags.keys():
                if key.startswith("APIC"):
                    image_data = tags[key].data
                    pil_image = Image.open(io.BytesIO(image_data))
                    pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
                    current_cover_img = ImageTk.PhotoImage(pil_image)
                    return current_cover_img
        except Exception as e:
            print(f"No embedded cover found: {e}")

    app_dir = os.path.dirname(__file__)
    fallback_path = os.path.join(app_dir, "..", "img", "unknown.png")
    pil_fallback = Image.open(fallback_path).resize(size, Image.Resampling.LANCZOS)
    current_cover_img = ImageTk.PhotoImage(pil_fallback)
    return current_cover_img

def set_progress(percentage):
    bar_width = progress_canvas.winfo_width()
    fill_width = (min(max(percentage, 0), 100) / 100.0) * bar_width
    progress_canvas.coords(progress_fill, 0, 0, fill_width, 6)

def play_song(file_path):
    global is_playing, is_paused, song_length, start_time

    if not file_path or file_path == "none":
        return
    
    # get total song length
    audio = MP3(file_path)
    song_length = audio.info.length

    # play the song
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    start_time = time.time()
    is_playing = True
    is_paused = False

    # upd song title label
    song_name = os.path.splitext(os.path.basename(file_path))[0]
    song_title_label.config(text=song_name)
    set_progress(0)

    cover = get_album_cover(file_path)
    if cover:
        album_label.config(image=cover)

def pause_song():
    global is_paused, start_time, pause_start

    if not is_playing:
        return
    
    if is_paused:
        pygame.mixer.music.unpause()
        start_time += (time.time() - pause_start)
        is_paused = False
    else:
        pygame.mixer.music.pause()
        pause_start = time.time()
        is_paused = True

def update_progress():
    global is_playing
    if is_playing and song_length > 0  and not is_paused:
        current_time_sec = time.time() - start_time
        if current_time_sec >= song_length:
            is_playing = False
            set_progress(100)
        else:
            percentage = (current_time_sec / song_length) * 100
            set_progress(percentage)

    root.after(100, update_progress)

current_song = "none"

def change_song():
    global current_song
    app_dir = os.path.dirname(os.path.abspath(__file__))
    library_path = os.path.join(app_dir, "library.py")

    result = subprocess.run(
        [sys.executable, library_path],
        capture_output=True,
        text=True,
    )

    chosen_file = result.stdout.strip()
    if chosen_file and chosen_file != "none":
        current_song = chosen_file
        play_song(current_song)

    return current_song

# SELECT SONG
change_songb = tk.Button(root, text="Change Song", command=change_song, bg="#018076", fg="#03BFB5")
change_songb.place(relx=0.1, rely=0.05, anchor="center")

# FUNCTIONS
def next_song():
    #
    print("Next Song")

def prev_song():
    #
    print("Previous Song")

def get_current_song():
    #
    return "Song Name Unknown"

def get_artist_name():
    #
    return "Artist Unknown"

def get_album_name():
    #
    return "Album Unknown"


# App


# Album Cover
album_frame = tk.Frame(root, bg="lightgray", bd=2, relief="sunken")
album_frame.place(relx=0.5, rely=0.38, anchor="center")

file_path = None

album_cover = get_album_cover(file_path)

album_label = tk.Label(album_frame, image=album_cover, bg="#004146")
album_label.pack()

# Progress bar (using tk.canvas instead)
progress_canvas = tk.Canvas(
    root,
    height=6,
    bg="#018076",
    highlightthickness=0
)
progress_canvas.place(relx=0.5, rely=0.69, relwidth=0.6, anchor="center")

# Create filled bar rectange
progress_fill = progress_canvas.create_rectangle(
    0, 0 , 0,6,
    fill="#038FB5",
    outline=""
)
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

# Update progress bar
update_progress()
# Keep window open
root.mainloop()