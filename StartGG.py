import APIFunction as API
import QUERRY_TEMPLATE as QTEMP
import streamlit as sl
from SL_PAGES import Page, Test

def main():
  if "key" not in sl.session_state:
    key = None
    try : 
      with open ("API_TEST_TOKEN.txt", mode='r', encoding='utf_8') as f:
        key = f.readline()
    except : 
      sl.warning('Unable to find the keyfile', icon="❌")
      return
    if (key == None):
      sl.warning('No key found in file', icon="❌")
      return
    sl.session_state["key"] = key
  
  if "page" not in sl.session_state:
    sl.session_state['page'] = 'home'

  Pages_Dict = {
    'home': Page,
    'test': Test
  }
  
  Pages_Dict[sl.session_state['page']].main()

if __name__ == '__main__':
  main()