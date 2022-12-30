import math
import requests
import time
import csv
import QUERRY_TEMPLATE as QTEMP
import Levenshtein as lev
import pandas as pd

url = "https://api.start.gg/gql/alpha"

def sendRequest(key, QUERRY, VAR, seconds=1):
    """
    Permet d'envoyer une requete post avec un payload et de retourner la reponse de la requete

    Args :
        key : Clé permetant d'acceder à l'API
        QUERRY : Type de requete que nous voulons envoyer
        VAR : Parametre de la requete
        seconds = 1 : Temps minimum pour renvoyer une requete si on dépasse le nombre de requete limité dans une periode de temps

    Returns :
        Retourne la réponse à la requete, ou retourne rien en cas d'erreur
    """

    #Permet de s'identifier à de l'API
    header = {"Authorization": "Bearer " + key}

    jsonRequest = {"query":QUERRY,"variables":VAR}

    req = requests.post( url = url,json=jsonRequest,headers=header)

    #From https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

    if(req.status_code == 429): #Trop de requete
        if(seconds < 20):
            #On attends et on renvoye une requete
            time.sleep(seconds)
            return sendRequest(key, QUERRY, VAR, seconds*2)
        else:
            print("Error Too Many Request" + str(req.status_code))
            return
    elif(500 <= req.status_code < 600):
        print("Server Error Responses" + str(req.status_code))
        return
    elif(200 <= req.status_code < 300):
        return req.json()
    else:
        print("Unknow Error" + str(req.status_code))
        return

def ReverseGeoCoding(adress : str):
    """
    Permet de retourner les coordonées d'une adresse, avec le site https://api-adresse.data.gouv.fr/

    Args :
        adress : Addresse dont on veut récuperer les coordonnées

    Returns :
        Retourne la coordonnées, ou retourne rien en cas d'erreur
    """
    gov_url = "https://api-adresse.data.gouv.fr/search/?q=" + adress.replace(" ", "+")
    req = requests.get(url=gov_url, headers=None, json=None)
    try:
        return req.json()['features'][0]['geometry']['coordinates']
    except:
        return
    
def SaveVideoGameAsCSV(key, num):
    VideoGamedict = fetchVideoGame(key, num)
    if VideoGamedict == None:
        return
    if isinstance(VideoGamedict, str):
        return VideoGamedict

    betterDict = VideoGamedict.copy()
    
    #get only one image for each video games
    for i, element in enumerate(VideoGamedict):
        if (len(element['images']) == 0):
            betterDict[i]['images'] = 'None'
        else : 
            betterDict[i]['images'] = element['images'][0]['url']

    #write the content into an csv
    field_names = ['id', 'name', 'images']
    with open('Games.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names, delimiter=';')
        writer.writeheader()
        writer.writerows(betterDict)

def fetchVideoGame(key, num): #return a dict with VideoGames
    var = QTEMP.VIDEOGAME_QUERRY_VAR
    List = []
    for i in range(math.ceil(num/500)):
        var['IdRange'] = list(range(i * 500, (i+1) * 500))
        try:
            List += sendRequest(key, QTEMP.VIDEOGAME_QUERRY, var)['data']['videogames']['nodes']
        except:
            return "Unable to retrieve data for the VideoGame"
        
    NewList = sorted(List, key=lambda videogame: videogame['id'])
    return NewList

def fectTournamentList(key, Ids, Latitude, Longitude, Range, StartDate, EndDate, Day=True):
    result = []
    for index in Ids:
        response = fetchTournamentsWithOneGame(key, index, Latitude, Longitude, Range, StartDate, EndDate, Day)
        if isinstance(response, str):
            return "Unable to retrieve tournaments"
        result += response
    return result

def fetchTournamentsWithOneGame(key, Id, Latitude, Longitude, Range, StartDate, EndDate, Day=True):
    var = QTEMP.TOURNAMENTS_QUERRY_VAR
    var['IdRange'] = [Id]
    var['Loca'] = str(Latitude) + "," + str(Longitude)
    var['Range'] = str(Range) + "km"
    var['Start'] = StartDate
    var['End'] = EndDate
    var['Page'] = 1
    Tournaments_dict = []
    Page = 0
    try:
        response = sendRequest(key, QTEMP.TOURNAMENTS_QUERRY, var)
        Tournaments_dict += response['data']['tournaments']['nodes']
        Page = response['data']['tournaments']['pageInfo']['totalPages']
    except:
        return "Unable to retrieve tournaments"

    for i in range(1, Page):
        var['Page'] = i+1
        try:
            Tournaments_dict += sendRequest(key, QTEMP.TOURNAMENTS_QUERRY, var)['data']['tournaments']['nodes']
        except:
            return "Unable to retrieve tournaments"
    
    if Day:
        for element in Tournaments_dict:
            element['Date'] = pd.to_datetime(int(element['endAt']) // 86400 * 86400, unit='s')
    else:
        for element in Tournaments_dict:
            element['Date'] = pd.to_datetime(int(element['endAt']) // 604800 * 604800, unit='s')
    
    for element in Tournaments_dict:
        if len(element['images']) == 0:
            element['images'] = "None"
        else:
            element['images'] = element['images'][0]['url']

    for Tournaments in Tournaments_dict:
        Tournaments['GameID'] = Id
    return Tournaments_dict

def returnCityNames(input, distMax):
    Cities = []
    with open('villes_france.csv', 'r', encoding='utf-8') as csvfile:
        result = FindClosetList(csv.reader(csvfile, delimiter=','), input, 10, 4, distMax)
        for city in result:
            Cities.append([city[0][5], city[0][1], city[0][20], city[0][19]])
    return Cities

def returnVideoGames(input, distMax):
    Games = []
    with open('games.csv', 'r', encoding='utf-8') as csvfile:
        result = FindClosetList(csv.DictReader(csvfile, delimiter=';'), input, 10, 'name', distMax)
        for game in result:
            Games.append([game[0]['id'], game[0]['name'], game[0]['images']])
    return Games

def returnTournament(key, Id):
    var = QTEMP.TOURNAMENT_QUERRY_VAR
    var['TournamentID'] = Id
    Tournament = sendRequest(key, QTEMP.TOURNAMENT_QUERRY, var)
    if Tournament == None:
        return 'Unable to retrieve info'
    Tournament = Tournament['data']['tournaments']['nodes'][0]
    PlayerWRP = []
    print(Tournament['participants']['nodes'])
    for player in Tournament['participants']['nodes']:
        playerP = player['entrants'][0]['seeds'][0]
        playerWR = returnPlayerWR(key, player['player']['id'])
        if playerWR != 'NetworkError':
            PlayerWRP.append({'WR' : playerWR, 'P' : playerP['placement']})
    del Tournament['participants']
    Tournament['data'] = PlayerWRP
    return Tournament

def returnPlayerWR(key, id):
    var = QTEMP.SETS_QUERRY_VAR
    var['PlayerID'] = id
    response = sendRequest(key, QTEMP.SETS_QUERRY, var)
    try:
        Game = 0
        Win = 0
        for element in response['data']['player']['sets']['nodes']:
            winnerId = element['winnerId']
            for player in element['slots']:
                if player['entrant']['id'] == winnerId:
                    Game += 1
                    if player['entrant']['participants'][0]['player']['id'] == id:
                        Win += 1
        return Win/Game
    except:
        return "An error as occured"
    
    


def FindClosetList(dict, input, nElements, key, distMax):
    result = [[None, 0]] * nElements
    for row in dict:
        ratio = lev.ratio(input.lower(), row[key])
        i = -1
        for index, element in enumerate(result):
            if (element[1] < ratio):
                i = index
                break
        if (i != -1):
            result.pop()
            result.insert(i, [row, ratio])
    indexs = []
    for index, element in enumerate(result):
        if(lev.distance(element[0][key],input) > distMax):
            indexs.append(index)
    
    if (len(indexs) != 0):
        indexs.reverse()
        for element in indexs:
            result.pop(element)
    return result
