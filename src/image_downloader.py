import os
import requests
import boto3
from botocore.exceptions import NoCredentialsError

def download_image(image_url):
    """
    Downloads an image from a given URL and returns the image content.
    """
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    return None

def upload_to_s3(image_content, bucket_name, object_name):
    """
    Uploads image content to an AWS S3 bucket.
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Body=image_content, Bucket=bucket_name, Key=object_name)
        print(f"Uploaded {object_name} to S3 bucket {bucket_name}.")
    except NoCredentialsError:
        print("Credentials not available for AWS S3.")

def process_tracks(tracks_with_cover_art, bucket_name):
    """
    Processes each track, downloads its cover art, and uploads it to S3.
    """
    for track in tracks_with_cover_art:
        image_content = download_image(track['cover_art_url'])
        if image_content:
            object_name = f"cover_art/{track['id']}.jpg"  # Example object name
            upload_to_s3(image_content, bucket_name, object_name)
        else:
            print(f"Failed to download image for track {track['name']}.")

if __name__ == "__main__":
    # Example usage
    bucket_name = 'your-s3-bucket-name'
    # Assume tracks_with_cover_art is obtained from spotify_client.py
    tracks_with_cover_art = [
        # This list should be filled with the actual data from spotify_client.py
    ]
    process_tracks(tracks_with_cover_art, bucket_name)
