import html as python_html
import re
import pickle

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

TEXTS = pd.read_pickle('pickles/philoso_sub_df.tar.gz')
with open('pickles/codes2names_web.pickle', 'rb') as fin:
    CODES2NAMES_WEB = pickle.load(fin)
with open('pickles/codes2names.pickle', 'rb') as fin:
    CODES2NAMES = pickle.load(fin)



def escape_markdown(string):
    """Escape characters which have functions in markdown strings.
    Return escaped string."""

    markdown_escape_chars = r"\`*_{}[]<>()#+-.!|"
    for escape_char in markdown_escape_chars:
        string = string.replace(escape_char, "\\"+escape_char)

    return string



def text_as_markdown(index, dataframe, boldface=None):
    """Render article corresponding to index in dataframe as markdown
    string. Any matches for boldface are rendered in bold.
    """

    date = index[index.find('_')+1:index.find('_')+9]
    newspaper = index[0:index.find('_')]

    title = (dataframe.loc[index, 'Title'])
    title = escape_markdown(title)

    web_prefix = "https://paperspast.natlib.govt.nz/newspapers/"
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    web_address = f"{web_prefix}{CODES2NAMES_WEB[newspaper]}/{year}/{month}/{day}"

    text_blocks = dataframe.loc[index, 'Text']
    text = ''
    for block in text_blocks:
        paragraph = escape_markdown(block)
        text += paragraph + '\n\n'

    if boldface:
        match = re.search(boldface, text)
        if match:
            text = re.sub(boldface, f'***{match.group(0)}***', text)

    markdown_text = f"""## {title}

*{CODES2NAMES[newspaper]}*

{day}/{month}/{year}

[View issue on Papers Past]({web_address})

{text}
"""

    return markdown_text



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
    dcc.Markdown(
        id = 'article-markdown',
        children = text_as_markdown(TEXTS.index[0], TEXTS, boldface='the'),
        style={'width': '70%',
            'padding': '50px'}
    )
]
