import cv2
import numpy as np
import requests
import boto3

# Create an S3 resource
s3 = boto3.resource('s3')

def download_image(url):
    response = requests.get(url)
    image = np.array(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image, -1)  # '-1' to read the image as is, including the alpha channel
    return image

def display_image(image):
    """Display the image using OpenCV"""
    cv2.imshow('Image', image)
    cv2.waitKey(0)  # Wait for a key press to close
    cv2.destroyAllWindows()

def upload_file_to_s3(file_name, bucket_name, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket_name: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        s3.meta.client.upload_file(file_name, bucket_name, object_name)
    except Exception as e:
        print(f"Upload failed: {e}")
        return False
    return True

if __name__ == '__main__':
    # Image URL
    file_name = '../images/test.jpeg'
    bucket_name = 'spotify-playlist-images'
    # Optionally, specify a different object name in S3
    object_name = 'test.jpg'  # You can change this to organize files in folders, etc.

    upload_successful = upload_file_to_s3(file_name, bucket_name, object_name)
    if upload_successful:
        print("Upload successful.")
    else:
        print("Upload failed.")
    
    # test_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/OpenCV_Logo_with_text_svg_version.svg/800px-OpenCV_Logo_with_text_svg_version.svg.png'
    # image = download_image(test_url)
    # display_image(image)
