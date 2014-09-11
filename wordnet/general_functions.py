def load_pickle(filename, silent = False):
	"""
	Loads pickle and prints to screen
	"""
	import pickle
	if not silent:
		print "Loading pickle (%s)" %(filename)
	try:
		return pickle.load( open( filename, "rb" ) )
	except:
		print "Error loading pickle."

def save_pickle(data, filename, silent = False):
	"""
	Saves pickle and prints to screen
	"""
	import pickle
	if not silent:
		print "Saving pickle (%s)" %(filename)
	pickle.dump( data, open( filename, "wb" ) )



def wait_for_random_time(wait_base = 10, wait_rand_ceil=10):
	"""
	Wait for random amount of time
	"""
	from random import randint
	import time
	seconds = wait_base + 0.99*randint(0,wait_rand_ceil)
	print "Waiting %s seconds" %seconds
	time.sleep(seconds)