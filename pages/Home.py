import dash
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div(className="HomePage", children=[
    dcc.Store("key-data"),
    
    html.Div(className="Home", children=[
        html.H1("Home Page"),
    ]),
    html.Div(className="pageInfo", children=[
        html.H3("Welcome to our website !"),
        html.H3("This one is separated into 2 parts : "),
        html.H3("With the <Get Tournaments> button, you will find the tournament you want in the list of tournament on the STARTGG website."),
        html.H3("With the <ID Tournament> button, you will access tournament's data with its ID."),
        html.H3("The third button let you reload the list of games."),
    ]),
    html.Div(className="link-btn", children=[
        html.Div(className="page-btn", children=[
                html.Img(className="img", src='assets/img/Loupe.png'),
                html.Div(className="btn", children=[html.A(html.Button("Get Tournaments"), href="gettournaments")])
            ]),
        html.Div(className="page-btn", children=[
            html.Img(className="img", src='assets/img/Information.png'),
            html.Div(className="btn", children=[html.A(html.Button("ID Tournament"), href="tournament")])
            ]),
    ]),
    html.Div(className="bottom-bar", children=[
        html.Div(className="load-btn", children=[html.A(html.Button("reload data"))]),
        html.H2("This could take some time.")
    ])
])