import requests
import time

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