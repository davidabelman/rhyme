from nltk.corpus import wordnet as wn
from nltk.corpus import cmudict
from stored_assets import general_collocations
pronunciations = cmudict.dict()


######### EXTEND SINGLE WORDS IN VARIOUS WAYS (helper functions) ##########

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
	This was created using pattern's similarity measure between most common nouns
	"""
	if POS=='any' or POS=='n':
		from stored_assets import simple_noun_similarity_dict
		if input_word in simple_noun_similarity_dict:
			similar_words = simple_noun_similarity_dict[input_word]
			return [word for (score, word) in similar_words]
		else:
			# Not in dictionary
			return []
	else:
		# Didn't want a noun
		return []

def get_general_collocations_from_input(input_word, collocations = general_collocations, POS='any'):
	"""
	Search collocations dictionary for collocations
	Input: word 
	Output: list of words
	TODO: currently collocations doesn't use proper POS information
	... though this is in the source files, not hard to make a unique entry for each POS (just do noun, adverb, very, adjective)
	"""
	output = []	
	# Look up in collocations dictionary
	from pattern.en import lemma
	results = collocations.get(lemma(input_word),'')
	if results:
		for score, word in results:
			synsets = wn.synsets(word)
			for synset in synsets:
				if (synset.pos in POS or POS=='any') and word not in output:
					output.append(word)
		return output
	else:
		# Not in the dictionary
		return []

def get_similar_english_vocab_from_input(input_word, POS='any'):
	"""
	Given input word, return words that appear in the same category on English vocab list website
	TODO Need to deal with part of speech somehow (note that 'verb', 'adjective' often contained within title of page extracted in HTML already, so could use this info, or lookup within wordnet)
	"""
	output = []
	# Load the lookup dictionaries
	from stored_assets import find_category_given_word, find_word_given_category

	# Find all inflections of the input word
	input_word_extended = expand_word_inflections([input_word])

	# Find any categories to which the word belongs to
	categories = []
	for word in input_word_extended:
		if word in find_category_given_word:
			categories.extend(find_category_given_word[word])
	categories = list(set(categories))

	# Extract all words belonging to these categories
	for category in categories:
		print category
		related_words = find_word_given_category[category]
		print related_words
		output.extend(related_words)

	# Return result
	return list(set(output))


######### EXPAND WORD LISTS (aggregating helper functions) ##########

def extend_words(word_list, n = 1, POS='any', fns=[		'get_antonyms_from_input',
														'get_synonyms_from_input',
														'get_relations_from_input',
														'get_similar_simple_nouns_from_input',
														'get_similar_english_vocab_from_input',
														'get_general_collocations_from_input'
													]):
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
	functions = [	
					get_synonyms_from_input,
					get_relations_from_input,
					get_similar_simple_nouns_from_input,
					get_antonyms_from_input
				]
	
	# Convert string to list if given just single word
	if type(word_list)==str:
		word_list = [word_list]

	# Make a copy, used for later
	original_word_list = [x for x in word_list]

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

	# Also find related words from same categories (only ever do this once though, not repeated)
	if 'get_similar_english_vocab_from_input' in fns and n>=1:
		for w in original_word_list:
			extra_vocab = get_similar_english_vocab_from_input(w, POS=POS)
			print extra_vocab
			for word in extra_vocab:
				if word not in word_list:
					word_list.extend(extra_vocab)

	# Also find common collocations (only ever do this once though, not repeated)
	if 'get_general_collocations_from_input' in fns:
		for w in original_word_list:
			collocations = get_general_collocations_from_input(w, POS=POS)
			for word in collocations:
				if word not in word_list:
					word_list.extend(collocations)

	return word_list


def extend_words_by_level(word_list, level=[1,2,3][0], POS='any'):
	"""
	Extend words by a certain 'level', i.e. certain order of expansions according to a set level
	Level can be (currently) 1,2 or 3
	Returns extended word list
	Uses extend_words to do so
	"""
	# Convert string to list if necessary
	word_list = [word_list] if type(word_list)==str else word_list
	original_word_list = [w for w in word_list]

	# Extend to different levels
	if level >=1:
		# Basic extension of word_list
		word_list = expand_word_inflections(word_list)
		word_list = extend_words(word_list, fns=[
												'get_antonyms_from_input',
												'get_synonyms_from_input',
												'get_relations_from_input',
											], 
										POS=POS) 
	if level >=2:
		# Further extension, get synonyms of all words found so far
		word_list = extend_words(word_list, fns=['get_synonyms_from_input'], POS=POS)
	if level >=3:
		# Further extension, bring in the related words
		additional_words = extend_words(original_word_list, fns=[
											'get_similar_english_vocab_from_input',
															], POS=POS)
		word_list.extend([w for w in additional_words if w not in word_list])
	
	return word_list


def expand_word_inflections(word_list, include_same_stress_variations=True):
	"""
	Expand words into various forms, so 'play' would become player, playing, plays etc.
	So that we can find more rhyming possibilities
	"""
	# Make sure we treat string as list of length 1
	if type(word_list) == str:
		word_list = [word_list]

	# Expand words one at a time
	from pattern.en import pluralize, singularize, comparative, superlative, lexeme
	inflections = []
	for word in word_list:
		if include_same_stress_variations:
			# Only do this if we want to have play, plays, played ,
			#i.e. we don't want this when finding similar stresses as they will all be matched with each other
			inflections.extend( lexeme(word) )   #[play plays playing played]
			inflections.append( singularize(word) )
			inflections.append( pluralize(word) )
		inflections.append( word )
		inflections.append( comparative(word) )		#hotter
		inflections.append( superlative(word) )		#hottest
		try:
			inflections.append( lexeme(word)[2] )   # playing
		except:
			None
	return list(set(inflections))





######### FIND GENERAL GROUPS OF WORDS IN WORDLISTS (helper functions) ##########

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
			print p
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

def find_sound_matches_given_wordlist(word_list, threshold=0.85):
	"""
	Input: word list
	Output: [ [she sells, sea shells], [braid, drab]]
	Finds words in the input list which have similar sounds, up to a threshold
	TODO: deal with words not in cmudict
	"""
	from nltk.corpus import cmudict
	pronunciations = cmudict.dict()
	import rhyme_score
	reload(rhyme_score)

	out, done_list = [], []
	for w1 in word_list:
		done_list.append(w1)
		for w2 in word_list:
			if w2 not in done_list:
				score = rhyme_score.words_same_sounds_score(w1, w2, pronunciations)
				out.append((score, w1, w2))
	return [[x[1], x[2]] for x in out if x[0]>threshold]




######### FIND GENERAL GROUPS OF WORDS GIVEN CONCEPTS ##########

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

def find_sound_matches_given_concepts(word_list, n=1, threshold=0.85):
	"""
	Input: word list of concepts
	Output: list of lists where each sublist is pair of similar sounding words
	Argument n says number of expansion iterations to find related words
	"""
	words_to_find_sounds = extend_words(word_list, n=n)
	return find_sound_matches_given_wordlist(words_to_find_sounds, threshold)




######### WORD FINDER FUNCTIONS ##########

def find_matches_given_base_words_and_conditionals(word_list=[], conditionals=[], mode=['rhyme','alliterate','sound','scan'][0]):
	"""
	Input: word list (generated previously by expanding some topic set), and conditionals (e.g. words to rhyme with, and mode (one of 'rhyme', 'alliterate' etc.) 
	Output: {'mat': [{'base':'volcano', 'score', 0}, {... } ] ,  'obtuse':[{'base':'extreme', 'score': 1}, { }  ]...}
	Given a word list (which is generated based on some requested topic(s)) and given some conditional words,
	and a mode (rhyme, alliterate, sound, scan), we pull out all pairs of words and score them.
	Only words with scores > 0 are returned.
	"""
	import rhyme_score
	reload(rhyme_score)
	from nltk.corpus import cmudict
	pronunciations = cmudict.dict()

	conditionals = [conditionals] if type(conditionals)==str else conditionals
	word_list = [word_list] if type(word_list)==str else word_list
	output = {}

	# Go through all topic words
	for topic_word in word_list:
		for condition_word in conditionals:

			# Calculate score for each word
			if mode=='rhyme':	
				score = rhyme_score.words_rhyme_score(condition_word, topic_word, pronunciations) or 0
				min_score, max_score = 0.01, 1.01
			if mode=='alliterate':	
				score = rhyme_score.words_alliterate_score(condition_word, topic_word, pronunciations) or 0
				min_score, max_score = 1, 4 
			if mode=='sound':	
				score = rhyme_score.words_same_sounds_score(condition_word, topic_word, pronunciations) or 0
				min_score, max_score = 0.7, 1.01
			if mode=='scan':	
				score = rhyme_score.words_scan_score(condition_word, topic_word, pronunciations) or 0
				min_score, max_score = 0.01, 1.01
			
			# add result if score was in correct range
			if score>=min_score and score<=max_score:
				# For the first time we  encounter this topic word...
				if topic_word not in output:
					output[topic_word] = []
				# Every time, append result
				output[topic_word].append({'base':condition_word, 'score':score})
				
	return output
	# i.e. {'mat': [{'base':'volcano', 'score', 0}, {... } ] ,  'obtuse':[{'base':'extreme', 'score': 1}, { }  ]...}


def word_finder(mode=['rhyme','alliterate','sound','scan'][0],

				base=[],
				base_extend_level=[0,1,2][0],
				base_POS='any',

				secondary_scans_with=[],

				include_common_rhymes=False,

				topics=[],
				topics_extend_level=[0,1,2][0],
				output_POS='any'):
	"""
	Wrapper for user to find word given inputs from AJAX
	User enters a base word (or words) which the target word needs to either:
		1 Rhyme with
		2 Alliterate with
		3 Share similar sounds with
		4 Scan with
	The target needs to be constrained within a certain subject (topic) set by user (and can be expanded to various degrees)
	For 1, 2, 3 the user can optionally supply a 'scan with' argument
	TODO: User can provide a POS for the output word
	"""
	# Housekeeping
	original_topics = [x for x in topics]
	original_base = [x for x in base]
	base = [base] if type(base)==str else base
	secondary_scans_with = [secondary_scans_with] if type(secondary_scans_with)==str else secondary_scans_with
	topics = [topics] if type(topics)==str else topics

	# Extend words to desired level
	# --> Topics	
	topics = extend_words_by_level(word_list = topics, level=topics_extend_level)
	# --> Base word	
	base = extend_words_by_level(word_list = base, level=base_extend_level)

	# Include common rhymes in topic list if required
	if include_common_rhymes:
		from stored_assets import common_rhyming_words
		topics.extend(common_rhyming_words)
	
	# Get primary list of results depending on mode
	primary_list = find_matches_given_base_words_and_conditionals(word_list = topics, conditionals = base, mode=mode)
	
	# If we are not looking to combine any additional scan scores, we have then finished our collection of results now
	if not secondary_scans_with:
		collection_of_results = primary_list

	# Combine scan score with the primary score if we have a secondary_scans_with supplied
	else:
		import rhyme_score
		reload(rhyme_score)
		from nltk.corpus import cmudict
		pronunciations = cmudict.dict()
		secondary_list = {}  # This is the new list to fill out
		for key in primary_list:  # i.e. primary list is {'represent': [{'base': 'runner', 'score': 0.66}, {'base': 'run', 'score': 0.9}], ...}
			w1 = key  # i.e. 'represent'
			w2 = secondary_scans_with[0]  # Only scan with one word (TODO? user can supply list? Just loop through these if so)
			scan_score = rhyme_score.words_scan_score(w1,w2,pronunciations)
			if scan_score>0:
				# We want to multiple scan score by other scores, e.g. for runner & run
				secondary_list[key] = []
				for base_item in primary_list[key]: # e.g. [{'base': 'runner', 'score': 0.66}, {'base': 'run', 'score': 0.9}]
					original_score = base_item['score']
					base_word = base_item['base']
					secondary_list[key].append({'base':base_word, 'score':original_score*1.0*scan_score})
		collection_of_results = secondary_list

	# Return results sorted by their score
	return sorted( [(word, combo) for word in collection_of_results for combo in collection_of_results[word] if combo['score']!=0] , key=lambda x: (x[1]['score'], len(x[0]) ) )


######### GENERIC FUNCTIONS ##########

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




########## LIVE IDEAS FEED ##########
def find_mutual_collocations(wordlist):
	"""
	Given list of words, convert to set, and return list of mutual collocations
	between any pairs of words
	"""
	from stored_assets import stopwords
	collocations = {}
	for w in list(set(wordlist)):
		c_list = get_general_collocations_from_input(w)
		for c in c_list:
			collocations[c] = collocations.get(c,0) + 1
	print collocations
	return [w for w in collocations if collocations[w]>1 if w not in wordlist and w not in stopwords]



########## SENTENCE SCANNER ##########
def scan_sentence_for_ideas(sentence):
	"""
	Given sentence by AJAX, generate substitutions, ideas etc. using other functions
	"""
	None
	# 

def get_sentence_synonyms(sentence):
	"""
	Given a single sentence, find synonyms (possible replacements) for each word_list_with_codes
	Split sentence into tokens
	Get POS for each word
	Find synonyms for appropriate words
	Input is a sentence string
	Output is list of tuples, each word in sentence=tuple[0], list of alternatives is tuple[1]
	"""
	intermediate = []
	output = []

	if type(sentence)!=str:
		print "Sentence must be a string."
		return 0

	# Parse the sentence
	from pattern.en import parse
	words = parse( sentence,
					tokenize = True,         # Split punctuation marks from words?
				       tags = True,         # Parse part-of-speech tags? (NN, JJ, ...)
				     chunks = True,         # Parse chunks? (NP, VP, PNP, ...)
				  relations = False,        # Parse chunk relations? (-SBJ, -OBJ, ...)
				    lemmata = True,        # Parse lemmata? (ate => eat)
				   encoding = 'utf-8'       # Input string encoding.
					).split()[0]  # We only take '0' index as there should only be one sentence

	# Find which words are valid words to get synonyms for
	#--> not in stopwords, one of VB/JJ/NN/RB
	from stored_assets import stopwords
	counter = 0
	for word in words:
		# i.e. word = [u'walked', u'VBD', u'B-VP', u'O', u'walk']
		POS = word[1][0:2]
		POS_clean = {
					'VB':'v',  # verb
					'JJ':'s',  # adj
					'NN':'n',  # noun
					'RB':'r'   # adverb
				}.get(POS, None)
		if word[4] not in stopwords:  # word[4] is lemmatized version of word
			intermediate.append([word[4],POS_clean])  # word[0] or word[4], i.e. actual word, or lemmatized version? TODO
		else:
			intermediate.append([word[4],None])  # we don't want to replace any stopwords
		# So output has the format:
		# [[u'Quickly', 'r'], [u'send', 'v'], [u'a', None], [u'short', 's'], [u'message', 'n'], [u'to', None], [u'you', None]]	

	for word in intermediate:
		w=word[0]
		POS=word[1]
		if POS:  
			if POS=='n':
				# Find synonyms (? - test with and without this. more often that not returns crap? TODO)
				extension = [w]
				#extension = extend_words([w], POS=POS, fns=['get_synonyms_from_input'])
				
			else:
				# Find synonyms and relations
				extension = x = extend_words([w], POS=POS, fns=[
														'get_synonyms_from_input',
														'get_relations_from_input',
														#'get_similar_english_vocab_from_input',
													])
			output.append([w,POS,extension])
		else:
			output.append([w,POS,[w]])

	return output

def group_sentence_synonyms(sentence_expanded, mode=['alliterate','vowel','scan'][0], silent=False):
	"""
	Input: sentence with alternative synonyms for some words:
	[
	 [[u'my', None, [u'my']],
	 [u'house', 'n', [u'house']],
	 [u'tremble',
	  'v',	[u'tremble',
	   'palpitate',
	   'quiver',
	   'thrill',
	   'throb',
	   'agitate',
	   'shudder',
	   'shiver',
	   'quake',
	   'shake',
	   'harang',
	   'hilter']],
    ]
    Output: 2 dimensional, 1st dimension is the grouping, 2nd is the word 
    	[ H , 
    		[
	    		['my', [] ],
	    		['house', ['house'] ], 
	    		['tremble', ['harang', 'hilter'] ] 
    		]
    	],
    	[ P , 
    		[
	    		['my', [] ],
	    		['house', [] ], 
	    		['tremble', ['palpitate'] ] 
    		]
    	], etc...

	Groups the sentence synonyms according to a mode:
	Alliterate - groups according to first sound
	Vowel - groups according to stressed vowel sound
	Scan - groups according to scan pattern
	"""
	import re
	collection = []
	# Remove numbers
	def remove_number(x):
		if x[-1] in ('0','1','2'):
			return x[:-1]
		else:
			return x

	# Alliteration collection of synonyms
	if mode=='alliterate':
		# Import phonemes to loop through
		from stored_assets import list_of_all_sounds
		for phoneme in list_of_all_sounds:
			collection.append([phoneme, [] ])
			# For each phoneme, we add each word of the sentence in turn, and then check its alternatives
			for original_word in sentence_expanded:
				index = len(collection)-1
				# Add each original word within phoneme
				collection[index][1].append([original_word[0],[]])
				# Loop through alternatives:
				for variant in original_word[2]:
					# Get pronunciation of first word if double barreled
					variant_first_word = re.split('-|_| ',variant)[0]
					p = pronunciations.get(variant_first_word)  
					if p:
						p=p[0]  # TODO: only looking at basic pronunciation here. OK for alliteration though
						start_sound = remove_number(p[0])  # First sound only, ignore stress
						if start_sound==phoneme:
							collection[index][1][-1][1].append(variant)  # Add variant to latest word in the variant list
	
	# Group synonyms by primary vowel sound
	elif mode=='vowel':
		# Import phonemes to loop through
		from stored_assets import list_of_vowel_sounds
		for phoneme in list_of_vowel_sounds:
			collection.append([phoneme, [] ])
			# For each phoneme, we add each word of the sentence in turn, and then check its alternatives
			for original_word in sentence_expanded:
				index = len(collection)-1
				# Add each original word within phoneme
				collection[index][1].append([original_word[0],[]])
				# Loop through alternatives:
				for variant in original_word[2]:					
					# Split words if double barrelled
					variant_split = re.split('-|_| ',variant)
					for v in variant_split:
						p = pronunciations.get(v)
						if p:  # i.e. if pronunciation exists
							for p1 in p: # consider all different pronunciations			
								try:
									stress_syllable_index = [x[-1] for x in p1].index('1')
									vowel = p1[stress_syllable_index][:-1]  # knock the '1' off the end
									if vowel==phoneme:
										collection[index][1][-1][1].append(variant)
								except:
									# No stress syllable, skip
									None
								
	elif mode=='scan':
		def get_scan_pattern(phonemes):
			"""
			Gets phoneme scan pattern, converts 2-->0
			Returns 1000 or 001 etc.
			"""
			import string
			scan = [str(letter[-1]) for letter in phonemes if letter[-1] in ('0', '1', '2')]  # ['0'.'1','2','0']
			scan_string = string.join(scan, '').replace('2','0')  # '0100'
			first_stress = scan_string.index('1')
			return scan_string[first_stress:]


		# Import phonemes to loop through
		from stored_assets import list_of_scan_patterns
		for pattern in list_of_scan_patterns:
			collection.append([pattern, [] ])
			# For each pattern, we add each word of the sentence in turn, and then check its alternatives
			for original_word in sentence_expanded:
				index = len(collection)-1
				# Add each original word within pattern
				collection[index][1].append([original_word[0],[]])
				# Loop through alternatives:
				for variant in original_word[2]:					
					# Split words if double barrelled. Ignore any which are double barreled (TODO? fix this? Or OK? Avoids mistakes, as hard to find dominant word otherwise, e.g. think_of)
					variant_split = re.split('-|_| ',variant)
					if len(variant_split)==1:
						p = pronunciations.get(variant)
						if p: # i.e. pronunciation exists
							variant_patterns_added = [] # Keep track of ones we're adding so as not to add words twice
							for p1 in p: # consider all different pronunciations	
								try:		
									variant_pattern = get_scan_pattern(p1)
									if variant_pattern not in variant_patterns_added:  # Don't add the same word (different pronunciations) twice
										if variant_pattern == pattern:
											collection[index][1][-1][1].append(variant)
											variant_patterns_added.append(variant_pattern)
								except:
									# No first stress so variant pattern doesn't work
									None

	# Sort by how many variations per option (double sort = by number of words for which variation exists, then by how many variations exist overall)
	collection = sorted(
		collection, 
		key=lambda x: 		( 	
								len( [1 for var in [z[1] for z in x[1]] if var] ) ,   # number of words with alternatives, primary sort
								len( [var for word in [z[1] for z in x[1]] for var in word] )    # total number of alternatives, secondary sort
							) 
						)

	# Print result to screen if required for debugging
	if not silent:
		for phoneme in collection:
			print "-----"
			print phoneme[0]
			for x in phoneme[1]:
				print "    ",x

	return collection



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


"""
What it can do:

1) Given a theme:
- generate word set
- generate rhymes set
- generate alliteration set
- generate scan set
"""