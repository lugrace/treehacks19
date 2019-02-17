import io
import os
from get_info import get_info

from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='C:\\Users\\eshao\\Documents\\Caltech\\treehacks2019\\treehacks19\\treehacks2019-d0ddac9f339e.json'
client = vision.ImageAnnotatorClient()

file_prefix = 'C:\\Users\\eshao\\Documents\\Caltech\\treehacks2019\\'
pic_prefix = 'C:\\Users\\eshao\\Pictures\\treehacks2019\\'

def rating(factors):
    '''
    Returns the environmental rating of a food given the significant factors
    the food has in respect to the environment.
    
    Arguments:
      - A list of factors that contribute CO2 to the environment
    
    Return Value:
      - A float score that represents the final CO2 score rating
    '''
    return 1

def print_results(food_items):
    '''
    Prints out the food items in order based on the inputed food array
    
    Arguments:
      - An array of food items (should be already sorted)
    
    Return Value:
      - None
    '''
    # Potential animation from the original location to the ranked location?
    print('Sorted from most environmentally friendly to least ' + \
          'environmentally friendly food choice')
    
    for food in food_items:
        print(list_to_string(food))
        print()

def list_to_string(lst):
    '''
    Converts a list of food descriptions into a string.
    
    Arguments:
      - A list containing food items
    
    Return Value:
      - A string containing the description of the food item
    '''
    output = ''
    for i in range(len(lst) - 1):
        output += lst[i] + ', '
    output += lst[len(lst) - 1]
    
    return output

def classify(image_name):
    '''
    Takes in an image name and return the food and the environmental effects
    each food has on the environment.
    
    Arguments:
      - Image name (e.g. 'sust.jpg')
    
    Return Value:
      - List of food objects ranked in best to worst for the environment
    '''
    file_string_name = pic_prefix + image_name
    file_name = os.path.join(os.path.dirname(__file__), file_string_name)
    
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)
    
    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    text_response = client.text_detection(image=image)
    texts = text_response.full_text_annotation
    
    print(file_name)
    '''
    print('Classifications:')
    for classification in labels:
        print(f'Description: {classification.description}, \t' + \
              f'Topicality: {classification.topicality}')
    '''
    
    # Obtaining the items of food on the menu
    pages = texts.pages
    food_items = []
    ratings = []
    
    for page in pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                words = []
                bounds = paragraph.bounding_box
                for word in paragraph.words:
                    curr_word = ""
                    for symbol in word.symbols:
                        curr_word += symbol.text
                    words.append(curr_word)
            if len(words) > 1:
                food_items.append((bounds, words))
            elif len(words) == 1:
                try:
                    num = int(words[0])
                except:
                    food_items.append((bounds, words))
                    
    # food_items:
    # (four vertices starting top left clockwise, list of words representing food)
    # raw_descriptions = []
    for food in food_items:
        # raw_descriptions.append(food[1])
        [co2, water, land] = get_info(food[1])

        # NLP to denote certain words (e.g. organic, processed, and add extra
        # to the rating or not
        factors = []
        ratings.append(rating(factors))
    
    # Low rating is good
    sorted_food = [x for _, x in sorted(zip(ratings, food_items))]
    print_results(sorted_food[1])
    
        
    
    
    
    '''
    # Prints out 1) the entire text and 2) each vertex of each word in the text
    print('Texts:')
    for text in texts:
        print(f'\n{text.description}')
        vertices = ['({},{})'.format(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        print(f'bounds: {",".join(vertices)}')
    '''