# from nltk.corpus import cmudict
# pronunciation_dict = cmudict.dict()

approx_sounds = {
	'AA':'xAA',
	# 'AH':'xAH',
	# 'AE':'xAH',
	'AO':'xAA',
	'B':'xB',
	'P':'xB',
	'CH':'xCH',
	'SH':'xCH',
	'D':'xD',
	'T':'xD',
	# 'EH':'xAH',
	# 'ER':'xAH',
	'F':'xTH',
	'G':'xD',
	'IH':'xIH',
	'IY':'xIH',
	'JH':'xCH',
	'K':'xD',
	'M':'xM',
	'N':'xM',
	'NG':'xM',
	'L':'xL',
	'R':'xR',
	'S':'xS',
	'V':'xTH',
	'TH':'xTH',
	'UH':'xUH',
	'UW':'xUH',
	'Y':'xW',
	'W':'xY',
	'ZH':'xCH',
	'Z':'xS',
}

def words_rhyme_score(w1, w2, pronunciations):
	"""
	Returns a score for word rhyme (0 = none, or same word, 1 = exact, etc.)
	TODO
	Note that when multiple pronunciations exist, the algo currently returns the first match it finds, even if it's not the best one
	Thus the words are found as a match, but their score MAY be too low. Would have to store all scores before returning
	Also should deal with words not in the CMU pronouncing dict
	"""
	from exact_rhyme_table import rhyme_codes
	import re

	# Split words at hyphen or space, if second word the same, return 0
	w1_split = re.split('-|_| ',w1)[-1]
	w2_split = re.split('-|_| ',w2)[-1]
	if w1_split==w2_split:
		# print "Words match"
		return 0

	# See if exact rhyme known in lookup table
	try:
		code1 = rhyme_codes[w1_split]
		code2 = rhyme_codes[w2_split]
		if code1==code2:
			# print "Words rhyme"
			return 1
	except:
		# Words not in code dict
		None

	
	# Use CMU dict
	p1_list = pronunciations.get(w1_split)  # ['AE2', 'N', 'AH0', 'K', 'D', 'OW1', 'T', 'AH0', 'L']
	p2_list = pronunciations.get(w2_split)

	if p1_list and p2_list:
		# Loop through all possible pairs of pronunciations	
		for p1_word in p1_list:
			for p2_word in p2_list:

				# Find part after main stress only
				try:
					stress1 = [x[-1] for x in p1_word].index('1')  # 5
					p1 = p1_word[stress1:]   # ['OW1', 'T', 'AH0', 'L']
				
					stress2 = [x[-1] for x in p2_word].index('1') 
					p2 = p2_word[stress2:] 
				except:
					# print "No stress found for one of:", w1, w2
					return None

				# print 'Words after stresses are:'
				# print p1, p2

				# If words are exact match after this, rhyme = 1
				if p1==p2:
					# Words same after main stress
					# print "Sounds same after stress"
					return 1

				# Remove numbers
				def remove_number(x):
					if x[-1] in ('0','1','2'):
						return x[:-1]
					else:
						return x
				p1_no_stress = [remove_number(x) for x in p1]
				p2_no_stress = [remove_number(x) for x in p2]

				# If words are approx match after this (ignoring stress), rhyme = 0.6
				p1_approx = [approx_sounds.get(x, x) for x in p1_no_stress]
				p2_approx = [approx_sounds.get(x, x) for x in p2_no_stress]
				# print 'Approx words after stresses are:'
				# print p1_approx, p2_approx
				if p1_approx==p2_approx:
					# Words approx same after main stress
					# print "Approx sounds same after stress"
					return 0.7

				# See if same final 4 phonemes the same
				if p1[-4:]==p2[-4:]:
					# print "Last 4 phonemes match"
					return 0.5

				# See if same final 3 phonemes the same
				if p1[-3:]==p2[-3:]:
					# print "Last 3 phonemes match"
					return 0.4

				# See if final 4 approx phonemes same
				if p1_approx[-4:]==p2_approx[-4:]:
					# print "Last 4 phonemes match approximately"
					return 0.3

				# See if final 3 approx phonemes same
				if p1_approx[-3:]==p2_approx[-3:]:
					# print "Last 3 phonemes match approximately"
					return 0.2
				
				# If vowels are exact match for whole word, rhyme = 0.25
				p1_vowels = [x for x in p1_word if x[-1] in ('0', '1', '2')]
				p2_vowels = [x for x in p2_word if x[-1] in ('0', '1', '2')]
				if p1_vowels == p2_vowels:
					# Vowels same after main stress
					# print "Vowels same overall for whole word"
					return 0.1

				# If vowels are exact match after stress, rhyme = 0.25
				p1_vowels = [x for x in p1 if x[-1] in ('0', '1', '2')]
				p2_vowels = [x for x in p2 if x[-1] in ('0', '1', '2')]
				if p1_vowels == p2_vowels:
					# Vowels same after main stress
					# print "Vowels same after stress"
					return 0.08

				# If vowels ignoring stress are exact match after this, rhyme = 0.1
				p1_vowels = [x[:-1] for x in p1 if x[-1] in ('0', '1', '2')]
				p2_vowels = [x[:-1] for x in p2 if x[-1] in ('0', '1', '2')]
				if p1_vowels == p2_vowels:
					# Vowels same after main stress
					# print "Vowels without stress same after stress"
					return 0.06

				# See if same final 2 phonemes the same
				if p1[-2:]==p2[-2:]:
					# print "Last 2 phonemes match"
					return 0.04

				# See if final 2 approx phonemes same
				if p1_approx[-2:]==p2_approx[-2:]:
					# print "Last 2 phonemes match approximately"
					return 0.02

				# No matches
				# print "No matches on CMU data"
				return 0
	else:
		# Words not in CMU dict
		# TODO approx pronounciation
		# print "No CMU entry for word"
		return 0

def words_scan_score(w1, w2, pronunciations):
	"""
	Returns a score for word scan (0 = none, 1 = exact, 0.5 = after stress etc.)
	TODO:
	Currently only uses default pronunciation from CMU, ignores any variations
	Also should deal with words not in the CMU pronouncing dict
	"""
	import re
	# If words are double, make sure pronunciations for words are found separately and joined
	w1_split, w2_split = re.split('-|_| ',w1) , re.split('-|_| ',w2)
	p1_list, p2_list = [], []

	try:
		for w in w1_split:
			p1_list.extend(pronunciations[w][0])
		for w in w2_split:
			p2_list.extend(pronunciations[w][0])
	except:
		# Can't find words in CMU dict
		return 0

	if p1_list and p2_list:
		# Look for exact scan equality
		scan1 = [letter[-1] for letter in p1_list if letter[-1] in ('0', '1', '2')]
		scan2 = [letter[-1] for letter in p2_list if letter[-1] in ('0', '1', '2')]
		
		if scan1==scan2:
			return 1

		# Look for scan equality only after the main stress
		# Find part after first main stress only
		try:
			list_ = [x[-1] for x in p1_list]
			# list_.reverse()  # If we wanted to find the last stress
			# stress1 = len(list_) - list_.index('1')  # If we wanted to find the last stress
			stress1 = list_.index('1')  # 5
			p1 = p1_list[stress1:]   # ['OW1', 'T', 'AH0', 'L']
		
			
			list_ = [x[-1] for x in p2_list]
			# list_.reverse() # If we wanted to find the last stress
			# stress2 = len(list_) - list_.index('1')  # If we wanted to find the last stress
			stress2 = list_.index('1')  # 5
			p2 = p2_list[stress2:] 
		except:
			# print "No stress found for one of:", w1, w2
			return None
		scan1 = [letter[-1] for letter in p1 if letter[-1] in ('0', '1', '2')]
		scan2 = [letter[-1] for letter in p2 if letter[-1] in ('0', '1', '2')]

		if scan1==scan2:
			return 0.5

		# No scan found
		return 0
	else:
		return 0
				


def words_same_sounds_score(w1, w2, pronunciations):
	"""
	Given 2 words and the pronunciation dictionary
	Returns a score for how alike they sound
	Works by looking at intersection of phonemes
	TODO:
	Currently only uses default pronunciation from CMU, ignores any variations
	Also should deal with words not in the CMU pronouncing dict
	"""
	import re
	# If words are double, make sure pronunciations for words are found separately and joined
	w1_split, w2_split = re.split('-|_| ',w1) , re.split('-|_| ',w2)
	p1_list, p2_list = [], []

	# Firstly, if w1 contains a word in w2 or vice versa, return score of 0
	from pattern.en import lemma
	w1_temp = [lemma(x) for x in w1_split]
	w2_temp = [lemma(x) for x in w2_split]
	overlap = [val for val in w1_temp if val in w2_temp]
	if overlap:
		return 0

	try:
		for w in w1_split:
			p1_list.extend(pronunciations[w][0])
		for w in w2_split:
			p2_list.extend(pronunciations[w][0])
	except:
		# Can't find words in CMU dict
		return 0

	# If we have pronunciations for each word we continue
	if p1_list and p2_list:
		
		# We will populate these scores
		exact_sounds_score, approx_sounds_score = 0, 0

		# Remove stresses, not interested in these
		def remove_number(x):
			if x[-1] in ('0','1','2'):
				return x[:-1]
			else:
				return x
		p1_no_stress = [remove_number(x) for x in p1_list]
		p2_no_stress = [remove_number(x) for x in p2_list]

		# Find the overlap in sounds
		overlap = [x for x in p1_no_stress if x in p2_no_stress]

		# Find proportion of original sounds covered by overlap
		prop_1 = len ( [x for x in p1_no_stress if x in overlap] )*1.0 /len(p1_no_stress)
		prop_2 = len ( [x for x in p2_no_stress if x in overlap] )*1.0/len(p2_no_stress)
		#print prop_1, prop_2
		
		if prop_1 + prop_2 > 0:
			exact_sounds_score = prop_1*prop_2*2.0/(prop_1+prop_2)

		# Now check with approximate sounds, same process (weight score lower though)
		p1_no_stress = [approx_sounds.get(x, x) for x in p1_no_stress]
		p2_no_stress = [approx_sounds.get(x, x) for x in p2_no_stress]

		# Find the overlap in approx sounds
		overlap = [x for x in p1_no_stress if x in p2_no_stress]
		prop_1 = len ([x for x in p1_no_stress if x in overlap])*1.0 /len(p1_no_stress)
		prop_2 = len ([x for x in p2_no_stress if x in overlap])*1.0/len(p2_no_stress)
		
		if prop_1 + prop_2 > 0:
			approx_sounds_score = prop_1*prop_2*2.0/(prop_1+prop_2) * 0.66   # Weighted down

		# Return the higher score of the two
		return max(exact_sounds_score, approx_sounds_score)

def words_alliterate_score(w1, w2, pronunciations):
	"""
	Given 2 words and the pronunciation dictionary
	Returns a score for how deep the alliteration is
	TODO:
	Currently only uses default pronunciation from CMU, ignores any variations
	Also should deal with words not in the CMU pronouncing dict
	"""
	import re

	# Add to score as we go, exact match = 1, approx match = 0.5 (or 0 if first sound)
	score=0

	# Use only the first word if it is double barrelled
	w1, w2 = re.split('-|_| ',w1)[0] , re.split('-|_| ',w2)[0]

	# If words match, return 0
	if w1==w2:
		return 0

	# Get pronunciations for each (TODO - deal with case where we don't have CMU dict entry)
	p1_list = pronunciations.get(w1)
	p2_list = pronunciations.get(w2)

	# If pronunciations exist...
	if p1_list and p2_list:
		p1=p1_list[0]
		p2=p2_list[0]

		# Find length of shortest one. We will loop through this many times (L)
		L = min(len(p1), len(p2))
		
		# Return 0 if first sound different
		if p1[0]!=p2[0]:
			if approx_sounds.get(p1[0],'blah1') != approx_sounds.get(p2[0],'blah2'):
				return 0
			else:
				# score+=0.25   # Return a score if first sound approx the same??
				return 0
		else:
			score+=1

		# Loop through all remaining sounds in shorter word and compare to longer word
		for i in range(L-1):
			if p1[i+1]==p2[i+1]:  # exact phoneme match
				score+=1
			elif approx_sounds.get(p1[i+1],'blah1') == approx_sounds.get(p2[i+1],'blah2'):  # approx phoneme match
				score+=0.5
			else:
				return score

		# If whole of shorter word has been completed, return 100 (can then filter this if required)
		return 100
	else:
		# No pronunciation in dict
		return 0
		
