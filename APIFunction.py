import math
import requests
import time
import csv
import QUERRY_TEMPLATE as QTEMP
import Levenshtein as lev
import pandas as pd

url = "https://api.start.gg/gql/alpha"

def sendRequest(key : str, QUERRY : str, VAR : dict, seconds = 1):
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
    
def SaveVideoGameAsCSV(key : str, num : int):
    """
    Permet de récupérer les différents jeux vidéos sur le site StartGG et de les enregister dans un csv

    Args :
        key : Clé permetant d'acceder à l'API
        num : Nombre de jeux que on veut récupérer

    Returns :
        Ne retourne rien, ou le message d'erreur
    """

    #On utilise l'API pour récupérer les Jeux vidéo
    VideoGamedict = fetchVideoGame(key, num)

    #Si il y a eu une erreur on interrompe la fonction
    if VideoGamedict == None:
        return
    if isinstance(VideoGamedict, str):
        #Si il y a message d'erreur on le renvoie
        return VideoGamedict

    betterDict = VideoGamedict.copy()
    
    #On récupere seulement une image par jeux vidéo
    for i, element in enumerate(VideoGamedict):
        if (len(element['images']) == 0):
            betterDict[i]['images'] = 'None'
        else : 
            betterDict[i]['images'] = element['images'][0]['url']

    #On écrit le contenue dans un fichier csv
    field_names = ['id', 'name', 'images']
    with open('Games.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names, delimiter=';')
        writer.writeheader()
        writer.writerows(betterDict)

def fetchVideoGame(key : str, num : int):
    """
    Permet de récupérer les différents jeux vidéos sur le site StartGG

    Args :
        key : Clé permetant d'acceder à l'API
        num : Nombre de jeux que on veut récupérer

    Returns :
        Retourne la list des jeux vidéo, ou retourne un message d'erreur en cas d'erreur
    """
    var = QTEMP.VIDEOGAME_QUERRY_VAR
    List = []
    #On ne peut que récupérer 500 élément par querry donc nous récupérons les éléments 500 par 500
    for i in range(math.ceil(num/500)):
        var['IdRange'] = list(range(i * 500, (i+1) * 500))
        try:
            List += sendRequest(key, QTEMP.VIDEOGAME_QUERRY, var)['data']['videogames']['nodes']
        except:
            return "Unable to retrieve data for the VideoGame"
        
    #On trie les jeux en fonction de leurs Id
    NewList = sorted(List, key=lambda videogame: videogame['id'])
    return NewList

def fectTournamentList(key : str, Ids : list[int], Latitude : float, Longitude : float, Range : int, StartDate : int, EndDate : int, Day=True):
    """
    Permet de récupérer les différents tournois sur une zone, une periode de temps et sur des jeux vidéos données, sur le site StartGG

    Args :
        key : Clé permetant d'acceder à l'API
        Ids : Id des jeux
        Latitude : Du centre de la zone
        Longitude : Du centre de la zone
        Range : Rayon de la zone
        StartDate : Début de la période de temps
        EndDate : Fin de la période de temps
        Day : Permet de savoir si on vas regrouper les jeux par jour (True) ou par semaine (False)

    Returns :
        Retourne la list des différents tournois, ou retourne un message d'erreur en cas d'erreur
    """
    result = []
    for index in Ids:
        #Récupere les tournois par un jeux a la fois
        response = fetchTournamentsWithOneGame(key, index, Latitude, Longitude, Range, StartDate, EndDate, Day) 
        if isinstance(response, str):
            return "Unable to retrieve tournaments"
        result += response
    return result

def fetchTournamentsWithOneGame(key : str, Id : int, Latitude : float, Longitude : float, Range : int, StartDate : int, EndDate : int, Day=True):
    """
    Permet de récupérer les différents tournois sur une zone, une periode de temps et sur le jeux vidéo donnée, sur le site StartGG

    Args :
        key : Clé permetant d'acceder à l'API
        Id : Id du jeux
        Latitude : Du centre de la zone
        Longitude : Du centre de la zone
        Range : Rayon de la zone
        StartDate : Début de la période de temps
        EndDate : Fin de la période de temps
        Day : Permet de savoir si on vas regrouper les jeux par jour (True) ou par semaine (False)

    Returns :
        Retourne la list des différents tournois, ou retourne un message d'erreur en cas d'erreur
    """

    #Definie la requete
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

    #Si il y a plus de 500 element alors il faut lire sur d'autre page et envoyer de nouvelles requetes
    for i in range(1, Page):
        var['Page'] = i+1
        try:
            Tournaments_dict += sendRequest(key, QTEMP.TOURNAMENTS_QUERRY, var)['data']['tournaments']['nodes']
        except:
            return "Unable to retrieve tournaments"
    
    #Regroupe les tournois par jour ou par semaine
    if Day:
        for element in Tournaments_dict:
            element['Date'] = pd.to_datetime(int(element['endAt']) // 86400 * 86400, unit='s')
    else:
        for element in Tournaments_dict:
            element['Date'] = pd.to_datetime(int(element['endAt']) // 604800 * 604800, unit='s')
    
    #---------------------- Amélioration -----------------------------------
    #Affiche que une image par tournois
    #for element in Tournaments_dict:
    #    if len(element['images']) == 0:
    #        element['images'] = "None"
    #    else:
    #        element['images'] = element['images'][0]['url']
    #------------------------------------------------------------------------

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
    try:
        Tournament = Tournament['data']['tournaments']['nodes'][0]
        Tournament['startAt'] = pd.to_datetime(int(Tournament['startAt']) // 86400 * 86400, unit='s')
        Tournament['endAt'] = pd.to_datetime(int(Tournament['endAt']) // 86400 * 86400, unit='s')
        PlayerWRP = []
        for player in Tournament['participants']['nodes']:
            playerP = []
            try:
                playerP = player['entrants'][0]['seeds'][0]
            except:
                continue
            playerWR = returnPlayerWR(key, player['player']['id'])
            if playerWR != 'NetworkError':
                PlayerWRP.append({'WR' : playerWR, 'P' : playerP['placement']})
        del Tournament['participants']
        Tournament['data'] = PlayerWRP
        return Tournament
    except:
        return 'An error as occured'

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
