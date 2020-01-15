# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection.
# PREVIOUSLY NOT WORKING - fixed by restarting mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

# identify the collection
mars = mongo.db.mars


@app.route("/")
def index():
    # PREVIOUSLY NOT WORKING/EDITED AFTER DEADLINE  - fixed by changing .find() to .find_one(), where 
    # .find() was pulling in all documents but only one was needed
    mars_data = mars.find_one()

    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape.html")
def scraper():
    # EDITED AFTER DEADLINE - drop any existing data before new scrape
    mars.drop()
    mars_data = scrape_mars.scrape()

    mars.insert_one(mars_data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)