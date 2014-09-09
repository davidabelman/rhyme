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



general_collocations = load_pickle('created/collocations_dict.p')
stopwords = load_pickle('created/stopwords.p')
simple_noun_similarity_dict = load_pickle('created/sim_dict_trimmed_n.p')
find_category_given_word = load_pickle('created/find_category_given_word.p')
find_word_given_category = load_pickle('created/find_word_given_category.p')