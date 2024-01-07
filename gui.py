import tkinter as tk
from tkinter import ttk, filedialog

class GUI:
    root = None
    file_path = ''
    api = None

    def __init__(self,api):
        GUI.api = api
        GUI.root = tk.Tk()
        GUI.root.title('playlist ranker')

    def init_widgets(self):
        # Song Info
        self.title = tk.Label(GUI.root, text='Title:')
        self.artist = tk.Label(GUI.root, text='Artist:')

        # Guessing
        self.title_guess = tk.Label(GUI.root, text='Guess Title:')
        self.title_entry = tk.Entry(GUI.root)
        self.artist_guess = tk.Label(GUI.root, text='Guess Artist:')
        self.artist_entry = tk.Entry(GUI.root)

        # Buttons
        self.play_button = tk.Button(GUI.root, text='Play', width=10, command=lambda: GUI.api.play_song([GUI.api.current_song.uri])) # plays current song
        self.pause_button = tk.Button(GUI.root, text='Pause', width=10, command=lambda: GUI.api.stop_song()) # pauses music
        self.submit_button = tk.Button(GUI.root, text='Submit', width=10, command=lambda: self.submit_data()) # gets next song

        # Misc
        self.notes_label = tk.Label(GUI.root, text='Extra Notes')
        self.notes = tk.Text(GUI.root, height=4, width=40)
        self.option_dropdown = ttk.Combobox(GUI.root,values=self.api.categories,width=30)
        self.option_dropdown.set(self.api.categories[-1])

    def style(self):
        pass

    def position_widgets(self):
        self.title.grid(column=0, row=0)
        self.artist.grid(column=0,row=1)
        self.enable_guess_boxes()
        self.option_dropdown.grid(columnspan=3, column=0, row=2)
        self.notes_label.grid(column=0, row=3)
        self.notes.grid(columnspan=3, column=0, row=4)
        self.play_button.grid(column=0, row=5)
        self.pause_button.grid(column=1, row=5)
        self.submit_button.grid(column=2, row=5)

    def start(self):
        self.init_widgets()
        self.menus()
        self.position_widgets()
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
        self.spotify_menu.add_command(label='Create Playlist...', command =  lambda: self.create_playlist())

        self.menu_bar.add_cascade(label='Spotify', menu=self.spotify_menu)

        self.guess_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.guess_menu.add_radiobutton(label='Enable', command = lambda: self.enable_guess_boxes())
        self.guess_menu.add_radiobutton(label='Disable', command = lambda: self.disable_guess_boxes())

        self.menu_bar.add_cascade(label='Guess Mode', menu=self.guess_menu)

    def save(self):
        GUI.file_path = filedialog.asksaveasfilename(initialdir='.', filetypes=(('Json File', '*.json'),))
        print('Saving file at:', GUI.file_path)
        GUI.api.save_json(GUI.file_path)

    def load(self):
        GUI.file_path = filedialog.askopenfilename(initialdir='.',filetypes=(('Json File', '*.json'),))
        print('Loading file from:', GUI.file_path)
        GUI.api.load_json(GUI.file_path)
        for song in GUI.api.playlist:
            print(song)

        GUI.api.current_song = None
        GUI.api.set_current_song()

    def song_info(self):
        if GUI.api.current_song == None:
            return
        self.title['text'] = f'Title: {GUI.api.current_song.title}'
        self.artist['text'] = f'Artist: {GUI.api.current_song.artist}'

    def submit_data(self):
        # get GUI data
        title = self.title_entry.get()
        artist = self.artist_entry.get()
        category = GUI.api.get_category_by_name(self.option_dropdown.get())
        notes = self.notes.get('1.0','end-1c').replace('\n', ' | ')
        
        # set new data 
        GUI.api.current_song.category = category
        GUI.api.current_song.title_guess = title
        GUI.api.current_song.artist_guess = artist
        GUI.api.current_song.notes = notes

        # update everything
        GUI.api.update_song(GUI.api.current_song)
        print(GUI.api.current_song)
        print(f'{title} by {artist} Rank: {category.__dict__}')
        self.add_song_to_temp_file(GUI.api.current_song)
        
        # change song 
        GUI.api.set_current_song()
        print(GUI.api.current_song)

        # clear guess entries after submitting
        self.title_entry.delete(0, 'end')
        self.artist_entry.delete(0, 'end')
        self.notes.delete('1.0','end')

    def create_playlist(self):
        print('create playlist')
        # TODO order songs in category rank order
        # dont add any with category.rank <= 1

    def add_song_to_temp_file(self, song):
        with open('.temp', 'a', encoding='utf-8') as file:
            file.write(str(song) + '\n')

    def load_spotify_playlist_popup(self):
        popup = tk.Toplevel(GUI.root)
        popup.geometry('200x100')
        popup.title('Enter Playlist ID')
        tk.Label(popup,text='Playlist ID:').pack()
        playlist_id_entry = tk.Entry(popup)
        playlist_id_entry.pack()
        tk.Button(popup, text='Submit', command=lambda: self.get_spotify_playlist(popup,playlist_id_entry.get())).pack()
    
    def get_spotify_playlist(self,popup,playlist_id):
        GUI.api.get_entire_spotify_playlist(playlist_id)
        popup.destroy()

    def enable_guess_boxes(self):
        self.title_guess.grid(column=1,row=0)
        self.title_entry.grid(column=2,row=0)
        self.artist_guess.grid(column=1,row=1)
        self.artist_entry.grid(column=2,row=1)
        self.title['text'] = 'Title: Secret'
        self.artist['text'] = 'Artist: Secret'
        
    def disable_guess_boxes(self):
        self.title_guess.grid_forget()
        self.title_entry.grid_forget()
        self.title_entry.delete(0, 'end')

        self.artist_guess.grid_forget()
        self.artist_entry.grid_forget()
        self.artist_entry.delete(0, 'end')
        self.song_info()
