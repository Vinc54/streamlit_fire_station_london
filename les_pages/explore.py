# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io


url_incident="https://data.london.gov.uk/download/london-fire-brigade-incident-records/73728cf4-b70e-48e2-9b97-4e4341a2110d/LFB%20Incident%20data%20-%20Datastore%20-%20with%20notional%20cost%20and%20UPRN%20from%20January%202009.zip"
url_incident="incident.csv"
@st.cache_data
def charge_data_incident():
    return pd.read_csv(url_incident, compression='zip', low_memory=False)

url_mobilisation="https://data.london.gov.uk/download/london-fire-brigade-mobilisation-records/fcbd2e97-b5bf-4117-a50f-d596181bc8d3/LFB%20Mobilisation%20data%20from%20January%202009.zip"
url_mobilisation="mobilisation.csv"
@st.cache_data
def charge_data_mobilisation():
    return pd.read_csv(url_mobilisation, compression='zip', low_memory=False)



#st.title("Projet des temps de déplacement des pompiers de Londre")
st.sidebar.title("Exploration des données")
pages=["Généralité", "Données d'incidents", "Données de mobilisation"]
page=st.sidebar.radio("============", pages)






if page == pages[0] : 
    st.write("### Généralité")
    st.markdown(
        """
        Les données sont réparties en 2 fichiers :
        - les incidents : l'ensemble des intervention réalisées par les pompiers'
        - les mobilisations : les différentes ressources (véhicules) mobilisées pour réaliser ces interventions
            
            
            ```[Table incidents]  1--->n [Table mobilisations]```
            
        
        """
    )

if page == pages[1] : 
    df_incident=charge_data_incident()
    st.write("## Incidents")
    
    st.write("#### dimensions du jeu de données")
    st.write('nbr de lignes :',df_incident.shape[0])
    st.write('nbr de colonnes :',df_incident.shape[1])
    
    st.write("#### Echantillon (5 lignes)")
    st.dataframe(df_incident.sample(5))
    
    st.write("#### Affichage du type des variables")
    buffer = io.StringIO()
    df_incident.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    
    #width = st.slider("plot width", 0.1, 25., 3.)
    #height = st.slider("plot height", 0.1, 25., 1.)
    st.write("#### répartition des type de variables")
    col1, col2 = st.columns([3, 1])
    with col1:
        list_type = df_incident.dtypes.value_counts()
        fig, ax = plt.subplots(figsize=(3,3))
        ax = plt.pie(list_type, labels = list_type.index, autopct = lambda x: str(round(x, 2)) + '%', textprops={'fontsize': 6})
        st.pyplot(fig)
        
        
if page == pages[2] : 
    df_mob=charge_data_mobilisation()
    st.write("## Mobilisation")
    
    st.write("#### dimensions du jeu de données")
    st.write('nbr de lignes :',df_mob.shape[0])
    st.write('nbr de colonnes :',df_mob.shape[1])
    
    st.write("#### Echantillon (5 lignes)")
    st.dataframe(df_mob.sample(5))
    
    st.write("#### Affichage du type des variables")
    buffer = io.StringIO()
    df_mob.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    
    #width = st.slider("plot width", 0.1, 25., 3.)
    #height = st.slider("plot height", 0.1, 25., 1.)
    st.write("#### répartition des type de variables")
    col1, col2 = st.columns([3, 1])
    with col1:
        list_type = df_mob.dtypes.value_counts()
        fig, ax = plt.subplots(figsize=(3,3))
        ax = plt.pie(list_type, labels = list_type.index, autopct = lambda x: str(round(x, 2)) + '%', textprops={'fontsize': 6})
        st.pyplot(fig)        