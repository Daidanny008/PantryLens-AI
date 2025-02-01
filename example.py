from google.cloud import vision

def detect_text(image_path):
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    # Load the image
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Print the detected text
    if texts:
        print("Detected Text:")
        print(texts[0].description)  # The first annotation contains the full text
    else:
        print("No text found.")

    if response.error.message:
        raise Exception(f"{response.error.message}")

# Example usage
detect_text("groceryReceipt.jpg")