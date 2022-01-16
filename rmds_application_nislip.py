import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

st.title("RMDS Competiion")

tabs = st.sidebar.selectbox("Portfolio Phase: ", ["EDA", "Forecast and Portfolio Performance"])

if tabs == "EDA":
    
    st.subheader("Upload your Portfolio data: ")
    investor_data = st.file_uploader('Upload a CSV file')
    
    st.subheader("Portfolio Overview")
    
    col1, col2, col3, col4 = st.columns(4) 
    col1.metric("Most valued Stock", 70)
    col1.metric("Least valued Stock", 80)
    col1.metric("test", 100)
    col1.metric("test", 900)
    
if tabs == "Forecast and Portfolio Performance":
    
    st.write("I am inevitable")

    
    
