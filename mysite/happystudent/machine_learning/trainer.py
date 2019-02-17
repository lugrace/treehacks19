from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageUrlCreateEntry, ImageFileCreateEntry
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

import os

ENDPOINT = "https://westus2.api.cognitive.microsoft.com"

training_key = "329610eab2ab4d5a8dee59cadbdffe1e"
prediction_key = "3ab50f6272c747d7831a72ef493fe46c"

trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)
project = trainer.get_project("9b50491c-c381-4b9f-9e5e-ed160ec8acd2")

def delete_all_iterations():
    for iteration in trainer.get_iterations(project.id):
        trainer.delete_iteration(project.id, iteration.id)

def add_training_images(to_add):
    '''
    to_add: list of (file, tagname) tuples
    '''
    for image_file, tagname in to_add:
        add_training_image(image_file, tagname)

def add_training_images_filenames(to_add):
    '''
    to_add: list of (filename, tagname) tuples
    '''
    for filename, tagname in to_add:
        image_file = open(filename, 'rb')
        add_training_image(image_file, tagname)


def add_training_image(image_file, tagname):
    for tag in trainer.get_tags(project.id):
        if tag.name == tagname:
            add_training_image_with_tag(image_file, tag)
            return

    tag = trainer.create_tag(project.id, tagname)
    add_training_image_with_tag(image_file, tag)


def add_training_image_with_tag(image_file, tag):
    f = image_file.read()
    b = bytearray(f)

    trainer.create_images_from_files(project.id, [ImageFileCreateEntry(contents=b, tag_ids=[tag.id])])

def train_model():
    '''
    Updates the model with new training data
    '''
    iteration = trainer.train_project(project.id)
    while (iteration.status != "Completed"):
        iteration = trainer.get_iteration(project.id, iteration.id)

    trainer.update_iteration(project.id, iteration.id, is_default=True)

if __name__ == '__main__':
    base_image_url = os.path.dirname(os.path.abspath(__file__))
    files = [(base_image_url + r'/images/hummus1.jpg', 'hummus'), 
    (base_image_url + r'/images/hummus2.jpg', 'hummus'),
    (base_image_url + r'/images/hummus3.jpg', 'hummus'), 
    (base_image_url + r'/images/hummus4.jpg', 'hummus'), 
    (base_image_url + r'/images/hummus5.jpg', 'hummus'),
    (base_image_url + r'/images/hummus6.jpg', 'hummus'),
    (base_image_url + r'/images/nut.jpg', 'bar'),
    (base_image_url + r'/images/nut2.jpg', 'bar'), 
    (base_image_url + r'/images/nut3.jpg', 'bar'), 
    (base_image_url + r'/images/nut4.jpg', 'bar'),
    (base_image_url + r'/images/nut5.jpg', 'bar')]


    add_training_images_filenames(files)
    train_model()