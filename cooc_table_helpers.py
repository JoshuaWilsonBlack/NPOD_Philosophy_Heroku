import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html

import pandas as pd

import search_terms



def return_cooc_df(corpus, dict, term, rep, stat):
    cooc_df = pd.read_pickle(
        f'pickles/cooc_{corpus}{rep.upper()}_{dict}_df.tar.gz'
    )
    term_df = pd.DataFrame(columns=['Term', 'Score'])
    coocs = cooc_df.loc[term+f'_{stat}']
    for i in range(50):
        term_df.loc[i+1] = (coocs.loc[f'Term {i}'], coocs.loc[f'Score {i}'])

    return term_df


def load_search_terms(corpus, dict, rep, stat):
    cooc_df = pd.read_pickle(
        f'pickles/cooc_{corpus}{rep.upper()}_{dict}_df.tar.gz'
    )
    terms = [i[:-(len(stat)+1)] for i in cooc_df.index if i.endswith(stat)]
    return sorted(terms)



# To get running
df = return_cooc_df('', 'all', 'philosophy', 'bow', 'mi')
terms = load_search_terms('', 'all', 'bow', 'mi')

cooc_table_tab = [
    html.P('This tab shows top-50 cooccurrence results for every term for which they have been pre-calculated.'),
    html.P("Corpus:"),
    dcc.Dropdown(
        id='table-corpus-select',
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
        id='table-rep',
        options=[
            {'label': 'Bag of Words', 'value': 'bow'},
            {'label': 'TF-IDF', 'value': 'tf-idf'}
        ],
        value='bow',
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
        value=terms[0],
        style={'width': '40%'}
    ),
    html.P("Statistic:"),
    dcc.Dropdown(
        id='table-stat-choice',
        options=[
            {'label': 'Mutual information', 'value': 'mi'},
            {'label': 'Log Dice', 'value': 'log dice'}
        ],
        value='mi',
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
