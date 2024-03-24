import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="playlist-read-private user-read-email"))


    # Add methods to interact with the Spotify API here
    def get_current_user_profile(self):
        return self.sp.current_user()
    
    def get_playlist_tracks_with_cover_art(self, playlist_id):
        tracks_with_cover_art = []
        results = self.sp.playlist_items(playlist_id)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        
        for track in tracks:
            track_info = track['track']
            album = track_info['album']
            cover_art_url = album['images'][0]['url']  # Assuming the first image is the cover art
            tracks_with_cover_art.append({
                'id': track_info['id'],
                'name': track_info['name'],
                'cover_art_url': cover_art_url
            })
        
        return tracks_with_cover_art

if __name__ == '__main__':
    # Initialize the SpotifyClient
    spotify_client = SpotifyClient()
    
    # Fetch the current user's profile
    user_profile = spotify_client.get_current_user_profile()
    
    # Print some basic information about the user
    print(f"User ID: {user_profile.get('id')}")
    print(f"Display Name: {user_profile.get('display_name')}")
    print(f"Email: {user_profile.get('email')}")
    print(f"Country: {user_profile.get('country')}")

