import pandas as pd
import streamlit as st
import geopandas as gpd
import pyproj
from pyproj import Transformer, transform
from shapely.geometry import Polygon
import json

years = [2022,2023]
years_string = "2022,2023"

url_incident="https://data.london.gov.uk/download/london-fire-brigade-incident-records/73728cf4-b70e-48e2-9b97-4e4341a2110d/LFB%20Incident%20data%20-%20Datastore%20-%20with%20notional%20cost%20and%20UPRN%20from%20January%202009.zip"
#url_incident="data/incident.csv"
@st.cache_data
def charge_data_incident():
    df = pd.read_csv(url_incident, compression='zip', low_memory=False)
    df = df[df.CalYear.isin(years)]
    return df

url_mobilisation="https://data.london.gov.uk/download/london-fire-brigade-mobilisation-records/fcbd2e97-b5bf-4117-a50f-d596181bc8d3/LFB%20Mobilisation%20data%20from%20January%202009.zip"
#url_mobilisation="data/mobilisation.csv"
@st.cache_data
def charge_data_mobilisation():
    df = pd.read_csv(url_mobilisation, compression='zip', low_memory=False)
    df = df[df.CalYear.isin(years)]
    return df

@st.cache_data
def charge_data_vehicule():
    return pd.read_csv(r"data/T_VehicleType.csv", sep=';')


@st.cache_data
def charge_geodata_quartier():
    df_quartier =[]
    liste_quartier = [ "Barking and Dagenham", "Barnet", "Bexley", "Brent",
          "Bromley", "Camden", "City of London", "Croydon", "Ealing", "Enfield",
          "Greenwich", "Hackney", "Hammersmith and Fulham", "Haringey", "Harrow",
          "Havering", "Hillingdon", "Hounslow", "Islington",
          "Kensington and Chelsea", "Kingston upon Thames", "Lambeth", "Lewisham",
          "Merton", "Newham", "Redbridge", "Richmond upon Thames", "Southwark",
          "Sutton", "Tower Hamlets", "Waltham Forest", "Wandsworth",
          "Westminster" ]
    for quartier in liste_quartier:
        df_quartier_temp = gpd.read_file("data/quartiers/" + quartier + ".json")
        if len(df_quartier)==0 :
            df_quartier = df_quartier_temp
        else :
            df_quartier = pd.concat([df_quartier, df_quartier_temp], ignore_index=True)
    df_quartier.crs = "EPSG:7406"
    return df_quartier


@st.cache_data
def charge_geodata_stations():
    df_stations = gpd.read_file("data/stations.csv")
    df_stations = gpd.GeoDataFrame(df_stations, geometry=gpd.points_from_xy(df_stations.longitude, df_stations.latitude))
    df_stations['borough'] = df_stations['borough'].str.replace('&nbsp;','')
    df_stations.crs = "EPSG:7406"
    return df_stations


@st.cache_data
def charge_geodata_interventions(df_incident):
    bng = 'epsg:27700'
    wgs84 ='epsg:7406'
    geo_data_pd = df_incident[['IncidentNumber','IncidentGroup','CalYear', 'Easting_rounded', 'Northing_rounded', 'Latitude', 'Longitude']].copy()#.sample(10000)
    eastings = geo_data_pd['Easting_rounded']
    northings = geo_data_pd['Northing_rounded']
    transformer = Transformer.from_crs(bng, wgs84)
    res_list_en = transformer.transform(eastings, northings)
    
    geo_data_pd['latitude_rounded']=  res_list_en[0]
    geo_data_pd['longitude_rounded']=  res_list_en[1]
    
    
    geo_data_pd['Latitude'].fillna(geo_data_pd['latitude_rounded'], inplace=True) 
    geo_data_pd['Longitude'].fillna(geo_data_pd['latitude_rounded'], inplace=True) 
    
    geo_data_gpd = gpd.GeoDataFrame(geo_data_pd, geometry=gpd.points_from_xy(geo_data_pd.longitude_rounded, geo_data_pd.latitude_rounded))

    # Il y a 1 point très loin au nord ->> suppression car certainement une erreur de saisie logiciel
    geo_data_gpd = geo_data_gpd[geo_data_gpd['Latitude']<51.8]
    return geo_data_gpd
    

@st.cache_resource   
def merge_df(df1,df2, the_left_on, the_right_on, the_how ):
    return pd.merge(df1,df2,left_on=the_left_on,right_on=the_right_on,how=the_how)


@st.cache_resource   
def merge_df_vehicule(df1,df2, the_left_on, the_right_on, the_how ):
    df1['Resource_Code_vehicule'] = df1['Resource_Code'].apply(lambda x:str(x)[3:])
    return pd.merge(df1,df2,left_on=the_left_on,right_on=the_right_on,how=the_how)