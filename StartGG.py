import APIFunction as API
import QUERRY_TEMPLATE as QTEMP
from dash import Output, dcc, Dash, html
import dash
import plotly.express as px
import pandas as pd

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
	html.H1('Multi-page app with Dash Pages'),
  dcc.Store(id="key-data"),
  html.Div(
      [
          html.Div(
              dcc.Link(
                  f"{page['name']} - {page['path']}", href=page["relative_path"]
              )
          )
          for page in dash.page_registry.values()
      ]
  ),
	dash.page_container
])

  
@app.callback(
  Output("key-data", "data")
)
def LoadKey():
  key = None
  try : 
    with open ("API_TEST_TOKEN.txt", mode='r', encoding='utf_8') as f:
      key = f.readline()
  except : 
    print('Unable to find the keyfile ❌')
    return ['No key found in file ❌']
  if (key == None):
    print('No key found in file ❌')
    return ['No key found in file ❌']
  return [key]

def main():
  data = API.fectTournamentList(LoadKey()[0], [1], "48.866667", "2.333333", "200", 1666811322, 1669493322)
  print(API.ReverseGeoCoding(data[0]['venueAddress']))

if __name__ == '__main__':
  #app.run_server()
  main()