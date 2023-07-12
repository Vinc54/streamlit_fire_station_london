import pandas as pd
import streamlit as st

years = [2022,2023]
years_string = "2022,2023"

url_incident="https://data.london.gov.uk/download/london-fire-brigade-incident-records/73728cf4-b70e-48e2-9b97-4e4341a2110d/LFB%20Incident%20data%20-%20Datastore%20-%20with%20notional%20cost%20and%20UPRN%20from%20January%202009.zip"
#url_incident="incident.csv"
@st.cache_data
def charge_data_incident():
    df = pd.read_csv(url_incident, compression='zip', low_memory=False)
    df = df[df.CalYear.isin(years)]
    return df

url_mobilisation="https://data.london.gov.uk/download/london-fire-brigade-mobilisation-records/fcbd2e97-b5bf-4117-a50f-d596181bc8d3/LFB%20Mobilisation%20data%20from%20January%202009.zip"
#url_mobilisation="mobilisation.csv"
@st.cache_data
def charge_data_mobilisation():
    df = pd.read_csv(url_mobilisation, compression='zip', low_memory=False)
    df = df[df.CalYear.isin(years)]
    return df

@st.cache_data
def charge_data_vehicule():
    return pd.read_csv(r"T_VehicleType.csv", sep=';')

@st.cache_resource   
def merge_df(df1,df2, the_left_on, the_right_on, the_how ):
    return pd.merge(df1,df2,left_on=the_left_on,right_on=the_right_on,how=the_how)


@st.cache_resource   
def merge_df_vehicule(df1,df2, the_left_on, the_right_on, the_how ):
    df1['Resource_Code_vehicule'] = df1['Resource_Code'].apply(lambda x:str(x)[3:])
    return pd.merge(df1,df2,left_on=the_left_on,right_on=the_right_on,how=the_how)