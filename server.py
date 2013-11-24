from flask import Flask, request, session
import flask
import tweepy
app = Flask(__name__)
import urllib
import os
import subprocess
#from twitter.api import Twitter
import oauth2 as ouath
import base64
#from flask_oauth import oauth

SERVER_PORT = 56555

@app.route('/', methods = ['GET'])
def display_something():
	return 'You give me cancer.'

@app.route('/', methods =['POST'])
def action():
#--------This is a change-------------	
	if request.form['goal'] == 'decrypt':
#--------End---------------------------		
		file1 = extract_image(request.form["url_id"])
		proc = subprocess.Popen(["./steg","-d", file1], stdout=subprocess.PIPE)
		message = proc.stdout.readline()
		signature = "__%%__$$__"
		if signature == message[0:len(signature)]:
			message = message[len(signature):]
			return message #True
		else:
			return message #False
#---------Changes begin here-------------------
	else:
		#signature = "__%%__$$__"
		msg = request.form['message']
		file1 = extract_image(request.form["url_id"])
		proc = subprocess.Popen(["./steg","-e", file1, file1, msg], stdout=subprocess.PIPE)
		#message = proc.stdout.readline()
		with open(file1, "rb") as f:
    		data = f.read()
    		data.encode("base64")
		send_file(file1)
#---------Tweet-------------------

def send_file(pic):
	return send_file(pic, mimetype='image/png')

def extract_image(link):
	f = open("test.png", "wb")
	f.write(urllib.urlopen(link).read())
	f.close()
	return f.name

if __name__ == '__main__':
    app.run(port=int(SERVER_PORT))



