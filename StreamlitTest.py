import streamlit as sl

sl.write("Test Write")
sl.dataframe(["Some Text element", 0, True])    
isCheck = sl.checkbox("Check Me")
if(isCheck):
    sl.write("I'm check")