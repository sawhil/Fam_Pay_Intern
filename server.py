import requests
from datetime import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# Function to Call The Youtube API
# And Fetch The Data

def API():
	# Youtube API Key
	YOUTUBE_API_KEY = 'AIzaSyA9lbI0zPuK6DzhK-i4rsKgv0-y-27V60M'
	
	# Youtube Search URL to send the Request
	search_url = 'https://www.googleapis.com/youtube/v3/search'
	
	# Parameters to Be Passed with the Request
	search_params = {
		'key' : YOUTUBE_API_KEY,
		'q' : 'football',
		'part' :'snippet',
		'maxResults' : 25,
		'order' : 'date',
		'type' : 'video',
		'publishedAfter' : '2021-01-01T00:00:00Z'
	}

	# Making the Request
	r = requests.get(search_url, params = search_params)
	
	# Returning the Response Data
	return r.json()


# Creating a Flask App Object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
db = SQLAlchemy(app)

# Video title, description, publishing datetime, thumbnails URLs
class Video(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(1000), nullable = False)
	description = db.Column(db.String(5000), nullable = True)
	publishing_time = db.Column(db.DateTime)

	def __repr__(self):
		return f'<id = {self.id}, title = {self.title}, publishing_time = {self.publishing_time}>'


# Decorator for Routing Initial GET Request
@app.route('/', methods = ['GET'])
def index():
	return jsonify(API())
	# return "Hello This will be the GET API For the Server"


# Decorator for Routing Search Request
@app.route('/search', methods = ['GET'])
def search():
	return "This will return all the vids based on the search query"

if __name__ == "__main__":
	app.run(debug = True)

