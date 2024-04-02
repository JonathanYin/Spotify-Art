import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class SpotifyClient:
    def __init__(self):
        """
        Initializes the SpotifyClient with authentication details.
        """
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="playlist-read-private user-read-email"))

    def get_current_user_profile(self):
        """
        Fetches the current user's profile information from Spotify.

        Returns:
        - dict: A dictionary containing the user's profile information.
        """
        return self.sp.current_user()

    def get_playlist_tracks_with_cover_art(self, playlist_id):
        """
        Retrieves tracks from a specified playlist, including their cover art URLs.

        Parameters:
        - playlist_id (str): The Spotify ID of the playlist.

        Returns:
        - list: A list of dictionaries, each containing a track's ID, name, and cover art URL.
        """
        tracks_with_cover_art = []
        results = self.sp.playlist_items(playlist_id)
        tracks = self._get_all_items(results)
        
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

    def _get_all_items(self, initial_results):
        """
        Handles pagination for Spotify API calls that return a collection of items.

        Parameters:
        - initial_results (dict): The initial result set from a Spotify API call.

        Returns:
        - list: A comprehensive list of items, accounting for all pages of results.
        """
        items = initial_results['items']
        while initial_results['next']:
            initial_results = self.sp.next(initial_results)
            items.extend(initial_results['items'])
        return items

if __name__ == '__main__':
    spotify_client = SpotifyClient()
    
    # Example usage: Fetch and display the current user's profile information
    user_profile = spotify_client.get_current_user_profile()
    print(f"User ID: {user_profile.get('id')}")
    print(f"Display Name: {user_profile.get('display_name')}")
    print(f"Email: {user_profile.get('email')}")
    print(f"Country: {user_profile.get('country')}")

    # Example usage: Fetch and display tracks with cover art from a specific playlist
    playlist_id = '3seDFtPQlYCdw0ymhWOPoq'
    tracks_with_cover_art = spotify_client.get_playlist_tracks_with_cover_art(playlist_id)
    for track in tracks_with_cover_art:
        print(f"Track ID: {track['id']}, Name: {track['name']}, Cover Art URL: {track['cover_art_url']}")
