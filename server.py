import requests
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import json



# Creating a Flask App Object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
db = SQLAlchemy(app)

# Video title, description, publishing datetime, thumbnails URLs
class Video(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(1000), nullable = False)
	description = db.Column(db.String(5000))
	thumbnail_url = db.Column(db.String(1000), nullable = False)
	publishing_time = db.Column(db.DateTime)
	def __repr__(self):
		return f'<id = {self.id}, title = {self.title}, publishing_time = {self.publishing_time}>'



# Function to Call The Youtube API
# And Fetch The Data
def YT_API():
	print("called YT_API")
	# Youtube API Key
	YOUTUBE_API_KEY = 'AIzaSyD7kQxHDlVc8KlQ7Xp1pPeYhzPuaCtBiNs'
	
	# Youtube Search URL to send the Request
	search_url = 'https://www.googleapis.com/youtube/v3/search'
	time_now = datetime.now()
	last_req_time = time_now - timedelta(seconds=60)
	req_time = last_req_time.replace(microsecond=0).isoformat()+'Z'
	# Parameters to Be Passed with the Request
	search_params = {
		'key' : YOUTUBE_API_KEY,
		'q' : 'cricket',
		'part' :'snippet',
		'maxResults' : 5,
		'order' : 'date',
		'type' : 'video',
		'publishedAfter' : req_time
	}

	# Making the Request
	# r = requests.get(search_url, params = search_params)
	# results = r.json()['items']

	# for result in results:
	# 	video_title = result['snippet']['title']
	# 	video_description = result['snippet']['description']
	# 	video_thumbnail_url = result['snippet']['thumbnails']['medium']['url']
	# 	video_publishing_time = result['snippet']['publishedAt']
	# 	video_publishing_time = datetime.strptime(video_publishing_time, '%Y-%d-%mT%I:%M:%SZ')
	# 	new_video = Video(title = video_title, description = video_description, thumbnail_url = video_thumbnail_url, publishing_time = video_publishing_time)
	# 	print(video_publishing_time)
	# 	try:
	# 		db.session.add(new_video)
	# 		db.session.commit()
	# 	except:
	# 		print('There was an Issue in Adding Video to the DataBase')


# Decorator for Routing Initial GET Request
@app.route('/', methods = ['GET'])
def index():
	page_no = int(request.args['page_no'])
	page_size = int(request.args['page_size'])
	videos = (
		Video.query
		.order_by(Video
		.publishing_time.desc())
		.limit(page_size)
		.offset((page_no - 1) * page_size)
		.all()
	)
	ret = {"data" : []}
	for vid in videos:
		ret["data"].append({
			'title' : vid.title,
			'description' : vid.description,
			'thumbnail_url' : vid.thumbnail_url,
			'publishing_time' : vid.publishing_time,
			'id' : vid.id
		})
	return ret


# Decorator for Routing Search Request
@app.route('/search', methods = ['GET'])
def search():
	search_txt = request.args['q'].split()
	videos = (
		Video.query
		.order_by(Video
		.publishing_time.desc())
		.all()
	)
	ret = {"data" : []}
	for vid in videos:
		if (any(word in vid.title for word in search_txt) or any(word in vid.title for word in search_txt)):
			ret["data"].append({
				'title' : vid.title,
				'description' : vid.description,
				'thumbnail_url' : vid.thumbnail_url,
				'publishing_time' : vid.publishing_time,
				'id' : vid.id
			})
	return ret




	return "This will return all the vids based on the search query"

if __name__ == "__main__":
	scheduler = BackgroundScheduler()
	scheduler.add_job(YT_API, 'interval', seconds = 5)
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())
	app.run(debug = True)