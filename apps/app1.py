import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table
import dash_cytoscape as cyto

import pandas as pd
from collections import OrderedDict
import networkx as nx
from criticalpath import Node

from app import app

# app = dash.Dash(__name__)
# server = app.server

# app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

USAGE = '''
### クリティカルパスとは
 - プロジェクトの各工程を、プロジェクト開始から終了まで「前の工程が終わらないと次の工程が始まらない」という依存関係に従って結んでいったときに、所要時間が最長となる経路のこと。
 - どの工程が原因でスケジュールに遅れが発生しているか。ボトルネックは何か。課題をいち早く見つけることに役立ちます。

### 使い方
 - 右のテーブルにデータを入力して下さい。
 - 「クリティカルパス」ボタンを押すと、画面右下にクリティカルパスを表示します。
'''

df_table = pd.DataFrame(OrderedDict([
    ('No',    ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']),
    ('Source',[None, None, None, None, None, None, None, None, None, None]),
    ('Target',[None, None, None, None, None, None, None, None, None, None]),
    ('Weight',[None, None, None, None, None, None, None, None, None, None]),
    ('S_G',   [None, None, None, None, None, None, None, None, None, None]),
]))

# df_table = pd.DataFrame(OrderedDict([
#     ('No',    ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']),
#     ('Source',[ 'A',  'A',  'A',  'B',  'C',  'C',  'D',  'D',  'E', None]),
#     ('Target',[ 'B',  'C',  'D',  'D',  'D',  'E',  'E',  'F',  'F', None]),
#     ('Weight',[   6,    5,    5,    4,    0,    3,    7,   10,    8, None]),
#     ('S_G',   ['START', None, None, None, None, None, None, None ,'GOAL', None]),
# ]))

list_NODE = [c for c in "ABCDEFGHIJ"]
list_WGT  = [i for i in range(11)]
list_SG   = ['START', 'GOAL']

layout = html.Div(
    className="app-header",
    children=[
# 最上段　タイトル
    html.H1("クリティカルパスを解いてみよう", className="app-header--title"),
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
                        {'id': 'Weight', 'name': 'Duration'}, #, 'presentation': 'dropdown'},
                        {'id': 'S_G', 'name': 'START/GOAL', 'presentation': 'dropdown'},
                    ],
                    editable=True,
                    dropdown={
                        'Source':{'options':[{'label':c, 'value':c} for c in list_NODE]},
                        'Target':{'options':[{'label':c, 'value':c} for c in list_NODE]},
                        'Weight':{'options':[{'label':str(i), 'value':i} for i in list_WGT]},
                        'S_G'   :{'options':[{'label':s, 'value':s} for s in list_SG]},
                    },
                    style_cell_conditional=[
                        {'width':'90px'},
                        {'if':{'column_id':'No'}, 'width':'40px'},
                        {'textAlign':'center'},
                    ],
                    style_data_conditional=[
                        {
                            'if':{
                                'filter_query':'{S_G}="START"',
                                'column_id':'Source',
                            },
                            'backgroundColor':'#39CCCC',
                        },
                        {
                            'if':{
                                'filter_query':'{S_G}="START"',
                                'column_id':'S_G',
                            },
                            'backgroundColor':'#39CCCC',
                        },
                        {
                            'if':{
                                'filter_query':'{S_G}="GOAL"',
                                'column_id':'Target',
                            },
                            'backgroundColor':'#FF4136',
                        },
                        {
                            'if':{
                                'filter_query':'{S_G}="GOAL"',
                                'column_id':'S_G',
                            },
                            'backgroundColor':'#FF4136',
                        },
                    ],
            )
        ], style={'display':'inline-block', 'width':'40%'}),
# 上段右　処理結果の出力用ボタン
        html.Div(
            className="app-button-area",
            children=[
                html.Button('クリティカルパス', 
                    className="app-button", id='id_btn_done', n_clicks=0,
                ),
                html.Button('データの保存', 
                    className="app-button", id='id_btn_save', n_clicks=0,
                ),
                html.Button('データの読込', 
                    className="app-button", id='id_btn_load', n_clicks=0,
                ),
        ],style={'display':'inline-block', 'width':'18%', 'float':'right'}),
    ]),
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
                stylesheet=[
                    {
                        'selector': 'node',
                        'style': {
                            'label': 'data(label)'
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'curve-style': 'bezier',
                            'width':6,
                            'target-arrow-shape': 'triangle',                            
                            'label': 'data(weight)'
                        }
                    },
                    {
                        'selector': '.START',
                        'style': {
                            'background-color': '#39CCCC'
                        }
                    },
                    {
                        'selector': '.GOAL',
                        'style': {
                            'background-color': '#FF4136'
                        }
                    },
                    ]
            )
        ], style={'display':'inline-block', 'width':'48%'},
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
                stylesheet=[
                    {
                        'selector': 'node',
                        'style': {
                            'label': 'data(label)'
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'curve-style': 'bezier',
                            'width':6,
                            'target-arrow-shape': 'triangle',                            
                            'label': 'data(weight)'
                        }
                    },
                    {
                        'selector': '.START',
                        'style': {
                            'background-color': '#39CCCC'
                        }
                    },
                    {
                        'selector': '.GOAL',
                        'style': {
                            'background-color': '#FF4136'
                        }
                    },
                    {
                        'selector': '.CP_node',
                        'style': {
                            'background-color': 'black'
                        }
                    },
                    {
                        'selector': '.CP_edge',
                        'style': {
                            'curve-style': 'bezier',
                            'width': 8,
                            'target-arrow-color': 'red',
                            'target-arrow-shape': 'triangle',                            
                            'line-color': '#FF4136'
                        }
                    }
                    ]
            )
        ], style={'display':'inline-block', 'width': "48%"},
        ),
    ]),
    dcc.ConfirmDialog(
        id='confirm_save',
        message='データを保存しました。',
    ),
    dcc.ConfirmDialog(
        id='confirm_load',
        message='データをロードしました。',
    ),
])

@app.callback(
    Output('id_problem', 'elements'),
    [Input('id_table', 'data')]
)
def update_problem(data):
    columns = ['Source', 'Target', 'Weight', 'S_G']
    df = pd.DataFrame(index=[], columns=columns, dtype=object)
    for d in data:
        row = [d['Source'], d['Target'], d['Weight'], d['S_G']]
        sr = pd.Series(row, index=df.columns)
        df = df.append(sr, ignore_index=True)

    sr_S = df['Source'].dropna()
    sr_T = df['Target'].dropna()
    sr_ST = pd.concat([sr_S, sr_T])

    df_STW = df.dropna(subset = ['Source', 'Target']) #, 'Weight'])

    elements = []
    for node in sr_ST.unique():
        dic_node = {'data': {'id': None, 'label': None}, 
#                    'position': {'x': None, 'y': None},
                    'classes': 'OTHER_node',
                    'selectable': False,
                    'grabbable': False,
                    }
        dic_node['data']['id'] = node
        dic_node['data']['label'] = node

        try:
            if df_STW['Source'][df_STW['S_G']=='START'].values[0] == node:
                dic_node['classes'] = 'START'
            elif df_STW['Target'][df_STW['S_G']=='GOAL'].values[0] == node:
                dic_node['classes'] = 'GOAL'
            else:
                dic_node['classes'] = 'OTHER_node'
        except:
            dic_node['classes'] = 'OTHER_node'
            pass

        elements.append(dic_node)    
    
    for edge in df_STW.iterrows():
        dic_edge = {'data': {'source': None, 'target': None, 'weight': None},
                    'classes': 'OTHER_edge',
                    }
        dic_edge['data']['source'] = edge[1][0]
        dic_edge['data']['target'] = edge[1][1]
        if edge[1][2]:
            dic_edge['data']['weight'] = edge[1][2]
        else:
            dic_edge['data']['weight'] = ""
        elements.append(dic_edge)

    return elements


# 処理結果出力用のボタンが押された時のコールバック
@app.callback(
    Output('id_answer', 'elements'),
    [Input('id_btn_done', 'n_clicks')],
    [State('id_table', 'data')]
)
def update_answer(n_clicks, data):
    # プログラム起動時のコールバック（ボタンを押さなくても作動する）
    if not data:
        return [] 

    # 入力データの前処理
    columns = ['Source', 'Target', 'Weight', 'S_G']
    df = pd.DataFrame(index=[], columns=columns, dtype=object)
    for d in data:
        d_weight = d['Weight']
        if type(d_weight) != int:
            try:
                d_weight = int(d['Weight'])
            except:
                d_weight = 0

        row = [d['Source'], d['Target'], d_weight, d['S_G']]
        sr = pd.Series(row, index=df.columns)
        df = df.append(sr, ignore_index=True)

    sr_S = df['Source'].dropna()
    sr_T = df['Target'].dropna()
    sr_ST = pd.concat([sr_S, sr_T])

    df_STW = df.dropna(subset = ['Source', 'Target', 'Weight'])

    try:
        start = df_STW['Source'][df_STW['S_G']=='START'].values[0]
        goal = df_STW['Target'][df_STW['S_G']=='GOAL'].values[0]
    except:
        return []


    # クリティカルパスを求める
    DG = nx.DiGraph()

    for ne in df_STW.iterrows():
        DG.add_edge(ne[1]['Source'], ne[1]['Target'], weight=ne[1]['Weight'])

    df_pair = pd.DataFrame(index=[], columns=['s', 't'], dtype=object)

    for path in nx.shortest_simple_paths(DG, start, goal, weight='weight'):
        p_edge = [s + t for s,t in zip(path[:-1],path[1:])]
        for s,t in zip(p_edge[:-1],p_edge[1:]):
            row = [s,t]
            sr = pd.Series(row, index=df_pair.columns)
            df_pair = df_pair.append(sr, ignore_index=True)

    sr_pair = pd.concat([df_pair.s, df_pair.t])

    p = Node('project')

    for con in sr_pair.drop_duplicates():
        d = df_STW[(df_STW['Source']==con[0]) & (df_STW['Target']==con[1])]['Weight'].values[0]
        p.add(Node(con, duration=d))

    for d in df_pair.drop_duplicates().iterrows():
        p.link(p.get_or_create_node(d[1]['s']), p.get_or_create_node(d[1]['t']))

    p.update_all()
    cp_sg = p.get_critical_path()
    cp_day= p.duration

    cp_node = [str(e)[0] for e in cp_sg][1:] # start goal を除く
    cp_edge = [[s,g] for s,g in zip(cp_sg[:-1],cp_sg[1:])]
    cp_edge = [[str(node)[0],str(node)[1]] for node in cp_sg]


    # 出力 elements の編集
    elements = []
    for node in sr_ST.unique():
        dic_node = {'data': {'id': None, 'label': None}, 
                    'classes': 'OTHER_node',
                    'selectable': False,
                    'grabbable': False,
                    }
        dic_node['data']['id'] = node
        dic_node['data']['label'] = node

        try:
            if df_STW['Source'][df_STW['S_G']=='START'].values[0] == node:
                dic_node['classes'] = 'START'
            elif df_STW['Target'][df_STW['S_G']=='GOAL'].values[0] == node:
                dic_node['classes'] = 'GOAL'
            else:
                dic_node['classes'] = 'OTHER_node'
        except:
            dic_node['classes'] = 'OTHER_node'
            pass

        # クリティカルパスが通過するノードにクラス名を設定
        if node in cp_node:
            dic_node['classes'] = 'CP_node'
        if node == goal:
            dic_node['data']['label'] = "{} ( {} )".format(node, cp_day)

        elements.append(dic_node)    
    
    for edge in df_STW.iterrows():
        dic_edge = {'data': {'source': None, 'target': None, 'weight': None},
                    'classes': 'OTHER_edge',
                    }
        dic_edge['data']['source'] = edge[1][0]
        dic_edge['data']['target'] = edge[1][1]
        dic_edge['data']['weight'] = edge[1][2]
        elements.append(dic_edge)

        # クリティカルパスのエッジにクラス名を設定
        for s,t in cp_edge:
            if dic_edge['data']['source'] == s and dic_edge['data']['target'] == t:
                dic_edge['classes'] = 'CP_edge'

    return elements

@app.callback(Output('confirm_save', 'displayed'),
              [Input('id_btn_save', 'n_clicks')])
def save_data(value):
    if value:
        return True
    return False

@app.callback(Output('confirm_load', 'displayed'),
              [Input('id_btn_load', 'n_clicks')])
def load_data(value):
    if value:
        return True
    return False


# if __name__ == "__main__":
#     app.run_server(host='localhost', debug=True)
#    app.run_server(debug=True)
