import ShoppingListApp

# Initialize the app with Google Gemini (Vertex AI) integration
app = ShoppingListApp(
    "client_secret_1068636668945-a24b31pr1v8p7iss82hd371kn4n9q966.apps.googleusercontent.com.json", 
    "your_google_sheet_id", 
    google_project_id="your_project_id", 
    endpoint_id="your_endpoint_id"
)

# Process an image of groceries
items, expiry = app.process_image("groceries.jpg")
print("Detected Items:", items)
print("Extracted Expiry Date:", expiry)

# Generate a shopping list for a dish
shopping_list = app.generate_shopping_list("Pasta")
print("Shopping List:", shopping_list)
