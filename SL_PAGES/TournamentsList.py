import streamlit as sl

def change_page(page):
    sl.session_state['page'] = page