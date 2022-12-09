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

    html.Div(className="rightbar", children=[
        dcc.Loading(children=[
            html.H1("Missing information", id='status'),
            dcc.Graph(id='histogramme'),
        ])
    ]),

    html.Div(className="leftbar", children=[
        dcc.Loading(children=[
            html.Div(className="NameGameInfo", children=[
                html.H1("GAME : "),
                html.H3("Ratio", id="gamename")
            ]),
            html.Div(className="AdresseInfo", children=[
                html.H1("ADRESSE : "),
                html.H3("Ratio", id="adress")
            ]),
            html.Div(className="AttendeesInfo", children=[
                html.H1("NOMBRE DE JOUEUR ATTENDU : "),
                html.H3("Ratio", id="attendees")
            ]),
            html.Div(className="Start&EndInfo", children=[
                html.H1("START : "),
                html.H3("Ratio", id="startAt"),
                html.H2("START : "),
                html.H3("Ratio", id="endAt")
            ]),
            html.Div(className="urlInfo", children=[
                html.H1("URL : "),
                html.H3("Ratio", id='url')
            ]),
        ])
    ]),
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
