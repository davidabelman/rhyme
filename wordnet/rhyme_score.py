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

	
	# Find last main stress in words
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