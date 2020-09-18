from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from mars_data_scrape import mars_scrape



# Initiate App
app = Flask(__name__)

# Connect to the Database
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/MissionToMars_DB"
mongo = PyMongo(app)

# Define Routes
@app.route('/')
def index():
	listings=mongo.db.mission_to_mars_data.find_one()
	return render_template('index.html', listings=listings)
	
	
@app.route('/scrape')
def scraper():
	collection=mongo.db.mission_to_mars_data
	post=mars_scrape()
	collection.update_one({}, post, upsert=True)
	return redirect('/', code=302)
	
	
if __name__ == '__main__':
	app.run(debug=True)
