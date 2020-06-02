#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 元ネタ
# https://traffic-accidents-uk.herokuapp.com
# https://github.com/richard-muir/uk-car-accidents

# import os

import dash
# import flask

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from pandas import read_csv, DataFrame, pivot_table

from app import app

### GLOBALS, DATA & INTIALISE THE APP ###

# Mapbox key to display the map
MAPBOX = 'pk.eyJ1Ijoicm11aXIiLCJhIjoiY2o1MjBxcnkwMDdnZTJ3bHl5bXdxNW9uaCJ9.QR6f0fRLkHzmCgL70u5Hzw'

# Make the colours consistent for each type of accident
SEVERITY = {'軽傷' : 'lightblue',
            '重傷' : 'orange',
            '死亡' : 'red'
            }
# Need to downsample the number of Slight and Serious accidents to display them
# on the map. These fractions reduce the number plotted to about 10k.
# There are only about 10k fatal accidents so don't need to downsample these
SLIGHT_FRAC = 0.1
SERIOUS_FRAC = 0.5

# This dict allows me to sort the weekdays in the right order
DAYSORT = dict(zip(['日', '土', '金', '木', '水', '火', '月'],[0, 1, 2, 3, 4, 5, 6]))
DAYSORT_R = dict(zip(['日', '土', '金', '木', '水', '火', '月'],[6, 5, 4, 3, 2, 1, 0]))

# Set the global font family
FONT_FAMILY =  "YuGothic"

# Read in data from csv stored on github
csvLoc = 'apps/h29.csv'
acc = read_csv(csvLoc)

AGE = ['1～21', '22～29', '30～39', '40～49', '50～59', '60～69', '70～74',
       '75～', '不明']

# # Set up the Dash instance. Big thanks to @jimmybow for the boilerplate code
# server = flask.Flask(__name__)
# server.secret_key = os.environ.get('secret_key', 'secret')

# app = dash.Dash(__name__, server = server)

## SETTING UP THE APP LAYOUT ##
# # Main layout container
# app.layout = html.Div(

layout = html.Div(
style={'color': 'black', 'background-color': 'white'},
children=[
    html.H1(
        '福岡県の交通事故',
        style={
            'paddingLeft' : 50,
            'fontFamily' : FONT_FAMILY
            }
        ),
    html.Div([   # Holds the widgets & Descriptions

        html.Div([

            html.H3(
                '''2017年福岡では {:,} 件の交通事故が発生、多くの方が死傷されました。'''.format(len(acc)),
                style={
                    'fontFamily' : FONT_FAMILY
                }
                ),
            html.H3(
                '''どんな状況で交通事故が起きたか、条件を変えながら探求してみよう。''',
                style={
                    'fontFamily' : FONT_FAMILY
                }
                ),
            html.Div(
                '''◆ 事故の種類を選んで下さい。''',
                style={
                    'paddingTop' : 20,
                    'paddingBottom' : 10,
                    'fontFamily' : FONT_FAMILY,
                }
            ),
            dcc.Checklist( # Checklist for the three different severity values
                options=[
                    {'label': sev, 'value': sev} for sev in SEVERITY
                ],
                value=[sev for sev in SEVERITY],
                labelStyle={
                    'display': 'inline-block',
                    'paddingRight' : 10,
                    'paddingLeft' : 10,
                    'paddingBottom' : 5,
                    'fontFamily' : FONT_FAMILY,
                    },
                id="severityChecklist"

            ),
            html.Div(
                '''◆ 事故が起きた曜日を選んで下さい。''',
                style={
                    'paddingTop' : 20,
                    'paddingBottom' : 10,
                    'fontFamily' : FONT_FAMILY,
                }
            ),
            dcc.Checklist( # Checklist for the dats of week, sorted using the sorting dict created earlier
                options=[
                    {'label': day[:3], 'value': day} for day in sorted(acc['発生曜日'].unique(), key=lambda k: DAYSORT_R[k])
                ],
                value=[day for day in acc['発生曜日'].unique()],
                labelStyle={  # Different padding for the checklist elements
                    'display': 'inline-block',
                    'paddingRight' : 10,
                    'paddingLeft' : 10,
                    'paddingBottom' : 5,
                    'fontFamily' : FONT_FAMILY,
                    },
                id="dayChecklist",
            ),
            html.Div(
                '''◆ 事故が起きた時間帯を選んで下さい。(0時〜23時)''',
                style={
                    'paddingTop' : 20,
                    'paddingBottom' : 10,
                    'fontFamily' : FONT_FAMILY,
                }
            ),
            dcc.RangeSlider( # Slider to select the number of hours
                id="hourSlider",
                count=1,
                min=-acc['発生時'].min(),
                max=acc['発生時'].max(),
                step=1,
                value=[acc['発生時'].min(), acc['発生時'].max()],
                marks={str(h) : str(h) for h in range(acc['発生時'].min(), acc['発生時'].max() + 1)}
            ),
            html.Div(
                '''◆ 死傷者の年齢層を選んで下さい。''',
                style={
                    'paddingTop' : 50,
                    'paddingBottom' : 10,
                    'fontFamily' : FONT_FAMILY,
                }
            ),
            dcc.Checklist( # Checklist for the dats of week, sorted using the sorting dict created earlier
                options=[
                    {'label': age, 'value': age} for age in AGE
                ],
                value=AGE,
                labelStyle={  # Different padding for the checklist elements
                    'display': 'inline-block',
                    'paddingRight' : 10,
                    'paddingLeft' : 10,
                    'paddingBottom' : 5,
                    'fontFamily' : FONT_FAMILY,
                    },
                id="ageChecklist",
            )

        ],
        style={
            "width" : '60%',
            'display' : 'inline-block',
            'paddingLeft' : 50,
            'paddingRight' : 50,
            'boxSizing' : 'border-box',            }
        ),

        html.Div([  # Holds the map & the widgets

            dcc.Graph(id="map") # Holds the map in a div to apply styling to it

        ],
        style={
            "width" : '40%',
            'float' : 'right',
            'display' : 'inline-block',
            'paddingRight' : 50,
            'paddingLeft' : 10,
            'boxSizing' : 'border-box',
            'fontFamily' : FONT_FAMILY
            })

    ],
    style={'paddingBottom' : 20}),

    html.Div([  # Holds the heatmap & barchart (60:40 split)
        html.Div([  # Holds the heatmap
            dcc.Graph(
                id="heatmap",
            ),
        ],
        style={
            "width" : '60%',
            'float' : 'left',
            'display' : 'inline-block',
            'paddingRight' :25,
            'paddingLeft' : 50,
            'boxSizing' : 'border-box'
            }
        ),
        html.Div([  # Holds the barchart
            dcc.Graph(
                id="bar",
            )
            #style={'height' : '50%'})
        ],
        style={
            "width" : '40%',
            'float' : 'right',
            'display' : 'inline-block',
            'paddingRight' : 50,
            'paddingLeft' : 5,
            'boxSizing' : 'border-box'
            })

    ]),
    html.Div([
        # Add a source annotation and a note for the downsampling
        html.Div(
            'https://ckan.open-governmentdata.org/dataset/401000_koutsuujiko2017',
            style={
                'fontFamily' : FONT_FAMILY,
                'fontSize' : 8,
                'fontStyle' : 'italic'
            }),
        html.Div(
            '出典: 福岡県 平成29年 交通事故（福岡県警察本部交通部交通企画課）',
            style={
                'fontFamily' : FONT_FAMILY,
                'fontSize' : 8,
                'fontStyle' : 'italic'
            }
        )])
])

## APP INTERACTIVITY THROUGH CALLBACK FUNCTIONS TO UPDATE THE CHARTS ##

# Callback function passes the current value of all three filters into the update functions.

# Feeds the filter outputs into the mapbox
@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='severityChecklist', component_property='value'),
    Input(component_id='dayChecklist', component_property='value'),
    Input(component_id='hourSlider', component_property='value'),
    Input(component_id='ageChecklist', component_property='value'),
    ]
)
def updateMapBox(severity, weekdays, time, age):
    # List of hours again
    hours = [i for i in range(time[0], time[1]+1)]
    # Filter the dataframe
    acc1 = DataFrame(acc[
            ['発生曜日', '発生時', '甲_年齢','死亡','重傷','軽傷','緯度','経度','市区町村']]
            [
            (acc['発生曜日'].isin(weekdays)) &
            (acc['発生時'].isin(hours)) &
            (acc['甲_年齢'].isin(age))
            ])
    def set_frac(sev):
        len_sev = len(acc1[sev])
        if len_sev < 5000:
            return 1.0
        else:
            return 5000/len_sev

    # Once trace for each severity value
    severities = sorted(severity, key=lambda k: SEVERITY[k])
    traces = []
    for sev in severities:
        acc_temp = acc1[acc1[sev]>0]
        acc_map = acc_temp.sample(frac=set_frac(sev))

        # Scattermapbox trace for each severity
        traces.append({
            'type' : 'scattermapbox',
            'mode' : 'markers',
            'lat' : acc_map.loc[:,'緯度'],
            'lon' : acc_map.loc[:,'経度'],
            'marker' : {
                'color' : SEVERITY[sev], # Keep the colour consistent
                'size' : 5,
            },
            'hoverinfo' : 'text',
            'name' : sev,
            'legendgroup' : sev,
            'showlegend' : False,
            'text' : acc_map['市区町村'] # Text will show location
        })

        # Append a separate marker trace to show bigger markers for the legend.
        #  The ones we're plotting on the map are too small to be of use in the legend.
        traces.append({
            'type' : 'scattermapbox',
            'mode' : 'markers',
            'lat' : [0],
            'lon' : [0],
            'marker' : {
                'color' : SEVERITY[sev],
                'size' : 10,
            },
            'name' : sev,
            'legendgroup' : sev,

        })
    layout = {
        'height' : 460,
        'paper_bgcolor' : 'lightgray',
              'font' : {
                  'color' : 'black'
              }, # Set this to match the colour of the sea in the mapbox colourscheme
        'autosize' : True,
        'hovermode' : 'closest',
        'mapbox' : {
            'accesstoken' : MAPBOX,
            'center' : {  # Set the geographic centre - trial and error
                'lat' :  33.48,
                'lon' : 130.50
            },
            'zoom' : 8.0,
            'style' : 'light',   # Dark theme will make the colours stand out
        },
        'margin' : {'t' : 0,
                   'b' : 0,
                   'l' : 0,
                   'r' : 0},
        'legend' : {
            'font' : {'color' : 'black'},
             'orientation' : 'h',
             'x' : 0,
             'y' : 1.01
        }
    }
    fig = dict(data=traces, layout=layout)
    return fig

# Pass in the values of the filters to the heatmap
@app.callback(
    Output(component_id='heatmap', component_property='figure'),
    [Input(component_id='severityChecklist', component_property='value'),
    Input(component_id='dayChecklist', component_property='value'),
    Input(component_id='hourSlider', component_property='value'),
    Input(component_id='ageChecklist', component_property='value'),
    ]
)
def updateHeatmap(severity, weekdays, time, age):
    # The rangeslider is selects inclusively, but a python list stops before the last number in a range
    hours = [i for i in range(time[0], time[1] + 1)]
    # Take a copy of the dataframe, filtering it and grouping
    acc2 = DataFrame(acc[
            ['発生曜日', '発生時','死亡','重傷','軽傷']]
            [(acc['甲_年齢'].isin(age))
            ])

    acc2_hmap = DataFrame(index=weekdays,columns=hours)
    for sev in severity:
        acc2_pivot = pivot_table(data=acc2, values=sev, index='発生曜日', columns='発生時', aggfunc='sum')
        try:
            acc2_sum = DataFrame(acc2_pivot.loc[weekdays,hours], index=weekdays, columns=hours)
        except:
            acc2_sum = DataFrame(index=weekdays, columns=hours)
        acc2_hmap = acc2_hmap.add(acc2_sum, fill_value=0).fillna(0)

    # Apply text after grouping
    def heatmapText(day, time, sr_hmap):
        FORMAT = '{}曜日  {:02d}時台<br>死傷者数: {:.0f}人'
        t_list = []
        for row in zip(range(time[0], time[1] + 1), sr_hmap):
                t_list.append(FORMAT.format(day,row[0],row[1]))
        return t_list

    # Pre-sort a list of days to feed into the heatmap
    days = sorted(weekdays, key=lambda k: DAYSORT[k])

    # Create the z-values and text in a nested list format to match the shape of the heatmap
    z = []
    text = []
    for d in days:
        row = acc2_hmap.loc[d]
        t = heatmapText(d, time, acc2_hmap.loc[d])
        z.append(row)
        text.append(t)

    # Plotly standard 'Electric' colourscale is great, but the maximum value is white, as is the
    #  colour for missing values. I set the maximum to the penultimate maximum value,
    #  then spread out the other. Plotly colourscales here: https://github.com/plotly/plotly.py/blob/master/plotly/colors.py

    Electric = [
        [0, 'rgb(0,0,0)'], [0.25, 'rgb(30,0,100)'],
        [0.55, 'rgb(120,0,100)'], [0.8, 'rgb(160,90,0)'],
        [1, 'rgb(230,200,0)']
        ]

    # Heatmap trace
    traces = [{
        'type' : 'heatmap',
        'x' : hours,
        'y' : days,
        'z' : z,
        'text' : text,
        'hoverinfo' : 'text',
        'colorscale' : Electric,
    }]

    fig = {'data' : traces,
          'layout' : {
              'paper_bgcolor' : 'white',
              'font' : {
                  'color' : 'black'
              },
              'height' : 300,
              'title' : '曜日・時間帯別の事故状況',
              'margin' : {
                  'b' : 25,
                  'l' : 30,
                  't' : 70,
                  'r' : 0,
              },
              'xaxis' : {
                  'ticktext' : hours, # for the tickvals and ticktext with one for each hour
                  'tickvals' : hours,
                  'tickmode' : 'array',
              }
          }}
    return fig

# This on updates the bar.
@app.callback(
    Output(component_id='bar', component_property='figure'),
    [Input(component_id='severityChecklist', component_property='value'),
    Input(component_id='dayChecklist', component_property='value'),
    Input(component_id='hourSlider', component_property='value'),
    Input(component_id='ageChecklist', component_property='value'),
    ]
)
def updateBarChart(severity, weekdays, time, age):
    # The rangeslider is selects inclusively, but a python list stops before the last number in a range
    hours = [i for i in range(time[0], time[1]+1)]

    # Create a copy of the dataframe by filtering according to the values passed in.
    # Important to create a copy rather than affect the global object.
    acc3 = DataFrame(acc[['甲_年齢','発生曜日', '発生時','死亡','重傷','軽傷']]
            [
            (acc['甲_年齢'].isin(age)) &
            (acc['発生曜日'].isin(weekdays)) &
            (acc['発生時'].isin(hours))
            ])

    # Pre-sort a list of days to feed into the heatmap
    severities = sorted(severity, key=lambda k: SEVERITY[k])

    # One trace for each accidents severity
    traces = []
    for sev in severities:
        acc3_bar =acc3[acc3[sev] > 0].groupby('甲_年齢').sum()
        traces.append({
            'type' : 'bar',
            'x' : acc3_bar.index.values.tolist(),
            'y' : acc3_bar[sev].values.tolist(),
            'marker' : {
                'color' : SEVERITY[sev],
            'line' : {'width' : 2,
                      'color' : '#333'}},
            'name' : sev
        })

    fig = {'data' : traces,
          'layout' : {
              'paper_bgcolor' : 'rgb(white)',
              'plot_bgcolor' : 'rgb(white)',
              'font' : {
                  'color' : 'black'
              },
              'height' : 300,
              'title' : '年齢層別の事故状況',
              'margin' : { # Set margins to allow maximum space for the chart
                  'b' : 25,
                  'l' : 30,
                  't' : 70,
                  'r' : 0
              },
              'legend' : { # Horizontal legens, positioned at the bottom to allow maximum space for the chart
                  'orientation' : 'h',
                  'x' : 0,
                  'y' : 1.01,
                  'yanchor' : 'bottom',
                  },
              'xaxis' : {
                  'tickvals' : sorted(acc3['甲_年齢'].unique()), # Force the tickvals & ticktext just in case
                  'ticktext' : sorted(acc3['甲_年齢'].unique()),
                  'tickmode' : 'array'
                  },
              'yaxis' : {
                  'type':'log'
              	  }
          }}

    # Returns the figure into the 'figure' component property, update the bar chart
    return fig


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
#    app.run_server(debug=False, threaded=True ,port=8050, host='192.168.11.37')
