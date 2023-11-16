import tkinter as tk
from tkinter import filedialog
from category import Category
from tkinter import ttk

import json

class GUI:
    root = None
    file_path = ''
    api = None

    def __init__(self,api):
        GUI.api = api
        GUI.root = tk.Tk()
        GUI.root.title('playlist ranker')
        GUI.root.geometry('500x500')

    def init_widgets(self):
        # song info
        self.title = tk.Label(GUI.root, text='Title:')
        self.artist = tk.Label(GUI.root, text='Artist:')

        # Guessing
        self.title_guess = tk.Label(GUI.root, text='Title:')
        self.title_entry = tk.Entry(GUI.root)
        self.artist_guess = tk.Label(GUI.root, text='Artist:')
        self.artist_entry = tk.Entry(GUI.root)

        # Buttons
        self.play_button = tk.Button(GUI.root, text='Play Song', command=lambda: print('play')) # plays current song
        self.pause_button = tk.Button(GUI.root, text='Pause Song', command=lambda: print('pause')) # pauses music
        self.submit_button = tk.Button(GUI.root, text='Submit', command=lambda: self.submit_data()) # gets next song

        # Misc
        self.notes = tk.Text(GUI.root, height=4, width=40)
        self.option_dropdown = ttk.Combobox(GUI.root,values=self.api.categories)
        self.option_dropdown.set(self.api.categories[-1])

    def style(self):
        pass

    def start(self):
        self.init_widgets()
        self.menus()
        # self.song_info(None,None)
        self.style()
        GUI.root.config(menu=self.menu_bar)
        GUI.root.mainloop()

    def menus(self):
        self.menu_bar = tk.Menu(GUI.root)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='Load Playlist...', command = lambda: self.load())
        self.file_menu.add_command(label='Save Progress...', command = lambda: self.save())

        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        self.spotify_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.spotify_menu.add_command(label='Load Playlist...', command = lambda: self.load_spotify_playlist_popup())
        self.spotify_menu.add_command(label='Create Playlist...', command =  lambda: print('create playlist'))

        self.menu_bar.add_cascade(label='Spotify', menu=self.spotify_menu)

        self.guess_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.guess_menu.add_radiobutton(label='Enable', command = lambda: self.enable_guess_boxes())
        self.guess_menu.add_radiobutton(label='Disable', command = lambda: self.disable_guess_boxes())

        self.menu_bar.add_cascade(label='Guess Mode', menu=self.guess_menu)


    def player(self):
        pass

    def save(self):
        GUI.file_path = filedialog.asksaveasfilename(initialdir='.', filetypes=(('Json File', '*.json'),))
        print(GUI.file_path)
        GUI.api.save_json(GUI.file_path)


    def load(self):
        GUI.file_path = filedialog.askopenfilename(initialdir='.',filetypes=(('Json File', '*.json'),))
        print(GUI.file_path)
        GUI.api.load_json(GUI.file_path)
        for song in GUI.api.playlist:
            print(song)

        self.api.current_song = None
        self.api.set_current_song()
        print("CURRENT SONG", self.api.current_song)
        # print(GUI.api.playlist)

    def song_info(self):
        self.title['text'] = f'Title: {self.api.current_song["title"]}'
        self.artist['text'] = f'Artist: {self.api.current_song["artist"]}'
        self.title.pack()
        self.artist.pack()

    def submit_data(self):
        title = self.title_entry.get()
        artist = self.artist_entry.get()
        category = self.api.get_category_by_name(self.option_dropdown.get()).__dict__
        
        print(f'{title} by {artist} Rank: {category}')

    def load_spotify_playlist_popup(self):
        popup = tk.Toplevel(GUI.root)
        popup.geometry('200x100')
        popup.title('Enter Playlist ID')
        tk.Label(popup,text='Playlist ID:').pack()
        playlist_id_entry = tk.Entry(popup)
        playlist_id_entry.pack()
        tk.Button(popup, text='Submit', command=lambda: self.get_spotify_playlist(popup,playlist_id_entry.get())).pack()
    
    def get_spotify_playlist(self,popup,playlist_id):
        popup.destroy()
        GUI.api.get_entire_spotify_playlist(playlist_id)



    def enable_guess_boxes(self):
        self.title_guess.pack()
        self.title_entry.pack()
        self.artist_guess.pack()
        self.artist_entry.pack()
        self.title['text'] = 'Title: Secret'
        self.artist['text'] = 'Artist: Secret'
        
    def disable_guess_boxes(self):
        self.title_guess.pack_forget()
        self.title_entry.pack_forget()
        self.artist_guess.pack_forget()
        self.artist_entry.pack_forget()
        self.song_info()
