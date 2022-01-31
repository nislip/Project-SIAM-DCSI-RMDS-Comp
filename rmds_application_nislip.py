import pandas as pd
import numpy as np
from sklearn import cluster
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go

st.title("RMDS Competiion")

tabs = st.sidebar.selectbox("Portfolio Phase: ", ["Portfolio Summary", "Kmeans-PCA Model", "Appendix"])

## ================ DATA =======================
##==============================================

def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)

def KMEANS(data, featurenames):
    '''
    input data of funds 
    featurenames will be used to subset the data 
    Kmeans algorithm will be run with the default of 8 clusters 
    return filtered data,  kmeans object. 
    '''
    df = data[featurenames]
    # Running Kmeans
    kmeans = KMeans(n_clusters=8).fit(df)
    st.write('Kmeans is finished')
    return df, kmeans

def pca_model(kmeans):
    '''
    input is a kmeans object 
    dictionary to track the clustering groups 
    return pca objects for each clustering 
    '''
    mydict = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}
    pcaobjects = []
    pca=PCA(n_components=3) # how many do we want? 
    for key, value in mydict.items():
        X_test = df[df.index.isin(list(value))] 
        pcaobjects.append( pca.fit(X_test))
    return pcaobjects

def pca_loadings(group, pcaobjects, data):
    '''
    Graphs the bar charts for the loadings by the group number 
    '''
    df = data
    
    test = pcaobjects[group]
    st.write(test.explained_variance_)
    loadings = pd.DataFrame(test.components_.T, index = df.columns, columns = ['PC1', 'PC2', 'PC3']).reset_index()
    loadings = loadings.reindex(loadings.PC1.abs().sort_values(ascending = False).index).head(5)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=loadings['index'],
        y=loadings['PC1'],
        name='Principal Component 1',
        marker_color='Black'
        ))
    fig.add_trace(go.Bar(
        x=loadings['index'],
        y=loadings['PC2'],
        name='Principal Component 2',
        marker_color='Red'
    ))
    fig.add_trace(go.Bar(
        x=loadings['index'],
        y=loadings['PC3'],
        name='Principal Component 3',
        marker_color='Blue'
    ))

    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    st.plotly_chart(fig)

# Containers
search_container = st.beta_container()
clustering_container = st.beta_container()


data = pd.read_csv('funds.csv') # define the original dataframe

prices_1 = pd.read_csv('prices_1.csv') # prices per day
prices_2 = pd.read_csv('prices_2.csv')
prices_3 = pd.read_csv('prices_3.csv')
prices_4 = pd.read_csv('prices_4.csv')
prices_5 = pd.read_csv('prices_5.csv')
prices_6 = pd.read_csv('prices_6.csv')

prices_per_day = pd.concat([prices_1, prices_2, prices_3, prices_4, prices_5, prices_6], axis=0) # concat the prices per day

# Convert 'Morningstar Category' to dictionary defined numerical value.
mornCategory = data['Morningstar Category'].unique()                          # Make list of all unique morningstar categories
categoryDict = {mornCategory[i] : i for i in range(0, len(mornCategory) ) }    # Create dictionary of form 'Category name' : number
data = data.replace({'Morningstar Category': categoryDict})                  # Replace Morningstar names with assigned number from dict

## Convert Yes/No to binary
yesNoDict = {'Yes':1, 'No':0}                                                  # Create Yes/No dict mapped to 1/0
data = data.replace({'Sustainable Investment by Prospectus' : yesNoDict})    # Replace assign 1/0 to Yes/No values from dict
data = data.replace({'Sustainable Investment - ESG Fund' : yesNoDict})
data = data.replace({'Sustainable Investment - Impact Fund' : yesNoDict})
data = data.replace({'Sustainable Investment - Environmental Sector Fund' : yesNoDict})

## Convert Average Credit Quality to dictionary defined numerical value (ordered least to greatest).
creditDict = {'B' : 0,
                'BB' : 1,
                'BBB' : 2,
                'A' : 3,
                'AA' : 4,
                'AAA' : 5,}
data = data.replace({'Average Credit Quality' : creditDict})               # Assign number to Average Credit Quality from dict

## Convert 'Equity StyleBox' to dictionary defined numerical value.
equityStyle = data['Equity StyleBox'].unique()                                # Make list of all unique Equity StyleBox
equityDict = {equityStyle[i] : i for i in range(0, len(equityStyle) ) }        # Create dictionary of form 'Equity Style' : number 
data = data.replace({'Equity StyleBox': equityDict})                         # Replace Equity StyleBox names with assigned number from dict

## Convert 'Fixed Income StyleBox' to dictionary defined numerical value.
fixedIncomeStyle = data['Fixed Income StyleBox'].unique()                                # Make list of all unique Fixed Income StyleBox
fixedIncomeDict = {fixedIncomeStyle[i] : i for i in range(0, len(fixedIncomeStyle) ) }        # Create dictionary of form 'Fixed Income Style' : number 
data = data.replace({'Fixed Income StyleBox': fixedIncomeDict})                         # Replace Fixed Income StyleBox names with assigned number from dict

## Replace all comma using numbers with form of floats with string type
data['Fund Size (Mil)'] = data['Fund Size (Mil)'].str.replace(',','')
data['Average Market Cap (Mil)'] = data['Average Market Cap (Mil)'].str.replace(',','')
## Convert string values to floats
data['Fund Size (Mil)'] = data['Fund Size (Mil)'].astype(float)
data['Average Market Cap (Mil)'] = data['Average Market Cap (Mil)'].astype(float)

tickersnames = list(data['Ticker'])
data = data.drop(columns = ['Name', 'Ticker']).reset_index()
df = clean_dataset(df = data) # Define the complete data set
df = df.drop(columns = ['index'])
featurenames = df.columns

#================== END DATA ======================
##=================================================

# Standard Scaler


# Exploratory Data Analysis
if tabs == "Portfolio Summary":
    # Portfolio Overview
    with search_container:
        st.subheader("Portfolio Overview")
        
        subsettickers = st.multiselect('Select a subset of tickers in your Portfolio', tickersnames) # Creates list
        selectfeatures = st.multiselect('Select a subset of tickers to cluster', featurenames) # Creates list
        
    with clustering_container:
        kmeans=None
        if st.checkbox('Run Clustering Algorithm (Yes/No)'):
            df, kmeans = KMEANS(df, selectfeatures)
            # st.write(kmeans.n_clusters) # testing
            option = st.selectbox("Choose clusters for pca: ", (0, 1, 2, 3, 4, 5, 6, 7)  )
            pcaobjects = pca_model(kmeans)
            pca_loadings(int(option), pcaobjects, df )

    
    
    #button = st.button('Run Clustering Algorithm (Yes/No)', on_click = KMEANS, arg = (df, selectfeatures))
    
    
    # Key Performance Indicators
    #col1, col2, col3, col4 = st.columns(4) 
    #col1.metric("Most valued Stock", 70, delta = 1)
    #col2.metric("Least valued Stock", 80, delta = -4)
    #col3.metric("test", 100, delta = 10)
    #col4.metric("test", 900, delta = -5)
    
    # Graphing
    
# Forecast and Portfolio Performance
if tabs == "Kmeans-PCA Model":
    
    st.write("I am inevitable")
    
    
if tabs == "Appendix":
    
    st.write("Put any clarifying information such as model type, assumptions ect...")
    
    
