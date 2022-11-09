import requests
import json
import csv
import QUERRY_TEMPLATE as QTEMP

url = "https://api.start.gg/gql/alpha"

def sendRequest(key, QUERRY, VAR):
  header = {"Authorization": "Bearer " + key}
  query = QUERRY
  variables = VAR

  jsonRequest = {"query":query,"variables":variables}

  req = requests.post( url = url,json=jsonRequest,headers=header)
  print(req.json())

with open('games.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'game', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

def fetchVideoGame(key, num):
    var = QTEMP.VIDEOGAME_QUERRY_VAR
    var['IdRange'] = range(0,50)
    sendRequest(key, QTEMP.VIDEOGAME_QUERRY, var)

