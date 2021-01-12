import html as python_html
import re

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

TEXTS = pd.read_pickle('pickles/philoso_sub_df.tar.gz')

text_style = """
<style>
h3, h4   {font-family: sans-serif;}
p    {font-family: serif;}
</style>
"""


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



def html_text(index, dataframe, boldface=None):
    """
    Given article code, return html formatted text
    containing both heading and body text. Optionally, boldface
    matches of the boldface regex expression.
    Assumes dataframe contains a 'Text' column containing lists of
    strings as entries as well as 'Title', 'Newspaper' columns
    containing strings and a 'Date' column containing integers.

    I only escape html characters in the title and text. Newspaper and
    data should not have any html in them. Leaving them unescaped
    increases the chance of finding any such errors.
    """
    date = index[index.find('_')+1:index.find('_')+9]
    newspaper = index[0:index.find('_')]
    title = python_html.escape(dataframe.loc[index, 'Title'])
    text_blocks = dataframe.loc[index, 'Text']
    text = ''
    for block in text_blocks:
        tagged_string = f'<p>{python_html.escape(block)}</p>'
        text += tagged_string

    if boldface:
        match = re.search(boldface, text)
        if match:
            text = re.sub(boldface, f'<b>{match.group(0)}</b>', text)

    article_string = f"""
<!DOCTYPE html>
<html>
<head>
{text_style}
</head>
<body>
<h3>{title}</h3>
<h4>{newspaper} - {date}</h4>
{text}'
"""

    return article_string



def search_text(dataframe, re_string, lower=False):
    """
    Given dataframe with 'Text' column as described above, search for
    re string within 'Text' column content and return article codes
    containing the search string.

    This can be very slow. OK on starter pack dataset though.
    """
    if re_string == '':
        article_codes = dataframe.index
    else:
        article_codes = set()
        for row in dataframe.itertuples():
            for string in row.Text:

                if lower:
                    string = string.lower()

                match = re.search(re_string, string)

                if match:
                    article_codes.add(row.Index)

    return list(article_codes)



text_tab = [
    html.P('Select sub-corpus (random sample of 500 articles)'),
    dcc.Dropdown(
        id='sub-corpus',
        options=[
            {'label': 'Keyword search ("philoso*")', 'value': 'philoso'},
            {'label': 'Naive Bayes 1', 'value': 'nb1'},
            {'label': 'Naive Bayes 2', 'value': 'nb2'}
        ],
        value='philoso',
        style={'width': '70%'}
    ),
    html.P('Filter by search term (regex)'),
    dcc.Input(
        id='search-box',
        value='',
        type='search',
        style={'width': '50%'}
    ),
    html.P('Select text'),
    dcc.Dropdown(
        id='text-select',
        options=[
            {'label': f"{TEXTS.loc[index]['Title']} ({index})", 'value': index}
            for index in TEXTS.index
        ],
        value=TEXTS.index[0],
        style={'width': '70%'}
    ),
    html.Div(
        id = 'text-display',
        children=html.Iframe(
            id='text-box',
            sandbox='',
            srcDoc=html_text(TEXTS.index[0], TEXTS, boldface='the'),
            style={'width': '90%',
                'height': '1000px',
                'border': '0px',
                'padding': '40px'}
            ),
        style={'width': '100%',
            'padding-left': '40px'}
    )
]
