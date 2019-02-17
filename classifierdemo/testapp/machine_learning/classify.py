import os
import io
from google.cloud import vision
from google.cloud.vision import types

DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

def classify(image_file):
	'''
	Takes in an image as file object and then uses Google Vision API 
	to regonize tags associated with it.
	'''
    client = vision.ImageAnnotatorClient()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(BASE_DIR, r"auth\treehacks-food-recognizer-3787a7fb5f64.json")

    content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    return labels
