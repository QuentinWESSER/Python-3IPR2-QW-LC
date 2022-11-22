import streamlit as sl

sl.write("Test Write")
select = sl.selectbox("Villes", ["Select a number"] + list(range(0,5)))
sl.write(select)