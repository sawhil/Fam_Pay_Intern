import requests
from datetime import datetime
from flask import Flask, jsonify

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
		'maxResults' : 5,
		'order' : 'date',
		'publishedAfter' : '2021-01-01T00:00:00Z'
	}

	# Making the Request
	r = requests.get(search_url, params = search_params)
	
	# Returning the Response Data
	return r.json()


# Creating a Flask App Object
app = Flask(__name__)



# Decorator for Routing Initial GET Request
@app.route('/', methods = ['GET'])
def index():
	return "Hello This will be the GET API For the Server"


# Decorator for Routing Search Request
@app.route('/search', methods = ['GET'])
def search():
	return "This will return all the vids based on the search query"

if __name__ == "__main__":
	app.run(debug = True)

