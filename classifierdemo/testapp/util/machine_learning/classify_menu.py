import io
import os
from .. import get_info

from google.cloud import vision
from google.cloud.vision import types

DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(DIR))))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= os.path.join(BASE_DIR, r"auth\treehacks2019-d0ddac9f339e.json")
client = vision.ImageAnnotatorClient()
MINIMUM_LENGTH = 20

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
        print(list_to_string(food[1]))
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

def classify_menu(image_file):
    '''
    Takes in an image name and return the food and the environmental effects
    each food has on the environment.
    
    Arguments:
      - Image name (e.g. 'sust.jpg')
    
    Return Value:
      - List of food objects ranked in best to worst for the environment
    '''
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
    counter = 0
    
    for page in pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                words = []
                bounds = paragraph.bounding_box
                for word in paragraph.words:
                    curr_word = ""
                    for symbol in word.symbols:
                        curr_word += symbol.text
                        counter += 1
                    words.append(curr_word)
            if len(words) > 1:
                food_items.append((bounds, words))
            elif len(words) == 1:
                try:
                    num = int(words[0])
                except:
                    food_items.append([bounds, words])
    
    if counter < MINIMUM_LENGTH:
        return None
    
    # food_items:
    # [(four vertices starting top left clockwise, list of words representing food)]
    ratings = []
    for i in range(len(food_items)):
        temp_food = food_items[i][1]
        ratings.append(get_info(temp_food))
    scores = []
    for rate in ratings:
        score_sum = sum(rate[1])/3
        scores.append(score_sum)

    for i in range(len(food_items)):
        food_items[i].append(scores[i])
        
    sorted_food = [x for _, x in sorted(zip(scores, food_items))]
    return sorted_food
    #print_results(sorted_food)
    
    return sorted_food
        
    
    
    
    '''
    # Prints out 1) the entire text and 2) each vertex of each word in the text
    print('Texts:')
    for text in texts:
        print(f'\n{text.description}')
        vertices = ['({},{})'.format(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        print(f'bounds: {",".join(vertices)}')
    '''
