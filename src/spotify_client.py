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

