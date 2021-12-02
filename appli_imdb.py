import streamlit as st
import numpy as np
import pandas as pd
import time


data_films = pd.read_csv("films.csv")
data_series = pd.read_csv("series.csv")

mask_genre_film = mask_acteur_film = mask_duree_film = mask_note_film = pd.Series(True, index=data_films.index)
mask_genre_serie = mask_acteur_serie = mask_duree_serie = mask_nb_episodes = mask_note_serie = pd.Series(True, index=data_series.index)

#---NETTOYAGE---

#NETTOYAGE ACTEURS FILMS
acteurs_films = data_films['Acteurs'].fillna("Inconnus").str.split(',').explode()
acteurs_films_liste = acteurs_films.sort_values()

def removeduplicates(acteurs_liste_film):
    liste_unique_acteurs_film = []
    for actor in acteurs_liste_film:
        if actor not in liste_unique_acteurs_film:
            liste_unique_acteurs_film.append(actor)

    return liste_unique_acteurs_film


#NETTOYAGE ACTEURS SERIES
acteurs_series = data_series['Acteurs'].fillna("Inconnus").str.split(',').explode()
acteurs_series_liste = acteurs_series.sort_values()

def removeduplicates(acteurs_liste_serie):
    liste_unique_acteurs_serie = []
    for actor in acteurs_liste_serie:
        if actor not in liste_unique_acteurs_serie:
            liste_unique_acteurs_serie.append(actor)

    return liste_unique_acteurs_serie

#NETTOYAGE DUREE FILMS
temp_film = data_films['Durée'].str.replace(",","")
temp_film = temp_film.str.replace(" ","")
heure_film = temp_film.str.extract(r'(\d+)h')
minutes_film = temp_film.str.extract(r'(\d+)m')
heure_film = heure_film.astype('float', errors='ignore')
minutes_film = minutes_film.astype('float', errors='ignore')
data_films['time_cleaned'] = heure_film * 60 + minutes_film

#NETTOYAGE DUREE SERIES
temp_serie = data_series['Durée'].str.replace(",","")
temp_serie = temp_serie.str.replace(" ","")
heure_serie = temp_serie.str.extract(r'(\d+)h')
minutes_serie = temp_serie.str.extract(r'(\d+)m')
heure_serie = heure_serie.astype('float', errors='ignore')
minutes_serie = minutes_serie.astype('float', errors='ignore')
data_series['time_cleaned'] = minutes_serie

#---PRESENTATION APP---

#HAUT DE PAGE
st.title("- Appli Ciné/Séries IMDB -")

#ACCROCHE + LOGO
st.subheader("Parmi les 250 meilleurs films et séries...")

from PIL import Image 
img = Image.open("image.jpg") 
st.image(img, width=500) 

st.subheader("Trouvez le programme qui VOUS convient !")

#DEUX COLONNES
left_column, right_column = st.columns(2)

#LEFT COLUMN = LISTE FILMS
left_column.header("250 meilleurs films")
if left_column.checkbox('Montrer la liste des films'):
    titre_films = data_films['Titre']
    left_column.dataframe(titre_films, width=None, height=None)

#RIGHT COLUMN = LISTE SERIES
right_column.header("250 meilleures séries")
if right_column.checkbox('Montrer la liste des séries'):
    titre_series = data_series['Titre']
    right_column.dataframe(titre_series, width=None, height=None)

#---SIDEBAR FILMS---

st.sidebar.subheader("RECHERCHER UN FILM")
st.sidebar.text("Choix par :")

#CRITERE TITRE
if st.sidebar.checkbox('Titre du film'):
    titre_films = data_films['Titre'].sort_values()
    data_filtered = st.container()
    titre_film_choisi = st.sidebar.selectbox(
        'Titre du film : ',
        (titre_films)
    )
    with data_filtered :
        mask_to_display = data_films['Titre'] == titre_film_choisi
    st.success("RESULTAT - Voici les détails du film concerné :")
    st.dataframe(data=data_films[mask_to_display])

#CRITERE GENRE
if st.sidebar.checkbox('Genre du film'):
    data_filtered = st.container()
    genre_choisi = st.sidebar.selectbox(
        'Genre de film recherché',
        ["Action","Adventure","Animation","Biography","Comedy","Crime","Drama","Family","Fantasy","Horror","Music","Mystery","Romance","Sci-Fi","Thriller","War","Western"],
        )
    with data_filtered :
        mask_genre_film = data_films['Genre'].str.contains(genre_choisi)

#CRITERE ACTEURS
if st.sidebar.checkbox('Acteur/Actrice du film'):
    data_filtered = st.container()
    acteur_film = st.sidebar.selectbox(
        'Acteur/Actrice du film recherché',
        (removeduplicates(acteurs_films_liste)),
        )
    with data_filtered :
        mask_acteur_film = data_films['Acteurs'].str.contains(acteur_film)


#CRITERE DUREE
if st.sidebar.checkbox('Durée du film'):
    data_filtered = st.container()
    duree_max_films = st.sidebar.number_input('Mettre la durée maximale (en minutes)',max_value=360, value=120, step=10, help='Une heure = 60 minutes')
    with data_filtered :
        mask_duree_film = data_films['time_cleaned'] < duree_max_films


#CRITERE NOTES
if st.sidebar.checkbox('Note du film'):
    data_filtered = st.container()
    note_min_films = st.sidebar.number_input('Mettre la note minimale',max_value=10.0,value=9.0,step=0.1)
    with data_filtered :
        mask_note_film = data_films['Note'] >= note_min_films


#BOUTTON DE RECHERCHE
if st.sidebar.button('Recherchez mon film !'):
    
    resultat_films = data_films[mask_genre_film & mask_acteur_film & mask_duree_film & mask_note_film]
    with st.spinner('Recherche en cours...'):
        time.sleep(3)
    st.success("RESULTAT - Voici la liste des films concernés :")
    st.dataframe(data=resultat_films)
    st.write("Soit un total de",len(resultat_films),"films.")


#---SIDEBAR SERIES---
st.sidebar.subheader("RECHERCHER UNE SERIE")
st.sidebar.text("Choix par :")

#CRITERE TITRE
if st.sidebar.checkbox('Titre de la série'):
    titre_series = data_series['Titre'].sort_values()
    titre_serie_choisie = st.sidebar.selectbox(
        'Titre de la série : ',
        (titre_series)
    )
    mask_serie = data_series['Titre'] == titre_serie_choisie
    new_data_series = data_series[mask_serie]
    st.success("RESULTAT - Voici les détails de la série concernée :")
    st.write(new_data_series)

#CRITERE GENRES
if st.sidebar.checkbox('Genres de la série'):
    data_filtered = st.container()
    genre_select = st.sidebar.selectbox(
        'Genres de série recherchée',
        ["Action","Adventure","Animation","Biography","Comedy","Crime","Drama","Family","Fantasy","Horror","Music","Mystery","Romance","Sci-Fi","Thriller","War","Western"],
        )
    with data_filtered :
        mask_genre_serie = data_series['Genre'].str.contains(genre_select)

#CRITERE ACTEURS
if st.sidebar.checkbox('Acteur/Actrice de la série'):
    data_filtered = st.container()
    acteur_serie = st.sidebar.selectbox(
        'Acteur/Actrice de série recherchée',
        (removeduplicates(acteurs_series_liste)),
        )
    with data_filtered :
        mask_acteur_serie = data_series['Acteurs'].str.contains(acteur_serie)

#CRITERE DUREE
if st.sidebar.checkbox("Durée moyenne d'un épisode"):
    data_filtered = st.container()
    duree_max_series = st.sidebar.number_input('Mettre la durée maximale (en minutes)',max_value=180, value=55, step=5, help='Une heure = 60 minutes')
    with data_filtered :
        mask_duree_serie = data_series['time_cleaned'] < duree_max_series

#CRITERE NOMBRE EPISODES
if st.sidebar.checkbox("Nombre d'épisodes total"):
    data_filtered = st.container()
    episodes_max_series = st.sidebar.number_input("Mettre le nombre maximum d'épisodes",min_value=1, value=50)
    with data_filtered :
        mask_nb_episodes = data_series["Nombre d'épisodes"] < episodes_max_series

#CRITERE NOTES
if st.sidebar.checkbox('Note de la série'):
    data_filtered = st.container()
    note_min_series = st.sidebar.number_input('Mettre la note minimale',max_value=10.0,value=8.0,step=0.1)
    with data_filtered :
        mask_note_serie = data_series['Note'] >= note_min_series


#BOUTTON DE RECHERCHE
if st.sidebar.button('Recherchez ma série !'):

    resultat_series = data_series[mask_genre_serie & mask_acteur_serie & mask_duree_serie & mask_nb_episodes & mask_note_serie]
    with st.spinner('Recherche en cours...'):
        time.sleep(3)
    st.success("RESULTAT - Voici la liste des séries concernées :")
    st.dataframe(data=resultat_series)
    st.write("Soit un total de",len(resultat_series),"séries.")

