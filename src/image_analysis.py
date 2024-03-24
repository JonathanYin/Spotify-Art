import cv2
import numpy as np
import requests

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

if __name__ == '__main__':
    # Image URL
    test_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/OpenCV_Logo_with_text_svg_version.svg/800px-OpenCV_Logo_with_text_svg_version.svg.png'
    image = download_image(test_url)
    display_image(image)
