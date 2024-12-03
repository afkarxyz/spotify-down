import requests
from pathlib import Path
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TYER
from urllib.request import urlretrieve

class SpotifyDown:
    def __init__(self):
        self.base_url = "https://spotify-down.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/",
        }

    def _sanitize_filename(self, filename):
        return "".join(x for x in filename if x.isalnum() or x in [' ', '-', '_', ',', '.'])

    def _format_metadata(self, metadata):
        artists = metadata["artists"] if isinstance(metadata["artists"], list) else [metadata["artists"]]
        return {
            "title": metadata["title"],
            "artists": ", ".join(artists),
            "album": metadata["album"],
            "duration": f"{metadata['duration']//60000}:{(metadata['duration']//1000)%60:02d}",
            "release_date": "-".join(reversed(metadata["release_date"].split("-"))),
            "cover_url": metadata["cover_url"]
        }

    def download_track(self, spotify_url, download=1):
        try:
            download = bool(download)
            
            metadata = requests.post(f"{self.base_url}/api/metadata", 
                params={"link": spotify_url}, 
                headers=self.headers).json()["data"]
            
            formatted = self._format_metadata(metadata)
            
            download_data = requests.get(f"{self.base_url}/api/download", 
                params={"link": spotify_url, "n": metadata["title"], "a": metadata["artists"]}, 
                headers=self.headers).json()["data"]
                
            if not download_data["success"]:
                raise ValueError("Download link not found")
                
            formatted["download_url"] = download_data["link"]

            if download:
                filename = self._sanitize_filename(f"{formatted['title']} - {formatted['artists']}")
                filename = Path(f"{filename}.mp3")
                urlretrieve(download_data["link"], filename)
                
                audio = ID3(filename)
                for tag, data in [
                    (TIT2, formatted["title"]),
                    (TPE1, formatted["artists"]),
                    (TALB, formatted["album"]),
                    (TYER, formatted["release_date"][-4:])
                ]:
                    audio.add(tag(encoding=3, text=data))
                    
                audio.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover',
                    data=requests.get(formatted["cover_url"]).content))
                audio.save()
                
                formatted["download_path"] = str(filename)
                print("Download completed successfully!")
            else:
                print("\n[ Track Information ]")
                for key, value in formatted.items():
                    if key != "download_url":
                        print(f"{key.replace('_', ' ').title()}: {value}")
                print(f"Download Url: {formatted['download_url']}")

            return formatted

        except Exception as e:
            if download:
                print(f"Download failed: {e}")
            raise ValueError(f"Download failed: {e}")

def download_track(spotify_url, download=1):
    return SpotifyDown().download_track(spotify_url, download)
