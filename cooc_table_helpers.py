import dash
from dash import dash_table
from dash import html
from dash import dcc

import pandas as pd

import search_terms



def return_cooc_df(corpus, dict, term, rep, stat):
    cooc_df = pd.read_pickle(
        f'pickles/cooc_{corpus}{rep.upper()}_{dict}_df.tar.gz'
    )
    term_df = pd.DataFrame(columns=['Term', 'Score'])
    coocs = cooc_df.loc[term+f'_{stat}']

    if corpus == "cc_3_":
        num_coocs = 200
    else:
        num_coocs = 50

    for i in range(num_coocs):
        term_df.loc[i+1] = (coocs.loc[f'Term {i}'], coocs.loc[f'Score {i}'])

    return term_df


def load_search_terms(corpus, dict, rep, stat):
    cooc_df = pd.read_pickle(
        f'pickles/cooc_{corpus}{rep.upper()}_{dict}_df.tar.gz'
    )
    terms = [i[:-(len(stat)+1)] for i in cooc_df.index if i.endswith(stat)]
    return sorted(terms)



# To get running
df = return_cooc_df('cc_3_', 'all', 'philosophy', 'bow', 'mi')
terms = load_search_terms('cc_3_', 'all', 'bow', 'mi')

cooc_table_tab = [
    html.P('This tab displays the top cooccurrence results for each term.'),
    html.P("Corpus:"),
    dcc.Dropdown(
        id='table-corpus-select',
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
        id='table-rep',
        options=[
            {'label': 'Bag of Words', 'value': 'bow'},
            {'label': 'TF-IDF', 'value': 'tf-idf'}
        ],
        value='tf-idf',
        style={'width': '40%'}
    ),
    html.P("Dictionary:"),
    dcc.Dropdown(
        id='table-dictionary',
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
        id='table-term',
        options=[{'label': word, 'value': word} for word in terms],
        value='reason',
        style={'width': '40%'}
    ),
    html.P("Statistic:"),
    dcc.Dropdown(
        id='table-stat-choice',
        options=[
            {'label': 'Mutual information', 'value': 'mi'},
            {'label': 'Log Dice', 'value': 'ld'}
        ],
        value='ld',
        style={'width': '40%'}
    ),
    html.Button(
        'Submit',
        id='table-submit-val',
        n_clicks=0,
        style={'margin': '10px'}),
    dash_table.DataTable(
        id='cooc-table',
        columns=[{"name": i, "id": i}
            for i in ['Term', 'Score']
            ],
        data=df.to_dict('records'),
        style_table ={'width': '40%'},
        style_cell={
            'textAlign': 'left',
            'fontSize': '12px'
        },
    )
]
