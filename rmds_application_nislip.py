import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

st.title("RMDS Competiion")

add_selectbox = st.sidebar.selectbox(
    "Select Competition Phase",
    ("Introduction", "EDA", "Modeling")
)

if st.sidebar.selectbox('Select Competition Phase',['Introduction']) == 'Introduction':
    
    st.write('test')
