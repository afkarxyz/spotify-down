## About
A Python script that extracts download links for Spotify tracks or downloads them with embedded cover art and metadata.

### Prerequisites
```bash
pip install requests mutagen
```

### Usage
```python
from spotifydown import download_track

song_url = "https://open.spotify.com/track/YOUR_TRACK_ID"

# Set download = False to print the download URL only. Use download = True to download the track.
download = True
result = download_track(song_url, download=download)

if not download:
    print(result['download_url'])
```
