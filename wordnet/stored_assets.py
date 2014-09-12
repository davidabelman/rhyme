from general_functions import load_pickle

general_collocations = load_pickle('created/collocations_dict.p')
stopwords = load_pickle('created/stopwords.p')
simple_noun_similarity_dict = load_pickle('created/sim_dict_trimmed_n.p')
find_category_given_word = load_pickle('created/find_category_given_word.p')
find_word_given_category = load_pickle('created/find_word_given_category.p')
common_rhyming_words = load_pickle('created/common_rhyming_words.p')
list_of_all_sounds = [
		'AA',
        'AE',
        'AH',
        'AO',
        'AW',
        'AY',
        'B',
        'CH',
        'D',
        'DH',
        'EH',
        'ER',
        'EY',
        'F',
        'G',
        'HH',
        'IH',
        'IY',
        'JH',
        'K',
        'L',
        'M',
        'N',
        'NG',
        'OW',
        'OY',
        'P',
        'R',
        'S',
        'SH',
        'T',
        'TH',
        'UH',
        'UW',
        'V',
        'W',
        'Y',
        'Z',
        'ZH']
list_of_vowel_sounds = [
		'AA',
        'AE',
        'AH',
        'AO',
        'AW',
        'AY',
        'EH',
        'ER',
        'EY',
        'IH',
        'IY',
        'OW',
        'OY',
        'UH',
        'UW']
list_of_scan_patterns = [ '1','01','10','100','010','001','1000','0100','0010','0001','10000','01000','00100','00010','00001' ]