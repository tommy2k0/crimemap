from flask import Flask
from flask import render_template
from flask import request
import dbconfig
import json

if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()

@app.route("/")
def home():
    crimes = DB.get_all_crimes()   #dump-s -> dump string 
    crimes = json.dumps(crimes)   #used to convert python dictionary into JSON string for displaying with JS
    return render_template("home.html", crimes=crimes)

@app.route("/submitcrime", methods=["POST"])
def submitcrime():
    category = request.form.get("category")
    date = request.form.get("date")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    description = request.form.get("description")
    DB.add_crime(category, date, latitude, longitude, description)
    return home()

if __name__ == "__main__":
    app.run(port=5000, debug=True)