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

# Set download = 0 to print the download URL only. Use download = 1 to download the track.
download = 0
result = download_track(song_url, download=download)
```
