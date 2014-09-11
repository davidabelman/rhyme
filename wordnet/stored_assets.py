from general_functions import load_pickle

general_collocations = load_pickle('created/collocations_dict.p')
stopwords = load_pickle('created/stopwords.p')
simple_noun_similarity_dict = load_pickle('created/sim_dict_trimmed_n.p')
find_category_given_word = load_pickle('created/find_category_given_word.p')
find_word_given_category = load_pickle('created/find_word_given_category.p')
common_rhyming_words = load_pickle('created/common_rhyming_words.p')