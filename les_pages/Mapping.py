# -*- coding: utf-8 -*-

import streamlit as st
import commun
import matplotlib.pyplot as plt



pages=["Londres", "les interventions", "autres cartos"]
page=st.sidebar.radio("Sommaire", pages)

df_quartier = commun.charge_geodata_quartier()
df_stations = commun.charge_geodata_stations()
df_incident = commun.charge_data_incident()
geo_data_gpd = commun.charge_geodata_interventions(df_incident)

if page == pages[0] : 
    st.title("Les quartiers de Londre")
    st.write(df_quartier.sample(1))
    
    fig, ax = plt.subplots()
    df_quartier.plot(ax=ax, edgecolor = 'black', facecolor="none", figsize = (5,5))
    st.pyplot(fig) 
    
    
    st.title("Les casernes de pompier")
    st.write(df_stations.sample(1))
    
    fig, ax = plt.subplots()
    df_quartier.plot(ax = ax, edgecolor = 'black', facecolor="none", figsize = (5,5))
    df_stations.plot(ax = ax, alpha = 1, color = 'red', markersize=5)
    st.pyplot(fig) 
    
if page == pages[1] :
    st.title("Les interventions")
    st.write(geo_data_gpd.sample(1))
       
    fig, ax = plt.subplots()
    df_quartier.plot(ax = ax, edgecolor = 'black', facecolor="none", figsize = (10,10),zorder=3)
    geo_data_gpd.plot(ax = ax, alpha = 0.1, color = 'blue',markersize=1)
    df_stations.plot(ax = ax, alpha = 0.8, color = 'red',markersize=20)
    st.pyplot(fig) 
    
    
    
if page == pages[2] :

    st.title("....")


    