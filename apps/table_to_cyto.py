import dash_table
import dash_cytoscape as cyto

import pandas as pd
from collections import OrderedDict
import networkx as nx


def get_elements(data):
    if not data:
        return [] 

    columns = ['Source', 'Target', 'Weight', 'S_G']
    df = pd.DataFrame(index=[], columns=columns, dtype=object)
    for d in data:
        row = [d['Source'], d['Target'], d['Weight'], d['S_G']]
        sr = pd.Series(row, index=df.columns)
        df = df.append(sr, ignore_index=True)

    sr_S = df['Source'].dropna()
    sr_T = df['Target'].dropna()
    sr_ST = pd.concat([sr_S, sr_T])

    df_STW = df.dropna(subset = ['Source', 'Target'])

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


def get_shortest_path(data):
    if not data:
        return []

    start = ""
    goal = "" 

    G = nx.DiGraph()

    for d in data:
        if d['Source']==None or d['Target']==None:
            continue

        try:
            d_weight = int(d['Weight'])
        except:
            d_weight = 0

        G.add_weighted_edges_from([(d['Source'], d['Target'], d_weight)])

        if d['S_G'] == 'START':
            start = d['Source']
        elif d['S_G'] == 'GOAL':
            goal = d['Target']

    if start=="" or goal=="":
        return []

    shortest_path = nx.dijkstra_path(G, start, goal)
    path_length = nx.dijkstra_path_length(G, start, goal)
    shortest_edges = [[s,t] for s,t in zip(shortest_path[:-1], shortest_path[1:])]

    # 出力 elements の編集
    elements = []

    for node in G.nodes():
        dic_node = {'data': {'id': None, 'label': None}, 
                    'classes': 'OTHER_node',
                    'selectable': False,
                    'grabbable': False,
                    }

        dic_node['data']['id'] = node
        dic_node['data']['label'] = node
        
        if node in shortest_path:
            if node==start:
                dic_node['classes'] = 'START'
            elif node==goal:
                dic_node['classes'] = 'GOAL'
                dic_node['data']['label'] = "{} ( {} )".format(node, path_length)
            else:
                dic_node['classes'] = 'SP_node'

        elements.append(dic_node)             
                
    for source,target,weight in G.edges(data=True):
        dic_edge = {'data': {'source': None, 'target': None, 'weight': None},
                    'classes': 'OTHER_edge',
                    }

        dic_edge['data']['source'] = source
        dic_edge['data']['target'] = target
        dic_edge['data']['weight'] = weight['weight']
        
        if [source, target] in shortest_edges:
            dic_edge['classes'] = 'SP_edge'
        
        elements.append(dic_edge)

    return elements
