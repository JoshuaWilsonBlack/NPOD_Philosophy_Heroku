import dash
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd

import text_content
import cytoscape_helpers
import text_helpers

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = 'Philosophical Discourse in Early New Zealand Newspapers'

server = app.server



app.layout = html.Div([
    dcc.Markdown(children=text_content.opening_text),
    dcc.Tabs([
        dcc.Tab(
            label='View Texts',
            children=text_helpers.text_tab
            ),
        dcc.Tab(
            label='Cooccurence Networks',
            children=cytoscape_helpers.cooc_tab),
        # dcc.Tab(
        #     label='Cooccurence Table',
        #     children=cytoscape_helpers.cooc_table)
    ])
])
# Cooccurence callbacks.
# First, change preloaded search terms given dictionary choice
@app.callback(
    Output(component_id='term', component_property='options'),
    Input(component_id='dictionary', component_property='value')
)
def return_terms(dict_type):
    """
    Given the type of dictionary required (string) for a
    collocation network, return the precalculated options (list).
    """
    if dict_type == 'all':
        words = cytoscape_helpers.ALL_WORD_TERMS
    elif dict_type == 'propn':
        words = cytoscape_helpers.PROPN_TERMS
    elif dict_type == 'entities':
        words = cytoscape_helpers.ENTITY_TERMS

    return [{'label': word, 'value': word} for word in words]

@app.callback(
    Output(component_id='cooccurence-network', component_property='elements'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='rep', component_property='value'),
    State(component_id='dictionary', component_property='value'),
    State(component_id='term', component_property='value'),
    State(component_id='stat-choice', component_property='value'),
    State(component_id='primary-coocs', component_property='value'),
    State(component_id='secondary-coocs', component_property='value'),
)
def update_network(n_clicks, rep, dict, term, stat, pri_cooc_num, sec_cooc_num):
    return cytoscape_helpers.generate_network(
        rep, dict, term, stat, pri_cooc_num, sec_cooc_num
    )

# Text display callbacks
# Update the displayed text.
@app.callback(
    Output(component_id='text-box', component_property='srcDoc'),
    Input(component_id='text-select', component_property='value'),
)
def update_text(index):
    return text_helpers.html_text(
        index,
        text_helpers.TEXTS
    )


# When corpus changes, load first doc
@app.callback(
    Output(component_id='text-select', component_property='value'),
    Input(component_id='text-select', component_property='options')
)
def load_first_doc(indices):
    return indices[0]['value']

# # Filter corpus by search term.
# @app.callback(
#     Output(component_id='text-select', component_property='options'),
#     Input(component_id='search-box', component_property='value'),
#     State(component_id='sub-corpus', component_property='value')
# )
# def search_corpus(search_string, corpus):
#     options = text_helpers.search_text(text_helpers.TEXTS, search_string)
#     return options



# Load subcorpus or filter by seach term.
@app.callback(
    Output(component_id='text-select', component_property='options'),
    Input(component_id='sub-corpus', component_property='value'),
    Input(component_id='search-box', component_property='value')
)
def change_corpus(subcorpus, search_term):
    ctx = dash.callback_context
    if not ctx.triggered:
        component_id='sub_-orpus'
    else:
        component_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if component_id == 'sub-corpus':
        text_helpers.TEXTS = pd.read_pickle(f'pickles/{subcorpus}_sub_df.tar.gz')
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

@app.callback(
    Output(component_id='search-box', component_property='value'),
    Input(component_id='sub-corpus', component_property='value')
)
def reset_searchbox(sub_corpus):
    return ''


if __name__ == '__main__':
    app.run_server(debug=True)
