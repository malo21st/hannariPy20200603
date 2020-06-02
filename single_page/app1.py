import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table
import dash_cytoscape as cyto

import pandas as pd
from collections import OrderedDict

import my_style
import table_to_cyto

app = dash.Dash(__name__)
server = app.server

app.css.config.serve_locally = True

TITLE = '最短経路問題を解いてみよう'

USAGE = '''
## 最短経路問題とは
 - グラフ理論における最短経路問題（shortest path problem）とは、重み付きグラフの与えられた
 ２つのノード間を結ぶ経路の中で、重みが最小の経路を求める最適化問題のことです。
## 使い方
 - 右のテーブルにデータを入力して下さい。
 - 「最短経路」ボタンを押すと、画面右下に最短経路を表示します。
 - 「事例読込」ボタンを押すと、入力例を表示しますので、「最短経路」ボタンを押して下さい。
 - 「クリア」ボタンを押すと、画面をクリアします。
'''

df_table = pd.DataFrame(OrderedDict([
    ('No',    ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']),
    ('Source',[None, None, None, None, None, None, None, None, None, None]),
    ('Target',[None, None, None, None, None, None, None, None, None, None]),
    ('Weight',[None, None, None, None, None, None, None, None, None, None]),
    ('S_G',   [None, None, None, None, None, None, None, None, None, None]),
]))

df_ex_table = pd.DataFrame(OrderedDict([
    ('No',    ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']),
    ('Source',['A', 'B', 'C', 'D', 'E', 'C', 'A', 'A', 'B', None]),
    ('Target',['B', 'C', 'D', 'E', 'F', 'E', 'C', 'D', 'F', None]),
    ('Weight',[5, 2, 3, 6, 4, 2, 4, 2, 6, None]),
    ('S_G',   ['START', None, None, None, 'GOAL', None, None, None, None, None]),
]))

list_NODE = [c for c in "ABCDEFGHIJ"]
list_SG   = ['START', 'GOAL']

app.layout = html.Div(
    className="app-header",
    children=[
# 最上段　タイトル
    html.H1(TITLE, className="app-header--title"),
    html.Div([
# 上段左　説明
        html.Div([
            dcc.Markdown(
                className="app-usage",
                children=USAGE,
            ),
        ], style={'display':'inline-block', 'width':'40%', 'height':'100%', 'float':'left'}, #'align-self':'flex-start'},),
        ),
# 上段中　データ入力用のテーブル
        html.Div([
            dash_table.DataTable(
                id='id_table',
                data=df_table.to_dict('records'),
                columns=[
                    {'id': 'No', 'name': '', 'editable': False},
                    {'id': 'Source', 'name': 'Source', 'presentation': 'dropdown'},
                    {'id': 'Target', 'name': 'Target', 'presentation': 'dropdown'},
                    {'id': 'Weight', 'name': 'Weight'}, #, 'presentation': 'dropdown'},
                    {'id': 'S_G', 'name': 'START/GOAL', 'presentation': 'dropdown'},
                ],
                editable=True,
                dropdown={
                    'Source':{'options':[{'label':c, 'value':c} for c in list_NODE]},
                    'Target':{'options':[{'label':c, 'value':c} for c in list_NODE]},
                    'S_G'   :{'options':[{'label':s, 'value':s} for s in list_SG]},
                },
                style_cell_conditional=[
                    {'width':'90px'},
                    {'if':{'column_id':'No'}, 'width':'40px'},
                    {'textAlign':'center'},
                    {'fontSize':20},
                ],
                style_data_conditional=my_style.get_style_data_conditional()
            )
        ], style={'display':'inline-block', 'width':'40%'}),
# 上段右　処理結果の出力用ボタン
        html.Div(
            className="app-button-area",
            children=[
                html.Div([
                    html.Button('最短経路', 
                        className="app-button", id='id_btn_done', n_clicks=0,
                    ),
                ], style={'height':'80px','margin-top':'30px'}),
                html.Div([
                    html.Button('事例読込', 
                        className="app-button", id='id_btn_load', n_clicks=0,
                    ),
                ], style={'height':'80px'}),
                html.Div([
                    html.Button('ク リ ア', 
                        className="app-button", id='id_btn_clear', n_clicks=0,
                    ),
                ], style={'height':'80px'}),
        ],style={'display':'inline-block', 'width':'18%', 'float':'right'}),
    ]),
# ここから下段    
    html.Div(
        className="app-output",
        children=[
# 下段左　入力データ確認用の表示エリア
        html.Div([
            cyto.Cytoscape(
                className="app-cytoscape",
                id='id_problem',
                elements=[],
                style={'width':'100%', 'height': '400px'},
                layout={'name':'circle'},
                stylesheet=my_style.get_stylesheet()
            )
        ], style={'display':'inline-block', 'width':'45%'},
        ),
# 下段右　処理結果の表示エリア
        html.Div([
            cyto.Cytoscape(
                className="app-cytoscape",
                id='id_answer',
                elements=[],
                style={'width':'100%', 'height': '400px'},
                layout={'name':'circle',
                        'padding': 10
                        },
                stylesheet=my_style.get_stylesheet()
            )
        ], style={'display':'inline-block', 'width': "45%"},
        ),
    ]),
])


@app.callback(
    Output('id_problem', 'elements'),
    [Input('id_table', 'data')]
)
def update_problem(data):
    if not data:
        return [] 

    return table_to_cyto.get_elements(data)

@app.callback(
    Output('id_answer', 'elements'),
    [Input('id_btn_done', 'n_clicks'),
     Input('id_btn_load', 'n_clicks'),
     Input('id_btn_clear', 'n_clicks')],
    [State('id_table', 'data')]
)
def update_answer(btn_done, btn_load, btn_clear, data):
    # プログラム起動時のコールバック（ボタンを押さなくても作動する）
    if not data:
        return []
    ctx = dash.callback_context
    if not ctx.triggered:
        return []
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'id_btn_done':
        return table_to_cyto.get_shortest_path(data)
    elif button_id == 'id_btn_load':
        return []
    elif button_id == 'id_btn_clear':
        return []

@app.callback(
    Output('id_table', 'data'),
    [Input('id_btn_load', 'n_clicks'),
     Input('id_btn_clear', 'n_clicks')],
)
def update_table(btn_load, btn_clear):
    # プログラム起動時のコールバック（ボタンを押さなくても作動する）
    ctx = dash.callback_context
    if not ctx.triggered:
        return df_table.to_dict('records')
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'id_btn_load':
        return df_ex_table.to_dict('records')
    elif button_id == 'id_btn_clear':
        return df_table.to_dict('records')


if __name__ == "__main__":
    app.run_server(host='localhost', debug=True)
#    app.run_server(debug=True)
