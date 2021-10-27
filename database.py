import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyA6eRXO1BLuAZ3OTLvSwKbtj85Ow9E-gMo",
    "authDomain": "bonchbot.firebaseapp.com",
    "databaseURL": "https://bonchbot-default-rtdb.firebaseio.com",
    "projectId": "bonchbot",
    "storageBucket": "bonchbot.appspot.com",
    "messagingSenderId": "25320630490",
    "appId": "1:25320630490:web:c51273f6cf9e7a7fc3dde3"
    }
firebase = pyrebase.initialize_app(firebaseConfig)
db= firebase.database()

def addUser(user_id, login, password):
    data = {
        "login": login,
        "password": password,
        "subscription": "2 mounth"
    }
    db.child("Users").child(user_id).set(data)