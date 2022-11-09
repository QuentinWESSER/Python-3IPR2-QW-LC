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

def Replace(element, listreplace):
    for replaceTerm in listreplace:
        if(replaceTerm[0] in element):
            return element.replace(replaceTerm[0], replaceTerm[1])
    return element
    
def SaveVideoGameAsCSV(key, num):
    VideoGamedict = fetchVideoGame(key, num)
    if VideoGamedict == None:
        return
    betterDict = VideoGamedict.copy()

    #Remove unwanted accent in the name of the videogame
    #Add any other unicode if needed
    for element in betterDict:
        element['name'] = Replace(element['name'],[
            (u'\u014d', 'o'),
            (u'\u014c', 'O'),
            (u'\u016b', 'u'),
            (u'\u2153', ''),
            (u'\ufeff', ''),
            (u'\u2665', ''),
            (u'\u266e', ''),
            (u'\u016b', 'u')
        ])

    #get only one image for each video games
    for i, element in enumerate(VideoGamedict):
        if (len(element['images']) == 0):
            betterDict[i]['images'] = 'None'
        else : 
            betterDict[i]['images'] = element['images'][0]['url']

    #write the content into an csv
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
        try:
            List += sendRequest(key, QTEMP.VIDEOGAME_QUERRY, var)['data']['videogames']['nodes']
        except:
            print("Unable to retrieve data for the VideoGame")
            return
        
    NewList = sorted(List, key=lambda videogame: videogame['id'])
    return NewList

