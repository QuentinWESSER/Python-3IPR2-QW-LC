import dash
from dash import html, dcc, callback, Output, Input, State
import APIFunction as API

dash.register_page(__name__)

layout = html.Div(children=[
    dcc.Store("key-data"),

    html.Div(className="sidebar", children=[
        html.H1("ratio"),
        html.Div(className="searchbar", children=[
            html.Div(className="searchbar-left", children=[
                dcc.Input(placeholder="Name of the city", type='text', id="enter-city", className="Input")
            ]),
            html.Div(className="searchbar-right", children=[
                dcc.Dropdown(id="city")
            ]),
        ])
    ]),

    html.Div(className="rightbar", children=[
        html.H1("this is main"),
        html.Div(id='key')
    ]),
    html.Button("ratio", id="btn")

])

@callback(
  Output("city", "options"),
  Input("enter-city", "value"),
  State("key-data", "data"),
  
)
def LoadCity(city_name, key):
    if(city_name != None):
        return[city_name]
    return ['No Result']
