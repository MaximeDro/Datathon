
# python -m venv env
# Set-ExecutionPolicy Unrestricted -Scope Process 
# Si la ligne ci-dessous ne veut pas s'exécuter
# env\Scripts\activate
# puis on peut faire nos pip install (nota pour sklearn : pip install -U scikit-learn)
# Pour executer le streamlit :
# streamlit run .\streamlit_datathon.py 
# quète streamlit : https://odyssey.wildcodeschool.com/quests/1627

############################### IMPORTATION ###############################
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import function 
from sklearn.neighbors import KNeighborsClassifier
from pathlib import Path
import nltk
import spacy
from wordcloud import WordCloud

nltk.download('popular')

######################################################################
############################### PAGE 1 ###############################

# Fonction pour la page 1
def menu():
    st.markdown("<h1 style='text-align: center;'>Welcome everybody</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>We are here to talk about the Global Warming! </h2>", unsafe_allow_html=True)
######################################################################
############################### PAGE 1 ###############################

# Fonction pour la page 1
def page1():

############################### CONTENT ###############################
    st.markdown("<h1 style='text-align: center;'>No change</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Global warming is a myth! </h2>", unsafe_allow_html=True)
      
    
    st.write("**Climato-skeptic:** a person who is not convinced that global warming is occurring, or that it is due to human activity.") 
    st.write("First of all, we will try to show you that global warming is a fact.")

    df_temperature = pd.read_csv("Data_Temperature_Country.csv")
    
############################### CELLULE TEXTE : SELECTION COUNTRY ###############################
    st.write("To discover that global warming is a fact. We propose you to look the evolution of the temperature in the world wide.")

    # Créer une cellule de saisie de texte avec les noms de pays comme options
    default_value_index = list(df_temperature['Country']).index("World")
    country_name = st.selectbox('Select a country:', list(df_temperature['Country']), index=default_value_index)
    
    if country_name != "World":
        function.KNN_pays(df_temperature, country_name)

############################### GRAPHIQUE : TEMPERATURE FUNCTION OF COUNTRY ###############################
    Temperature_country = sns.lineplot(x = function.get_temp_by_country_nan_opti(df_temperature, country_name).keys(),
                                y = function.get_temp_by_country_nan_opti(df_temperature, country_name).values() 
                                    )
    level_0 = sns.lineplot(x = function.get_temp_by_country_nan_opti(df_temperature, country_name).keys(), y = 0)
    plt.xlabel('Year')
    plt.ylabel('Temperature change [°C]')
    plt.title(f'Surface temperature change mean in {country_name}')
    st.pyplot(Temperature_country.figure)

    st.write("Nota: For some countries, informations were missing. To complete it, we take the mean of the neighboring countries.")

    st.write(f"In 2022, the temperature of {country_name} has improve of {float(df_temperature[df_temperature['Country'] == country_name]['F2022'])}°C since 1961. ")
    st.write("As you can see it is not a local phenomena. The global warming is a fact. Now we will show you that it is strongly linked with the human activity.")

######################################################################
############################### PAGE 2 ###############################
def page2():
    st.markdown("<h1 style='text-align: center; '>Not us</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; '>It's the others' fault! </h2>", unsafe_allow_html=True)
    
    st.write("**Never my fault:** When it is never our fault, it is because we lack the self-confidence to shoulder responsibility. This attitude reflects narcissistic fragility and a lack of confidence.")

    st.markdown("<h2 style='text-align: left; '>Global warming causes: </h2>", unsafe_allow_html=True)
    st.write("When greenhouse gas emissions multiply, they act like a blanket around the Earth, trapping the sun's heat. This leads to global warming and climate change.")
    st.write("The CO2 produced by human activities is the main cause of global warming.")

    st.markdown("<h2 style='text-align: left; '>Greenhouse gas emissions: </h2>", unsafe_allow_html=True)
    st.write("There are different types of greenhouse gas, and their global warming potential varies. Gases naturally present in the atmosphere, but also generated by human activities, include: carbon dioxide (CO2), methane (CH4), nitrous oxide (N2O)...")

    df_gazes = pd.read_csv("Data_Gazes_Country.csv")

    
    st.write("To learn more about the emission of these gazes. We propose you to look the evolution of their emissions around the world.")
    # Créer une cellule de saisie de texte avec les noms de pays comme options
    default_value_index = list(set(df_gazes['country'])).index("World")
    country_name = st.selectbox('Select a country:', list(set(df_gazes['country'])), index=default_value_index)

    liste_gazes = function.get_gazes_by_iso_code(df_gazes,country_name)
    ######### GRAPHIQUE EMISSIONS
    fig, axes = plt.subplots(ncols = 3, figsize = [15,5])
    sns.lineplot(x = liste_gazes[0].keys(), 
                 y = liste_gazes[0].values(), 
                 ax = axes[0],
                 c = 'orange')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('CO2 Emissions')
    axes[0].set_title(f'CO2 Emissions in {country_name}')

    sns.lineplot(x = liste_gazes[1].keys(), 
                 y = liste_gazes[1].values(), 
                 ax = axes[1],
                 c = 'green')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('CH4 Emissions')
    axes[1].set_title(f'CH4 Emissions in {country_name}')

    sns.lineplot(x = liste_gazes[2].keys(), 
                 y = liste_gazes[2].values(), 
                 ax = axes[2],
                 c = 'red')
    axes[2].set_xlabel('Year')
    axes[2].set_ylabel('N2O Emissions')
    axes[2].set_title(f'N2O Emissions in {country_name}')
    st.pyplot(fig)

    ################ GRAPHIQUE TEMPERATURE 
    df_temperature = pd.read_csv("Data_Temperature_Country.csv")
    
    # Récupération du nom du pays au format de df_temperature
    if country_name == 'World':
        country_name_temp = country_name
    else :
        code_iso = df_gazes[df_gazes['country'] == country_name]['iso_code'].iloc[0]
        country_name_temp = df_temperature[df_temperature['ISO3'] == code_iso]['Country'].iloc[0]

    fig, axes = plt.subplots(figsize = [15,5])
    sns.lineplot(x = function.get_temp_by_country_nan_opti(df_temperature, country_name_temp).keys(),
                y = function.get_temp_by_country_nan_opti(df_temperature, country_name_temp).values())
    plt.xlabel('Year')
    plt.ylabel('Temperature change [°C]')
    plt.title(f'Surface temperature change mean in {country_name}')
    st.pyplot(fig)
    
    st.write("An increase in greenhouse gases due to human activity traps some of this radiation, causing surface temperatures to rise until a new equilibrium is reached. This is the main cause of global warming in recent decades.")
    st.write("Carbon dioxide (CO2) and methane (CH4) account for 90% of greenhouse gas emissions caused by human activities. The combustion of fossil fuels such as coal, oil and natural gas for energy production is the main source of these emissions, to which are added contributions from agriculture, deforestation and industry. There is scientific consensus on the human cause of climate change.")
######################################################################
############################### PAGE 3 ###############################
def page3():
    st.title("GIEC report")
    st.write("We have analyzed for you the GEIC's report to highlight the main topics.")
    texte_giec = Path("GIEC_report.txt").read_text().replace("\n", " ")
    
    # Création des tokens en mots
    tokens = nltk.word_tokenize(texte_giec.lower())
    # Nettoyage stopwords et ponctuation
    tokens_clean = []
    for words in tokens:
        if (words not in nltk.corpus.stopwords.words("english")) and (words.isalpha() == True ):
            tokens_clean.append(words)
    
    # python -m spacy download en_core_web_sm # pour télécharger le module
    nlp = spacy.load('en_core_web_sm')

############ nuage de mot ############
    
    # Création du nuage de 
    wordcloud = WordCloud(width=2000, height=2000, max_font_size=400, min_font_size=1)
    lemm_tokens = nlp(' '.join(tokens_clean))
    dico_word = nltk.FreqDist([token.lemma_ for token in lemm_tokens])
    wordcloud= WordCloud(background_color='#0e1117').generate_from_frequencies(dico_word)

    plt.figure(figsize=(20, 20))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.show()

    # Enregistrer l'image du nuage de mots dans un fichier temporaire
    image_file = "wordcloud_temp_file.png"
    plt.savefig(image_file, bbox_inches="tight", pad_inches=0)
    plt.close()
    # Afficher le nuage de mots dans Streamlit en utilisant st.image
    st.image(image_file)

######################################################################
############################### PAGE 4 ###############################
def page4():
    st.title("Futur")
    st.write("Incomming")
    st.write("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.write("Sources:")
    st.write("https://climatedata.imf.org/")
    st.write("https://www.ecologie.gouv.fr/comprendre-giec")    
    st.write("https://datahub.io/collections/climate-change")
    st.write("https://data.world/datasets/global-warming")
    st.write("Article updated 20/12/2023")
    st.write("Author: Geraldo del rive")

############################################################################
############################### SIDEBAR MENU ###############################
# Menu de navigation dans la sidebar
menu_selection = st.sidebar.radio("Menu", ("Accueil","1.No change", "2.Not us", "3.Words are better than number", "4.Futur"))

# Conteneurs vides pour charger le contenu des pages
container = st.empty()

# Gérer les sélections du menu pour afficher le contenu approprié
if menu_selection == "Accueil":
    menu()
if menu_selection == "1.No change":
    page1()
elif menu_selection == "2.Not us":
    page2()
elif menu_selection == "3.Words are better than number":
    page3()
elif menu_selection == "4.Futur":
    page4()

