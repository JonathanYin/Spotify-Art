import os
import requests
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
# Import SpotifyClient from spotify_client.py for Spotify API interactions
from spotify_client import SpotifyClient

def download_image(image_url):
    """
    Downloads an image from a given URL and returns the image content.
    
    Parameters:
    - image_url (str): URL of the image to download.
    
    Returns:
    - bytes: The content of the image if download is successful, None otherwise.
    """
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def upload_to_s3(image_content, bucket_name, object_name):
    """
    Uploads image content to an AWS S3 bucket if it does not already exist.
    
    Parameters:
    - image_content (bytes): The content of the image to upload.
    - bucket_name (str): The name of the S3 bucket.
    - object_name (str): The S3 object name under which the image will be stored.
    """
    s3_client = boto3.client('s3')
    try:
        # Check if the object already exists in S3
        s3_client.head_object(Bucket=bucket_name, Key=object_name)
        print(f"{object_name} already exists in S3 bucket {bucket_name}. Skipping upload.")
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            # Object does not exist, proceed with upload
            try:
                s3_client.put_object(Body=image_content, Bucket=bucket_name, Key=object_name)
                print(f"Uploaded {object_name} to S3 bucket {bucket_name}.")
            except NoCredentialsError:
                print("Credentials not available for AWS S3.")
        else:
            print(f"Error checking object existence: {e}")

def process_tracks(tracks_with_cover_art, bucket_name, playlist_id):
    """
    Processes each track, downloads its cover art, and uploads it to S3.
    
    Parameters:
    - tracks_with_cover_art (list): A list of tracks, each with cover art URL and other metadata.
    - bucket_name (str): The name of the S3 bucket for uploads.
    - playlist_id (str): Spotify playlist ID to organize cover art in S3.
    """
    for track in tracks_with_cover_art:
        image_content = download_image(track['cover_art_url'])
        if image_content:
            # Construct a unique object name based on playlist ID and track ID
            object_name = f"{playlist_id}/cover_art/{track['id']}.jpg"
            upload_to_s3(image_content, bucket_name, object_name)
        else:
            print(f"Failed to download image for track {track['name']}.")

if __name__ == "__main__":
    # Initialize SpotifyClient
    spotify_client = SpotifyClient()

    # Specify the playlist ID
    playlist_id = '3seDFtPQlYCdw0ymhWOPoq'  

    # Fetch tracks with cover art from the specified playlist
    tracks_with_cover_art = spotify_client.get_playlist_tracks_with_cover_art(playlist_id)

    # Specify the S3 bucket name
    bucket_name = 'spotify-playlist-images'
    
    # Process and upload the tracks' cover art to S3
    process_tracks(tracks_with_cover_art, bucket_name, playlist_id)
