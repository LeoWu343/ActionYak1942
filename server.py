from flask import Flask, request
app = Flask(__name__)
import urllib
import os

SERVER_PORT = 56555

@app.route('/', methods =['POST'])
def decrypt():
	file1 = extract_image(request.form['url_id'])
	proc = subprocess.Popen(["./steg","-d", file1], stdout=subprocess.PIPE)
	message = proc.stdout.readline()
	signature = "__%%__$$__"
	if signature == message[0:len(signature)]:
		message = message[len(signature):]
		return message
	else:
		return None

def extract_image(link):
	f = open("test.png", "wb")
	f.write(urllib.urlopen(link).read())
	f.close()
	return f.name

if __name__ == '__main__':
    app.run(port=int(SERVER_PORT))



#f = open("test.png", "wb")
#f.write(urllib.urlopen("http://placekitten.com.s3.amazonaws.com/homepage-samples/408/287.jpg").read())
