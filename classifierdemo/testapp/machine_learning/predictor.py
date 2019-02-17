import os
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

training_key = "329610eab2ab4d5a8dee59cadbdffe1e"
prediction_key = "3ab50f6272c747d7831a72ef493fe46c"
ENDPOINT = "https://westus2.api.cognitive.microsoft.com"

trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)
project = trainer.get_project("9b50491c-c381-4b9f-9e5e-ed160ec8acd2")
predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)

def classify_image(image_file):
	'''
	image_file: an image file opened as read bytes

	Classifies the image according to the custom vision model
	'''
	image_data = image_file.read()

	results = predictor.predict_image(project.id, image_data, custom_headers={'Content-Type': 'application/octet-stream'})

	return results

if __name__ == '__main__':
	base_image_url = os.path.dirname(os.path.abspath(__file__))
	filename = os.path.join(os.path.dirname(base_image_url), r'images/test4.jpg')

	file = open(filename, 'rb')

	results = classify_image(file)

	for p in results.predictions:
		print(p.tag_name, p.probability)
