import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

st.title("RMDS Competiion")

tabs = st.sidebar.selectbox("Portfolio Phase: ", ["EDA", "Forecast and Portfolio Performance"])

if tabs == "EDA":
    
    st.subheader("Upload your Portfolio data: ")
    investor_data = st.file_uploader('Upload a CSV file')
    
if tabs == "Forecast and Portfolio Performance":
    
    st.write("I am inevitable")
