import os
import json
import requests
from google.cloud import vision
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load Google Vision API credentials
credentials_path = "gen-lang-client-0372513634-d622802d853e.json"
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Store API key securely in an environment variable
#os.environ["GEMINI_API_KEY"] = os.getenv("AIzaSyBIShnhDYlGX2uxJf3V3IIbuvs9obM4Gk8")
os.environ["GEMINI_API_KEY"] = "AIzaSyBIShnhDYlGX2uxJf3V3IIbuvs9obM4Gk8"

# Base URL for Gemini API (using gemini-1.5-flash to match your cURL request)
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={os.environ['GEMINI_API_KEY']}"

# Initialize Google Vision API client
client = vision.ImageAnnotatorClient(credentials=credentials)

groceries = "Not generated"

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
        #print(extracted_text[0].description)
        #groceries += extracted_text[0].description
        return extracted_text[0].description
    else:
        print("No text found in the image.")

def call_gemini(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error {response.status_code}: {response.text}"

def getTable(user_message):
    prompt = f"given this extracted text from an image of a receipt, what did I buy, and what are their price and quantity each? Also estimate the expiry date of each item by their names, space the table properly please {user_message}"
    return call_gemini(prompt)

def getGroceries():
    return groceries

# Example usage
image_path = "image/receipt.jpeg"  # Replace with your image path
groceries = process_image(image_path)
groceries = getTable(groceries)
