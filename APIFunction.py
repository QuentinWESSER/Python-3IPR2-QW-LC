import math
import requests
import time
import csv
import QUERRY_TEMPLATE as QTEMP

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

#with open('games.csv', 'w', newline='') as csvfile:
#    fieldnames = ['id', 'game', 'url']
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

def SaveVideoGameAsCSV(key, num):
    dict = fetchVideoGame(key, num)
    betterDict = dict.copy()

    for element in betterDict:
        if(u'\u014d' in element['name']):
            element['name'] = element['name'].replace(u'\u014d', 'o')
        if(u'\u014c' in element['name']):
            element['name'] = element['name'].replace(u'\u014c', 'O')
        if(u'\u016b' in element['name']):
            element['name'] = element['name'].replace(u'\u016b', 'u')

    field_names = ['id', 'name', 'images']
    with open('Games.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names, delimiter=';')
        writer.writeheader()
        writer.writerows(betterDict)

def fetchVideoGame(key, num): #return a dict with VideoGames
    var = QTEMP.VIDEOGAME_QUERRY_VAR
    List = []
    for i in range(math.ceil(num/500)):
        var['IdRange'] = list(range(i * 500, (i+1) * 500))
        response = sendRequest(key, QTEMP.VIDEOGAME_QUERRY, var)['data']['videogames']['nodes']
        try:
            List += response
        except:
            print("Unable to retrieve data for the VideoGame")
            return
        
    NewList = sorted(List, key=lambda videogame: videogame['id'])
    return NewList

