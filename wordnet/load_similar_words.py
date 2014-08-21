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

simple_noun_similarity_dict = load_pickle('created/sim_dict_trimmed_n.p')