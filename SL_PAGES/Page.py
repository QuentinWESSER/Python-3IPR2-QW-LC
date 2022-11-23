import streamlit as sl

def main():
    sl.button("Go to Page 2", on_click=change_page('test'))
    sl.write("home page")

def change_page(page):
    sl.session_state['page'] = page