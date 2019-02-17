import sys
import os
import csv
import pyrebase

import random

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def write_data(name, water_use, co2, land_use):
    with open(os.path.join(DIR, r'dictionary.csv'), 'a') as d:
        writer = csv.writer(d, delimiter=',')
        writer.writerow(name)

    #get stats from firebase
    config = {
        "apiKey": "R0j6JfG91yeNdN1QZDPufpClbAMB5STTx2X4Z3L1",
        "authDomain": "treehacks-3750e.firebaseapp.com",
        "databaseURL": "https://treehacks-3750e.firebaseio.com",
        "storageBucket": "treehacks-3750e.appspot.com",
        "serviceAccount": 'firebase_cred.json'
        }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()

    db.child(name).child("GHG").set(float(co2))
    db.child(name).child("landUse").set(float(land_use))
    db.child(name).child("water").set(float(water_use))
    db.child(name).child("GHGscore").set(random.randint(0, 100))
    db.child(name).child("waterscore").set(random.randint(0, 100))
    db.child(name).child("landscore").set(random.randint(0, 100))
