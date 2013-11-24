from flask import Flask, request
app = Flask(__name__)
import urllib
import os


@app.route('/', methods =['POST'])
def decrypt():
	file1 = extract_image(request.form['url_id'])
	#encrypt = os.system("go run {0}".format(filename))()
	proc = subprocess.Popen(["go", "run", "steg.go", "-d", file1], stdout=subprocess.PIPE)
	message = proc.stdout.readline()
	signature = "__%%__$$__"
	if signature == message[0:len(signature)]:
		message = message[len(signature):]
		#return send_string_back(message)
		return message
	else:
		return None

#def send_string_back(msg):
#	return msg

def extract_image(link):
	#urllib.urlretrieve(link, "/aakashjapi/dropbox/my_projects")
	f = open("test.png", "wb")
	f.write(urllib.urlopen(link).read())
	f.close()
	return f.name


if __name__ == '__main__':
    app.run()



#f = open("test.png", "wb")
#f.write(urllib.urlopen("http://placekitten.com.s3.amazonaws.com/homepage-samples/408/287.jpg").read())
