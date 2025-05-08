# SpotiMover

SpotiMover is a simple Python script that lets you automatically move all tracks that come **after** a specific "flag track" to the **start** of a Spotify playlist. Useful for keeping your newest additions at the top.


## Installation

1. Clone the repository:

    ```
    git clone https://github.com/your-username/SpotiMover.git
    cd SpotiMover
    ```
2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```
3. Set up your environment:

    ```
    python EnvInstaller.py
    ```
You will be prompted to enter:

- `Client ID` and `Client Secret` from your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- The name of your "flag track"

---

## Usage

1. run the main script:
   
    ```
    python SpotiMover.py
    ```
    
2. Then paste the playlist URL (either `https://open.spotify.com/playlist/...` or `spotify:playlist:...`).

### The script will:

1. Authenticate with Spotify API
2. Find the flag track
3. Remove all tracks after it
4. Add them back at the top of the playlist in reverse order

---

## Important Notes

- This script modifies your playlist. Use with caution. Make a copy of playlist before running it
- Only works with playlists you own.
- The flag track is searched by partial name match (case-insensitive).

---

## Example

Your playlist contains the track "Whatever It Takes" and you set it as the flag, all tracks **after it** will be moved to the beginning of the playlist.

---

## Project Structure

    SpotiMover/
    ├── SpotiMover.py         # Main logic
    ├── EnvInstaller.py       # .env file setup
    ├── requirements.txt      # Dependencies
    └── .env                  # Auto-generated

---
