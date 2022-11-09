import requests
import json

url = "https://api.start.gg/gql/alpha"


def sendRequest(key):
  header = {"Authorization": "Bearer " + key}
  query = '''
  query GetVideoGameLocation($cCode: String, $perPage: Int!) {
    Videogame(id: $eventId) {
      id
      name
      sets(
        page: $page
        perPage: $perPage
        sortType: STANDARD
      ) {
        pageInfo {
          total
        }
        nodes {
          id
          slots {
            id
            entrant {
              id
              name
            }
          }
        }
      }
    }
  },'''

  variables = {
    "eventId":261856,
    "page": 1,
    "perPage": 3
  }

  jsonRequest = {"query":query,"variables":variables}

  req = requests.post( url = url,json=jsonRequest,headers=header)
  print(req.json())


def main():
  key = None
  try : 
    with open ("API_TEST_TOKEN.txt", mode='r', encoding='utf_8') as f:
      key = f.readline()
  except : 
    print("Unable to find the keyfile")
    return
  if (key == None):
    print("No key found in file")
    return
  sendRequest(key)

if __name__ == '__main__':
  main()
