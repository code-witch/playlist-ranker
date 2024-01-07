import json
import random

from song import Song
from category import Category

class API:
    def __init__(self,spotify_client):
        self.sc = spotify_client
        self.playlist = [] 
        self.spotify_playlist = []
        self.current_song = None
        self.position = 0
        self.categories = [
            Category('Perfect', 10),
            Category('Almost Perfect', 9),
            Category('Very Good', 8),
            Category('Good', 7),
            Category('Fine', 6),
            Category('Mediocre', 5),
            Category('Boring', 4),
            Category('Havent Heard and Very Good', 3),
            Category('Havent Heard and Good', 2),
            Category('Havent Heard and Bad', 1),
            Category('Bad', 0)
        ]

    def load_json(self,path):
        self.playlist = []
        with open(path,'r',encoding='utf-8') as file:
            temp_json = json.loads(file.read())
            for song in temp_json:
                if song['category'] == None:
                    category = None
                else:
                    category = self.get_category_by_name(song['category']['description'])

                self.playlist.append(Song(song['uri'],song['title'],song['artist'],song['album'], category, song['title_guess'], song['artist_guess'], song['notes']))

    def save_json(self,path):
        with open(path, 'w', encoding='utf-8') as file:
            temp_json = []
            for song in self.playlist:
                if song.category == None:
                    category = None
                else:
                    category = song.category.__dict__
                temp_json.append(song)
                temp_json[-1].category = category
                temp_json[-1] = temp_json[-1].__dict__
            
            file.write(json.dumps(temp_json,indent=4, ensure_ascii=False))

    def set_current_song(self):
        if self.current_song == None:
            self.current_song = self.get_next_song()
        elif self.current_song.category != None:
            self.position += 1
            self.current_song = self.get_next_song()

    def get_next_song(self):
        for i in range(self.position,len(self.playlist)):
            if self.playlist[i].category == None:
                self.position = i
                return self.playlist[i]

    def get_category_by_name(self,name):
        for category in self.categories:
            if category.description.lower() == name.lower():
                return category
        return None

    def update_song(self,updated_song):
        for i in range(0,len(self.playlist)):
            if self.playlist[i].uri == updated_song.uri:
                self.playlist[i] = updated_song
                break

    def get_entire_spotify_playlist(self,playlist_id):
        self.playlist = []
        self.spotify_playlist = []
        offset = 0
        total = 0
        limit = 100
        while True:
            query = self.sc.playlist_items(playlist_id,offset=offset,limit=limit,fields='total,items(track(artists.name,name,album.name,uri))')
            total = query['total']
            for song in query['items']:
                self.spotify_playlist.append(song['track'])
            if limit + offset <= total:
                offset += limit
                continue
            elif total - offset > 0:
                offset += total - offset
                continue
            break
        for song in self.spotify_playlist:
            self.playlist.append(self.convert_spotify_format_to_different_format(song))

        self.shuffle()

    def convert_spotify_format_to_different_format(self,song):
        index = 0
        excluded_artists = [
        '88rising',
        'thefatrat',
        'daedo',
        'just b',
        'lady gaga',
        'rich brian',
        'dua lipa',
        'anne-marie',
        'yellow claw'
        ]
        if len(song['artists']) > 1:
            for i in range(0,len(song['artists'])):
                for artist in excluded_artists:
                    if artist.replace(' ','').lower() == song['artists'][index]['name'].replace(' ','').lower():
                        index += 1
        return Song(song['uri'],song['name'],song['artists'][index]['name'],song['album']['name'])

    def play_song(self,uri=None):
        self.sc.start_playback(uris=uri)

    def stop_song(self):
        self.sc.pause_playback()

    def shuffle(self):
        for _ in range(0,10):
            random.shuffle(self.playlist)
