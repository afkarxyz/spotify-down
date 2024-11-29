import requests
import urllib.request
from pathlib import Path
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TYER

class SpotifyDownloaderError(Exception):
    pass

class SpotifyDownloader:
    def __init__(self):
        self.base_url = "https://spotify-down.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://spotify-down.com",
            "Referer": "https://spotify-down.com/",
        }

    def _sanitize_filename(self, filename):
        return "".join(x for x in filename if x.isalnum() or x in [' ', '-', '_']).rstrip()

    def download_track(self, spotify_url, download=True):
        try:
            metadata_response = requests.post(
                f"{self.base_url}/api/metadata", 
                params={"link": spotify_url}, 
                headers=self.headers
            )
            metadata_response.raise_for_status()
            metadata = metadata_response.json()['data']

            download_response = requests.get(
                f"{self.base_url}/api/download", 
                params={
                    "link": spotify_url,
                    "n": metadata['title'],
                    "a": metadata['artists']
                }, 
                headers=self.headers
            )
            download_response.raise_for_status()
            download_data = download_response.json()

            if not download_data['data']['success']:
                raise SpotifyDownloaderError("Download link not found")

            result = {
                "title": metadata['title'],
                "artist": metadata['artists'],
                "album": metadata['album'],
                "release_date": metadata['release_date']
            }

            if download:
                safe_filename = self._sanitize_filename(f"{metadata['artists']} - {metadata['title']}")
                mp3_path = Path(f"{safe_filename}.mp3")

                urllib.request.urlretrieve(download_data['data']['link'], mp3_path)

                cover_response = requests.get(metadata['cover_url'])
                self._add_track_metadata(mp3_path, metadata, cover_response.content)

                result['download_path'] = str(mp3_path)
            else:
                result['download_url'] = download_data['data']['link']

            return result

        except (requests.RequestException, KeyError, ValueError) as e:
            raise SpotifyDownloaderError(f"Download failed: {e}")

    def _add_track_metadata(self, mp3_path, metadata, cover_data):
        audio = ID3(mp3_path)
        
        audio.add(TIT2(encoding=3, text=metadata['title']))
        audio.add(TPE1(encoding=3, text=metadata['artists']))
        audio.add(TALB(encoding=3, text=metadata['album']))
        audio.add(TYER(encoding=3, text=metadata['release_date'][:4]))
        
        audio.add(APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=cover_data
        ))
        
        audio.save()

_downloader = SpotifyDownloader()

def download_track(spotify_url, download=True):
    return _downloader.download_track(spotify_url, download)