import string
from turtle import reset
import pyrebase
import pickle as pkl

config = {}
with open("secrets.bin","rb") as f:
    config = pkl.load(f)

firebase = pyrebase.initialize_app(config["FIREBASE_CONFIG"])
auth = firebase.auth()
db = firebase.database()

def signUpUser(userEmail, userPassword):
    status = False
    try:
        auth.create_user_with_email_and_password(userEmail, userPassword)
        status = True
    except Exception as e:
        return e
    if status:
        userData = {
            'userEmail' : userEmail,
            'userPassword' : userPassword,
            'followers' : ["0"],
            'following' : ["0"],
            'videos' : ["0"],
            'mont' : 0,
            'profileImage' : ""
        }
        db.child('users').child(userEmail.split('@')[0]).set(userData)
        return userData

def signInUser(userEmail, userPassword):
    status = False
    try:
        auth.sign_in_with_email_and_password(userEmail, userPassword)
        status = True
    except Exception as e:
        return e
    if status:
        userData = db.child('users').child(userEmail.split('@')[0]).get()
        return userData.val()


def createPost(userEmail, postURL, postCaption):
  userData = dict(db.child('users').child(userEmail.split('@')[0]).get().val())
  userData["videos"].append([postURL, postCaption])
  userData["mont"] += 5
  db.child('users').child(userEmail.split('@')[0]).set(userData)
  return userData

def fetchProfile(userEmail):
  userData = dict(db.child('users').child(userEmail.split('@')[0]).get().val())
  return userData

def updateProfile(userEmail, profImg):
  userData = dict(db.child('users').child(userEmail.split('@')[0]).get().val())
  userData["profileImage"] = profImg
  db.child('users').child(userEmail.split('@')[0]).set(userData)
  return userData

def fetchFollowers(userEmail):
  return dict(db.child('users').child(userEmail.split('@')[0]).child("followers").get().val())

def fetchFollowing(userEmail):
  return db.child('users').child(userEmail.split('@')[0]).child("following").get().val()

def follow(userEmail, followEmail):
  userData = dict(db.child('users').child(userEmail.split('@')[0]).get().val())
  userData["following"].append(followEmail.split('@')[0])
  db.child('users').child(userEmail.split('@')[0]).set(userData)
  followData = dict(db.child('users').child(followEmail.split('@')[0]).get().val())
  followData["followers"].append(userEmail.split('@')[0])
  db.child('users').child(followEmail.split('@')[0]).set(followData)
  return True

def fetchPosts(userEmail):
  following = tuple(fetchFollowing(userEmail))
  res = []
  for i in following:
    if i != "0":
      res.append(i)
  posts = []
  for i in res:
    posts.append(db.child('users').child(i).child('videos').get().val())
  return posts