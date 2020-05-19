import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto
import dash_table

import pandas as pd
from collections import OrderedDict

from app import app

#app = dash.Dash(__name__)

df_table = pd.DataFrame(OrderedDict([
    ('No',    ['01', '02', '03', '04', '05', '06', '07']),
    ('Source',[None, None, None, None, None, None, None]),
    ('Target',[None, None, None, None, None, None, None]),
    ('Classes',[None, None, None, None, None, None, None]),
 ]))

list_NODE = [c for c in "ABCDEFG"]
list_CLASS = ['red', 'blue']

layout = html.Div(
    className="app-header",
    children=[
    html.H1("コールバック実験　　連携編　　　プロパティ：data (DataTable)  =>  elements (Cytoscape)", className="app-header--title"),
    html.Div([
        html.Div([
            cyto.Cytoscape(
                id='id4_output_object',
                layout={'name': 'circle'},
                elements=[],
                stylesheet=[
                    # Group selectors
                    {
                        'selector': 'node',
                        'style': {
                            'content': 'data(label)'
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'curve-style': 'bezier',
                            'target-arrow-shape': 'triangle',
                            'width':5,
                        }
                    },
                    # Class selectors
                    {
                        'selector': '.red',
                        'style': {
                            'background-color': 'red',
                            'line-color': 'red',
                            'target-arrow-color': 'red',
                        }
                    },
                    {
                        'selector': '.blue',
                        'style': {
                            'background-color': 'blue',
                            'line-color': 'blue',
                            'target-arrow-color': 'blue',
                        }
                    },
                    {
                        'selector': '.triangle',
                        'style': {
                            'shape': 'triangle'
                        }
                    },
                    {
                        'selector': '.rectangle',
                        'style': {
                            'shape': 'rectangle'
                        }
                    }
                ], style={'width':'100%', 'height':'380px'}),
        ], style={'display':'inline-block', 'width':'45%'}),
        html.Div([
            html.Div([
                html.Button('＜＝　プロパティの設定',
                    className="app-button", 
                    id='id4_button_send', n_clicks=0,
                ),
                dcc.Textarea(
                    className="app-textarea",
                    id='id4_output_value',
                    style={'width':'100%', 'height': '335px'},
                ),
                html.Button('↑↑↑　データ変換　↑↑↑',
                    className="app-button", 
                    id='id4_button_trans', n_clicks=0,
                ),
            ]),
        ], style={'display':'inline-block', 'width':'45%'}),
    ]),
    html.Div(children="　"),
    html.Div([
        html.Div([
            dash_table.DataTable(
                id='id4_input_object',
                data=df_table.to_dict('records'),
                style_table={'width':'95%', 'height':'350px'},
                columns=[
                    {'id': 'No', 'name': '', 'editable': False},
                    {'id': 'Source', 'name': 'Source', 'presentation': 'dropdown'},
                    {'id': 'Target', 'name': 'Target', 'presentation': 'dropdown'},
                    {'id': 'Classes', 'name': 'Classes', 'presentation': 'dropdown'},
                ],
                editable=True,
                dropdown={
                    'Source':{'options':[{'label':c, 'value':c} for c in list_NODE]},
                    'Target':{'options':[{'label':c, 'value':c} for c in list_NODE]},
                    'Classes':{'options':[{'label':c, 'value':c} for c in list_CLASS]},
                },
                style_cell_conditional=[
                    {'width':'80px'},
                    {'if':{'column_id':'No'}, 'width':'30px'},
                    {'textAlign':'center'},
                ],
                style_data_conditional=[
                    {
                        'if':{
                            'filter_query':'{Classes}="blue"',
                            'column_id':'Source',
                        },
                        'backgroundColor':'#39CCCC',
                    },
                    {
                        'if':{
                            'filter_query':'{Classes}="blue"',
                            'column_id':'Classes',
                        },
                        'backgroundColor':'#39CCCC',
                    },
                    {
                        'if':{
                            'filter_query':'{Classes}="red"',
                            'column_id':'Source',
                        },
                        'backgroundColor':'#FF4136',
                    },
                    {
                        'if':{
                            'filter_query':'{Classes}="red"',
                            'column_id':'Classes',
                        },
                        'backgroundColor':'#FF4136',
                    },
                ]
            ),
        ], style={'display':'inline-block', 'width':'45%', 'height':'100%', 'float':'left'}),

        html.Div([
            html.Div([
                html.Button('＝＞　プロパティの取得',
                    className="app-button", 
                    id='id4_button_get', n_clicks=0,
                ),
                dcc.Textarea(
                    className="app-textarea",
                    id='id4_input_value',
                    style={'width':'100%', 'height': '250px'},
                    value="[]",
                ),
            ]),
        ], style={'display':'inline-block', 'width':'45%'}),
    ])
])


@app.callback(
    Output('id4_input_value', 'value'),
    [Input('id4_button_get', 'n_clicks')],
    [State('id4_input_object', 'data')]
)
def update_input_value(n_clicks, data):
    if not n_clicks:
        return repr([])
    ##　改行を入れて再編集
    str_data = "[\n"
    for d in data:
        str_data += "{},\n".format(repr(d))
    else:
        str_data += "]"

    return str_data


@app.callback(
    Output('id4_output_value', 'value'),
    [Input('id4_button_trans', 'n_clicks')],
    [State('id4_input_value', 'value')]
)
def trans_output_value(n_clicks, value):
    if not n_clicks:
        return "[]"
    cyto_data = trans_data(value)
    return cyto_data


@app.callback(
    Output('id4_output_object', 'elements'),
    [Input('id4_button_send', 'n_clicks')],
    [State('id4_output_value', 'value')]
)
def update_output_object(n_clicks, value):
    if not n_clicks:
        return []
    return eval(value)
#    return eval(value.rstrip("\n"))


def trans_data(data):
    columns = ['Source', 'Target', 'Classes']

    # 前処理
    df = pd.DataFrame(index=[], columns=columns, dtype=object)
    for d in eval(data):
        row = [d['Source'], d['Target'], d['Classes']]
        sr = pd.Series(row, index=df.columns)
        df = df.append(sr, ignore_index=True)

    sr_S = df['Source'].dropna()
    sr_T = df['Target'].dropna()
    sr_ST = pd.concat([sr_S, sr_T]).unique()
    df_ST = df.dropna(subset = ['Source', 'Target'])

    # 出力（elements）の編集
    elements = []
    ##　ノードの編集
    for node in sr_ST:
        dic_node = {'data': {'id': None, 'label': None}, 
                    'classes': '_'
                    }
        dic_node['data']['id'] = node
        dic_node['data']['label'] = node

        try:
            if node in list(df['Source'][df['Classes']=='red']):
                dic_node['classes'] = 'red'
            elif node in list(df['Source'][df['Classes']=='blue']):
                dic_node['classes'] = 'blue'
        except:
            dic_node['classes'] = '_'        
        elements.append(dic_node) 
    ##　エッジの編集
    for edge in df_ST.iterrows():
        dic_edge = {'data': {'source': None, 'target': None},
                    'classes': '_',
                    }
        dic_edge['data']['source'] = edge[1][0]
        dic_edge['data']['target'] = edge[1][1]
        dic_edge['classes'] = df['Classes'][df['Source']==edge[1][0]].values[0]
        elements.append(dic_edge)

    ##　改行を入れて再編集
    str_elements = "[\n"
    for d in elements:
        str_elements += "{},\n".format(repr(d))
    else:
        str_elements += "]"

    return str_elements


if __name__ == "__main__":
    app.run_server(host='localhost', debug=True)
