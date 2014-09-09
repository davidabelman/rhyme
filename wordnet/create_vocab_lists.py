"""
Using vocab lists from e.g. www.manythings.org/vocabulary/lists/c/ we can create lists of 'related' objects
E.g. sporting equipment, and so on 
We crawl the pages to get the vocab
Then we create two Python dictionaries (could convert to SQL tables...)

One is a lookup of this form:
word_categories = { 'apple':'FOOD', 'banana':'FOOD', 'cat':'PETS', 'cucumber':'FOOD', 'cycle':'SPORTS' etc...}

The other is a list of all related words by category, e.g.:
category_lists = { 	'FOOD': ['apple', 'banana', 'cucumber'....],
					'SPORTS': [ ... ], 
					'PETS': [ ... ]
					}
"""


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

def filter_dict(list_of_dicts, key):
	"""
	Given a list of dictionaries, returns a list of just a chosen key
	"""
	return [x[key] for x in list_of_dicts]

def get_html(url):
	"""
	Gets HTML given any URL
	"""
	import urllib2
	print "Requesting %s" %url
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
	req = urllib2.Request(url, headers=hdr)
	page = urllib2.urlopen(req)
	html = page.read()
	return html

def get_vocab_page_urls():
	"""
	Takes 10 seconds or so to crawl a list of all internal links within the manythings site
	"""
	root_paths = 	[	'http://www.manythings.org/vocabulary/lists/a/',
						'http://www.manythings.org/vocabulary/lists/b/',
						'http://www.manythings.org/vocabulary/lists/z/',
						'http://www.manythings.org/vocabulary/lists/c/',
						'http://www.manythings.org/vocabulary/lists/e/',						
					]
	vocab_page_urls = []
	for url in root_paths:
		wait_for_random_time(wait_base = 1, wait_rand_ceil=3)
		html = get_html(url)
		from bs4 import BeautifulSoup
		soup = BeautifulSoup(html)
		links = soup.findAll('li')
		for link in links:
			try:
				php_href = link.find('a')['href']
				joined_url = url+php_href  # (i.e. 'http://www.manythings.org/vocabulary/lists/a/' + 'words.php?f=animals_1')
				if joined_url not in vocab_page_urls:
					vocab_page_urls.append(joined_url)
			except:
				# The list element does not contain an href
				None
		save_pickle(vocab_page_urls, 'working/vocab_page_urls.p')


def extract_HTML_from_all_vocab_pages():
	"""
	Loops through all vocab pages and extracts HTML from each, saves to pickle
	Created list looks like this:
	[
		{'url':'http://www.manythings.org/vocabulary/lists/e/words.php?f=baseball_positions',
		'html':...
		},
	]
	"""
	vocab_pages_HTML = load_pickle('working/vocab_pages_HTML.p')
	vocab_page_urls = load_pickle('working/vocab_page_urls.p')
	for url in vocab_page_urls:
		already_pulled = [i['url'] for i in vocab_pages_HTML]
		if url not in already_pulled:			
			print "We have not pulled this url before"
			html = get_html(url)
			vocab_pages_HTML.append (
					{
						'url':url,
						'html':html
					}
				)
			save_pickle(vocab_pages_HTML, 'working/vocab_pages_HTML.p')
			wait_for_random_time(wait_base = 4, wait_rand_ceil=10)
		else:
			print "We have already pulled this url (%s)" %url

def extract_words_and_create_dicts():
	"""
	Extracts word lists and categories from all HTML pages
	Saves to appropriate formats
	"""
	choose_to_continue = raw_input("\nDo you really wish to overwrite existing lookups\n(which have been manually filtered)?\nYou should create a backup first.\nType 'done' to continue. >> ")
	if choose_to_continue != 'done':
		print "Not continuing."
		return 0
	from bs4 import BeautifulSoup
	vocab_pages_HTML = load_pickle('working/vocab_pages_HTML.p')
	gathered_data = []

	for page in vocab_pages_HTML:
		category = ""
		vocab_list = []
		
		# Create soup
		html = page['html']
		soup = BeautifulSoup(html)
		
		# Get category name
		category = soup.find('h2').text.split('\n')[0]

		# Get vocab lists
		ul_list = soup.findAll('ul')
		for ul in ul_list:
			li_list = ul.findAll('li')
			for li in li_list:
				vocab_list.append(li.text)

		gathered_data.append (
				{
					'url':page['url'],
					'category':category,
					'vocab_list':vocab_list
				}
			)

	# Now we have gathered all of the data, we can create the appropriate lookup tables
	word_lookup = {}
	category_lookup = {}

	total, counter = len(gathered_data), 0
	for page in gathered_data:
		counter += 1
		print page['vocab_list']
		print page['category']
		print "Number %s out of %s..." %(counter, total)
		user_input = raw_input("""
		Type:
			0 to discard
			1 to keep as is
			words (separate by commas) to add to list (animals,pets)
			R, followed by words (separate by commas) to remove from list (R,pig,cow)
		>> """	
		)
		# User wants to skip
		if user_input=='0':
			print "Skipped..."
			continue

		# User wants to add words
		if user_input!='1' and user_input[0]!='R':
			print "Adding extra words..."
			words_to_add = page['vocab_list'] + [x.strip() for x in user_input.split(',')]

		# User wants to remove words
		if user_input[0]=='R':
			print "Removing these words..."
			words_to_add = [x for x in page['vocab_list'] if x not in [y.strip() for y in user_input.split(',')]]
			
		# User wants to keep as is
		if user_input == '1':
			words_to_add = page['vocab_list']

		if user_input == 'QUIT':
			break

		if user_input == '':
			words_to_add = page['vocab_list']			

		# Now continue with the process, sorting out words
		# Create category lookup
		category_lookup[page['category']] = words_to_add
		
		# Create word lookup for each word
		# Create new entry for word, or add to entry
		for word in words_to_add:
			if word in word_lookup:
				word_lookup[word].append(page['category'])
			else:
				word_lookup[word]=[page['category']]

		save_pickle(word_lookup, 'created/find_category_given_word.p')
		save_pickle(category_lookup, 'created/find_word_given_category.p')
		print "---"
	

# Get all vocab page URLs once (10 seconds)
# get_vocab_page_urls()

# Get HTML for every vocab page (400 or so in total, takes a while)
# extract_HTML_from_all_vocab_pages()

# Create dictionaries based on crawled data (very quick, no more crawling is required for this)
# extract_words_and_create_dicts()