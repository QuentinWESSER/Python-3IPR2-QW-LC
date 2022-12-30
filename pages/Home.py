import dash
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div(className="HomePage",children=[
    dcc.Store("key-data"),
    html.Img(className="img", src='assets/img/home-background.png'),
    
    html.Div(className="Home", children=[
        html.H1("Home"),
    ]),
    html.Div(className="presentation", children=[
        html.H3("Bienvenue sur notre site !"),
        html.H3("Celui-ci est séparé en 2 parties : "),
        html.H3("Avec le bouton <ID Tournament> vous pourrez accéder au données d'un tournoi via son ID"),
        html.H3("Avec le bouton <Get Tournaments> vous pourrez trouver le tournoi que vous voulez"),
        html.H3("dans la liste des tournois du site STARTGG."),
        html.H3("Le troisième bouton tout en bas vous permet d'update la liste des jeux."),
    ]),
    html.Div(className="link-btn", children=[
        html.Div(className="page-btn", children=[
                html.Img(className="img", src='assets/img/Loupe.png'),
                html.A(html.Button("Get Tournaments"), href="gettournaments")
            ]),
        html.Div(className="page-btn", children=[
            html.Img(className="img", src='assets/img/Loupe.png'),
            html.A(html.Button("ID Tournament"), href="tournament")
            ]),
    ]),
    html.Div(className="bottom-bar", children=[]),
    html.Div(className="btn3", children=[html.A(html.Button("reload data"))]),
])