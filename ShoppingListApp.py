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

# Initialize the app
app = ShoppingListApp("credentials.json", "your_google_sheet_id", "your_gemini_api_key")

# Process an image
items, expiry = app.process_image("groceries.jpg")
print("Detected Items:", items)
print("Extracted Expiry Date:", expiry)

# Generate a shopping list
shopping_list = app.generate_shopping_list("Pasta")
print("Shopping List:", shopping_list)
