import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "treehacks-food-recognizer-3787a7fb5f64.json"
client = vision.ImageAnnotatorClient()

def classify(image_file):
	file_name = os.path.join(
	    os.path.dirname(__file__),
	    image_file)

	with io.open(file_name, 'rb') as image_file:
	    content = image_file.read()

	image = types.Image(content=content)

	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations

	return labels

