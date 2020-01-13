# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection.
# NOT WORKING
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

# identify the collection and drop any existing data for this demonstration
mars = mongo.db.mars
# mars.drop()

@app.route("/")
def index():
    mars_data = mars.find()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape.html")
def scraper():

    mars_data = scrape_mars.scrape()

    mars.insert_one(mars_data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)