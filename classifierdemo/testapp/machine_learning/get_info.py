import sys
import os
import csv

import pyrebase

def get_info(list_of_words):
    
    config = {
        "apiKey": "R0j6JfG91yeNdN1QZDPufpClbAMB5STTx2X4Z3L1",
        "authDomain": "treehacks-3750e.firebaseapp.com",
        "databaseURL": "https://treehacks-3750e.firebaseio.com",
        "storageBucket": "treehacks-3750e.appspot.com",
        "serviceAccount": "firebase_cred.json"
        }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()
    list_of_words = [x.lower() for x in list_of_words]

    co2 = 0;
    water = 0;

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

    for word in list_of_words:
        for x in data:
            if word in x:
                ind = data.index(x)
                category = data[ind][0]
                print(category)
    #              get associated from firebase
    #             print(co2)
                ghg = db.child(category).child("GHG").get().val()
    #             print(ghg)
                h2o = db.child(category).child("water").get().val()
                co2 = co2 + ghg
                water = water + h2o
                break;

    return [co2, water]
