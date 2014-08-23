"""
Script to create a similarity dictionary for a part of speech
e.g. nouns
Saved to a pickle which can be loaded by the application (saves 2 pickles - one trimmed, one raw)
Format: 
{'American': [(0.45777972268018446, 'person'),
  (0.45777972268018446, 'individual'),
  (0.3770113703254509, 'worker')],
 'Congress': [(0.8168565958659604, 'Senate'),
  (0.7811872158731489, 'court'),
  (0.5935568859765277, 'community')],
 'Democrat': [(0.6413425010935097, 'candidate'),
  (0.6249089934229491, 'Republican'),
  (0.5333606323182627, 'executive')],... etc.
  }
"""


def save_pickle(data, filename, silent = False):
	"""
	Saves pickle and prints to screen
	"""
	import pickle
	if not silent:
		print "Saving pickle (%s)" %(filename)
	pickle.dump( data, open( filename, "wb" ) )

def create_noun_list_from_noun_list(path = 'common_nouns.txt'):
	"""
	Depricated - uses a 2000 word noun list I found online
	"""
	# From http://www.desiquintans.com/articles.php?page=nounlist
	f = open(path).readlines()
	nouns = []
	# rhyme_codes_inverse = {}
	for line in f:
		nouns.append(line.strip())
	return nouns

def create_POS_list_from_word_list(path = 'downloaded_data/common_words.txt', length=1000, POS='n'):
	"""
	Uses 5000 word list of words to pick out X most common of POS-type P.
	create_POS_list_from_word_list(path = 'common_words.txt', length=1000, POS='n')
	POS = 'n' or 'v' or 'j' etc.
	length = number of words extracted
	"""
	# from http://www.wordfrequency.info/top5000.asp
	print "Creating a POS list (%s)" %POS
	f = open(path).readlines()
	nouns = []
	counter = 0
	for line in f:
		try:
			(rank, word, pos, freq, dispersion) = line.strip().split()
			if pos==POS:
				nouns.append(word)
				counter += 1
				if counter == length:
					break
		except:
			None		
	return nouns

def word_similarity(word1, word2):
	"""
	Similarity of 2 words as a score from 0 to 1, uses wordnet
	"""
	from pattern.en import wordnet
	try:
		a = wordnet.synsets(word1)[0]
		b = wordnet.synsets(word2)[0]
		return wordnet.similarity(a, b) 
	except:
		return 0

def create_noun_similarity_dict(nouns, threshold=0.5):
	"""
	Input: list of words of one POS
	Output: Dictionary of similarities between combinations of words (if > 0)
	i.e. {'cat':[(0.443, 'dog'), (0.829, 'kitten')], 'money':[(…), (…)]}
	"""
	print "Creating a similarity dictionary"
	output = {}
	total_nouns = len(nouns)
	counter = 0
	for i in nouns:
		entry = [(word_similarity(i, j),j) for j in nouns if i!=j and word_similarity(i, j)>threshold]
		output[i] = entry
		counter+=1
		print "Compared %s/%s" %(counter, total_nouns)
	return output

def trim_noun_similarity_dict(sim_dict, N=5):
	"""
	Input: similarity dictionary
	Returns: similarity dictionary with entries trimmed to highest N similar words
	Words with no similars are removed
	"""
	print "Trimming similarity dictionary"
	output = {}
	for word in sim_dict:
		sims = sim_dict[word]
		if sims:
			sims.sort()
			sims.reverse()
			output[word] = sims[0:N]
	return output

if __name__ == '__main__':
	i = raw_input("Are you sure you wish to create a new similarity dictionary (takes a few minutes) - 'y' to continue:")
	if i=='y':
		POS = 'n'
		nouns = create_POS_list_from_word_list(length = 1000, POS=POS)
		sim_dict = create_noun_similarity_dict(nouns, threshold=0.3)
		save_pickle(sim_dict, 'created/sim_dict_raw_%s.p' %POS)
		sim_dict = trim_noun_similarity_dict(sim_dict, N=5)
		save_pickle(sim_dict, 'created/sim_dict_trimmed_%s.p' %POS)
