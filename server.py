from flask import Flask, request, Response, json, session
import flask
import urllib
import subprocess
import json
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
	key_guess = request.form["key_guess"]

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
	elif request.form['goal'] == 'encrypt':
		return encrypt_to_imgur()
	else:
		return "BAD REQUEST" # TODO: return a real http response more reflective of situation

def encrypt_to_imgur():
	key = request.form['protection_key']	
	msg = request.form['message']
	src_file = extract_image(request.form["url_id"])
	outfile = src_file + ".out"
	proc = subprocess.Popen(["./steg","-e", src_file, outfile, msg, key], stdout=subprocess.PIPE)
#	time.sleep(5) # hack to keep IMGUR from running ahead of POPEN. Should make process synchronous instead
	proc.wait()

	link1 = imgur(outfile)
	return link1

#---------Imgur-------------------

def imgur(path):
	client_id1 = '435af258a810ee9'
	client_secret1 = '30c186991750dbe5619579ad8f8845ad9a224232'
	im = pyimgur.Imgur(client_id1, client_secret1)
	uploaded_image = im.upload_image(path, title = "Anonymous upload with PyImgur")
	return uploaded_image.link

def extract_image(link):
	f = open("tmp.png", "wb")
	f.write(urllib.urlopen(link).read())
	f.close()
	return f.name

if __name__ == '__main__':
    app.run(port=int(SERVER_PORT))



