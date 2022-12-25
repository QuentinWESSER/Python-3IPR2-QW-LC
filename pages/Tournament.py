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
        html.Div(className="rightBar", children=[
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
                    html.H3("Ratio", id="adressTournament")
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
