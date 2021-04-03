from flask import Flask

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
	return "Hello This will be the GET API For the Server"


@app.route('/search', methods = ['GET'])
def search():
	return "This will return all the vids based on the search query"

if __name__ == "__main__":
	app.run(debug = True)

