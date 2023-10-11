from category import Category

class Song:
    def __init__(self,uri:str, title: str, artist: str, album: str, category: Category=None, title_guess: str=None,artist_guess: str=None, notes: str=None):
        self.uri = uri
        self.title = title
        self.artist = artist
        self.album = album
        self.category = category
        self.title_guess = title_guess
        self.artist_guess = artist_guess
        self.notes = notes

    def update_category(self, category):
        self.category = category.__dict__
