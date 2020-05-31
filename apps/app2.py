import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from app import app

# app = dash.Dash(__name__)

CODE = '''{
    'data': [
        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'LA'},
    ],
    'layout': {
        'title': 'Dash Data Visualization'
    }
}
'''

# app.layout = html.Div(

layout = html.Div(
    className="app-header",
    children=[
    html.H1("コールバック実験　　Graph編　　　プロパティ：Figure", className="app-header--title"),
    html.Div(children=[
        dcc.Graph(
            id='id2_output_object',
            style={'display':'inline-block', 'width':'48%', 'height': '400px'},
        ),

        html.Div(children=[
            html.Div([
                html.Button('＜＝　プロパティの設定',
                    className="app-button", id='id2_button_send', n_clicks=0,
                ),
                dcc.Textarea(
                    className="app-textarea",
                    id='id2_output_value',
                    style={'width':'100%', 'height': '340px', 'margin-top':'3px'},
                ),
            ]),
        ], style={'display':'inline-block', 'width':'48%', 'float':'top'}),
    ]),
    html.Div(children=[
        dcc.Graph(
            id='id2_input_object',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'LA'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            },
            style={'display':'inline-block', 'width':'48%', 'height': '400px'},
        ),
        html.Div(children=[
            html.Div([
                html.Button('＝＞　プロパティの取得',
                    className="app-button", id='id2_button_get', n_clicks=0,
                ),
                dcc.Textarea(
                    className="app-textarea",
                    style={'width':'100%', 'height': '335px', 'margin-top':'3px',
                           'background-color': 'lightgray'
                    },
                    value=CODE,
                ),
            ]),
        ], style={'display':'inline-block', 'width':'48%', 'float':'top'}),
    ]),
])


@app.callback(
    Output('id2_output_value', 'value'),
    [Input('id2_button_get', 'n_clicks')],
    [State('id2_input_object', 'figure')]
)
def memory_children(n_clicks, figure):
    if not n_clicks:
        return '{}'
    return repr(figure)


@app.callback(
    Output('id2_output_object', 'figure'),
    [Input('id2_button_send', 'n_clicks')],
    [State('id2_output_value', 'value')]
)
def update_output_object(n_clicks, value):
    if not n_clicks:
        return {}
    return eval(value)

if __name__ == "__main__":
    app.run_server(host='localhost', debug=True)
