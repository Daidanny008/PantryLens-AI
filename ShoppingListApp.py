class ShoppingListApp:
    def __init__(self, credentials_file, spreadsheet_id, gemini_api_key):
        """Initialize all components of the shopping list app."""
        self.vision_processor = VisionProcessor()
        self.sheets_manager = GoogleSheetsManager(credentials_file, spreadsheet_id)
        self.shopping_generator = ShoppingListGenerator(gemini_api_key)

    def process_image(self, image_path):
        """Detects food items and extracts expiry dates from an image."""
        food_items = self.vision_processor.detect_objects(image_path)
        expiry_text = self.vision_processor.detect_text(image_path)

        # Store detected items in Google Sheets
        for item in food_items:
            self.sheets_manager.add_ingredient(item, expiry_text)

        return food_items, expiry_text

    def generate_shopping_list(self, dish_name):
        """Generates a shopping list based on what the user has."""
        inventory = self.sheets_manager.get_inventory()
        return self.shopping_generator.generate_shopping_list(dish_name, inventory)

from google.cloud import vision
import io

class VisionProcessor:
    def __init__(self):
        """Initialize the Google Vision API client."""
        self.client = vision.ImageAnnotatorClient()

    def detect_objects(self, image_path):
        """Detects food items in an image using object detection."""
        with io.open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.object_localization(image=image)

        detected_items = [obj.name for obj in response.localized_object_annotations]
        return detected_items

    def detect_text(self, image_path):
        """Extracts expiry date or other text from an image."""
        with io.open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)

        extracted_text = response.text_annotations[0].description if response.text_annotations else ''
        return extracted_text

import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetsManager:
    def __init__(self, credentials_file, spreadsheet_id):
        """Initialize Google Sheets API client."""
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(spreadsheet_id).sheet1

    def add_ingredient(self, name, expiry_date="Unknown", quantity=1):
        """Adds or updates an ingredient in Google Sheets."""
        data = self.sheet.get_all_records()

        for i, row in enumerate(data):
            if row["Item Name"].lower() == name.lower():
                self.sheet.update_cell(i+2, 2, row["Quantity"] + quantity)
                self.sheet.update_cell(i+2, 3, expiry_date)
                return

        # If item not found, append a new row
        self.sheet.append_row([name, quantity, expiry_date])

    def get_inventory(self):
        """Fetches all stored ingredients from Google Sheets."""
        return self.sheet.get_all_records()

from google.cloud import aiplatform

class ShoppingListGenerator:
    def __init__(self, google_project_id, endpoint_id):
        """Initialize Google Gemini (via Vertex AI) for generating shopping lists."""
        aiplatform.init(project=google_project_id, location="us-central1")
        self.endpoint = aiplatform.Endpoint(endpoint_id=endpoint_id)

    def generate_shopping_list(self, dish_name, inventory):
        """Uses Google Gemini API to suggest missing ingredients."""
        try:
            prompt = f"""
            Given the dish "{dish_name}", list the ingredients needed. 
            Compare with the following inventory and suggest missing items:
            {inventory}
            """

            # Use the Google Vertex AI endpoint (Gemini model)
            response = self.endpoint.predict(instances=[{"content": prompt}])

            # Extract the response (this depends on the API response format)
            return response.predictions[0]  # Adjust based on actual response structure
        except Exception as e:
            print(f"Error generating shopping list with Google Gemini: {e}")
            return ""


# Initialize the app
app = ShoppingListApp("client_secret_1068636668945-a24b31pr1v8p7iss82hd371kn4n9q966.apps.googleusercontent.com.json", "your_google_sheet_id", "your_gemini_api_key")

# Process an image
items, expiry = app.process_image("groceryReceipt.jpg")
print("Detected Items:", items)
print("Extracted Expiry Date:", expiry)

# Generate a shopping list
shopping_list = app.generate_shopping_list("Pasta")
print("Shopping List:", shopping_list)
