import io
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Kevin\AppData\Local\Programs\Python\Python37-32\treehacks\djangotest\testsite\vision\treehacks-food-recognizer-3787a7fb5f64.json"


# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()

def classify(image_file):
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Kevin\AppData\Local\Programs\Python\Python37-32\treehacks\djangotest\testsite\vision\treehacks-food-recognizer-3787a7fb5f64.json"

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

