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

# Global Set to keep track of Video IDs
vidIds = set()

# Video Model For SQLite
class Video(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(1000), nullable = False)
	description = db.Column(db.String(5000))
	thumbnail_url = db.Column(db.String(1000), nullable = False)
	publishing_time = db.Column(db.DateTime)
	def __repr__(self):
		return f'<id = {self.id}, title = {self.title}, publishing_time = {self.publishing_time}>'



api_keys = []
def import_api_keys():
	file1 = open('keys.txt', 'r')
	Lines = file1.readlines()
	for line in Lines:
		api_keys.append(line)


# Function to Call The Youtube API
# And Fetch The Data

def YT_API():
	# Youtube Search URL to send the Request
	search_url = 'https://www.googleapis.com/youtube/v3/search'
	time_now = datetime.now()
	last_req_time = time_now
	req_time = last_req_time.replace(microsecond=0).isoformat()+'Z'
	print("-----------------")
	print(req_time)
	print("-----------------")
	
	for api_key in api_keys:
		# Youtube API Key
		YOUTUBE_API_KEY = api_key
		# Parameters to Be Passed with the Request
		search_params = {
			'key' : YOUTUBE_API_KEY,
			'q' : 'cricket',
			'part' :'snippet',
			'maxResults' : 50,
			'order' : 'date',
			'type' : 'video',
			'publishedAfter' : req_time
		}

		# Making the Request
		r = requests.get(search_url, params = search_params)
		if r.json().get('items'):
			results = r.json()['items']
			for result in results:
				video_title = result['snippet']['title']
				if(result['id']['videoId'] in vidIds):
					continue
				video_description = result['snippet']['description']
				video_thumbnail_url = result['snippet']['thumbnails']['medium']['url']
				video_publishing_time = result['snippet']['publishedAt']
				vidIds.add(result['id']['videoId'])
				video_publishing_time = datetime.strptime(video_publishing_time, '%Y-%m-%dT%H:%M:%SZ')
				# print(video_publishing_time)
				new_video = Video(title = video_title, description = video_description, thumbnail_url = video_thumbnail_url, publishing_time = video_publishing_time)
				try:
					db.session.add(new_video)
					db.session.commit()
				except:
					print('There was an Issue in Adding Video to the DataBase')
			break


# Decorator for Routing Initial GET Request
@app.route('/', methods = ['GET'])
def index():
	page_no = 1
	page_size = 10
	if request.args.get('page_no'):
		page_no = int(request.args['page_no'])
	if request.args.get('page_size'):
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
	search_txt = set(request.args['q'].split())
	print(search_txt)
	videos = (
		Video.query
		.order_by(Video
		.publishing_time.desc())
		.all()
	)
	ret = {"data" : []}
	for vid in videos:
		if (search_txt.intersection(set(vid.title.split())) or search_txt.intersection(set(vid.description.split()))):
			ret["data"].append({
				'title' : vid.title,
				'description' : vid.description,
				'thumbnail_url' : vid.thumbnail_url,
				'publishing_time' : vid.publishing_time,
				'id' : vid.id
			})
	return ret

if __name__ == "__main__":
	import_api_keys()
	YT_API()
	scheduler = BackgroundScheduler()
	scheduler.add_job(YT_API, 'interval', minutes = 1)
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())
	app.run(debug = True)