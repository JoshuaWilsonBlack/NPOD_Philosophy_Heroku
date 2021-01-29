"""
Contains preloaded search terms for each corpus.
"""

philoso_all = sorted([
    'philosophy',
    'theology',
    'speculative',
    'ethics',
    'metaphysics',
    'theosophy',
    'materialism',
    'idealism',
    'liberalism',
    'socialism',
    'stout',
    'freethinker',
    'transcend',
    'intellectual',
    'institute',
])

philoso_propn = sorted([
    'Besant',
    'Stout',
    'Vogel',
    'Plato',
    'Aristotle',
    'Spencer',
    'Carlyle',
    'Darwin',
    'Hosking',
    'Worthington',
    'Collins',
    'Cook',
    'Stella',
    'Henderson',
    'Runanga',
    'Frankland',
    'Ideal',
    'Philosopher'
])

philoso_entities = sorted([
    'plato',
    'stout',
    'theosophy',
    'university',
    'canterbury college',
    'the new zealand institute',
    'the church',
    'new zealand',
    'salmond',
    'stella',
    'henderson',
    'lady cook',
    "mechanics' institute",
    'philosophical institute',
    'the philosophical society',
    'positivism',
    'dr macgregor',
    'butler',
    'robert elsmere',
    'the temple of truth',
    'rangatira',
    'maoridom',
    'maoriland',
    'the native land court'
])

nb2_all = sorted([
    'philosophy',
    'philosophical',
    'theology',
    'speculative',
    'ethics',
    'metaphysics',
    'theosophy',
    'materialism',
    'idealism',
    'liberalism',
    'socialism',
    'stout',
    'freethinker',
    'transcend',
    'intellectual',
    'institute',
    'conflict',
    'harmony',
    'evolution',
    'creation',
    'colony'
])

nb2_propn = sorted([
    'Besant',
    'Stout',
    'Vogel',
    'Plato',
    'Aristotle',
    'Spencer',
    'Carlyle',
    'Darwin',
    'Hosking',
    'Worthington',
    'Collins',
    'Cook',
    'Stella',
    'Henderson',
    'Ideal',
    'Philosopher',
    'Huxley',
    'Salmond',
    'McGregor'
])

nb2_entities = sorted([
    'plato',
    'stout',
    'theosophy',
    'university',
    'canterbury college',
    'the new zealand institute',
    'the church',
    'new zealand',
    'salmond',
    'henderson',
    'lady cook',
    "mechanics' institute",
    'the philosophical society',
    'positivism',
    'dr macgregor',
    'butler',
    'robert elsmere',
    'the temple of truth',
    'the native land court',
    'reign of grace'
])

rel_all = sorted([
    'philosophy',
    'theology',
    'evolutionary',
    'conflict',
    'priestcraft',
    'ancestor',
    'primate',
    'monkey',
    'lower',
    'design',
    'designed',
    'heretic',
    'heresy',
    'creator', # Perhaps I should have stemmed these?
    'warfare'
])

rel_propn = sorted([
    'Darwin',
    'Huxley',
    'White',
    'Draper',
    'Wilberforce',
    'Wallace',
    'Stout',
    'Haast',
    'Evolution',
    'Science',
    'Religion',
    'Theology',
    'Salmond',
    'Macgregor',
    'Parker'
])

rel_entities = sorted([
    'darwin',
    'the church',
    'synod',
    'truth',
    'creation',
    'the reign of grace'
])


search_terms = {
    'all': philoso_all,
    'entities': philoso_entities,
    'propn': philoso_propn,
    'nb2_v2_all': nb2_all,
    'nb2_v2_entities': nb2_entities,
    'nb2_v2_propn': nb2_propn,
    'rel_v2_all': rel_all,
    'rel_v2_entities': rel_entities,
    'rel_v2_propn': rel_propn
}

# # Useful for testing search terms:
#
# word_lists = {
#     'all': rel_all,
#     'propn': rel_propn,
#     'entities': rel_entities
# }
#
# import pandas as pd
# for dict_type in ['all', 'propn', 'entities']:
#     df = pd.read_pickle(f'pickles/cooc_rel_v2_BOW_{dict_type}_df.tar.gz')
#     for word in word_lists[dict_type]:
#         test_index = word+'_mi'
#         if not test_index in df.index:
#             print(f'{dict_type}: {word}')
