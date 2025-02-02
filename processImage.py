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
    prompt = f"given this extracted text from an image of a receipt, what did I buy, and what are their price and quantity each? Also estimate the expiry date of each item by their names as a best before date (YYYY/MM/DD) assuming its purchased today's date, space the table properly please {user_message}"
    return call_gemini(prompt)

def getGroceries():
    return groceries

""" def get_groceries_from_image(image_path):
    if image_path is None:
        return "No image uploaded yet."
    
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    if not texts:
        return "No text detected in the image."
    
    groceries = texts[0].description
    groceries = getTable(groceries)
    return groceries """

def get_groceries_from_image(image_path):
    if image_path is None:
        return "", []

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        print("No text detected in the image.")
        return "", []

    groceries_text = texts[0].description
    groceries_text = getTable(groceries_text)
    print("Extracted text:", groceries_text)  # Debugging information

    # Extract the table from the text
    table_start = groceries_text.find("| Item")
    table_end = groceries_text.find("**Note:**")
    if table_start == -1 or table_end == -1:
        print("Table not found in the text.")
        return groceries_text, []

    table_text = groceries_text[table_start:table_end].strip()
    print("Extracted table:", table_text)  # Debugging information

    groceries = []
    lines = table_text.split('\n')
    for line in lines[2:]:  # Skip the first two lines (headings and separator)
        parts = line.split('|')
        if len(parts) >= 5:
            item = parts[1].strip()
            quantity = parts[2].strip()
            estimated_expiry_date = parts[5].strip()
            groceries.append({
                'name': item,
                'quantity': quantity,
                'expiration': estimated_expiry_date
            })
    print("Parsed groceries:", groceries)  # Debugging information
    return groceries_text, groceries


image_path = "image/receipt.jpeg"  # Replace with your image path
groceries = process_image(image_path)
groceries = getTable(groceries)
