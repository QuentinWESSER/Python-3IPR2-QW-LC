import math
import requests
import time
import csv
import QUERRY_TEMPLATE as QTEMP
import Levenshtein as lev

url = "https://api.start.gg/gql/alpha"

def sendRequest(key, QUERRY, VAR, second=1):
    header = {"Authorization": "Bearer " + key}
    query = QUERRY
    variables = VAR

    jsonRequest = {"query":query,"variables":variables}

    req = requests.post( url = url,json=jsonRequest,headers=header)

    #From https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

    if(req.status_code == 429):
        if(second < 20):
            time.sleep(second)
            return sendRequest(key, QUERRY, VAR, second*2)
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

def Replace(element, listreplace):
    for replaceTerm in listreplace:
        if(replaceTerm[0] in element):
            element = element.replace(replaceTerm[0], replaceTerm[1])
    return element
    
def SaveVideoGameAsCSV(key, num):
    VideoGamedict = fetchVideoGame(key, num)
    if VideoGamedict == None:
        return
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
            print("Unable to retrieve data for the VideoGame")
            return
        
    NewList = sorted(List, key=lambda videogame: videogame['id'])
    return NewList

def fectTournamentList(key, Id, Latitude, Longitude, Range, StartDate, EndDate):
    var = QTEMP.VIDEOGAME_QUERRY_VAR
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
        print("Unable to retrieve tournaments")
        return

    for i in range(1, Page):
        var['Page'] = i+1
        try:
            Tournaments_dict += sendRequest(key, QTEMP.TOURNAMENTS_QUERRY, var)['data']['tournaments']['nodes']
        except:
            print("Unable to retrieve tournaments")
            return
    
    return Tournaments_dict
    
def returnCityNames(input, distMax):
    result = [[None,0,0,0]]
    with open('villes_france.csv', 'r', encoding='utf-8') as csvfile:
        r = csv.reader(csvfile, delimiter=',')
        for row in r:
            ratio = lev.ratio(input.lower(),row[4])
            i = -1
            for index, element in enumerate(result):
                if (element[1] < ratio):
                    i = index
                    break
            if (i != -1):
                result.pop()
                result.insert(i, [row[5],ratio, row[20], row[19]])
    indexs = []
    for index, element in enumerate(result):
        if(lev.distance(element[0],input) > distMax):
            indexs.append(index)
    
    if (indexs):
        for element in indexs.reverse():
            result.pop(element)
    return result


        
    
        
                


    
