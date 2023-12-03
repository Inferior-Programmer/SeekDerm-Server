import pyrebase
import datetime
import json 
from textblob import TextBlob
from profanity_check import predict, predict_prob
import random
import numpy as np
def predicts(text):
    return predict([text])


def sigmoid(x): 
    return 1/(1 + np.exp(-x))

def stringProcess(x): 
    arr = np.array([float(i) for i in x.split(",")])
    return arr
def learnFromString(x, y, rating):
    rating = np.array([[rating]])
    xVector = stringProcess(x).reshape(1,-1)
    yVector = stringProcess(y).reshape(-1,1)
    i = 0 
    error = 10000
    while error*error > 1e-4 and i <= 5000:
        a = sigmoid(xVector @ yVector)
        errors = rating - a
        errorZ = (rating - a)*-1
        xVectorDelta = 0.1*(errorZ @ np.transpose(yVector))
        yVectorDelta = 0.1*(errorZ @ xVector)
        xVector = xVector - xVectorDelta
        yVector = yVector - np.transpose(yVectorDelta)
        error = errors[0][0]
        i += 1
    return error, xVector, yVector



def predictFromString(x, y): 
    xVector = stringProcess(x).reshape(1,-1)
    yVector = stringProcess(y).reshape(-1,1)
    val = sigmoid(xVector @ yVector)[0][0]
    return val

class UserAndAnimeDatabase():
    def __init__(self):
        firebaseConfig = {
              'apiKey': "AIzaSyCpFUAa47wOl6XK7bIpTO4Ud9WnzORMmy0",
              'authDomain': "newapps-aecbe.firebaseapp.com",
              'databaseURL': "https://newapps-aecbe-default-rtdb.firebaseio.com",
              'projectId': "newapps-aecbe",
              'storageBucket': "newapps-aecbe.appspot.com",
              'messagingSenderId': "173224452195",
              'appId': "1:173224452195:web:381075b1b54bc5f81b1856",
              'measurementId': "G-J25PFZ1FH0"

        }
        firebase = pyrebase.initialize_app(firebaseConfig)
        self.db = firebase.database()

    def login(self,user, password):
        datasets = self.db.child("Users").child(user).get()
        if(datasets.val() == None):
            return -1
        data = json.loads(json.dumps(datasets.val()))
        if(data != None and data['password'] == password): 
            return data
        else: 
            return -1
    
    
    def signup(self,user, password):
        numbah = self.db.child("userNumber").get().val()
        datasets = self.db.child("Users").child(user).get()
        print(datasets.val())
        if(datasets.val() != None):
            return -1
        dictionary = {
            "Users/" + user + '/': {
                "password": password, 
                "data": "",
                "userId": numbah 
            }
        }
        self.db.update(dictionary)
        self.db.child("userNumber").set(numbah + 1)
        return numbah 

if __name__ == '__main__':
    userdb = UserAndAnimeDatabase() 
    #print(userdb.doReview("Jeremy", "Your Lie in April", "It is a work of art that cannot be seen in this generation", 3))
    #print(userdb.signup("Jer4", "jerPass"))
    #userdb.doReview("Jer4", "Berserk", "It is a work of art that cannot be seen in this generation", 5)
    
    print(userdb.setPrediction("user2s", "anime1", 0.5))

    