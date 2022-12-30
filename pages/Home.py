import dash
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div(children=[
    dcc.Store("key-data"),

    html.Div(className="Home", children=[
        html.H1("Home"),
    ]),
    html.Div(className="link-btn", children=[
        html.Div(className="btn1", children=[html.A(html.Button("Get Tournaments"), href="gettournaments")]),
        html.Div(className="btn2", children=[html.A(html.Button("ID Tournament"), href="tournament")]),
    ]),
    html.Div(className="btn3", children=[html.A(html.Button("reload data"), href="/")]),
])