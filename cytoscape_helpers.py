import dash
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_table
import dash_html_components as html

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
    return search_terms.search_terms[f'{corpus}{dict_type}']



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
            min = 3
            max = 6
        elif rep == 'tf-idf':
            min = 3
            max = 7
    elif stat_choice == 'log dice':
        if rep == 'bow':
            min = -2
            max = 2
        elif rep == 'tf-idf':
            min = -5
            max = -1
    STYLESHEET[0]['style']['width'] = f'mapData(weight, {min}, {max}, 1, 5)'
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
            {'label': 'Philoso*', 'value': ''},
            {'label': 'Naive Bayes 2', 'value': 'nb2_v2_'},
            {'label': 'Religion-Science', 'value': 'rel_v2_'}
        ],
        value='',
        style={'width': '40%'}
    ),
    html.P("Document representation:"),
    dcc.Dropdown(
        id='rep',
        options=[
            {'label': 'Bag of Words', 'value': 'bow'},
            {'label': 'TF-IDF', 'value': 'tf-idf'}
        ],
        value='bow',
        style={'width': '40%'}
    ),
    html.P("Dictionary:"),
    dcc.Dropdown(
        id='dictionary',
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': 'Proper nouns', 'value': 'propn'},
            {'label': 'Named entities', 'value': 'entities'}
        ],
        value='all',
        style={'width': '40%'}
    ),
    html.P("Search Term (Precalulated Cooccurrences)"),
    dcc.Dropdown(
        id='term',
        options=[{'label': word, 'value': word} for word in search_terms.search_terms['all']],
        value=search_terms.search_terms['all'][0],
        style={'width': '40%'}
    ),
    html.P("Statistic:"),
    dcc.Dropdown(
        id='stat-choice',
        options=[
            {'label': 'Mutual information', 'value': 'mi'},
            {'label': 'Log Dice', 'value': 'log dice'}
        ],
        value='mi',
        style={'width': '40%'}
    ),
    html.P('Primary Cooccurences'),
    dcc.Slider(
        id='primary-coocs',
        min=1,
        max=50,
        step=1,
        value=15,
        marks = {n: f'{n}' for n in [i for i in range(1, 51) if i%5==0]}
    ),
    html.P('Secondary Cooccurences'),
    dcc.Slider(
        id='secondary-coocs',
        min=1,
        max=15,
        step=1,
        value=5,
        marks = {n: f'{n}' for n in [i for i in range(1, 51) if i%5==0]}
    ),
    html.Button('Submit', id='submit-val', n_clicks=0),
    cooc_cytoscape
    ]
