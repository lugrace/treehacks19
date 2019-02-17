import sys
import os
import csv
import pyrebase

DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

def get_info(list_of_words):
    
    list_of_words = [x.lower() for x in list_of_words]
    co2, water, land, co2_score, water_score, land_score = 0, 0, 0, 0, 0, 0;

    #get stats from firebase
    config = {
        "apiKey": "R0j6JfG91yeNdN1QZDPufpClbAMB5STTx2X4Z3L1",
        "authDomain": "treehacks-3750e.firebaseapp.com",
        "databaseURL": "https://treehacks-3750e.firebaseio.com",
        "storageBucket": "treehacks-3750e.appspot.com",
        "serviceAccount": os.path.join(BASE_DIR, r"auth\firebase_cred.json")
        }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()

    # get words and categories
    with open('dictionary.csv', newline='', encoding='utf-8', errors='ignore') as csvfile:
            data = list(csv.reader(csvfile))
            
    new_data = [];

    for x in data:
        temp = [];
        for j in x:
            if (j != ''):
                temp.append(j.lower())
        new_data.append(temp)
        
    data = new_data
    counter = 1;

    #check if each word is in a category, and increment the values if so
    for word in list_of_words:
        for x in data:
            if word in x:
                ind = data.index(x)
                category = data[ind][0].replace(" ", "")
                ghg = db.child(category).child("GHG").get().val()
                landUse = db.child(category).child("landUse").get().val()
                h2o = db.child(category).child("water").get().val()
                co2 = co2 + ghg
                water = water + h2o
                land = land + landUse
                co2_score = co2_score + (1/counter) * db.child(category).child("GHGscore").get().val() #weigh based on certainty/importance
                water_score = water_score + (1/counter) *db.child(category).child("waterscore").get().val()
                land_score = land_score + (1/counter) * db.child(category).child("landscore").get().val()
                counter = counter + 1;
                data.remove(x); #prevent double-counting an item
                break;


    return [[co2, water, land], [co2_score, water_score, land_score]]
