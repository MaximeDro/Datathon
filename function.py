
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib as plt
from sklearn.neighbors import KNeighborsClassifier

# ################################# MACHINE LEARNING ############################
def KNN_pays(df, country) : #Fonctionne avec le dataset merge
    X = df.drop(df[df["Country"] == "World"].index)[['Latitude (average)','Longitude (average)']]
    y = df.drop(df[df["Country"] == "World"].index)['ISO3']
    modelKNN_pays = KNeighborsClassifier(n_neighbors=6).fit(X,y)
    liste_voisin = list(df.drop(df[df["Country"] == "World"].index)['Country'].iloc[modelKNN_pays.kneighbors(df[df['Country'] == country][['Latitude (average)','Longitude (average)']])[1][0]])
    return liste_voisin 

liste_pays = ['Djibouti',
 'Eritrea, The State of',
 'Ethiopia, The Federal Dem. Rep. of',
 'Yemen, Rep. of',
 'Somalia',
 'Kenya']
####### TEST #########""
def get_salut():
    st.write("Salut")

################################# FUNCTION ####################################
def get_temp_by_country_nan_opti(df, country):
    dico_year_temp = {}
    temperature = 0
    for i in range(10, len(df.columns)-2):
        # Si la température est un Nan
        if pd.isna(df.loc[df['Country'] == country, df.columns[i]].iloc[0]):
            # Récupération des pays voisins



            # voisins = liste_pays # ATTENTION TEMPORAIRE en attendant le ML
            voisins = KNN_pays(df, country)


            # voisins = df.drop(df[df["Country"] == "World"].index)['Country'].iloc[modelKNN_pays.kneighbors(df[df['Country'] == country][['Latitude (average)','Longitude (average)']])[1][0]]
            # Récupération de la moyenne température de cette année pour ces pays voisins (en enlevant les Nan)
            df_selected_countries = df[df['Country'].isin(voisins)].iloc[:,i]
            temperature = round(np.nanmean(df_selected_countries),3)
        else :
            # On prend la température du pays demandé
            temperature = float(df[df['Country'] == country].iloc[:,i])
        # Implémentation du dictionnaire
        dico_year_temp[int(df.columns[i].replace("F",""))] = temperature

    return dico_year_temp # Si on veut récupérer les données thermique




##############################################################################
def get_gazes_by_iso_code(df,country):

    dico_year_co2 = {}
    dico_year_CH4 = {}
    dico_year_N2O = {}
    for i in range(1, len(df[df['country'] == country])):
        # CO2
        dico_year_co2[df[df['country'] == country]['year'].iloc[i]] = df[df['country'] == country]['co2'].iloc[i]
        # methane            
        dico_year_CH4[df[df['country'] == country]['year'].iloc[i]] = df[df['country'] == country]['methane'].iloc[i]
    # for i in range(1, len(df[df['country'] == country])):
        # nitrous_oxide 
        dico_year_N2O[df[df['country'] == country]['year'].iloc[i]] = df[df['country'] == country]['nitrous_oxide'].iloc[i]
               
    
    # for i in range(1, len(df[df['country'] == country])):
        

    # On retourne une liste de dictionnaire
    return [dico_year_co2,dico_year_CH4,dico_year_N2O]

