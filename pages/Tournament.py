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
    ]),

    html.Div(className="principalBar", children=[
        html.Div(className="IDInput", children=[
            dcc.Input(placeholder="Tournament's ID", type='number', id="enter-ID", className="Input")
        ]),

        html.Div(className="middlebar", children=[
            dcc.Loading(children=[
                html.Div(className="Info", children=[
                    html.Div(className="inline-row-label", children=[html.H2("Name : ")]),
                    html.Div(className="inline-row", children=[html.H2("Placeholder", id="gamename")]),
                ]),
                html.Div(className="Info", children=[
                    html.Div(className="inline-row-label", children=[html.H2("Adress : ")]),
                    html.Div(className="inline-row", children=[html.H2("Placeholder", id="adressTournament")]),
                ]),
                html.Div(className="Info", children=[
                    html.Div(className="inline-row-label", children=[html.H2("Number of attendees : ")]),
                    html.Div(className="inline-row", children=[html.H2("Placeholder", id="attendees")]),
                ]),
                html.Div(className="Info", children=[
                    html.Div(className="inline-row-label", children=[html.H2("Start : ")]),
                    html.Div(className="inline-row", children=[html.H2("Placeholder", id="startAt")]),
                ]),
                html.Div(className="Info", children=[
                    html.Div(className="inline-row-label", children=[html.H2("End : ")]),
                    html.Div(className="inline-row", children=[html.H2("Placeholder", id="endAt")]),
                ]),
                html.Div(className="Info", children=[
                    html.Div(className="inline-row-label", children=[html.H2("URL : ")]),
                    html.Div(className="inline-row", children=[html.H2("Placeholder", id='url')]),
                ]),     
            ])
        ]),

        html.Div(className="endbar", children=[
            dcc.Loading(children=[
                html.Div(className="title", children=[html.H1("Histogram of placement as fuction of the Winrate of the last 50 games :", id='status')]),
                dcc.Graph(id='histogramme'),
            ])
        ]),
    ])
])

@callback(
    Output('gamename', 'children'),
    Output('adressTournament', 'children'),
    Output('attendees', 'children'),
    Output('startAt', 'children'),
    Output('endAt', 'children'),
    Output('url', 'children'),
    Output('histogramme', 'figure'),
    Input('enter-ID', 'value'),
    State("key-data", "data")
)

def LoadTournament(id, key):
    """
    Permet de retourner une liste d'informations sur un tournoi en fonction de son ID

    Args :
        ID : ID d'un tournoi
        key : Clé permetant d'acceder à l'API

    Returns :
        Retourne une liste d'informations sur ce tournoi
    """
    if(id is None or key is None):
        return 'Unable to retrieve data', 'Unable to retrieve data', 'Unable to retrieve data' , 'Unable to retrieve data', 'Unable to retrieve data', 'Unable to retrieve data', px.line({})
    
    data = API.returnTournament(key[0], id)
    if isinstance(data, str):
        return 'Unable to retrieve data', 'Unable to retrieve data', 'Unable to retrieve data' , 'Unable to retrieve data', 'Unable to retrieve data', 'Unable to retrieve data', px.line({})
    
    linedata = data['data']
    df = pd.DataFrame(linedata, columns=['WR','P'])
    df = df.sort_values(by="WR")
    fig = px.line(df, x='WR', y='P')
    fig.update_layout(
        yaxis = dict(autorange="reversed")
    )
    return data['name'], data['city'] + " " + data['venueAddress'], data['numAttendees'], data['startAt'], data['endAt'], data['url'], fig 
