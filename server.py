from flask import Flask, request, Response, json
app = Flask(__name__)
import urllib
import os
import subprocess

SERVER_PORT = 56555
SIGNATURE = "__%%__$$__"
KEY_DELIMETER = "|||"

@app.route('/', methods = ['GET'])
def display_something():
	return 'You give me cancer.'

@app.route('/', methods =['POST'])
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


def extract_image(link):
	f = open("test.png", "wb")
	f.write(urllib.urlopen(link).read())
	f.close()
	return f.name

if __name__ == '__main__':
    app.run(port=int(SERVER_PORT))



#f = open("test.png", "wb")
#f.write(urllib.urlopen("http://placekitten.com.s3.amazonaws.com/homepage-samples/408/287.jpg").read())
