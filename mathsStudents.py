import re
import pickle
import sklearn
import numpy
from flask import Flask, redirect, url_for, render_template, request, session
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)
app.secret_key = "1234hhhhhttttt"

@app.route("/", methods = ["POST", "GET"])
def Home():
    if request.method == "POST":
        # get values from form
        abs = 0
        if request.form["abcenses"] != '':
            abs = request.form["abcenses"]

        if request.form['sem1'] == '':
            sem1 = 0
        else:
            sem1 = int(request.form['sem1'])
        
        if request.form['sem2'] == '':
            sem2 = 0
        else:
            sem2 = int(request.form['sem2'])

        if request.form.get == "on":
            famSup = 1
        else:
            famSup = 0

        mEd = int(request.form["mEd"])
        fEd = int(request.form["fEd"])
        travel = request.form["travel"]
        study = request.form["study"]
        fails = request.form["fails"]
        health = request.form["health"]

        #store in session dict
        session["abs"] = abs
        session["sem1Input"] = sem1
        session["sem2Input"] = sem2
        session["sem1"] = sem1*0.20
        session["sem2"] = sem2*0.20
        session["famSup"] = famSup
        session["mEd"] = mEd
        session["fEd"] = fEd
        session["travel"] = travel
        session["study"] = study
        session["fails"] = fails
        session["health"] = health

        return redirect(url_for("prediction"))
    else:
        return render_template("index.html")

@app.route("/prediction")
def prediction():
    #run model on data

    myModel = pickle.load(open("model/finalized_model_maths.sav", 'rb'))

    arr = myModel.predict([[int(session["mEd"]), int(session["fEd"]),
     int(session["travel"]), int(session["study"]), int(session["fails"]),
     int(session["famSup"]), int(session["health"]),
     int(session["abs"]), int(session["sem1"]), int(session["sem2"])]])
    

    session["prediction"] = arr[0]

    if session["prediction"] < 0:
        session["prediction"] = 0
    session["prediction"] = round((session["prediction"]/20) * 100)
    return render_template("prediction.html")


if __name__ == "__main__":
    app.run()


