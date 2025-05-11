import os
import time
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URL')
track_flag = os.getenv('TrackFlag')

if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, track_flag]):
    print("Error: Required environment variables are missing.")
    exit(1)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-public playlist-modify-private playlist-read-private"
))
print("Spotify authorization successful.")

playlist_url = input("Enter playlist URL: ").strip()
if "playlist/" in playlist_url:
    playlist_id = playlist_url.split("playlist/")[-1].split("?")[0]
elif playlist_url.startswith("spotify:playlist:"):
    playlist_id = playlist_url.split(":")[-1]
else:
    playlist_id = playlist_url
print(f"Using playlist ID: {playlist_id}")

print("Loading playlist tracks...")
all_tracks = []
results = sp.playlist_items(playlist_id, fields='items.track.name,items.track.uri,next', additional_types=['track'])
while results:
    items = results['items']
    for item in items:
        track = item['track']
        if track:
            all_tracks.append({'name': track['name'], 'uri': track['uri']})
    if results['next']:
        results = sp.next(results)
    else:
        results = None
print(f"Total tracks loaded: {len(all_tracks)}")

flag_index = None
for idx, track in enumerate(all_tracks):
    if track_flag.lower() in track['name'].lower():
        flag_index = idx
        flag_track = track
        break

if flag_index is None:
    print(f"Flag track '{track_flag}' not found in the playlist.")
    exit(0)

print(f"Flag track \"{flag_track['name']}\" found at position {flag_index} (index {flag_index}).")
tracks_after = all_tracks[flag_index+1:]
if not tracks_after:
    print("No tracks after the flag track. Nothing to move.")
    exit(0)
print(f"Tracks after the flag: {len(tracks_after)}. Moving them to the beginning in reverse order.")

items_to_remove = []
for pos in range(flag_index+1, len(all_tracks)):
    uri = all_tracks[pos]['uri']
    items_to_remove.append({'uri': uri, 'positions': [pos]})

print("Removing the following tracks after the flag:")
for pos in range(flag_index+1, len(all_tracks)):
    print(f"  - {pos}: {all_tracks[pos]['name']} ({all_tracks[pos]['uri']})")
time.sleep(0.5)

for i in range(0, len(items_to_remove), 100):
    chunk = items_to_remove[i:i+100]
    sp.playlist_remove_specific_occurrences_of_items(playlist_id, chunk)
    time.sleep(0.5)

print("Track removal complete.")
print("Waiting 3 seconds before adding tracks...")
time.sleep(3)

uris_after = [track['uri'] for track in tracks_after]
uris_after_reversed = list(reversed(uris_after))
print("Adding tracks in reverse order:")
for idx, uri in enumerate(uris_after_reversed):
    print(f"  - {idx}: {all_tracks[flag_index+1 + len(tracks_after) - 1 - idx]['name']} ({uri})")

for i in range(len(uris_after_reversed), 0, -100):
    start = max(0, i-100)
    chunk = uris_after_reversed[start:i]
    sp.playlist_add_items(playlist_id, chunk, position=0)
    time.sleep(0.5)

print("Track addition complete. Playlist order updated.")
