import dash
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html

import pandas as pd


ALL_WORD_TERMS = [
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
    'freethinker'
]

ENTITY_TERMS = [
    'plato',
    'stout',
    'theosophy',
    'university',
    'canterbury college',
    'the new zealand institute',
    'the church',
    'new zealand'
]

PROPN_TERMS = [
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
    'Collins'
]


def node_degree(name, edges):
    """Helper for generate_network. Returns degree of node given
    list of edges formatted for Dash cytoscape."""
    degree=0
    for edge in edges:
        if edge['data']['source'] == name or edge['data']['target'] == name:
            degree += 1
    return degree



def generate_network(rep, dict, term, stat, pri_cooc_num, sec_cooc_num):
    """Produce network list from precalulated results,
    given input from cooccurence tab."""
    nodes = []
    node_names = set([term])
    edges = []

    cooc_df = pd.read_pickle(f'pickles/cooc_{rep.upper()}_{dict}_df.tar.gz')

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


cooc_cytoscape = cyto.Cytoscape(
        id='cooccurence-network',
        minZoom=1,
        layout={'name': 'cose'},
        style={'width': '85%', 'height': '800px', 'margin': 'auto'},
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
    html.P("Document representation:"),
    dcc.Dropdown(
        id='rep',
        options=[
            {'label': 'Bag of Words', 'value': 'bow'},
            {'label': 'TF-IDF', 'value': 'tf-idf'}
        ],
        value='bow'
    ),
    html.P("Dictionary:"),
    dcc.Dropdown(
        id='dictionary',
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': 'Proper nouns', 'value': 'propn'},
            {'label': 'Named entities', 'value': 'entities'}
        ],
        value='all'
    ),
    html.P("Search Term (Precalulated Cooccurrences)"),
    dcc.Dropdown(
        id='term',
        options=[{'label': word, 'value': word} for word in ALL_WORD_TERMS],
        value=ALL_WORD_TERMS[0]
    ),
    html.P("Statistic:"),
    dcc.Dropdown(
        id='stat-choice',
        options=[
            {'label': 'Mutual likelihood', 'value': 'ml'},
            {'label': 'Log Dice', 'value': 'log dice'}
        ],
        value='ml'
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
        max=50,
        step=1,
        value=5,
        marks = {n: f'{n}' for n in [i for i in range(1, 51) if i%5==0]}
    ),
    html.Button('Submit', id='submit-val', n_clicks=0),
    cooc_cytoscape
    ]
