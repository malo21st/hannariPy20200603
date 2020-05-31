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
]

stylesheet=[
    {
        'selector': 'node',
        'style': {
            'label': 'data(label)',
            'font-size': '30vh',
        }
    },
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'width':6,
            'target-arrow-shape': 'triangle',                            
            'label': 'data(weight)',
            'font-size': '30vh',
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
        'selector': '.SP_node',
        'style': {
            'background-color': 'black'
        }
    },
    {
        'selector': '.SP_edge',
        'style': {
            'curve-style': 'bezier',
            'width': 8,
            'target-arrow-color': 'red',
            'target-arrow-shape': 'triangle',                            
            'line-color': '#FF4136'
        }
    }
    ]

def get_style_data_conditional():
	return style_data_conditional

def get_stylesheet():
	return stylesheet
