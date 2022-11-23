import dash
from dash import html, dcc, callback, Output, Input, State
import APIFunction as API

dash.register_page(__name__)

layout = html.Div(children=[
    dcc.Store("key-data"),

    html.Div(className="sidebar", children=[
        html.H1("Tournaments"),
        html.Div(className="searchbar", children=[
            html.Div(className="searchbar-left", children=[
                dcc.Input(placeholder="Name of the city", type='text', id="enter-city", className="Input")
            ]),
            html.Div(className="searchbar-right", children=[
                dcc.Dropdown(id="city")
            ]),
        ]),
        html.Div(className="Range", children=[
            dcc.Input(placeholder="Range", type='number', id="range", className="Input"),
            html.H3("Km")
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
)
def LoadCity(city_name):
    if(city_name != None or city_name == ""):
        response = API.returnCityNames(city_name, 10)
        CityName = []
        for City in response:
            CityName.append(str(City[0]) + ', ' + str(City[2]))
        return CityName
    return ['No Result']
