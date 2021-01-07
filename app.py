import dash
import dash_core_components as dcc
import dash_html_components as html

import text_content

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

top_markdown_text = '''
This is my first deployed app
'''

# philo_cytoscape = cyto.Cytoscape(
#         id='philosophy-network',
#         minZoom=1,
#         layout={'name': 'cose'},
#         style={'width': '100%', 'height': '800px'},
#         elements=philo_net,
#         stylesheet=[
#             {
#                 'selector': 'edge',
#                 'style': {
#                     'width': 'mapData(weight, 3, 6, 1, 3)',
#                     'line-color': 'silver'
#                 }
#             },
#             {
#                 'selector': 'node',
#                 'style': {
#                     'content': 'data(label)',
#                     'width': 'mapData(size, 1, 10, 10, 20)',
#                     'height': 'mapData(size, 1, 10, 10, 20)'
#                 }
#             },
#             {
#                 'selector': 'label',
#                 'style': {
#                     'font-size': 6,
#                     'text-valign': 'center',
#                     'text-background-color': 'white',
#                     'text-background-opacity': 0.6,
#                     'text-background-padding': 1,
#                     'text-border-color': 'black',
#                     'text-border-opacity': 1,
#                     'text-border-width': 0.5
#                 }
#             }
#         ]
#     )

app.layout = html.Div([
    dcc.Markdown(children=text_content.opening_text),
    dcc.Input(
        id='search-term',
        type='text',
        value='philosophy'
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
    html.Button('Submit', id='submit-val', n_clicks=0)#,
    #philo_cytoscape
])
#
# @app.callback(
#     Output(component_id='philosophy-network', component_property='elements'),
#     Input(component_id='submit-val', component_property='n_clicks'),
#     State(component_id='stat-choice', component_property='value'),
#     State(component_id='search-term', component_property='value'),
# )
# def update_network_stat(n_clicks, stat_value, search_value):
#     network = NL_helpers.network_dash(
#         term=search_value,
#         stat=stat_value,
#         dtm=dtm,
#         ttm=tt_df,
#         num_coocs=10,
#         sec_coocs=5
#     )
#     return network

if __name__ == '__main__':
    app.run_server(debug=True)
