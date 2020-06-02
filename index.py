import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app0, app1, app2, app3, app4


app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-0', children=[
        dcc.Tab(label='インタラクティブ・ダッシュボード', value='tab-0'),
        dcc.Tab(label='最短経路問題を解いてみよう', value='tab-1'),
        dcc.Tab(label='コールバックの実験【Graph】', value='tab-2'),
        dcc.Tab(label='コールバックの実験【Cytoscape】', value='tab-3'),
        dcc.Tab(label='コールバックの実験【連携編】', value='tab-4'),
    ], colors={
        "border": "white",
        "primary": "red",
        "background": "lightgray"
    }),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-0':
        return app0.layout
    elif tab == 'tab-1':
        return app1.layout
    elif tab == 'tab-2':
        return app2.layout
    elif tab == 'tab-3':
        return app3.layout
    elif tab == 'tab-4':
        return app4.layout
    else:
        return '404 File not found'

if __name__ == '__main__':
    app.run_server(host='localhost', debug=True)
