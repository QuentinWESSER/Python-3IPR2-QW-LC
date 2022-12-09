import dash
from dash import html, dcc, callback, Output, Input, State
import APIFunction as API
import datetime 
import time
import plotly.express as px
import pandas as pd

layout = html.Div(children=[
    dcc.Store("key-data"),

    html.Div(className="IDbar", children=[
        html.H1("ID Tournaments"),
        dcc.Input(placeholder="Tournament's ID", type='number', id="enter-ID", className="Input")
    ]),

    html.Div(className="principalBar", children=[
        html.Div(className="rightBar", children=[
            dcc.Loading(children=[
                html.H1("Missing information", id='status'),
                dcc.Graph(id='histogramme'),
            ])
        ]),

        html.Div(className="leftBar", children=[
            dcc.Loading(children=[
                html.Div(className="NameGameInfo", children=[
                    html.H1("GAME : ", id='status'),
                    html.H3("Ratio")
                ]),
                html.Div(className="VilleInfo", children=[
                    html.H1("VILLE : ", id='status'),
                    html.H3("Ratio")
                ]),
                html.Div(className="AdresseInfo", children=[
                    html.H1("ADRESSE : ", id='status'),
                    html.H3("Ratio")
                ]),
                html.Div(className="AttendeesInfo", children=[
                    html.H1("NOMBRE DE JOUEUR ATTENDU : ", id='status'),
                    html.H3("Ratio")
                ]),
                html.Div(className="Start&EndInfo", children=[
                    html.H1("START : ", id='status'),
                    html.H3("Ratio"),
                    html.H2("START : ", id='status'),
                    html.H3("Ratio")
                ]),
                html.Div(className="urlInfo", children=[
                    html.H1("URL : ", id='status'),
                    html.H3("Ratio")
                ]),
            ])
        ]),
    ]),
])
