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
    import geoplot as gplt
    #import geoplot.crs as gcrs
    import geopandas as gpd
    st.title("Evolution dans le temps")
    valeur_echantillon = 0.001
    
    list_annee = sorted(geo_data_gpd['CalYear'].unique().tolist())
    i_annee=0
    # display(list_annee)
    nb_col = int(len(list_annee)**(0.5))+1
    st.write('nombre d\'année' , len(list_annee))
    st.write('nombre de colonne ', nb_col)
    fig, axes = plt.subplots(figsize=(20, 20), ncols=nb_col, nrows=nb_col)
    for x in range(nb_col):
        for y in range(nb_col):
            st.write(x,y)
            ax=axes[x, y]
            if 0 <= i_annee < len(list_annee):
                geo_data_gpd_tmp = geo_data_gpd[geo_data_gpd['CalYear']==list_annee[i_annee]]
                nb_point = len(geo_data_gpd_tmp)
                # geo_data_gpd_tmp_echantillon = geo_data_gpd_tmp.sample(int(nb_point * valeur_echantillon))
                # gplt.kdeplot(geo_data_gpd_tmp_echantillon, cmap='Reds', fill=True, thresh=0.04, clip=df_quartier, ax=ax)
                # df_quartier.plot(ax=ax,facecolor='None')
                # ax.title.set_text(str(list_annee[i_annee]) + " nb d'inter : " + str(len(geo_data_gpd_tmp)))
                i_annee +=1
    st.pyplot(fig) 

    