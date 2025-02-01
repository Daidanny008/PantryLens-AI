import os
import json
import requests
from google.cloud import vision
from google.oauth2 import service_account

# Load Google Vision API credentials
credentials_path = "jasonfile/gen-lang-client-0372513634-d622802d853e.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Initialize Google Vision API client
client = vision.ImageAnnotatorClient(credentials=credentials)

def process_image(image_path):
    """Extracts text information from an image using Google Vision API."""
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error.message:
        print(f"Error: {response.error.message}")
        return None

    # Extract and print detected text
    extracted_text = response.text_annotations
    if extracted_text:
        print("Extracted Text from Image:")
        print(extracted_text[0].description)
    else:
        print("No text found in the image.")

# Example usage
image_path = "image/receipt.jpeg"  # Replace with your image path
process_image(image_path)
