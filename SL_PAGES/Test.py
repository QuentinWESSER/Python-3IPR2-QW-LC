import streamlit as sl

def main():
    sl.button("Go to Home page", on_click=change_page('home'))
    sl.write("page2")

def change_page(page):
    sl.session_state['page'] = page