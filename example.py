from spotifydown import download_track

song_url = 'https://open.spotify.com/track/5vNRhkKd0yEAg8suGBpjeY'

# Set download = 0 to print the download URL only. Use download = 1 to download the track.
download = 0
result = download_track(song_url, download=download)
