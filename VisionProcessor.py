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

