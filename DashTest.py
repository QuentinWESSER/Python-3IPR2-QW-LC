import APIFunction as API
import QUERRY_TEMPLATE as QTEMP
from dash import Output, dcc, Dash, html, State, Input
import dash

key = None

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
  dcc.Store(id="key-data"),
  html.Div(className="btn-home", children=[html.A(html.Button("Home"), href="home")]),
	dash.page_container
])

@app.callback(
  Output("key-data", "data"),
  Input("btn", "n_clicks"),
  State("key-data", "data")
)
def LoadKey(_, data):
  if data == None:
    key = None
    try : 
      with open ("API_TEST_TOKEN.txt", mode='r', encoding='utf_8') as f:
        key = f.readline()
    except : 
      return ['No key found in file ❌', 'No key found in file ❌']
    if (key == None):
      return ['No key found in file ❌', 'No key found in file ❌']
    return [str(key), str(key)]
  else:
    return [str(data), str(data)]

if __name__ == '__main__':
	app.run_server(debug=True)