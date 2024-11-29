from spotifydown import download_track

# Example usage
song_url = "https://open.spotify.com/track/4rXtQ0AKr3gOQQW5UKZSHP"

download = True
result = download_track(song_url, download=download)

if not download:
    print(result['download_url'])