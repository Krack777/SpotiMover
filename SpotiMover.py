import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import re

def getID(link):
    match = re.search(r"playlist/([a-zA-Z0-9]+)", link)
    return match.group(1) if match else None

load_dotenv(dotenv_path='.env')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URL"),
    scope="playlist-modify-private playlist-modify-public",
))

def Find_track_position(playlist_id, track_flag):
    results = sp.playlist_tracks(playlist_id)
    for idx, item in enumerate(results['items']):
        track = item['track']
        if track_flag.lower() == track['name'].lower():
            return idx
    return None

if __name__ == "__main__":
    track_flag = os.getenv('TrackFlag')
    playlist_url = str(input("Enter playlist link: "))
    playlistID = getID(playlist_url)

    tracks = []
    offset = 0
    while True:
        response = sp.playlist_tracks(playlistID, offset=offset)
        tracks.extend(response['items'])
        if response['next'] is None:
            break
        offset += len(response['items'])

    position = Find_track_position(playlistID, track_flag)

    if position is None:
        print(f"Track '{track_flag}' not found in the playlist.")
    elif position + 1 >= len(tracks):
        print("No tracks after the flag to move.")
    else:
        tail_uris = [item['track']['uri'] for item in tracks[position+1:]]
        reversed_uris = list(reversed(tail_uris))

        for i in range(0, len(reversed_uris), 100):
            sp.playlist_remove_all_occurrences_of_items(
                playlist_id=playlistID,
                items=reversed_uris[i:i+100]
            )

        for uri in reversed_uris:
            sp.playlist_add_items(playlist_id=playlistID, items=[uri], position=0)

        print("All tracks moved successfully!")
