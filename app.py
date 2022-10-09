import dash
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc

import pandas as pd

import text_content
import cytoscape_helpers
import text_helpers
import cooc_table_helpers

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP]

dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

dash_app.title = 'Philosophical Contestation in Early New Zealand Newspapers'

# For Heroku
server = dash_app.server

# For Azure
app = dash_app.server

dash_app.layout = dbc.Container([
    dcc.Markdown(children=text_content.opening_text),
    dbc.Tabs([
        dbc.Tab(
            label='Cooccurrence Networks',
            children=cytoscape_helpers.cooc_tab
            ),
        # dcc.Tab(
        #     label='Cooccurence Table',
        #     children=cytoscape_helpers.cooc_table)
        dbc.Tab(
            label='Cooccurrence Tables',
            children=cooc_table_helpers.cooc_table_tab
        ),
        dbc.Tab(
            label='View Texts',
            children=text_helpers.text_tab
        )
    ])
])
# Cooccurrence callbacks.
# Change preloaded search terms given dictionary or corpus change choice
@dash_app.callback(
    [Output(component_id='term', component_property='options'),
    Output(component_id='dictionary', component_property='options')],
    [Input(component_id='dictionary', component_property='value'),
    Input(component_id='corpus-select', component_property='value')]
)
def return_terms_and_opts(dict_type, corpus):
    """
    Given the type of dictionary required (string) for a
    collocation network, return the precalculated options (list).
    """
    words = cytoscape_helpers.preloaded_search_terms(dict_type, corpus)
    formatted_words = [{'label': word, 'value': word} for word in words]

    # update options for dictionary choice if corpus is Rel corpus
    default_dict_options = [
        {'label': 'All', 'value': 'all'},
        {'label': 'Proper nouns', 'value': 'propn'},
        {'label': 'Named entities', 'value': 'entities'}
    ]
    if corpus == 'rel_v2_':
        dict_options = [
            {'label': 'All (filtered)', 'value': 'all'},
            {'label': 'All (unfiltered)', 'value': 'all_un'},
            {'label': 'Proper nouns', 'value': 'propn'},
            {'label': 'Named entities', 'value': 'entities'}
        ]
    elif corpus == 'cc_3_' or corpus == 'cc_4_':
        dict_options = [
            {'label': 'Word list supplemented with proper nouns', 'value': 'all'}
        ]
    else:
        dict_options = default_dict_options

    return formatted_words, dict_options


# Function on press submit, to change cooccurrence network.
@dash_app.callback(
    [Output(component_id='cooccurrence-network', component_property='elements'),
    Output(component_id='cooccurrence-network', component_property='stylesheet')],
    [Input(component_id='submit-val', component_property='n_clicks')],
    [State(component_id='corpus-select', component_property='value'),
    State(component_id='rep', component_property='value'),
    State(component_id='dictionary', component_property='value'),
    State(component_id='term', component_property='value'),
    State(component_id='stat-choice', component_property='value'),
    State(component_id='primary-coocs', component_property='value'),
    State(component_id='secondary-coocs', component_property='value')]
)
def update_network(n_clicks, corpus, rep, dict, term, stat, pri_cooc_num, sec_cooc_num):
    elements = cytoscape_helpers.generate_network(
        corpus, rep, dict, term, stat, pri_cooc_num, sec_cooc_num
    )
    # style = cytoscape_helpers.change_cytoscape_width(stat, rep)
    style = cytoscape_helpers.change_cytoscape_width_auto(elements)
    return elements, style



#### Text display callbacks
# Update the displayed text.
@dash_app.callback(
    Output(component_id='article-markdown', component_property='children'),
    Input(component_id='text-select', component_property='value'),
    State(component_id='search-box', component_property='value')
)
def update_text_dangerous(index, search):
    if search == '':
        boldface = None
    else:
        boldface = search

    if index == '':
        text = '### No matches found'
    else:
        text = text_helpers.text_as_markdown(
            index,
            text_helpers.TEXTS,
            boldface=boldface
        )

    return text



# When corpus changes or search is made, load first doc
@dash_app.callback(
    Output(component_id='text-select', component_property='value'),
    Input(component_id='text-select', component_property='options')
)
def load_first_doc(indices):
    if len(indices) > 1:
        first_doc = indices[0]['value']
    else:
        first_doc = ''
    return first_doc


# Load subcorpus or filter by seach term.
@dash_app.callback(
    Output(component_id='text-select', component_property='options'),
    Input(component_id='sub-corpus', component_property='value'),
    Input(component_id='search-box', component_property='value')
)
def change_corpus(subcorpus, search_term):
    ctx = dash.callback_context
    if not ctx.triggered:
        component_id='sub-corpus'
    else:
        component_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if component_id == 'sub-corpus':
        text_helpers.TEXTS = pd.read_pickle(f'pickles/{subcorpus}sub_df.tar.gz')
        formatted_index = [
            {'label': f"{text_helpers.TEXTS.loc[index]['Title']} ({index})", 'value': index}
            for index in text_helpers.TEXTS.index
        ]
    elif component_id == 'search-box':
        search_index = text_helpers.search_text(text_helpers.TEXTS, search_term)
        formatted_index = [
            {'label': f"{text_helpers.TEXTS.loc[index]['Title']} ({index})", 'value': index}
            for index in search_index
        ]
    else:
        formatted_index = []
    return formatted_index

@dash_app.callback(
    Output(component_id='search-box', component_property='value'),
    Input(component_id='sub-corpus', component_property='value')
)
def reset_searchbox(sub_corpus):
    return ''



### Cooccurrence table updates.
## Load new table on pressing 'submit'
@dash_app.callback(
    Output(component_id='cooc-table', component_property='data'),
    Input(component_id='table-submit-val', component_property='n_clicks'),
    State(component_id='table-corpus-select', component_property='value'),
    State(component_id='table-rep', component_property='value'),
    State(component_id='table-dictionary', component_property='value'),
    State(component_id='table-term', component_property='value'),
    State(component_id='table-stat-choice', component_property='value')
)
def update_table(n_clicks, corpus, rep, dict, term, stat):
    new_df = cooc_table_helpers.return_cooc_df(corpus, dict, term, rep, stat)
    return new_df.to_dict('records')

## Load new search terms on corpus change
@dash_app.callback(
    Output(component_id='table-term', component_property='options'),
    Input(component_id='table-dictionary', component_property='value'),
    Input(component_id='table-corpus-select', component_property='value'),
    Input(component_id='table-rep', component_property='value'),
    Input(component_id='table-stat-choice', component_property='value')
)
def table_return_terms(dict, corpus, rep, stat):
    """
    Given the type of dictionary required (string) for a
    collocation table, return the precalculated options (list).
    """
    words = cooc_table_helpers.load_search_terms(corpus, dict, rep, stat)
    formatted_words = [{'label': word, 'value': word} for word in words]
    return formatted_words

# Restrict dictionary choices based on corpus.
@dash_app.callback(
    Output(component_id='table-dictionary', component_property='options'),
    Input(component_id='table-corpus-select', component_property='value')
)
def return_dictionary_options(corpus):
    """
    Given the corpus name as a string, return possible dictionaries.
    """

    # update options for dictionary choice if corpus is Rel corpus
    default_dict_options = [
        {'label': 'All', 'value': 'all'},
        {'label': 'Proper nouns', 'value': 'propn'},
        {'label': 'Named entities', 'value': 'entities'}
    ]
    if corpus == 'rel_v2_':
        dict_options = [
            {'label': 'All (filtered)', 'value': 'all'},
            {'label': 'All (unfiltered)', 'value': 'all_un'},
            {'label': 'Proper nouns', 'value': 'propn'},
            {'label': 'Named entities', 'value': 'entities'}
        ]
    elif corpus == 'cc_3_' or corpus == 'cc_4_':
        dict_options = [
            {'label': 'Word list supplemented with proper nouns', 'value': 'all'}
        ]
    else:
        dict_options = default_dict_options

    return dict_options


if __name__ == '__main__':
    dash_app.run_server(debug=True)
