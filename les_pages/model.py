# -*- coding: utf-8 -*-

import streamlit as st
import commun
import pandas as pd
from datetime import datetime


mem_usage_text = st.sidebar.empty()


st.title("Projet des temps de déplacment des pompiers de Londre")
st.sidebar.title("Sommaire")
pages=["Nettoyage", "preprocessing", "Modélisation"]
page=st.sidebar.radio("Sommaire", pages)

#Chargement des dataframes
df_incident = commun.charge_data_incident()
df_mob = commun.charge_data_mobilisation()
df_vehicule = commun.charge_data_vehicule()
df_calend = commun.charge_data_calendrier()
df_stations = commun.charge_geodata_stations()

#################################################################################################################################
# #Nettoyage jeu de données Mobilisation
#################################################################################################################################

###########################################
##### Supression des colonnes inutiles ####
###########################################
df_mob_cleaned = df_mob.drop(['CalYear','HourOfCall','ResourceMobilisationId','PerformanceReporting',
                                  'DateAndTimeMobile','DateAndTimeArrived','DateAndTimeLeft',
                                  'DateAndTimeReturned','PumpOrder','PlusCode_Code',
                                  'PlusCode_Description','DelayCodeId','DelayCode_Description'],axis=1)
###########################
#### Création variable ####
###########################

# Création d'une colonne "DateMobilised" à partir de la colonne "DateAndTimeMobilised"
df_mob_cleaned['DateMobilised']=df_mob_cleaned['DateAndTimeMobilised'].str.split(' ', expand=True)[0]

#### conversion format date ####
# Convertir la colonne "DateAndTimeMobilised" au format Date Heure
df_mob_cleaned['DateAndTimeMobilised']=pd.to_datetime(df_mob_cleaned['DateAndTimeMobilised'], format='%d/%m/%Y %H:%M:%S')


#### Séparation colonne 'Resource_Code' ####
df_mob_cleaned['VehicleFromStation_Code'] = df_mob_cleaned['Resource_Code'].str[:3]
df_mob_cleaned['ID_Vehicle'] = df_mob_cleaned['Resource_Code'].str[-1]
# Déplacement des colonnes
colonne_1 = df_mob_cleaned.pop('VehicleFromStation_Code')
colonne_2 = df_mob_cleaned.pop('ID_Vehicle') 
colonne_3 = df_mob_cleaned.pop('DateMobilised')
# Réinsertion à l'index 2, 3 et 4
df_mob_cleaned.insert(2, 'VehicleFromStation_Code', colonne_1)  
df_mob_cleaned.insert(3, 'ID_Vehicle', colonne_2)
df_mob_cleaned.insert(4, 'DateMobilised', colonne_3)                                
# Supression de la colonne 'Resource_Code'
df_mob_cleaned = df_mob_cleaned.drop(['Resource_Code'],axis=1)

###########################################
#### Suppression des lignes manquantes ####
###########################################

#### Suppression des lignes dont la variable 'DeployedFromStation_Code' est manquante ####
df_mob_cleaned = df_mob_cleaned.dropna(subset=['DeployedFromStation_Code'])

############################################
#### Remplissage des valeurs manquantes ####
############################################

#### Remplissage des valeurs manquantes de la variable 'DeployedFromLocation' ####
df_mob_cleaned['DeployedFromLocation'] = df_mob_cleaned['DeployedFromLocation'].fillna(
    df_mob_cleaned.apply(lambda row: 'Home Station' if row['VehicleFromStation_Code'] == row['DeployedFromStation_Code'] else 'Other Station', axis=1))

st.write("Données mobilisation nettoyées")
st.dataframe(df_mob_cleaned.sample(5))


#################################################################################################################################
# #Nettoyage jeu de données incidents
#################################################################################################################################
###########################################
##### Supression des colonnes inutiles ####
###########################################
df_incident_cleaned = df_incident.drop(['CalYear','IncidentGroup','StopCodeDescription','SpecialServiceType',
                                  'PropertyType','AddressQualifier','Postcode_full',
                                  'Postcode_district','UPRN','USRN','IncGeo_BoroughCode',
                                  'IncGeo_BoroughName','IncGeo_WardCode','IncGeo_WardName','Easting_m',
                                  'Northing_m','FRS','FirstPumpArriving_AttendanceTime',
                                  'FirstPumpArriving_DeployedFromStation','SecondPumpArriving_AttendanceTime',
                                  'SecondPumpArriving_AttendanceTime','SecondPumpArriving_DeployedFromStation',
                                  'NumStationsWithPumpsAttending','NumPumpsAttending','PumpCount',
                                 'Notional Cost (£)','NumCalls'],axis=1)

# Fonction pour convertir une date de type "01 Jan 2009" au format "01/01/2009"
def convert_date(date_string):
    '''
    Fonction permettant de convertir le fomat d'une date de type 01 Jan 2009
    en 01/01/2009
    '''
    date = datetime.strptime(date_string, "%d %b %Y")
    return date.strftime("%d/%m/%Y")

# Appliquer la fonction à la colonne 'DateOfCall' du DataFrame
df_incident_cleaned['DateOfCall'] = df_incident_cleaned['DateOfCall'].apply(convert_date)

# Concaténer les deux colonnes avec un espace entre elles
df_incident_cleaned['DateTimeOfCall'] = df_incident_cleaned.apply(lambda row: row['DateOfCall'] + ' ' + row['TimeOfCall'], axis=1)

# Convertir la colonne "DateTimeOfCall" au format Date Heure dans la colonne "DateTimeOfCall"
df_incident_cleaned['DateTimeOfCall']=pd.to_datetime(df_incident_cleaned['DateTimeOfCall'], format='%d/%m/%Y %H:%M:%S')

# Déplacement des colonnes
colonne_1 = df_incident_cleaned.pop('DateTimeOfCall')
# Réinsertion à l'index 2
df_incident_cleaned.insert(3, 'DateTimeOfCall', colonne_1)  


st.write("Données incidents nettoyées")
st.dataframe(df_incident_cleaned.sample(5))

df_merged_mobil_incid = pd.merge(df_mob_cleaned, df_incident_cleaned, left_on='IncidentNumber', right_on='IncidentNumber', how='left')
st.write("Données fusionnées")
st.dataframe(df_mob_cleaned.sample(5))



# df_merged_mobil_incid[df_merged_mobil_incid['Northing_rounded'].isna()]




    
####################################################
# conso memoire
####################################################
commun.conso_memoire(mem_usage_text)    
####################################################