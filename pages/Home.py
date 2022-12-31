import dash
from dash import html, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate   
import APIFunction as API

dash.register_page(__name__)

layout = html.Div(className="HomePage", children=[
    dcc.Store("key-data"),
    
    html.Div(className="Home", children=[
        html.H1("Home Page"),
    ]),
    html.Div(className="pageInfo", children=[
        html.H3("Welcome to our website !"),
        html.H3("This website is separated into 2 parts : "),
        html.H3("With the <Get Tournaments> button, you will find the tournament you want in the list of tournament on the StartGG website."),
        html.H3("With the <Info Tournament> button, you will access tournament's data with its ID."),
        html.H3("With the <Reload Data> button, you will be able to reload the game list of StartGG"),
    ]),
    html.Div(className="link-btn", children=[
        html.Div(className="page-btn", children=[
                html.Img(className="img", src='assets/img/Loupe.png'),
                html.Div(className="btn", children=[html.A(html.Button("Get Tournaments"), href="gettournaments")])
            ]),
        html.Div(className="page-btn", children=[
            html.Img(className="img", src='assets/img/Information.png'),
            html.Div(className="btn", children=[html.A(html.Button("Info Tournament"), href="tournament")])
            ]),
    ]),
    html.Div(className="bottom-bar", children=[
        html.Div(className="load-btn", children=[html.A(html.Button("Reload Data", id="load-btn"))]),
        dcc.Loading(children=[
            html.H2("This could take some time.", id='reloadstate')
        ])
    ])
])

@callback(
    Output('reloadstate', 'children'),
    Input('load-btn', 'n_clicks'),
    State("key-data", "data")
)
def ReloadGameList(n_clicks, key):
    """
    Permet de faire d'update la liste des jeux vidéos qui proviens de StartGG

    Args :
        n_clicks : nombre de click du boutton
        key : Clé permetant d'acceder à l'API

    Returns :
        Retourne le status de la fonction
    """
    if n_clicks is None:
        #Empeche l'appel au démarrage de la page
        raise PreventUpdate
    response = API.SaveVideoGameAsCSV(key[0], 30_000)
    if isinstance(response, str):
        return response
    return 'The list as been updated'