import openai

class ShoppingListGenerator:
    def __init__(self, gemini_api_key):
        """Initialize Gemini API for generating shopping lists."""
        openai.api_key = gemini_api_key

    def generate_shopping_list(self, dish_name, inventory):
        """Uses Gemini API to suggest missing ingredients."""
        prompt = f"""
        Given the dish "{dish_name}", list the ingredients needed. 
        Compare with the following inventory and suggest missing items:
        {inventory}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",  # Replace with Gemini model if needed
            messages=[{"role": "user", "content": prompt}]
        )

        return response["choices"][0]["message"]["content"]
