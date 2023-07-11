# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

@st.cache_data
def charge_data_incident():
    return pd.read_csv(r"LFB Incident data - Datastore - with notional cost and UPRN from January 2009.csv")

@st.cache_data
def charge_data_mobilisation():
    return pd.read_csv(r"LFB Mobilisation data from January 2009.csv")

@st.cache_data
def charge_data_vehicule():
    return pd.read_csv(r"T_VehicleType.csv", sep=';')

@st.cache_resource   
def merge_df(df1,df2, the_left_on, the_right_on, the_how ):
    return pd.merge(df1,df2,left_on=the_left_on,right_on=the_right_on,how=the_how)

df_incident = charge_data_incident()
df_mob = charge_data_mobilisation()
df=merge_df(df_incident,df_mob, 'IncidentNumber', 'IncidentNumber', 'left' )

#st.title("Projet des temps de déplacement des pompiers de Londre")
st.sidebar.title("Data visualisation")
pages=["Généralité", "Analyses temporelles", "Analyses croisées"]
page=st.sidebar.radio("============", pages)




if page == pages[0] : 
    st.write("## Dataframe fusionnés")
    st.write("Incidents shape :", df_incident.shape)
    st.write("Mobilisations shape :",df_mob.shape)
    st.write("df shape :",df.shape)


if page == pages[1] : 

    st.write("### nombre d'appels par heure")
    df_group1 =  df_incident.groupby(['HourOfCall', 'IncidentGroup'], as_index = False).agg({'IncidentNumber':'count'})

    fig = plt.figure()
    plot = sns.relplot(x='HourOfCall', y='IncidentNumber', kind='line', data=df_group1, hue='IncidentGroup', height=4, aspect=2)
    plt.title("Nombre d'incidents par heure") 
    plt.xlabel("Heures") 
    plt.ylabel("Nb incidents") 
    st.pyplot(plot.fig)
    st.markdown(
    """
    On constate un creux vers 5h du matin et une stabilisation du pic d'appel entre 10h et 17h.
    Pas vraiment d'impact du type d'incident sur la répartition du volume d'appels par heure
    Prévoir une classification en 2 groupes pour le model de prédiction :
    * 1 groupe entre 22h et 6h
    * 1 groupe entre 7h et 21h
    """
    )
    
    
    st.write("#### Différence entre moyenne et mediane sur le temps total d'arrivée sur site")
    df_stats_attendancetime = df.groupby(['ProperCase'], as_index = False).agg({'AttendanceTimeSeconds':['mean','median']})
  
    fig = plt.figure()
    plot = plt.plot(df_stats_attendancetime['AttendanceTimeSeconds'],label='Temps' )
    plt.title("écart entre moyenne et mediane sur le temps de préparation") 
    plt.xlabel("Heures") 
    plt.ylabel("Secondes") 
    st.pyplot(fig) 
    
if page == pages[2] : 
    st.write("### Analyse de l'usage des types de véhicule par typologie d'incident")
    