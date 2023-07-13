# -*- coding: utf-8 -*-
import commun
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io



st.set_page_config(
    page_title="LFB",
    page_icon="🚨",
)


#st.title("Projet des temps de déplacement des pompiers de Londre")
st.sidebar.title("Exploration des données")
pages=["Généralité", "Données d'incidents", "Données de mobilisation", "Données jointes"]
page=st.sidebar.radio("============", pages)

df_incident=commun.charge_data_incident()
df_mob=commun.charge_data_mobilisation()
df=commun.merge_df(df_incident,df_mob, 'IncidentNumber', 'IncidentNumber', 'left' )


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
        
if page == pages[3] :
    
    st.write("#### Quelques dénombrements")
    st.write("Le nombre d'incidents total",len(df))
    st.write("Le nombre d'incidents n'ayant pas d'information de pompe est de",len(df[(df['FirstPumpArriving_AttendanceTime'].isnull())]))
    st.write("Le nombre d'incidents n'ayant pas d'information de mobilisation est de",len(df[(df['ResourceMobilisationId'].isnull())]))
    st.write("Le nombre d'incidents pour lesquelles nous n'avons pas de pompe mais qui a nécessité des mobilisations est de", len(df[(df['FirstPumpArriving_AttendanceTime'].isnull()) & (df['ResourceMobilisationId'].notnull())]))
    st.dataframe(df[(df['FirstPumpArriving_AttendanceTime'].isnull()) & (df['ResourceMobilisationId'].notnull())])
    
    st.write("#### Intégration de la typologie de véhicule dans nos analyses")
    st.markdown(f'Les valeurs prises par "Resource_Code" sont : \n {df.Resource_Code.unique().tolist()}')
    