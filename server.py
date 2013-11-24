<<<<<<< HEAD
from flask import Flask, request, Response, json
=======
from flask import Flask, request, session
import flask
import tweepy
>>>>>>> 9c2cb1f590b5400960e4ac10a3adf396077597ae
app = Flask(__name__)
import urllib
import os
import subprocess
#from twitter.api import Twitter
import oauth2 as ouath
import base64
#from flask_oauth import oauth

SERVER_PORT = 56555
SIGNATURE = "__%%__$$__"
KEY_DELIMETER = "|||"

@app.route('/', methods = ['GET'])
def display_something():
	return 'You give me cancer.'

def decrypt():
	file1 = extract_image(request.form["url_id"])
	key_guess = request.form["key"]

	proc = subprocess.Popen(["./steg","-d", file1], stdout=subprocess.PIPE)
	message = proc.stdout.readline()
	
	key = message[len(SIGNATURE): message.find(KEY_DELIMETER)]
	has_message = SIGNATURE == message[0:len(SIGNATURE)]
	correct_key = key_guess == key
	data = {'correct_key': correct_key, 'has_message': has_message}
	if correct_key:
		message = message[len(SIGNATURE)+len(key)+len(KEY_DELIMETER):]
		data['message'] = message
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route('/', methods =['POST'])
def action():
	if request.form['goal'] == 'decrypt':
		return decrypt()
#		file1 = extract_image(request.form["url_id"])
#		proc = subprocess.Popen(["./steg","-d", file1], stdout=subprocess.PIPE)
#		message = proc.stdout.readline()
#		signature = "__%%__$$__"
#			message = message[len(signature):]
#			return message #True
#		else:
#			return message #False
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



