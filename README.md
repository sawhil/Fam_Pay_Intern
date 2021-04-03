# Fam_Pay_Intern

An API to fetch latest videos from youtube sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response with page size. The server fetches latest videos async after every 60 Seconds and saves it to the db.

Tech Stack Used : Python - Flask

## Necessary Requriments 
- Python 3+

## Setup Guide

- Clone the Repository
- Install All Dependencies Using 'pip install -r requirements.txt'.
- In the 'keys.txt' File add Youtube Data V3 API Keys line by line.
- Run the server using python3 server.py

## Usage Guide

- GET Request to '127.0.0.1:5000/' would fetch all the stored videos in a paginated response. You can externally define URL arguments (Page No. and Page Size) to fetch a specific page of specific size.

- GET Request to '127.0.0.1:5000/search?q=fam+pay' would fetch all the stored videos which have even one word matching with either video title or video description

## Example - 

- 'http://127.0.0.1:5000/?page_no=5&page_size=20'
- 'http://127.0.0.1:5000/' - By default it take page_no = 1 and page_size = 10

- 'http://127.0.0.1:5000/search?q=fam+pay'


