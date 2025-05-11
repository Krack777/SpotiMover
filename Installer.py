import os

print("Installing installer dependencies, please wait...")

try:
    os.system("pip install colorama==0.4.6")
    os.system("pip install pathlib==1.0.1")
    os.system("pip install pyfiglet==1.0.2")
    print("Installation complete!")
except Exception as e:
    print(f"Error: {e}!")

from colorama import init, Fore, Back, Style
from pathlib import Path
import pyfiglet


code = """
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

print(f"Flag track '{flag_track['name']}' found at position {flag_index} (index {flag_index}).")

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
"""

dependencies = [
"certifi==2025.4.26",
"charset-normalizer==3.4.2",
"idna==3.10",
"python-dotenv==1.1.0",
"redis==6.0.0",
"requests==2.32.3",
"spotipy==2.25.1",
"urllib3==2.4.0",
]

init(autoreset=True)

def shortcut():
    desktop_path = Path.home() / 'Desktop'
    current_directory = os.getcwd()
    file_path = os.path.join(desktop_path, "SpotiMover.bat")
    with open(file_path, 'w') as file:
        file.write(f"""
@echo off
python {current_directory}\SpotiMover.py
pause
        """)

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + pyfiglet.figlet_format("SpotiMover Installer", font="small"))

def printI(text):
    input(text)
    logo()

def add_to_env(key, value, env_path=".env"):
    line = f"{key}={value}\n"
    with open(env_path, "a") as file:
        file.write(line)

def install():
    if os.name == 'nt':
        for i in range(len(dependencies)):
            logo()
            print(Fore.RED + f"installing {dependencies[i]}....")
            try:
                os.system(f"pip install {dependencies[i]}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            logo()
            print(Fore.RED + f"installing {dependencies[i]}....")
            try:
                os.system(f"pip3 install {dependencies[i]}")
            except Exception as e:
                print(f"Error: {e}")

def make():
    try:
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, "spotiMover.py")
        with open(file_path, 'w') as file:
            file.write(code)
    except Exception as e:
        print(f"Error: {e}")


logo()
printI("Step 1 of 7: Go to https://developer.spotify.com/dashboard/ and click create. Enter to continue...")
printI("""Step 2 of 7: Add "http://127.0.0.1:8888/callback" as Redirect URI. Enter to continue...""")
printI("""Step 3 of 7: Choose "Web API" and "Web Playback SDK" at checkboxes. Enter to continue...""")
printI("Step 4 of 7: Click Save. Enter to continue...")
ClientID = str(input("Step 5 of 7: Paste Client ID there: "))
logo()
ClientSecret = str(input("""Step 6 of 7: Click "View client secret" and paste it there: """))
logo()
TrackFlag = str(input("Step 7 of 7 Enter Track-Flag Name(all tracks after the track you selected can be moved): "))
logo()

if str(input("Dependencies wil be install in auto mode. Y to continue, N to see list and install manually: ")) == "N":
    print(dependencies)
else:
    if os.name == 'nt':
        print("Installing Python dependencies...")
        install()

logo()
if str(input("Would you like to make desktop shortcut(Only Windows)? Y to yes, N to no: ")) == "Y":
    shortcut()
logo()


print("Creating .env file, please wait...")
add_to_env("CLIENT_ID", ClientID)
add_to_env("CLIENT_SECRET", ClientSecret)
add_to_env("SPOTIPY_REDIRECT_URL", 'http://127.0.0.1:8888/callback')
add_to_env("TrackFlag", TrackFlag)
logo()
print(".env file created successfully.")


logo()
print("Creating SpotiMover.py, please wait...")
make()
logo()
print("SpotiMover.py file created successfully")
logo()
print("SpotiMover installation complete. Enjoy!")