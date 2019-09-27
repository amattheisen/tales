# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


EXTERNAL_STYLESHEETS = ['style.css']
CONTENT = {
    'a': dcc.Markdown("""This is the A page.

![Image](static/a.jpg)"""),
    'b': dcc.Markdown("""This is the B page.
        
![Image](static/b.jpg)"""),
    'up': dcc.Markdown("""This is the Up page.

![Image](static/up.jpg)"""),
    'down': dcc.Markdown("""This is the Down page.

![Image](static/down.jpg)"""),
    'left': dcc.Markdown("""This is the Left page.

![Image](static/left.jpg)"""),
    'right': dcc.Markdown("""This is the Right page.

![Image](static/right.jpg)"""),
    'start': dcc.Markdown("""This is the Start page.

![Image](static/start.jpg)"""),
    'select': dcc.Markdown("""This is the Select page.

![Image](static/select.jpg)"""),
}

app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

app.layout = html.Div(children=[
    html.H1(children='Tales'),
    html.Div(children="""
        Built on Dash: A web application framework for Python.
        """),

    #dcc.Graph(
    #    id='example-graph',
    #    figure={
    #        'data': [
    #            {'x': [1, 2, 3], 'y': [4, 1, 2],
    #             'type': 'bar',
    #             'name': 'SF'},
    #            {'x': [1, 2, 3], 'y': [2, 4, 5],
    #             'type': 'bar',
    #             'name': u'Montréal'},
    #        ],
    #        'layout': {
    #            'title': 'Dash Data Visualization'
    #        },
    #    },
    #),
    dcc.RadioItems(id='selector', value='start',
        options=[
            {'label': 'Up', 'value': 'up'},
            {'label': 'Down', 'value': 'down'},
            {'label': 'Left', 'value': 'left'},
            {'label': 'Right', 'value': 'right'},
            {'label': 'A', 'value': 'a'},
            {'label': 'B', 'value': 'b'},
            {'label': 'Select', 'value': 'select'},
            {'label': 'Start', 'value': 'start'},
            {'label': 'Clear', 'value': 'clear'},
            {'label': 'Back', 'value': 'back'},
        ],
    ),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    # html.Button(id='back', n_clicks=0, children='Back'),
    html.Div(id='err', style={'color': 'red'}),
    html.Div(id='history'),
    html.Div(id='content'),
])


@app.callback([Output('content', 'children'),
               Output('history', 'children'),
               Output('err', 'children')],
              [Input('submit-button', 'n_clicks')],
              [State('content', 'children'),
               State('history', 'children'),
               State('selector', 'value')])
def update_browsing_history(n_clicks, content, old_value, new_value):
    """
    Update browsing history using selector each time the Append button is clicked.

    """
    # # Don't accept inputs containing quotes or commas
    # if new_value.find('\"') >= 0:
    #     return dash.no_update, 'ERROR: Do not include Quotes', ''
    # if new_value.find(',') >= 0:
    #     return dash.no_update, 'ERROR: Do not include Commas', ''

    # Clear History
    if new_value == "clear":
        return CONTENT['start'], '{' + "{}: \"start\"".format(n_clicks) + '}', ''

    # Back (delete last history entry)
    if new_value == "back":
        # split off last value
        split_value = old_value.split(',')
        if len(split_value) > 1:
            old_value = ','.join(split_value[:-1]) + '}'
            last_value = split_value[-2].split(':')[1][2:-1]
            return CONTENT[last_value], old_value, ''
        else:
            return CONTENT['start'], '{' + "{}: \"start\"".format(n_clicks) + '}', ''

    # Standard processing
    new_value_str = "{}: \"{}\"".format(n_clicks, new_value)
    if not old_value or len(old_value) <= 2:
        new_value_str = '{' + new_value_str + '}'
    else:
        new_value_str = '{' + ', '.join([old_value[1:-1], new_value_str]) + '}'
    return CONTENT[new_value], new_value_str, ''



if __name__ == '__main__':
      app.run_server(host='0.0.0.0', debug=True)
