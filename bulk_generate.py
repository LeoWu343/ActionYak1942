# generate and post argv[1] pictures with random msgs and argv[2] key
import twitter_post
import sys
import random
import string
from twython import TwythonError

def random_sequence(N):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))

N = sys.argv[1]
key = sys.argv[2]
for i in range(int(N)):
	print("generating and posting {0} out of {1}".format(i+1, N))
	try:
		twitter_post.generate_and_post(random_sequence(25), key)
	except TwythonError:
		print("Not posting this image.. Twitter thinks it's a duplicate")