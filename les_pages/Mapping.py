# -*- coding: utf-8 -*-

import streamlit as st
import commun
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd

import seaborn as sns

st.set_page_config(
    page_title="LFB",
    page_icon="🚨",
    layout="wide"
)
mem_usage_text = st.sidebar.empty()

pages=["Londres", "les interventions", "autres cartos", "test"]
page=st.sidebar.radio("Sommaire", pages)

df_quartier = commun.charge_geodata_quartier()
df_stations = commun.charge_geodata_stations()
df_incident = commun.charge_data_incident()
df_mob = commun.charge_data_mobilisation()
geo_data_gpd = commun.charge_geodata_interventions(df_incident)
df_vehicule = commun.charge_data_vehicule()
df=commun.merge_df(df_incident,df_mob, 'IncidentNumber', 'IncidentNumber', 'left' )
df=commun.merge_df_vehicule(df,df_vehicule, 'Resource_Code_vehicule', 'Id_VehicleType', 'left' )

if page == pages[0] : 
    st.title("Les quartiers de Londre")
    st.write(df_quartier.sample(1), text_align="center")
    
    col1, col2 , col3= st.columns(3)
    with col2:
        fig, ax = plt.subplots(figsize = (5,5))
        df_quartier.plot(ax=ax, edgecolor = 'black', facecolor="none")
        st.pyplot(fig) 
        
    
    
    st.title("Les casernes de pompier")
    st.write(df_stations.sample(1))
        
    col1, col2 , col3= st.columns(3)
    with col2:        
        fig, ax = plt.subplots()
        df_quartier.plot(ax = ax, edgecolor = 'black', facecolor="none", figsize = (5,5))
        df_stations.plot(ax = ax, alpha = 1, color = 'red', markersize=5)
        st.pyplot(fig) 

    
    
    
    
    
    
if page == pages[1] :
    st.title("Les interventions")
    st.write(geo_data_gpd.sample(1))
   
    #width = st.sidebar.slider("plot width", 1, 25, 3)
    #height = st.sidebar.slider("plot height", 1, 25, 1)
    
    fig, ax = plt.subplots()
    df_quartier.plot(ax = ax, edgecolor = 'black', facecolor="none", zorder=3)
    geo_data_gpd.plot(ax = ax, alpha = 0.1, color = 'blue',markersize=1)
    df_stations.plot(ax = ax, alpha = 0.8, color = 'red',markersize=20)
    temp_file = "temp_plot.png"
    plt.savefig(temp_file)
    st.image(temp_file, width=600)

    



if page == pages[2] :
    
    df_quartier['borough'] = df_quartier['borough'].str.upper()
    st.title("Les temps de déplacement moyens")
    
    def display_time_filters(df):
        year_list = list(df['CalYear_x'].unique())
        year_list.sort()
        year = st.sidebar.selectbox('Année', year_list, len(year_list)-1)
        #st.header(f'Année : {year}')
        return year
    
    
    
    def Affiche_resultat(df, year, quartier):
        
        df_filtered = df[(df['CalYear_x'] == year) & (df['IncGeo_BoroughName'] == quartier)]
        #sns.set(font_scale=.3)
        sns.set(rc={"figure.figsize":(15, 20)})
        fig = plt.figure()
        
        plot =  sns.displot(df_filtered['FirstPumpArriving_AttendanceTime'], bins=20, rug=True, kde=True, color='blue');
        valeur_target = 360
        plt.axvline(x=valeur_target, color='red', linestyle='--', label=f'Target ({valeur_target / 60 } min)')
        plt.legend()
        st.pyplot(plot.fig)
        st.metric('titre', 123456)
        
        
        
    def display_map(df, year):
        #filtre sur l'annee choisie
        df_filtered = df[df['CalYear_x'] == year]
        df_avg = df_filtered.groupby('IncGeo_BoroughName')['FirstPumpArriving_AttendanceTime'].mean().reset_index()
        
        map = folium.Map(location=[51.470000, -0.100000], zoom_start=10, scrollWheelZoom=False)

        choropleth = folium.Choropleth(
                geo_data=df_quartier,
                data=df_avg,
                columns=('IncGeo_BoroughName', 'FirstPumpArriving_AttendanceTime'),
                key_on='feature.properties.borough',
                line_opacity=0.8,
                highlight=True
            )
        choropleth.geojson.add_to(map)
        
        df_indexed = df_filtered.set_index('IncGeo_BoroughName')
        
        
        for feature in choropleth.geojson.data['features']:
            state_name = feature['properties']['borough']
            feature['properties']['Nb_Inter'] = 'Nb Inter : '
           
        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(['borough', 'response', 'score','Nb_Inter'], labels=False)
        )
        
        
        tooltip = "Click me!"
        for (index, station) in df_stations.iterrows():
            folium.CircleMarker([station['latitude'], station['longitude']],radius=3, color='black',  popup=str(station['name']), tooltip=tooltip).add_to(map)
        
        st_map = st_folium(map, width=700, height=550)
        
        state_name = ''
        if st_map['last_active_drawing']:
            state_name = st_map['last_active_drawing']['properties']['borough']

        return state_name



    def main():
        year = display_time_filters(df)
        col1, col2 = st.columns(2)
        with col1:
            quartier = display_map(df, year)
            st.header(f'Année : {year} pour le quatier : {quartier}')
        with col2:
            Affiche_resultat(df, year, quartier)   
        
        
        st.subheader(f'Nom du Quatier : {quartier}')
        
        
    #if __name__ == "__main__":
    main()    
    
    

if page == pages[3] :
    st.write("fin")
    
    
    
####################################################
# conso memoire
####################################################
commun.conso_memoire(mem_usage_text)    
####################################################
