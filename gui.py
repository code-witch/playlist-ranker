import tkinter as tk
from tkinter import filedialog
from category import Category
# from tkinter import ttk

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
        self.submit_button = tk.Button(GUI.root, text='Submit', command=lambda: print('submit')) # gets next song

        # Misc
        self.notes = tk.Text(GUI.root, height=4, width=40)


    def style(self):
        pass

    def start(self):
        self.init_widgets()
        self.menus()
        self.song_info(None,None)
        self.categories()
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

    def categories(self):
        options = [
            Category('1',0),
            Category('2',1),
            Category('3',2),
            Category('4',3),
            Category('5',4),
        ]
        option_dropdown = tk.OptionMenu(GUI.root, 'test', options)
        option_dropdown.pack()

    def player(self):
        pass

    def save(self):
        # TODO only select .json
        GUI.file_path = filedialog.asksaveasfilename(initialdir='.')
        print(GUI.file_path)
        GUI.api.save_json(GUI.file_path)


    def load(self):
        # TODO only select .json
        GUI.file_path = filedialog.askopenfilename(initialdir='.')
        print(GUI.file_path)
        GUI.api.load_json(GUI.file_path)
        for song in GUI.api.playlist:
            print(song)
        # print(GUI.api.playlist)

    def song_info(self, title, artist):
        # TODO maybe instead of passing it in, get it from api?
        self.title['text'] = f'Title: {title}'
        self.artist['text'] = f'Artist: {artist}'
        self.title.pack()
        self.artist.pack()



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
        
    def disable_guess_boxes(self):
        self.title_guess.pack_forget()
        self.title_entry.pack_forget()
        self.artist_guess.pack_forget()
        self.artist_entry.pack_forget()
