from flask import Flask, request, Response, json, session
import flask
import urllib
import os
import subprocess
import base64
import json
import requests
from base64 import b64encode
import pyimgur

app = Flask(__name__)
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
		# with open(file1, "rb") as f:
		# 	data = f.read()
  		#	data.encode("base64")
		# send_file(file1)
		link1 = imgur(file1)
		return link1
#---------Tweet-------------------

def imgur(file1):
	# client_id = '435af258a810ee9'
	# headers = {"Authorization": "Client-ID my-client-id"}
	# api_key = 'my-api-key'
	# url = "https://api.imgur.com/3/upload.json"
	# j1 = requests.post(url, headers = headers,
	#     data = {
	#         'key': api_key, 
	#         'image': b64encode(open('file1','rb').read()),
	#         'type': 'base64',
	#         'name': '1.jpg',
	#         'title': 'Picture no. 1'
	#     })
	client_id = '435af258a810ee9'
	client_secret = '30c186991750dbe5619579ad8f8845ad9a224232'
	url = 'https://api.imgur.com/3/upload.json'
	path = file1
	#headers = {'Authorization':'Client-ID {0}'.format(client_id)}
	im = pyimgur.Imgur(client_id, client_secret)
	uploaded_image = im.upload_image(path, "Anonymous upload with PyImgur")
	print(uploaded_image.title)
	print(uploaded_image.link)
	print(uploaded_image.size)
	print(uploaded_image.type)
	return uploaded_image.link


def send_file(pic):
	return send_file(pic, mimetype='image/png')

def extract_image(link):
	f = open("test.png", "wb")
	f.write(urllib.urlopen(link).read())
	f.close()
	return f.name

if __name__ == '__main__':
    app.run(port=int(SERVER_PORT))



