import dash
from dash import html, dcc, callback, Output, Input, State
import APIFunction as API
import datetime 
import time
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

layout = html.Div(children=[
    dcc.Store("key-data"),

    html.Div(className="IDbar", children=[
        html.H1("ID Tournaments"),
        dcc.Input(placeholder="Tournament's ID", type='number', id="enter-ID", className="Input")
    ]),

    html.Div(className="principalBar", children=[

        html.Div(className="leftbar", children=[
            dcc.Loading(children=[
                html.Div(className="NameGameInfo", children=[
                    html.Div(className="row1", children=[html.H2("GAME : ")]),
                    html.Div(className="row2", children=[html.H3("Ratio", id="gamename")]),
                ]),
                html.Div(className="AdresseInfo", children=[
                    html.Div(className="row3", children=[html.H2("ADRESSE : ")]),
                    html.Div(className="row4", children=[html.H3("Ratio", id="adress")]),
                ]),
                html.Div(className="AttendeesInfo", children=[
                    html.Div(className="row5", children=[html.H2("NOMBRE DE JOUEUR ATTENDU : ")]),
                    html.Div(className="row6", children=[html.H3("Ratio", id="attendees")]),
                ]),
                html.Div(className="StartInfo", children=[
                    html.Div(className="row7", children=[html.H2("START : ")]),
                    html.Div(className="row8", children=[html.H3("Ratio", id="startAt")]),
                ]),
                html.Div(className="EndInfo", children=[
                    html.Div(className="row9", children=[html.H2("END : ")]),
                    html.Div(className="row10", children=[html.H3("Ratio", id="endAt")]),
                ]),
                html.Div(className="urlInfo", children=[
                    html.Div(className="row11", children=[html.H2("URL : ")]),
                    html.Div(className="row12", children=[html.H3("Ratio", id='url')]),
                ]),     
            ])
        ]),

        html.Div(className="rightBar", children=[
            dcc.Loading(children=[
                html.H1("Missing information", id='status'),
                dcc.Graph(id='histogramme'),
            ])
        ]),
    ])
])

@callback(
    Output('gamename', 'children'),
    Input('enter-ID', 'value'),
    State("key-data", "data")
)

def LoadTournament(id, key):
    if(id is None or key is None):
        return ''
    
    data = API.returnTournament(key[0], id)
    if isinstance(data, str):
        return 'Unable to retrieve data'
    
    return data['name']
