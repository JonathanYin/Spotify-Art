import cv2
import numpy as np
import boto3
from collections import Counter
import matplotlib.pyplot as plt

# Initialize a boto3 client for AWS S3 access
s3_client = boto3.client('s3')

def download_image_from_s3(bucket_name, object_key):
    """
    Downloads an image from an AWS S3 bucket and converts it into a format suitable for OpenCV processing.
    
    Parameters:
    - bucket_name (str): The name of the S3 bucket.
    - object_key (str): The S3 object key where the image is stored.
    
    Returns:
    - image (numpy.ndarray): The downloaded image as a NumPy array in OpenCV format.
    """
    s3_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_content = s3_response['Body'].read()
    image_as_np_array = np.frombuffer(image_content, dtype=np.uint8)
    image = cv2.imdecode(image_as_np_array, flags=cv2.IMREAD_COLOR)
    return image

def find_dominant_colors(image, k=3):
    """
    Identifies the k dominant colors in an image using k-means clustering.
    
    Parameters:
    - image (numpy.ndarray): The image for which to find the dominant colors, in OpenCV format.
    - k (int): The number of dominant colors to identify.
    
    Returns:
    - dominant_colors_bgr (list of lists): The dominant colors found in the image, in BGR format.
    """
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centroids = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    label_counts = Counter(labels.flatten())
    common_labels = label_counts.most_common(k)
    dominant_colors = [centroids[label].tolist() for label, _ in common_labels]
    dominant_colors_bgr = [color[::-1] for color in dominant_colors]
    return dominant_colors_bgr

def visualize_colors(dominant_colors_bgr):
    """
    Visualizes the dominant colors found in an image.
    
    Parameters:
    - dominant_colors_bgr (list of lists): The dominant colors to visualize, in BGR format.
    """
    dominant_colors_rgb = [color[::-1] for color in dominant_colors_bgr]
    for color in dominant_colors_rgb:
        color_square = np.array([[[component / 255 for component in color] for _ in range(10)] for _ in range(10)])
        plt.figure(figsize=(2,2))
        plt.axis("off")
        plt.imshow(color_square)
        plt.show()

if __name__ == '__main__':
    bucket_name = 'spotify-playlist-images'
    object_key = '3seDFtPQlYCdw0ymhWOPoq/cover_art/0CPWIY1etGeJLg12CAuP4n.jpg'

    # Download the image from S3
    image = download_image_from_s3(bucket_name, object_key)

    # Find dominant colors
    dominant_colors = find_dominant_colors(image, k=3)
    
    print("Dominant colors (in BGR):", dominant_colors)

    # Visualize the dominant colors
    visualize_colors(dominant_colors)
