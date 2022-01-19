import dash
import dash_cytoscape as cyto
from dash import dash_table
from dash import dcc
from dash import html

import pandas as pd

import search_terms
import text_content


STYLESHEET = [
    {
        'selector': 'edge',
        'style': {
            'width': 'mapData(weight, 3, 6, 1, 3)',
            'line-color': 'silver'
        }
    },
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)',
            'width': 'mapData(size, 1, 10, 10, 20)',
            'height': 'mapData(size, 1, 10, 10, 20)'
        }
    },
    {
        'selector': 'label',
        'style': {
            'font-size': 6,
            'text-valign': 'center',
            'text-background-color': 'white',
            'text-background-opacity': 0.6,
            'text-background-padding': 1,
            'text-border-color': 'black',
            'text-border-opacity': 1,
            'text-border-width': 0.5
        }
    }
]



def preloaded_search_terms(dict_type, corpus):
    """For the final corpus all terms have had their collocations generated.
    For the previous corpora, terms are loaded from a hand written list."""

    if corpus == "cc_3_":
        term_list = list(pd.read_pickle('pickles/cc3_dictionary.tar.gz'))
    else:
        term_list = search_terms.search_terms[f'{corpus}{dict_type}']

    return term_list



def node_degree(name, edges):
    """Helper for generate_network. Returns degree of node given
    list of edges formatted for Dash cytoscape."""
    degree=0
    for edge in edges:
        if edge['data']['source'] == name or edge['data']['target'] == name:
            degree += 1
    return degree



def generate_network(corpus, rep, dict, term, stat, pri_cooc_num, sec_cooc_num):
    """Produce network list from precalulated results,
    given input from cooccurence tab."""
    nodes = []
    node_names = set([term])
    edges = []

    cooc_df = pd.read_pickle(f'pickles/cooc_{corpus}{rep.upper()}_{dict}_df.tar.gz')

    primary_coocs = {
        cooc_df.loc[f'{term}_{stat}'][f'Term {i}']: cooc_df.loc[f'{term}_{stat}'][f'Score {i}']
        for i in range(pri_cooc_num)
    }
    for word, score in primary_coocs.items():
        node_names.add(word)
        if word != term:
            edges.append({'data': {
                'source': term,
                'target': word,
                'weight': score}
                }
            )
        secondary_coocs = {
            cooc_df.loc[f'{word}_{stat}'][f'Term {i}']: cooc_df.loc[f'{word}_{stat}'][f'Score {i}']
            for i in range(sec_cooc_num)
        }
        for sec_word, sec_score in secondary_coocs.items():
            node_names.add(sec_word)
            if word != sec_word:
                edges.append({'data': {
                    'source': word,
                    'target': sec_word,
                    'weight': sec_score}
                    }
                )

    for name in node_names:
        nodes.append({'data': {
            'id': name,
            'label': name,
            'size': node_degree(name, edges)}
            }
        )

    network = nodes + edges

    return network



def change_cytoscape_width(stat_choice, rep):
    if stat_choice == 'mi':
        if rep == 'bow':
            min_weight = 3
            max_weight = 6
        elif rep == 'tf-idf':
            min_weight = 3
            max_weight = 7
    elif stat_choice == 'ld':
        if rep == 'bow':
            min_weight = -2
            max_weight = 2
        elif rep == 'tf-idf':
            min_weight = 7
            max_weight = 7.5
    STYLESHEET[0]['style']['width'] = f'mapData(weight, {min_weight}, {max_weight}, 1, 5)'
    return STYLESHEET



def change_cytoscape_width_auto(elements):
    """Scales the edge weights depending on score."""

    weights = []

    for dict in elements:
        try:
            weights.append(dict['data']['weight'])
        except KeyError:
            pass

    min_weight = min(weights)
    max_weight = max(weights)

    # Cludge: want to avoid fake differences when all weights clustered together.
    if abs(max_weight-min_weight) < 2:
        min_weight = max_weight - 2

    STYLESHEET[0]['style']['width'] = f'mapData(weight, {min_weight}, {max_weight}, 1, 5)'
    return STYLESHEET


cooc_cytoscape = cyto.Cytoscape(
        id='cooccurrence-network',
        minZoom=1,
        maxZoom=10,
        layout={'name': 'cose'},
        style={'width': '85%', 'height': '800px',
            'margin': 'auto', 'border-style': 'solid',
            'margin-top': '10px'},
        elements=[],
        stylesheet=[
            {
                'selector': 'edge',
                'style': {
                    'width': 'mapData(weight, 7, 7.5, 1, 3)',
                    'line-color': 'silver'
                }
            },
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)',
                    'width': 'mapData(size, 1, 10, 10, 20)',
                    'height': 'mapData(size, 1, 10, 10, 20)'
                }
            },
            {
                'selector': 'label',
                'style': {
                    'font-size': 6,
                    'text-valign': 'center',
                    'text-background-color': 'white',
                    'text-background-opacity': 0.6,
                    'text-background-padding': 1,
                    'text-border-color': 'black',
                    'text-border-opacity': 1,
                    'text-border-width': 0.5
                }
            }
        ]
    )



cooc_tab = [
    dcc.Markdown(
        id = 'cyto-explainer',
        children = text_content.cytoscape_explainer,
        style={'width': '80%',
            'padding': '50px'}),
    html.P("Corpus:"),
    dcc.Dropdown(
        id='corpus-select',
        options=[
            {'label': 'Candidate Corpus 0', 'value': 'cc_0_'},
            {'label': 'Candidate Corpus 2', 'value': 'cc_2_'},
            {'label': 'Iteration 2 Religion Science Subcorpus',
                'value': 'rel_v2_'},
            {'label': 'Final Corpus', 'value': 'cc_3_'}
        ],
        value='cc_3_',
        style={'width': '40%'}
    ),
    html.P("Document representation:"),
    dcc.Dropdown(
        id='rep',
        options=[
            {'label': 'Bag of Words', 'value': 'bow'},
            {'label': 'TF-IDF', 'value': 'tf-idf'}
        ],
        value='tf-idf',
        style={'width': '40%'}
    ),
    html.P("Dictionary:"),
    dcc.Dropdown(
        id='dictionary',
        options=[
            {'label': 'Word list (with corpus proper nouns)', 'value': 'all'}
        ],
        value='all',
        style={'width': '40%'}
    ),
    html.P("Search Term (Precalulated Cooccurrences)"),
    dcc.Dropdown(
        id='term',
        options=[{'label': word, 'value': word} for word in preloaded_search_terms('all', 'cc_3_')],
        value='reason',
        style={'width': '40%'}
    ),
    html.P("Statistic:"),
    dcc.Dropdown(
        id='stat-choice',
        options=[
            {'label': 'Mutual information', 'value': 'mi'},
            {'label': 'Log Dice', 'value': 'ld'}
        ],
        value='ld',
        style={'width': '40%'}
    ),
    html.P('Primary Cooccurences'),
    dcc.Slider(
        id='primary-coocs',
        min=1,
        max=50,
        step=1,
        value=20,
        marks = {n: f'{n}' for n in [i for i in range(1, 51) if i%5==0]}
    ),
    html.P('Secondary Cooccurences'),
    dcc.Slider(
        id='secondary-coocs',
        min=1,
        max=15,
        step=1,
        value=10,
        marks = {n: f'{n}' for n in [i for i in range(1, 51) if i%5==0]}
    ),
    html.Button('Submit', id='submit-val', n_clicks=0),
    cooc_cytoscape
    ]
