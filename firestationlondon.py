import commun
import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages

st.set_page_config(
    page_title="LFB",
    page_icon="🚨",
)
mem_usage_text = st.sidebar.empty()

show_pages(
    [
        Page("firestationlondon.py", "Home", "👨‍🚒"),
        # Can use :<icon-name>: or the actual icon
        Page("les_pages/explore.py", "Exploration des données", "📄"),
        # Since this is a Section, all the pages underneath it will be indented
        # The section itself will look like a normal page, but it won't be clickable
        #Section(name="Analyse des données", icon="📈"),
        # The pages appear in the order you pass them
        Page("les_pages/dataviz.py", "Data visualisation", "📊"),
        Page("les_pages/Mapping.py", "Cartographie", "🌍"),
 
        Page("les_pages/model.py", "Modélisation", "🔣", in_section=False),

    ]
)

add_page_title()  # Optional method to add title and icon to current page


st.title("Temps de Réponse de la Brigade des Pompiers de Londres 🚒")

st.sidebar.success("Introduction")

texte = f"""
    L’objectif de ce projet est d’analyser et/ou d’estimer les temps de réponse et de mobilisation de la Brigade des Pompiers de Londres. La brigade des pompiers de Londres est le service d'incendie et de sauvetage le plus actif du Royaume-Uni  et l'une des plus grandes organisations de lutte contre l'incendie et de sauvetage au monde.
    
    Le premier jeu de données fourni contient les détails de chaque incident traité depuis janvier 2009. Des informations sont fournies sur la date et le lieu de l'incident ainsi que sur le type d'incident traité.

    Le second jeu de données contient les détails de chaque camion de pompiers envoyé sur les lieux d'un incident depuis janvier 2009. Des informations sont fournies sur l'appareil mobilisé, son lieu de déploiement et les heures d'arrivée sur les lieux de l'incident.

    **👈 Selectionnez sur la gauche les différentes étapes** 
    ### <div align="center">⚠️</div>
    
    #### :red[Pour des raison de limitation de la plateforme Streamlit.io (Max 1Go de mémoire), l'analyse est effectuée sur la prériode {commun.years_string} ]*
    *L'analyse complete a été réalisée sur les postes de travail dont le reflet est disponible dans le rapport.
"""


st.markdown(texte,unsafe_allow_html=True)

####################################################
# conso memoire
####################################################
commun.conso_memoire(mem_usage_text)    
####################################################
