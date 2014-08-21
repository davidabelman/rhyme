from nltk.corpus import wordnet as wn
from nltk.corpus import cmudict
pronunciations = cmudict.dict()

def find_synonyms(word):
	"""
	Temp function
	"""
	# Find all synsets (entities) of the word	
	synsets = wn.synsets(word)
	all_lemmas = set()
	for synset in synsets:
		print "Synset is %s" %synset
		syns = [n.replace('_', ' ') for n in synset.lemma_names]
		counts = [l.count() for l in synset.lemmas]
		ants = [a for m in synset.lemmas for a in m.antonyms()]  # Find antonym at each lemma level
		print "Synonyms: ",syns
		print "Counts: ", counts
		print "Antonyms:", ants


def get_synonyms_from_input(input_word, separate=False, primary_only=False, POS='any'):
	"""
	Given input word, find all related words
	Looks up synsets that this word is in
	Extracts all lemmas of all synsets
	Returns either a list: ['word', 'word2'...]
	of if separate=True:
	{
		'shot' : {
						'v':['shot', 'pulled the trigger', 'fired'],
						'n':['shot', 'ball']
				  }			
	}
	get_synonyms_from_input(input_word, separate=True, primary_only=False):
		--> separate: determines whether we return a dictionary separating all the different forms, or whether to put them all together
		--> primary_only: determines whether to only return lemmas for which input was the primary definition
	"""
	# If any spaces, switch to underscore
	input_word = input_word.replace(" ","_")
	output = {}
	synsets = wn.synsets(input_word)
	for synset in synsets:
		if synset.pos in POS or POS=='any':
			lemmas = synset.lemma_names
			word = lemmas[0].replace('_',' ')
			pos = synset.pos
			if word in output:
				if pos in output[word]:
					output[word][pos].update([title.replace('_', ' ') for title in lemmas])
				else:
					output[word][pos] = set([title.replace('_', ' ') for title in lemmas])
			else:
				output[word] = {}
				output[word][pos] = set([title.replace('_', ' ') for title in lemmas])

	# If only want primary (i.e. words where original query is the primary definition of synset)
	if primary_only:
		import copy		
		outputcopy = copy.deepcopy(output)
		output = {}
		for key in outputcopy:
			if key == input_word:
				output[key] = outputcopy[key]

	# If we want separated words, we can return like this
	if separate:
		return output

	# If we want all words in one list, we need to combine
	output_list = []
	if input_word in output:   # start with primary synonyms, if the input word is a primary definition
		for pos in output[input_word]:
			for lemma_name in output[input_word][pos]:
				if lemma_name not in output_list:
					output_list.append(lemma_name)
		output.pop(input_word, None)
	for key in output:  # now do all the others
		for pos in output[key]:
			for lemma_name in output[key][pos]:
				if lemma_name not in output_list:
					output_list.append(lemma_name)
	return output_list


# def get_synonyms_from_input_recursive(input_word, n=1):
# 	"""
# 	Gets synonym lemmas from input word, then lemmas of these words, etc.
# 	n is number of times to recur (default = 1, one recursion)
# 	"""
# 	done_list = [input_word]
# 	results = get_synonyms_from_input(input_word = input_word, separate=False)

# 	# Now we go through results adn reapply the function
# 	for x in range(n):
# 		for i in results:
# 			if i not in done_list:
# 				more_results = get_synonyms_from_input(input_word = i, separate=False)
# 				done_list.append(i)
# 				for j in more_results:
# 					if j not in results:
# 						results = results + [j]
# 	return results


def get_antonyms_from_input(input_word, POS='any'):
	"""
	Given an input word return any antonyms we can find for its synonyms
	"""
	output = []	
	input_word = input_word.replace(" ","_")
	synsets = wn.synsets(input_word)
	for synset in synsets:
		if synset.pos in POS or POS=='any':
			for lemma in synset.lemmas:
				if lemma.antonyms():
					output.append(lemma.antonyms()[0].name)
	return list(set(output))


def get_relations_from_input(input_word, POS='any'):
	"""
	Given an input word return any related words (e.g. homonyms, etc.) we can find for its synonyms
	"""
	output = []	
	final_synset_collection = []
	input_word = input_word.replace(" ","_")
	synsets = wn.synsets(input_word)
	for synset in synsets:
		if synset.pos in POS or POS=='any':
			final_synset_collection.extend(synset.entailments())
			final_synset_collection.extend(synset.hypernyms())
			final_synset_collection.extend(synset.hyponyms())
			final_synset_collection.extend(synset.instance_hyponyms())
			final_synset_collection.extend(synset.instance_hypernyms())
			final_synset_collection.extend(synset.part_holonyms())
			final_synset_collection.extend(synset.part_meronyms())
			final_synset_collection.extend(synset.member_holonyms())
			final_synset_collection.extend(synset.member_meronyms())
			final_synset_collection.extend(synset.similar_tos())
			final_synset_collection.extend(synset.substance_holonyms())
			final_synset_collection.extend(synset.substance_meronyms())
	for synset in final_synset_collection:
		for lemma in synset.lemma_names:
			output.append(lemma)
	return list(set(output))


def get_similar_simple_nouns_from_input(input_word, POS='any'):
	"""
	Given an input noun, return any related nouns if they exist in the simple-noun-similarity dict
	"""
	if POS=='any' or POS=='n':
		from load_similar_words import simple_noun_similarity_dict
		if input_word in simple_noun_similarity_dict:
			similar_words = simple_noun_similarity_dict[input_word]
			return [word for (score, word) in similar_words]
		else:
			# Not in dictionary
			return []
	else:
		# Didn't want a noun
		return []


def extend_words(word_list, n = 1, POS='any', fns=[		'get_antonyms_from_input',
														'get_synonyms_from_input',
														'get_relations_from_input',
														'get_similar_simple_nouns_from_input']):
	"""
	Input: a list of words or a single word
	Returns: a list of words (synonyms, relations, antonyms, related_nouns -- as specified)
	Can control for how many repeats (n=1 means one iteration of algorithm)
	Can control for which functions are applied if you specify them individually
	NB best results may be found through:
	extend_words(word_list, n = 1, fns=['get_synonyms_from_input', 'get_relations_from_input'])
	extend_words(_, n = 1, fns=['get_synonyms_from_input'])
	i.e. only finding one set of relations, then applying another synonyms round on this
	"""
	# Functions to loop through (excludes any not in arguments though)
	functions = [	get_synonyms_from_input,
					get_relations_from_input,
					get_similar_simple_nouns_from_input,
					get_antonyms_from_input]
	
	# Convert string to list if given just single word
	if type(word_list)==str:
		word_list = [word_list]

	# Repeat n times
	for _ in range(n):
		temp_found_list = []
		# Go through words supplied (or found so far)
		for w in word_list:
			# For each function find words and add to list if not already there
			for fn in functions:
				if fn.__name__ in fns:
					temp_find_in_loop = fn(w, POS=POS)   # This finds the syns/ants/relations whatever
					for r in temp_find_in_loop:
						if r not in temp_found_list:
							temp_found_list.append(r)
		for finding in temp_found_list:
			if finding not in word_list:
				word_list.append(finding)
	return word_list




def rhymes(s):
	# See http://www.garysieling.com/blog/rhyming-with-nlp-and-shakespeare
	import nltk
	from nltk.corpus import cmudict
	word = [(w,p) for (w,p) in cmudict.entries() if w==s][0]
	print "OUR WORD IS", word
	filtered = [wt for (wt, pt) in cmudict.entries() if word[1][-3:] == pt[-3:]]
	print filtered

def expand_word_inflections(word_list, include_same_stress_variations=True):
	"""
	Expand words into various forms, so 'play' would become player, playing, plays etc.
	So that we can find more rhyming possibilities
	"""
	from pattern.en import pluralize, singularize, comparative, superlative, lexeme
	inflections = []
	for word in word_list:
		if include_same_stress_variations:
			# Only do this if we want to have play, plays, played ,
			#i.e. we don't want this when finding similar stresses as they will all be matched with each other
			inflections.extend( lexeme(word) )   #[play plays playing played]
		inflections.append( word )
		inflections.append( comparative(word) )		#hotter
		inflections.append( superlative(word) )		#hottest
		inflections.append( lexeme(word)[2] )   # playing
	return list(set(inflections))

def find_exact_rhymes_given_wordlist(word_list):
	"""
	Given some input list of words, finds any exact rhyming collections
	Uses exact-rhyme lookup table I have, but note that this doesn't do near rhymes, and many words aren't listed
	Input: [cat, dog, mat, hog, pig, log]
	Ouput: [ [cat, mat], [dog, hog, log] ]
	"""
	from exact_rhyme_table import rhyme_codes
	import re
	
	word_list_with_codes = []
	# Loop through words, and find their rhyme codes
	for word in word_list:
		try:
			#word_split = re.split('-|_| ',word)  # If hyphenated or two words, use second part only
			#code=rhyme_codes[word_split[-1]]   # Use second part only
			code = rhyme_codes[word]  # This alternative avoids having same second word repeated as a 'rhyme'
			word_list_with_codes.append((word, code))  # i.e. [('cat', '2341'), ('dog', '417'), ('log', '417'), ('excite', '1285'), ('ignite', '1285')]
		except:
			None
	
	return find_identical_tuple_codes(word_list_with_codes)


def find_alliteration_given_wordlist(word_list, depth=2):
	"""
	Input: word list
	Output: Ouput: [ [cat, kit], [dog, dig, down] ]
	Finds words in the input list who start with the same exact phonemes, to a certain (specified) depth
	"""
	import re
	from nltk.corpus import cmudict
	pronunciations = cmudict.dict()
	
	word_list_with_codes = []
	# Loop through words, and find their pronunciations
	for word in word_list:
		# If word has hyphen or space or underscore, only use first part
		word_split = re.split('-|_| ',word)
		first_word = word_split[0]  # First part of word only
		try:
			p = pronunciations[first_word][0]
			word_list_with_codes.append((word, ''.join(p[0:depth])))  # i.e. [('cat', 'CAH1T']), ('dog'...)]
		except:
			None
	return find_identical_tuple_codes(word_list_with_codes)

def find_stresses_given_wordlist(word_list):
	"""
	Input: word list
	Output: [ [extreme, align], ['particular', 'emancipate']]
	Finds words in the input list who have the same stress pattern
	TODO - deal with double-words and words not in CMU
	"""
	from nltk.corpus import cmudict
	pronunciations = cmudict.dict()
	
	word_list_with_codes = []
	# Loop through words, and find their pronunciations
	for word in word_list:
		try:
			p = pronunciations[word][0]
			emphases = [letter[-1] for letter in p if letter[-1] in ['1','2','0']]
			word_list_with_codes.append((word, ''.join(emphases)))  # i.e. [('emancipate', '0102']), ('dog'...)]
		except:
			None
	
	return find_identical_tuple_codes(word_list_with_codes)

def find_vowel_matches_given_wordlist(word_list):
	"""
	Input: word list
	Output: [ [miserly, bribery], [handy, banshee]]
	Finds words in the input list who have the same stress pattern and vowel pattern
	TODO: deal with double words
	"""
	from nltk.corpus import cmudict
	pronunciations = cmudict.dict()
	
	word_list_with_codes = []
	# Loop through words, and find their pronunciations
	for word in word_list:
		try:
			p = pronunciations[word][0]
			emphases = [letter for letter in p if letter[-1] in ['1','2','0']]
			word_list_with_codes.append((word, ''.join(emphases)))  # i.e. [('emancipate', '0102']), ('dog'...)]
		except:
			None
	
	return find_identical_tuple_codes(word_list_with_codes)


def find_exact_rhymes_given_concepts(word_list, n=1):
	"""
	Input: word list of concepts
	Output: list of lists where each sublist is full of exact rhymes
	Argument n says number of expansion iterations to find related words
	"""
	words_to_rhyme = extend_words(word_list, n=n)
	words_to_rhyme_inflected = expand_word_inflections(words_to_rhyme)
	return find_exact_rhymes_given_wordlist(words_to_rhyme_inflected)


def find_alliteration_given_concepts(word_list, n=1, depth=2):
	"""
	Input: word list of concepts
	Output: list of lists where each sublist is full of alliterations
	Argument n says number of expansion iterations to find related words, and how far into word (depth) phonemes must align
	"""
	words_to_alliterate = extend_words(word_list, n=n)
	return find_alliteration_given_wordlist(words_to_alliterate, depth=depth)


def find_stresses_given_concepts(word_list, n=1):
	"""
	Input: word list of concepts
	Output: list of lists where each sublist has same stress pattern
	Argument n says number of expansion iterations to find related words
	"""
	words_to_stress = extend_words(word_list, n=n)
	words_to_stress_inflected = expand_word_inflections(words_to_stress, include_same_stress_variations=False)
	def av_word_len(words):
		return sum(len(word) for word in words)/len(words)

	# Find stresses for all words, and sort by average word length (decreasing) so that longest returned first
	result = find_stresses_given_wordlist(words_to_stress_inflected)
	return sorted(result, key = av_word_len, reverse = True)


def find_vowel_matches_given_concepts(word_list, n=1):
	"""
	Input: word list of concepts
	Output: list of lists where each sublist has same stress pattern and vowel sounds
	Argument n says number of expansion iterations to find related words
	"""
	words_to_stress = extend_words(word_list, n=n)
	words_to_stress_inflected = expand_word_inflections(words_to_stress, include_same_stress_variations=False)
	def av_word_len(words):
		return sum(len(word) for word in words)/len(words)

	# Find vowel matches for all words, and sort by average word length (decreasing) so that longest returned first
	result = find_vowel_matches_given_wordlist(words_to_stress_inflected)
	return sorted(result, key = av_word_len, reverse = True)

def find_rhyme_matches_given_wordlist_and_conditionals(word_list, conditionals):
	"""
	Input: word list [mat, pat, dog, rug], condition word(s) ['cat','log']
	Output: list of dictionary results with rhyme scores [{ 'result':'mat', 'rhymes_with':'cat', 'score':0.8},  {'result':'pat', 'rhymes_with'...} ...}
	Given a word list (which is generated based on some requested topic(s)) and given some conditional rhyming words
	(i.e. words we want to rhyme with) we pull out all rhyming pairs, and give them scores.
	"""
	import rhyme_score
	reload(rhyme_score)
	from nltk.corpus import cmudict
	pronunciations = cmudict.dict()

	if type(conditionals)==str:
		conditionals = [conditionals]
	
	output = []
	for rhyme_word in conditionals:
		for topic_word in word_list:
			score = rhyme_score.words_rhyme_score(rhyme_word, topic_word, pronunciations) or 0
			output.append ( {'result_word':topic_word, 'rhymes_with':rhyme_word, 'score':score} )

	return output

def find_scan_matches_given_wordlist_and_conditionals(word_list, conditionals):
	"""
	Input: word list [mat, pat, obtuse, volcanic], condition word(s) ['extreme','volcano']
	Output: word list of dicts with scores [{'result':'mat', 'scans_with':'volcano', 'score', 0}, {'result':'obtuse', 'scans_with':'extreme', 'score': 1}...]
	Given a word list (which is generated based on some requested topic(s)) and given some conditional rhyming words
	(i.e. words we want to rhyme with) we pull out all pairs with same scan pattern.
	"""
	import rhyme_score
	reload(rhyme_score)
	from nltk.corpus import cmudict
	pronunciations = cmudict.dict()

	if type(conditionals)==str:
		conditionals = [conditionals]
	output = []
	for scan_word in conditionals:
		for topic_word in word_list:
			score = rhyme_score.words_scan_score(scan_word, topic_word, pronunciations) or 0
			output.append( {'result_word':topic_word, 'scans_with':scan_word, 'score':score} )

	return output


def word_finder(rhymes_with=[],
				rhymes_with_extend=False,
				rhymes_with_POS='any',

				scans_with=[],

				topics=[],
				topics_extend=False,
				output_POS='any'):
	"""
	Wrapper for user to find word given inputs from AJAX
	"""
	result_set = []

	# Either rhyme with specific word(s) or extend the rhyme set given some part of speech
	if type(rhymes_with)==str:
		rhymes_with = [rhymes_with]
	if rhymes_with_extend:
		rhymes_with = extend_words(rhymes_with, POS=rhymes_with_POS)

	# Extend the topic set (level should be set by the user)
	topics = extend_words(topics, POS=output_POS)
	if topics_extend:
		topics = extend_words(topics, fns=['get_synonyms_from_input'], POS=output_POS)

	# Find rhymes and return if we are not looking at scans
	if rhymes_with:
		r_list = find_rhyme_matches_given_wordlist_and_conditionals(word_list = topics, conditionals = rhymes_with)
		if not scans_with:
			return sorted(r_list, key = lambda x: x['score'])

	# Find scans, and return if we are not looking at rhymes
	if scans_with:
		s_list = find_scan_matches_given_wordlist_and_conditionals(word_list = topics, conditionals = scans_with)
		result_set.append(s_list)
		if not rhymes_with:
			return sorted(s_list, key = lambda x: x['score'])

	if rhymes_with and scans_with:
		result_list = [
			{
				'result_word':r_entry['result_word'],
				'rhymes_with':r_entry['rhymes_with'], 
				'scans_with':s_entry['scans_with'],
				'score':s_entry['score']*r_entry['score'],
			}

			for r_entry in r_list for s_entry in s_list			
			if r_entry['result_word'] == s_entry['result_word']
		]

		return sorted(result_list, key = lambda x: x['score'])


def find_identical_tuple_codes(word_list_with_codes):
	"""
	General function.
	Input: a list of tuples, with identifier codes as second entry in each
	e.g. [('cat', '2341'), ('dog', '417'), ('log', '417'), ('excite', '1285'), ('ignite', '1285')]
	Returns: [ [cat, mat], [dog, hog, log] ] based on codes
	"""
	# Count number of rhyme codes that have appeared
	codes = [entry[1] for entry in word_list_with_codes]  # i.e [4, 77, 4, 342, 77, 123131]
	from collections import Counter
	counts = Counter(codes)  # i.e. {'4':2, '77':2, '12412':1}

	# Loop through and extract all words corresponding to codes where count>1
	output_list_of_lists = []
	for code in counts:
		if counts[code]>1:
			# We know this code has multiple entries, so let's find them
			single_word_list = [entry[0] for entry in word_list_with_codes if entry[1]==code]
			output_list_of_lists.append(sorted(single_word_list))
	print "Found %s to output" %(len(output_list_of_lists))
	return sorted(output_list_of_lists)


def word_similarity(word1, word2):
	"""
	Similarity of 2 words as a score from 0 to 1
	"""
	from pattern.en import wordnet
	try:
		a = wordnet.synsets(word1)[0]
		b = wordnet.synsets(word2)[0]
		return wordnet.similarity(a, b) 
	except:
		return 0


# Given a sentence, finds substitute words (alliteration)
# Find near rhymes, sounds likes
# Find alliteration

# Find substitute word given conditions:
# POS (given part of speech)
# stresses (given a stress pattern extracted from current word)
# alliteration (given a sound or list of sounds word must start with, or first stressed syllable must have)
# desired sounds (general list of sounds that word should have, vowels and consonants, see how close a match we can get)
# rarity (word count in literature)
# frequency of use in songs (relative frequency used in song lyrics)
# rhymes with (strength of rhyme with a given word)
# song sentiment (using pattern, though should probably expand sentiment.__init__ with some bootstrapping magic at some point - low priority)
# i.e. each of these would be a function that takes a list of sub words already found
# and it gives it a score on its criteria.
# We can then have an overall AJAX function where someone enters criteria (through sliders etc) including weights, and we return weighted list of words

# Given a sentence, tag that POS of each element
# Given a word in this, find alternatives

"""DONE"""
# Find exact rhyming pairs given theme   

# Find similar sounding words (alliteration, anaphones) given theme

# Option to include common rhyming words in the rhyming processes (wordnet excludes 'too', 'but', 'you' etc.)


# Pattern.en
# http://www.clips.ua.ac.be/pages/pattern-en#wordnet


# Find sentiment for real songs (do it for whole song, but also in 4-line blocks, and find average and deviation scores)
# Can give score to writing on website for sentiment, and also suggest words fitting into the current sentiment

"""DONE"""
# Create similarity set for most common nouns
# Use list of 3000 most common nouns in English
# Precompute mutual similarities
# Store similar nouns in big dicitonary
# When a noun is entered by a user within a word expansion we can also throw in any other similar nouns
# e.g. ocean and fish are related, duck and egg are related