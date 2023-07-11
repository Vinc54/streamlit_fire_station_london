# -*- coding: utf-8 -*-

import streamlit as st


st.title("Projet des temps de déplacment des pompiers de Londre")
st.sidebar.title("Exploration")
pages=["Exploration", "DataVizualization", "Modélisation"]
page=st.sidebar.radio("Sommaire", pages)

