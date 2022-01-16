import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

st.title("RMDS Competiion")

tabs = st.sidebar.selectbox("Portfolio Phase: ", ["EDA", "Forecast and Portfolio Performance", "Appendix"])

# Exploratory Data Analysis
if tabs == "EDA":
    
    st.subheader("Upload your Portfolio data: ")
    investor_data = st.file_uploader('Upload a CSV file')
    df = pd.DataFrame(data = investor_data)
    
    # Portfolio Overview

    st.subheader("Portfolio Overview")
    
    # Key Performance Indicators
    col1, col2, col3, col4 = st.columns(4) 
    col1.metric("Most valued Stock", 70, delta = 1)
    col2.metric("Least valued Stock", 80, delta = -4)
    col3.metric("test", 100, delta = 10)
    col4.metric("test", 900, delta = -5)
    
    # Graphing
    selection = alt.selection_multi(fields = ['Morningstar Category'], bind = 'legend')

    test = alt.Chart(test).mark_area().encode(
        alt.X('Date:T', axis = alt.Axis(domain=False, format = '%Y-%m-%d')), 
        alt.Y('Open:Q'), 
        alt.Color('Morningstar Category:N')).add_selection(selection)
    
    st.altair_chart(test)
    
# Forecast and Portfolio Performance
if tabs == "Forecast and Portfolio Performance":
    
    st.write("I am inevitable")
    
    
if tabs == "Appendix":
    
    st.write("Put any clarifying information such as model type, assumptions ect...")

    
    
