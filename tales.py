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

    dcc.Store(id='session', storage_type='session'),
    # I would like to convert the radio items and submit button into 
    # a group of buttons instead.
    #dcc.RadioItems(id='selector', value='start',
    #    options=[
    #        {'label': 'Up', 'value': 'up'},
    #        {'label': 'Down', 'value': 'down'},
    #        {'label': 'Left', 'value': 'left'},
    #        {'label': 'Right', 'value': 'right'},
    #        {'label': 'A', 'value': 'a'},
    #        {'label': 'B', 'value': 'b'},
    #        {'label': 'Select', 'value': 'select'},
    #        {'label': 'Start', 'value': 'start'},
    #        {'label': 'Clear', 'value': 'clear'},
    #        {'label': 'Back', 'value': 'back'},
    #    ],
    #),
    #html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Button(id='a', n_clicks=0, children='a'),
    html.Button(id='b', n_clicks=0, children='b'),
    html.Button(id='up', n_clicks=0, children='up'),
    html.Button(id='down', n_clicks=0, children='down'),
    html.Button(id='left', n_clicks=0, children='left'),
    html.Button(id='right', n_clicks=0, children='right'),
    html.Button(id='select', n_clicks=0, children='select'),
    html.Button(id='start', n_clicks=0, children='start'),
    html.Button(id='back', n_clicks=0, children='back'),
    html.Button(id='clear', n_clicks=0, children='clear'),
    html.Div(id='err', style={'color': 'red'}),
    html.Div(id='history'),
    html.Div(id='content'),
])


@app.callback([Output('content', 'children'),
               Output('history', 'children'),
               Output('err', 'children')],
              [Input('a', 'n_clicks'),
               Input('b', 'n_clicks'),
               Input('up', 'n_clicks'),
               Input('down', 'n_clicks'),
               Input('left', 'n_clicks'),
               Input('right', 'n_clicks'),
               Input('select', 'n_clicks'),
               Input('start', 'n_clicks'),
               Input('back', 'n_clicks'),
               Input('clear', 'n_clicks')],
              [State('content', 'children'),
               State('history', 'children')])
def update_browsing_history(a, b, up, down, left, right, select, start, back,
        clear, content, old_value):
    """
    Update browsing history from a button press.

    """
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
        n_clicks = 0
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        n_clicks = ctx.triggered[0]['value']

    # Clear History
    if button_id == "clear":
        return CONTENT['start'], '{' + "{}: \"start\"".format(n_clicks) + '}', ''

    # Back (delete last history entry)
    if button_id == "back":
        # split off last value
        split_value = old_value.split(',')
        if len(split_value) > 1:
            old_value = ','.join(split_value[:-1]) + '}'
            last_value = split_value[-2].split(':')[1][2:-1]
            return CONTENT[last_value], old_value, ''
        else:
            return CONTENT['start'], '{' + "{}: \"start\"".format(n_clicks) + '}', ''

    # Standard processing
    new_value_str = "{}: \"{}\"".format(n_clicks, button_id)
    if not old_value or len(old_value) <= 2:
        new_value_str = '{' + new_value_str + '}'
    else:
        new_value_str = '{' + ', '.join([old_value[1:-1], new_value_str]) + '}'
    return CONTENT[button_id], new_value_str, ''


## XYZ BUTTON PRESS
#@app.callback([Output('content', 'children'),
#               Output('history', 'children'),
#               Output('err', 'children')],
#              [Input('up-button', 'children')],
#              [State('content', 'children'),
#               State('history', 'children'),
#               ])
#def update_browsing_history(up, down, content, old_value):
#    """
#    Update browsing history using selector each time the Append button is clicked.
#
#    """
#
#    # Clear History
#    if new_value == "clear":
#        return CONTENT['start'], '{' + "{}: \"start\"".format(n_clicks) + '}', ''
#
#    # Back (delete last history entry)
#    if new_value == "back":
#        # split off last value
#        split_value = old_value.split(',')
#        if len(split_value) > 1:
#            old_value = ','.join(split_value[:-1]) + '}'
#            last_value = split_value[-2].split(':')[1][2:-1]
#            return CONTENT[last_value], old_value, ''
#        else:
#            return CONTENT['start'], '{' + "{}: \"start\"".format(n_clicks) + '}', ''
#
#    # Standard processing
#    new_value_str = "{}: \"{}\"".format(n_clicks, new_value)
#    if not old_value or len(old_value) <= 2:
#        new_value_str = '{' + new_value_str + '}'
#    else:
#        new_value_str = '{' + ', '.join([old_value[1:-1], new_value_str]) + '}'
#    return CONTENT[new_value], new_value_str, ''



if __name__ == '__main__':
      app.run_server(host='0.0.0.0', debug=True)
