import io
import os

from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='C:\\Users\\eshao\\Documents\\Caltech\\treehacks2019\\treehacks2019-d0ddac9f339e.json'
client = vision.ImageAnnotatorClient()

file_prefix = 'C:\\Users\\eshao\\Documents\\Caltech\\treehacks2019\\'
pic_prefix = 'C:\\Users\\eshao\\Pictures\\treehacks2019\\'

file_string_name = pic_prefix + 'menu.png'
file_name = os.path.join(os.path.dirname(__file__), file_string_name)

with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

response = client.label_detection(image=image)
labels = response.label_annotations

text_response = client.text_detection(image=image)
texts = text_response.text_annotations

print(file_name)
print('Classifications:')
for classification in labels:
    print(f'Description: {classification.description}, \t' + \
          f'Topicality: {classification.topicality}')   

print('Texts:')
for text in texts:
    print(f'\n{text.description}')
    print('lol')
    vertices = ['({},{})'.format(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
    print(f'bounds: {",".join(vertices)}')