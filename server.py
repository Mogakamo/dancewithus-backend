from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pickle as pkl
import firebaseDatabase

data = {}
with open("secrets.bin", "rb+") as f:
    data = pkl.load(f)

app = Flask(__name__)
CORS = CORS(app)

@app.route('/')
@cross_origin()
def home():
  return "Hello World!"

@app.route("/signup", methods=["GET", "POST"])
@cross_origin()
def index():
    if request.method == "GET":
        return jsonify({
            "Name" : "Sign Up route",
            "Input type" : "UserEmail, UserPassword, auth_key"
        })
    elif request.method == "POST":
        userEmail = request.json["userEmail"]
        userPassword = request.json["userPassword"]
        authKey = request.json["auth_key"]
        if authKey != data['AUTH_KEY']:
            return jsonify({"Error": "Unauthorized access"})
        else:
            res = firebaseDatabase.signUpUser(userEmail=userEmail, userPassword= userPassword)
            return jsonify({"status" : 1, "message": "User created successfully!", 'userDetails' : str(res)})
    else:
      return "Method Forbidden!"

@app.route("/signin", methods=["GET", "POST"])
@cross_origin()
def singin():
    if request.method == "GET":
        return jsonify({
            "Name" : "Sign In route",
            "Input type" : "UserEmail, UserPassword, auth_key"
        })
    elif request.method == "POST":
        userEmail = request.json["userEmail"]
        userPassword = request.json["userPassword"]
        authKey = request.json["auth_key"]
        if authKey != data['AUTH_KEY']:
            return jsonify({"Error": "Unauthorized access"})
        else:
            res = firebaseDatabase.signInUser(userEmail=userEmail, userPassword= userPassword)
            return jsonify({"status" : 1, "message": "User signed in successfully!", 'userDetails' : str(res)})
    else:
      return "Method Forbidden!"
    
@app.route("/createpost", methods=["GET", "POST"])
@cross_origin()
def createpost():
    if request.method == "GET":
        return jsonify({
            "Name" : "Create Post route",
            "Input type" : "User Email, post URL, post Caption, auth_key"
        })
    elif request.method == "POST":
        userEmail = request.json["userEmail"]
        postURL = request.json["postURL"]
        postCaption = request.json["postCaption"]
        authKey = request.json["auth_key"]
        if authKey != data['AUTH_KEY']:
            return jsonify({"Error": "Unauthorized access"})
        else:
            firebaseDatabase.createPost(userEmail, postURL, postCaption)
            return jsonify("Post Created!")
    else:
      return "Method Forbidden!"

@app.route('/profile', methods=["GET","POST"])
@cross_origin()
def profile():
  if request.method == "GET":
    userEmail = request.json["userEmail"]
    authKey = request.json["auth_key"]
    if authKey != data['AUTH_KEY']:
        return jsonify({"Error": "Unauthorized access"})
    else:
        res = firebaseDatabase.fetchProfile(userEmail)
        return jsonify(res)
  elif request.method == "POST":
    userEmail = request.json["userEmail"]
    profImg = request.json["profImg"]
    res = firebaseDatabase.updateProfile(userEmail, profImg)
    return jsonify(res) 
  else:
    return "Method Forbidden!"

@app.route('/follow', methods=["GET","POST"])
@cross_origin()
def follow():
  if request.method == "GET":
    userEmail = request.json["userEmail"]
    authKey = request.json["auth_key"]
    if authKey != data['AUTH_KEY']:
        return jsonify({"Error": "Unauthorized access"})
    else:
        res = firebaseDatabase.fetchFollowers(userEmail)
        return jsonify(res)
  elif request.method == "POST":
    userEmail = request.json["userEmail"]
    followEmail = request.json["followEmail"]
    res = firebaseDatabase.follow(userEmail, followEmail)
    return jsonify(res) 
  else:
    return "Method Forbidden!"
  
if __name__ == "__main__":
    app.run(
        host = "localhost",
        port = 5000,
        debug= True
    )
