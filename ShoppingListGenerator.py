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
