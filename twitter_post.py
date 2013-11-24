# a script to demo encryption by downloading a random cat image, encrypting a message
# with the given key into it, and posting it to Kevin's twitter

import sys
from twython import Twython
from random import randint
import urllib
import subprocess
import time

CONSUMER_KEY = "H6FLAcWzq4mSACiJEZlJtg"
CONSUMER_SECRET = "7R82Tfr0lZIoGZl4gDq3GtbfpF3AmauGobChz7W3Kk"
ACCESS_TOKEN = "2211331747-CYz3sFQyR1SUqX1OIYtM3NI8mZELpdJBxISgehA"
ACCESS_TOKEN_SECRET = "6egCVK0W3lvqMf2537mwzWlwr7ozoNB7HvrSvja8CwV4d" # meh

def extract_image(link):
	f = open("tmp.png", "wb")
	f.write(urllib.urlopen(link).read())
	f.close()
	return f.name

def random_cat_url():
	return "http://placekitten.com/{0}/{1}".format(randint(200, 400), (randint(400, 800)))

src_file = extract_image(random_cat_url())
outfile = src_file + ".out"
msg = sys.argv[1]
key = sys.argv[2]
proc = subprocess.Popen(["./steg","-e", src_file, outfile, msg, key], stdout=subprocess.PIPE)
# time.sleep(5)
proc.wait()

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
photo = open(outfile, 'rb')
twitter.update_status_with_media(media=photo)
