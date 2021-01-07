import re

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

TEXTS = pd.read_pickle('pickles/philoso_sub_df.tar.gz')

# TO DO: Bring back search function
def text_as_html(index):
    """Given article index, return formatted using Dash html components."""
    html_components = []

    title = TEXTS.loc[index, 'Title']
    html_components.append(html.H2(title))

    date = index[index.find('_')+1:index.find('_')+9]
    newspaper = index[0:index.find('_')]
    html_components.append(html.H3(f"{newspaper}-{date}"))

    text_blocks = TEXTS.loc[index, 'Text']
    for block in text_blocks:
        html_components.append(html.P(block))

    return html_components


text_tab = [
    # html.P('Filter by search term (regex)'),
    # dcc.Input(
    #     id='search-box',
    #     value='',
    #     type='search'
    # )
    html.P('Select text'),
    dcc.Dropdown(
        id='text-select',
        options=[
            {'label': f"{TEXTS.loc[index]['Title']} ({index})", 'value': index}
            for index in TEXTS.index
        ],
        value=TEXTS.index[0]
    ),
    html.Div(
        id = 'text-display',
        children=text_as_html(TEXTS.index[0]),
        style={'width': '80%',
            'padding-left': '40px'}
    )
]
