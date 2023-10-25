import json
import random
from song import Song
# from category import Category

class API:
    def __init__(self,spotify_client):
        self.sc = spotify_client
        self.playlist = [] 
        self.spotify_playlist = []

    def load_json(self,path):
        with open(path,'r') as file:
            f = file.read()
            self.playlist = json.loads(f)

    def save_json(self,path):
        with open(path, 'w') as file:
            file.write(json.dumps(self.playlist,indent=4))

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
            print(song)

        self.shuffle()
        # might not need to return it if just setting it
        return self.playlist 


    def convert_spotify_format_to_different_format(self,song):
        position = 0
        if len(song['artists']) > 1:
            for i in range(0,len(song['artists'])):
                pass
                # put these in a hash? check over them? or just use if?
                # 88rising
                # thefatrat
                # daedo
                # just b
                # lady gaga
                # rich brian
                # dua lipa
                # anne-marie
                # yellow claw
                
                # "".replace(' ', '').lower()
                # if any of those
                #   position += 1
                # else
                #   break 

                # TODO
                # maybe check if first artist doesnt match like 88rising or something
                # so it doesnt find like bibi as a feature when theres more than 2
                # find correct artists
                # maybe use album artists? 

        self.playlist.append(Song(song['uri'],song['name'],song['artists'][position],song['album']['name']).__dict__)

    def play_song(self,song):
        self.sc.start_playback(uris=song.uri)

    def stop_song(self):
        self.sc.pause_playback()

    def shuffle(self):
        for _ in range(0,10):
            random.shuffle(self.playlist)
