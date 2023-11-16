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
            Category('PLACE HOLDER CHANGE ME', 5),
            Category('Boring', 4),
            Category('Havent Heard and Very Good', 3),
            Category('Havent Heard and Good', 2),
            Category('Havent Heard and Bad', 1),
            Category('Bad', 0)
        ]

    def load_json(self,path):
        with open(path,'r',encoding='utf-8') as file:
            self.playlist = json.loads(file.read())

    def save_json(self,path):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.playlist,indent=4, ensure_ascii=False))

    def set_current_song(self):
        if self.current_song == None:
            self.current_song = self.get_next_song()
        elif self.current_song['category'] != None:
            self.position += 1
            self.current_song = self.get_next_song()

    def get_next_song(self):
        for i in range(self.position,len(self.playlist)):
            if self.playlist[i]['category'] == None:
                self.position = i
                return self.playlist[i]

    def get_category_by_name(self,name):
        for category in self.categories:
            if category.description.lower() == name.lower():
                return category
        return None

    def get_entire_spotify_playlist(self,playlist_id):
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
            self.convert_spotify_format_to_different_format(song)
            # print(song)

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

        self.playlist.append(Song(song['uri'],song['name'],song['artists'][index]['name'],song['album']['name']).__dict__)

    def play_song(self,uri=None):
        self.sc.start_playback(uris=uri)

    def stop_song(self):
        self.sc.pause_playback()

    def shuffle(self):
        for _ in range(0,10):
            random.shuffle(self.playlist)
