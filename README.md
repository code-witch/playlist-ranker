# Requirements
- Python 3.8.x (tested on 3.11)
- python-dotenv 1.0.0
- spotipy 2.23.0

# Setup
- `pip install python-dotenv spotipy`
- Make a file named `.env` and add the variables: 
```env
SPOTIFY_ID=YOUR_APP_ID
SPOTIFY_SECRET=YOUR_SECRET
SPOTIFY_URI=http://localhost
```
# Usage
- Do the setup
- Run `python main.py`

# Guess mode
- Defaults to disabled
- Enable makes entries visable 

# Load Playlist
- need to get a spotify ID
- https://open.spotify.com/playlist/THIS_IS_THE_ID?si=IGNORE_THIS

# Data
- After loading the playlist `File>Save Progress` to save to a json file
- Before exiting the program, `File>Save Progress` to save
- Continuing from a previous session, use `File>Load Playlist` 