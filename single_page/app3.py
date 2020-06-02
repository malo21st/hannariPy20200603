import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto

app = dash.Dash(__name__)

DATA = '''[
    {
        'data': {'id': 'A', 'label': 'A'},
        'classes': 'red' # Single class
    },
    {
        'data': {'id': 'B', 'label': 'B'},
        'classes': 'triangle' # Single class
    },
    {
        'data': {'id': 'C', 'label': 'C'},
        'classes': 'red triangle' # Multiple classes
    },
    {
        'data': {'id': 'D', 'label': 'D'},
    },
    {'data': {'source': 'A', 'target': 'B'}, 'classes': 'red'},
    {'data': {'source': 'B', 'target': 'C'}},
    {'data': {'source': 'C', 'target': 'D'}, 'classes': 'red'},
    {'data': {'source': 'B', 'target': 'D'}},
]
=========== Python ===========

cyto.Cytoscape(
    className="app-cytoscape",
    id='id_output_object',
    layout={'name': 'circle'},
    elements=[],
    stylesheet=[
        # Group selectors
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                'font-size': '30vh',
            }
        },
        # Class selectors
        {
            'selector': '.red',
            'style': {
                'background-color': 'red',
                'line-color': 'red'
            }
        },
        {
            'selector': '.triangle',
            'style': {
                'shape': 'triangle'
            }
        },
        {
            'selector': '.blue',
            'style': {
                'background-color': 'blue',
                'line-color': 'blue'
            }
        },
        {
            'selector': '.rectangle',
            'style': {
                'shape': 'rectangle'
            }
        },
        {
            'selector': '.star',
            'style': {
                'shape': 'star'
            }
        },
        {
            'selector': '.vee',
            'style': {
                'shape': 'vee'
            }
        },
        {
            'selector': '.tag',
            'style': {
                'shape': 'tag'
            }
        },
        {
            'selector': '.barrel',
            'style': {
                'shape': 'barrel'
            }
        },
        {
            'selector': '.diamond',
            'style': {
                'shape': 'diamond'
            }
        },
        {
            'selector': '.polygon',
            'style': {
                'shape': 'polygon',
                'shape-polygon-points': '-1 -1  1 -0.5  1 1  -1 0.5',
                'border-width':'1',
                'border-color':'black',
            }
        },
    ],
'''

simple_elements = [
    {
        'data': {'id': 'A', 'label': 'A'},
        'classes': 'red' # Single class
    },
    {
        'data': {'id': 'B', 'label': 'B'},
        'classes': 'triangle' # Single class
    },
    {
        'data': {'id': 'C', 'label': 'C'},
        'classes': 'red triangle' # Multiple classes
    },
    {
        'data': {'id': 'D', 'label': 'D'},
    },
    {'data': {'source': 'A', 'target': 'B'}, 'classes': 'red'},
    {'data': {'source': 'B', 'target': 'C'}},
    {'data': {'source': 'C', 'target': 'D'}, 'classes': 'red'},
    {'data': {'source': 'B', 'target': 'D'}},
]

app.layout = html.Div(
    className="app-header",
    children=[
    html.H1("コールバック実験　　Cytoscape編　　　プロパティ：elements", className="app-header--title"),
    html.Div(children=[
        cyto.Cytoscape(
            className="app-cytoscape",
            id='id_output_object',
            layout={'name': 'circle'},
            elements=[],
            stylesheet=[
                # Group selectors
                {
                    'selector': 'node',
                    'style': {
                        'content': 'data(label)',
                        'font-size': '30vh',
                    }
                },
                # Class selectors
                {
                    'selector': '.red',
                    'style': {
                        'background-color': 'red',
                        'line-color': 'red'
                    }
                },
                {
                    'selector': '.triangle',
                    'style': {
                        'shape': 'triangle'
                    }
                },
                {
                    'selector': '.blue',
                    'style': {
                        'background-color': 'blue',
                        'line-color': 'blue'
                    }
                },
                {
                    'selector': '.rectangle',
                    'style': {
                        'shape': 'rectangle'
                    }
                },
                {
                    'selector': '.star',
                    'style': {
                        'shape': 'star'
                    }
                },
                {
                    'selector': '.vee',
                    'style': {
                        'shape': 'vee'
                    }
                },
                {
                    'selector': '.tag',
                    'style': {
                        'shape': 'tag'
                    }
                },
                {
                    'selector': '.barrel',
                    'style': {
                        'shape': 'barrel'
                    }
                },
                {
                    'selector': '.diamond',
                    'style': {
                        'shape': 'diamond'
                    }
                },
                {
                    'selector': '.polygon',
                    'style': {
                        'shape': 'polygon',
                        'shape-polygon-points': '-1 -1  1 -0.5  1 1  -1 0.5',
                        'border-width':'1',
                        'border-color':'black',
                    }
                },
            ],
            style={'display':'inline-block', 'width':'48%', 'height': '390px'},
        ),
        html.Div(children=[
            html.Div([
                html.Button('＜＝　プロパティの設定',
                    className="app-button", id='id_button_send', n_clicks=0,
                ),
                dcc.Textarea(
                    className="app-textarea",
                    id='id_output_value',
                    style={'width':'100%', 'height': '330px', 'margin-top':'3px'},
                ),
            ]),
        ], style={'display':'inline-block', 'width':'48%', 'float':'top'}),
    ]),
    html.Div(children=[
        cyto.Cytoscape(
            className="app-cytoscape",
            id='id_input_object',
            layout={'name': 'circle'},
            elements=simple_elements,
            stylesheet=[
                # Group selectors
                {
                    'selector': 'node',
                    'style': {
                        'content': 'data(label)',
                        'font-size': '30vh',
                    }
                },

                # Class selectors
                {
                    'selector': '.red',
                    'style': {
                        'background-color': 'red',
                        'line-color': 'red'
                    }
                },
                {
                    'selector': '.triangle',
                    'style': {
                        'shape': 'triangle'
                    }
                },
            ], style={'display':'inline-block', 'width':'48%', 'height': '390px'},
        ),
        html.Div(children=[
            html.Div([
                html.Button('＝＞　プロパティの取得',
                    className="app-button", id='id_button_get', n_clicks=0,
                ),
                dcc.Textarea(
                    className="app-textarea",
                    style={'width':'100%', 'height': '330px', 'margin-top':'3px',
                           'background-color': 'lightgray'
                    },
                    value=DATA,
                ),
            ]),
        ], style={'display':'inline-block', 'width':'48%', 'float':'top'}),
    ]),
])


@app.callback(
    Output('id_output_value', 'value'),
    [Input('id_button_get', 'n_clicks')],
    [State('id_input_object', 'elements')]
)
def memory_children(n_clicks, elements):
    if not n_clicks:
        return '[]'
    return repr(elements)


@app.callback(
    Output('id_output_object', 'elements'),
    [Input('id_button_send', 'n_clicks')],
    [State('id_output_value', 'value')]
)
def update_output_object(n_clicks, value):
    if not n_clicks:
        return []
    return eval(value)

if __name__ == "__main__":
    app.run_server(host='localhost', debug=True)
