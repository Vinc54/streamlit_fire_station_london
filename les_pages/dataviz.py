# -*- coding: utf-8 -*-
import commun
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df_incident = commun.charge_data_incident()
df_mob = commun.charge_data_mobilisation()
df_vehicule = commun.charge_data_vehicule()
df=commun.merge_df(df_incident,df_mob, 'IncidentNumber', 'IncidentNumber', 'left' )
df=commun.merge_df_vehicule(df,df_vehicule, 'Resource_Code_vehicule', 'Id_VehicleType', 'left' )

#st.title("Projet des temps de déplacement des pompiers de Londre")
st.sidebar.title("Data visualisation")
pages=["Généralité", "Analyses temporelles", "Utilisation des véhicules", "Temps de prépatations et de déplacement"]
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
    
    > Prévoir une classification en 2 groupes pour le model de prédiction :
    > * 1 groupe entre 22h et 6h
    > * 1 groupe entre 7h et 21h
    ***
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
    
    fig = plt.figure()
    df_mediane_attendancetime = df.groupby(['ProperCase'], as_index = False).agg({'AttendanceTimeSeconds':'median'}).sort_values(by ='AttendanceTimeSeconds' ,ascending = False)
    #display(df_mediane_attendancetime.sort_values(by ='AttendanceTimeSeconds' ,ascending = False))
    plot = sns.catplot(x='ProperCase', y='AttendanceTimeSeconds', data=df_mediane_attendancetime, kind='bar', height = 4, aspect=2);
    plt.xticks(rotation=90);
    plt.title("Analyse du temps de préparation par rapport aux arrondissements") 
    st.pyplot(plot.fig)
    st.markdown(
    """
    Il peut y avoir jusqu'à 2 minutes d'écart entre deux arrondissements
    La variable catégorielle arrondissements est donc à garder pour affiner nos analyses
    """
    )
    
    
    fig = plt.figure()
    df_mediane_attendancetime = df.groupby(['DeployedFromStation_Name'], as_index = False).agg({'AttendanceTimeSeconds':'median'}).sort_values(by ='AttendanceTimeSeconds' ,ascending = False)
    #display(df_mediane_attendancetime.sort_values(by ='AttendanceTimeSeconds' ,ascending = False))
    plot = sns.catplot(x='DeployedFromStation_Name', y='AttendanceTimeSeconds', data=df_mediane_attendancetime, kind='bar', height = 4, aspect=2);
    plt.xticks(rotation=90, size = 5);
    st.pyplot(plot.fig)
    st.markdown(
    """
    Il peut y avoir de grosses disparités entre les stations.
La variable catégorielle "DeployedFromStation_Name" est donc à garder pour affiner nos analyses
    """
    )
    
    
if page == pages[2] : 
    st.write("### Analyse de l'usage des types de véhicule par typologie d'incident")

    df_count_vehicule = df.groupby(['VehicleType']).count()
    #st.dataframe(df_count_vehicule.head())
    col1, col2 = st.columns([3, 1])
    with col1:
        fig = plt.figure(figsize=(2,2))
        plot = plt.pie(df_count_vehicule.IncidentNumber, labels = df_count_vehicule.index,  autopct = '%1.0f%%', textprops={'fontsize': 6})
        plt.title("Répartition d'utilisation des véhicules", fontsize=5);
        st.pyplot(fig) 
    
    
    
    fig1 = plt.figure(figsize = (10, 7)) 
    ax1 = plt.subplot(121) 
    df_graph = df[df['VehicleType'] == 'Dual Pump Ladder'].groupby(['IncidentGroup']).count()
    #st.dataframe(df_graph.head())
    plot = plt.pie(df_graph.IncidentNumber, labels = df_graph.index,  autopct = '%1.0f%%', textprops={'fontsize': 10})
    plt.title("Utilisation du 'Dual Pump Ladder' par type d'accident", fontsize=12) 
    
    st.markdown(
    """
    Nous constatons que dans notre dataframe, nous n'avons que deux types de véhicule alors qu'il existe jusqu'à 10 type de véhicules mobilisables
    
    Nous utilisons pour les 2/3 des incidents un "Dual Pump Ladder", regardons s'il y a une corrélation avec la typologie d'incident
    """
    )
    
    ax2 = plt.subplot(122) 
    df_graph = df[df['VehicleType'] == 'Pump'].groupby(['IncidentGroup']).count()
    #st.dataframe(df_graph.head())
    plot = plt.pie(df_graph.IncidentNumber, labels = df_graph.index,  autopct = '%1.0f%%', textprops={'fontsize': 10})
    plt.title("Utilisation du 'Pump' par type d'accident", fontsize=12);
    
    st.pyplot(fig1) 
    
    st.markdown(
    """
    Nous constatons que peu importe la typologie d'incident, la répartition d'utilisation du type de véhicule est identique.
    """
    )
    
    
if page == pages[3] : 
    st.write("### Analyse des temps de préparation et de déplacement")   
   
    col1, col2 = st.columns([20, 1])
    with col1:
        fig2 = plt.figure(figsize = (15, 10)) 

        plt.subplot(221) 
        sns.boxenplot(x="IncidentGroup", y="TurnoutTimeSeconds", data=df)
        plt.ylim([1,500])
        plt.xticks(rotation = 45)
        plt.xlabel("Type d'incident") 
        plt.ylabel("Temps de préparation") 
        plt.title('Analyse du temps de préparation par type d\'accident')
        
        plt.subplot(222) 
        sns.boxenplot(x="IncidentGroup", y="TravelTimeSeconds", data=df)
        plt.ylim([1,800])
        plt.xticks(rotation = 45)
        plt.xlabel("Type d'incident") 
        plt.ylabel("Temps de transport") 
        plt.title("Analyse du temps de transport par type d'incident")
        
        plt.subplot(223) 
        sns.boxenplot(x="VehicleType", y="TurnoutTimeSeconds", data=df)
        plt.ylim([1,500])
        plt.xticks(rotation = 45)
        plt.xlabel("Type de véhicule") 
        plt.ylabel("Temps de préparation") 
        plt.title('Analyse du temps de préparation par Type de véhicule')
        
        plt.subplot(224) 
        sns.boxenplot(x="VehicleType", y="TravelTimeSeconds", data=df)
        plt.ylim([1,800])
        plt.xticks(rotation = 45)
        plt.xlabel("Type de véhicule") 
        plt.ylabel("Temps de transport") 
        plt.title('Analyse du temps de transport par Type de véhicule');
        
        fig2.tight_layout()
        
        st.pyplot(fig2) 
        
        st.markdown(
        """
        Nous constatons que peu importe le type de véhicule ou le type d'incident, cela ne semble pas influer sur les temps de préparation ou de transport, nous pouvons considérer que ce sont des variables explicatives peu pertinentes dans le cadre de l'apprentissage du machine learning
        """
        )
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    