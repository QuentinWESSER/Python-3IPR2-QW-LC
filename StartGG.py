import APIFunction as API
import QUERRY_TEMPLATE as QTEMP

def main():
  if "key" not in sl.session_state:
    key = None
    try : 
      with open ("API_TEST_TOKEN.txt", mode='r', encoding='utf_8') as f:
        key = f.readline()
    except : 
      print('Unable to find the keyfile ❌')
      return
    if (key == None):
      print('No key found in file ❌')
      return
  

if __name__ == '__main__':
  main()