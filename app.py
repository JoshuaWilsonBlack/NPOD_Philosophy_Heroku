import dash
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output, State

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
            children=cytoscape_helpers.cooc_tab)
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
@app.callback(
    Output(component_id='text-display', component_property='children'),
    Input(component_id='text-select', component_property='value')
)
def update_text(value):
    return text_helpers.text_as_html(value)


if __name__ == '__main__':
    app.run_server(debug=True)
