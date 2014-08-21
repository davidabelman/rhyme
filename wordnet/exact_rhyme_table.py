f = open('exact_rhyme_table.txt').readlines()
rhyme_codes = {}
# rhyme_codes_inverse = {}
for line in f:
	(word, syl, code) = line.strip().split(' ')
	rhyme_codes[word] = code

# from http://www.chiark.greenend.org.uk/~tthurman/rhymes.txt