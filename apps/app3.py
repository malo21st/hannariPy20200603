import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto

from app import app

# app = dash.Dash(__name__)

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
    id='id3_input_object',
    layout={'name': 'circle'},
    elements=simple_elements,
    stylesheet=[
        # Group selectors
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)'
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
        }
    ], style={'display':'inline-block', 'width':'48%', 'height': '400px'},
)
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

layout = html.Div(
    className="app-header",
    children=[
    html.H1("コールバック実験　　Cytoscape編　　　プロパティ：elements", className="app-header--title"),
    html.Div(children=[
        cyto.Cytoscape(
            id='id3_output_object',
            layout={'name': 'circle'},
#            style={'width': '100%', 'height': '400px'},
            elements=[],
            stylesheet=[
                # Group selectors
                {
                    'selector': 'node',
                    'style': {
                        'content': 'data(label)'
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
                }
            ],
            style={'display':'inline-block', 'width':'48%', 'height': '400px'},
        ),
        html.Div(children=[
            html.Div([
                html.Button('＜＝　プロパティの設定',
                    className="app-button",
                    id='id3_button_send', n_clicks=0,
                ),
                dcc.Textarea(
                    className="app-textarea",
                    id='id3_output_value',
                    style={'width':'100%', 'height': '340px'},
                ),
            ]),
        ], style={'display':'inline-block', 'width':'48%', 'float':'top'}),
    ]),
    html.Div(children=[
        cyto.Cytoscape(
            id='id3_input_object',
            layout={'name': 'circle'},
            elements=simple_elements,
            stylesheet=[
                # Group selectors
                {
                    'selector': 'node',
                    'style': {
                        'content': 'data(label)'
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
                }
            ], style={'display':'inline-block', 'width':'48%', 'height': '400px'},
        ),
        html.Div(children=[
            html.Div([
                html.Button('＝＞　プロパティの取得',
                    className="app-button",
                    id='id3_button_get', n_clicks=0,
                ),
                dcc.Textarea(
                    className="app-textarea",
                    style={'width':'100%', 'height': '335px'},
                    value=DATA,
                ),
            ]),
        ], style={'display':'inline-block', 'width':'48%', 'float':'top'}),
    ]),
])


@app.callback(
    Output('id3_output_value', 'value'),
    [Input('id3_button_get', 'n_clicks')],
    [State('id3_input_object', 'elements')]
)
def memory_children(n_clicks, elements):
    if not n_clicks:
        return 'None'
    return repr(elements)


@app.callback(
    Output('id3_output_object', 'elements'),
    [Input('id3_button_send', 'n_clicks')],
    [State('id3_output_value', 'value')]
)
def update_output_object(n_clicks, value):
    if not n_clicks:
        return []
    return eval(value)

if __name__ == "__main__":
    app.run_server(host='localhost', debug=True)
