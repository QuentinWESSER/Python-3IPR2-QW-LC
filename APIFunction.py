import requests
import json

url = "https://api.start.gg/gql/alpha"

def sendRequest(key, QUERRY, VAR):
  header = {"Authorization": "Bearer " + key}
  query = QUERRY
  variables = VAR

  jsonRequest = {"query":query,"variables":variables}

  req = requests.post( url = url,json=jsonRequest,headers=header)
  print(req.json())