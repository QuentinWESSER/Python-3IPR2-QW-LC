import dash
from dash import html, dcc, callback, Output, Input, State
import APIFunction as API
import datetime 
import time
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

CitiesBuffer = []
GamesBuffer = []

layout = html.Div(children=[
    dcc.Store("key-data"),
    html.Div(className="topbar", children=[
        html.H1("Tournaments"),
    ]),
    html.Div(className="sidebar", children=[
        html.Div(className="block1", children=[
            html.H2("Select a location"),
            html.Div(className="searchbar", children=[
                html.Div(className="searchbar-left", children=[
                    dcc.Input(placeholder="Name of the city", type='text', id="enter-city", className="Input")
                ]),
                html.Div(className="searchbar-right", children=[
                    dcc.Dropdown(id="cities")
                ]),
            ]),
            html.Div(className="Range", children=[
                dcc.Input(placeholder="Range", type='number', id="range", className="Input"),
                html.H3("Km")
            ]),
        ]),
        html.Br(),
        html.Div(className="block2", children=[
            html.H2("Select a videogame"),
            html.Div(className="DropDown", children=[
                dcc.Input(placeholder="Name of the game", type='text', id="enter-game", className="Input"),
                html.Br(),
                html.Br(),
                html.Div(className="Select", children=[
                    dcc.Dropdown(id="games", multi=True)
                ]),
            ]),
            html.Br(),
        ]),
        html.Br(),
        html.Div(className="block3", children=[
            html.H2("Select a period of time"),
            html.Div(className="Picker", children=[
                dcc.DatePickerRange(id="date-picker")
            ]),
        ]),
    ]),

    html.Div(className="rightbar", children=[
        dcc.Dropdown(['Line Graph', 'Earth'], 'Line Graph', id='fig'),
        dcc.Loading(children=[
            html.H1("Missing information", id='status'),
            dcc.Graph(id='graph'),
            dcc.Graph(id='earth-graph'),
        ])
    ]),
])

@callback(
  Output("cities", "options"),
  Input("enter-city", "value"),
)
def LoadCity(city_name):
    if(city_name != None or city_name == ""):
        global CitiesBuffer
        CitiesBuffer = API.returnCityNames(city_name, 10)
        CityName = []
        for City in CitiesBuffer:
            CityName.append(str(City[0]) + ', ' + str(City[1]))
        return CityName
    return ['No Result']

@callback(
  Output("games", "options"),
  Input("enter-game", "value"),
  Input("games", "value")
)
def LoadGames(game_name, previous_game):
    if(game_name != None or game_name == ""):
        global GamesBuffer
        previous_game_list = []
        if previous_game is not None:
            for element in previous_game:
                for game in GamesBuffer:
                    if element == game[1]:
                        previous_game_list.append(game)
    
        GamesBuffer = API.returnVideoGames(game_name, 10)
        if previous_game_list is not None:
            GamesBuffer += previous_game_list
        
        GamesBuffer = [i for n, i in enumerate(GamesBuffer) if i not in GamesBuffer[:n]]
        GameName = []
        for game in GamesBuffer:
            GameName.append({
            "label": html.Div(
                [
                    html.Img(src=game[2], height=20),
                    html.Div(game[1], style={'font-size': 15, 'padding-left': 10}),
                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
            ),
            "value": game[1],
        })
        return GameName
    return ['No Result']

@callback(
    Output('status', 'children'),
    Output("graph","figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
    Input("games", "value"),
    Input("cities", "value"),
    Input("range", "value"),
    Input("fig", "value"),
    State("key-data", "data")
)
def LoadGraph(start_date, end_date, games, city, range, selected, key):
    if(start_date is None or end_date is None or games is None or city is None or range is None or key is None):
        return 'Missing informations', px.bar({})
    
    lattitude = ''
    longitude = ''
    for City in CitiesBuffer:
        if(city == str(City[0]) + ', ' + str(City[1])):
            lattitude = City[2]
            longitude = City[3]
    
    GameIdList = []
    for Game in GamesBuffer:
        for SelectGame in games:
            if SelectGame == Game[1]:
                GameIdList.append(int(Game[0]))

    
    endAt = time.mktime(datetime.date.fromisoformat(end_date).timetuple())
    startAt = time.mktime(datetime.date.fromisoformat(start_date).timetuple())
    endAt = round(endAt)
    startAt = round(startAt)
    data = API.fectTournamentList(key[0], GameIdList, lattitude, longitude, range, startAt, endAt, endAt - startAt < 5_000_000 )
    if isinstance(data, str):
        return data, px.bar({})
    for tournament in data:
        for Game in GamesBuffer:
            if tournament['GameID'] == int(Game[0]):
                tournament['Game'] = Game[1]
    
    if selected == 'Line Graph':
        #Line Chart
        df = pd.DataFrame(data, columns=['id', 'name', 'Date', 'Game'])
        Title = 'Number of tournaments per day'
        if endAt - startAt < 5_000_000:
            Title = 'Number of tournaments per week'
        return 'Tournaments', px.bar(df, x='Date', hover_data=['name'], color='Game', title=Title)
    else:
        #Map chart
        for tournament in data:
            coordinates = API.ReverseGeoCoding(tournament['venueAddress'])
            tournament['lattitude'] = coordinates[1]
            tournament['longitude'] = coordinates[0]

        df = pd.DataFrame(data, columns=['id', 'name', 'Date', 'Game', 'lattitude', 'longitude'])
        return 'Tournaments', px.scatter_mapbox(df, lat='lattitude', lon='longitude', color_discrete_sequence=["fuchsia"], zoom=8, mapbox_style="open-street-map", hover_data=['name', 'Date', 'Game'])
    


