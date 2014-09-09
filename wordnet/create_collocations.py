"""
This file creates the collocation dictionary pickle
TODO: create proper collocation score based on P(x+y)/P(x)P(y)
Would need to record number of occurances of each word individually, as well as how many collocations per word
When calculating MI, look up number of collocations between words, and number of each word, as per formula
Could then re-include stopwords?
TODO: include POS information within the dictionary?
"""


def save_pickle(data, filename, silent = False):
	"""
	Saves pickle and prints to screen
	"""
	import pickle
	if not silent:
		print "Saving pickle (%s)" %(filename)
	pickle.dump( data, open( filename, "wb" ) )


def create_stopwords():
	"""
	Returns a stopword list
	"""
	# Already existing list
	from nltk.corpus import stopwords
	stop = stopwords.words('english')

	# Add more on from file
	f = open('downloaded_data/stopwords.txt').readlines()	
	# Create a combined set
	output = list ( set( stop + [w.strip() for w in f] ) )
	save_pickle(output, 'created/stopwords.p')
	return output


def create_collocations_dictionary():
	"""
	Create collocation dictionary using ngram data, save to pickle
	TODO: include individual word count
	"""
	# Reduce words to lemmas
	from pattern.en import lemma
	stop = create_stopwords()

	collocations = {}
	for filenumber in ['2','3','4','5']:
		f = open('downloaded_data/w%s_.txt' %filenumber ).readlines()
		print "Loading file %s" %filenumber
		for line in f:
			# Take all entries that aren't the index (i.e. line[0])
			line = line.strip().split()[1:]
			# Loop through each word in the line
			for word in line:
				if word not in stop:
					word = lemma(word)
					if word not in collocations:
						collocations[word] = {}
					# Go through all other words in line and add 1 for collocation
					for other_word in line:
						if other_word not in stop:
							other_word = lemma(other_word)
							if other_word!=word:
								# Add 1 to dictionary count if it exists, or =1 if not
								collocations[word][other_word] = collocations[word].get(other_word, 0) + 1
	return collocations


def trim_collocations_dictionary(collocations, n=20, mincount = 2):
	"""
	Cut the number of entries per word to n
	"""
	out = {}
	errorcount=0
	totalcount = len(collocations)
	for word in collocations:
		try:
			# Take first n or less entries by score, only words with >= minimum count
			entry = sorted([(collocations[word][subword], subword) for subword in collocations[word] if collocations[word][subword]>=mincount], reverse=True)[0:n]
			# Only save if there are any entries!
			if entry:
				out[word] = entry
		except:
			print "Error (number %s out of %s)" %(errorcount, totalcount)
			errorcount+=1
	return out

############ RUN PROGRAM ###########
# Save all data at end
if __name__=='__main__':
	choice = raw_input("Are you sure you wish to recreate collocation dictionary lookup?\nThis can take a few minutes ('y' to continue) >> ")
	if choice=='y':
		print "Creating collocations dictionary as a pickle..."
		c = create_collocations_dictionary()
		c = trim_collocations_dictionary(c, n=20, mincount=2)
		save_pickle(c, 'created/collocations_dict.p')