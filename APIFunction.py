import requests
import time
import json
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
    if(second < 10):
        time.sleep(second)
        return sendRequest(key, QUERRY, VAR, second*2)
    else:
        print("Error Too Many Request")
        return
  elif(500 <= req.status_code < 600):
    print("Server Error Responses")
    return
  elif(200 <= req.status_code < 300):
    return req.json()
  else:
    print("Unknow Error")
    return

#with open('games.csv', 'w', newline='') as csvfile:
#    fieldnames = ['id', 'game', 'url']
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

def SaveVideoGameAsCSV(key, num):
    dict = fetchVideoGame(key, num)

def fetchVideoGame(key, num): #return a dict with VideoGames
    var = QTEMP.VIDEOGAME_QUERRY_VAR
    var['IdRange'] = list(range(0,50))
    return sendRequest(key, QTEMP.VIDEOGAME_QUERRY, var)

