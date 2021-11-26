import streamlit as st
import numpy as np
import pandas as pd
import time


data_films = pd.read_csv("films.csv")
data_series = pd.read_csv("series.csv")

mask_duree_film = mask_note_film = pd.Series(True, index=data_films.index)
mask_duree_serie = mask_nb_episodes = mask_note_serie = pd.Series(True, index=data_series.index)

#---NETTOYAGE---

#NETTOYAGE GENRE FILMS
# genre_explode = data_films.explode('Genre',ignore_index=False)
# liste_genres_films = genre_explode['Genre']
# data_films['type_cleaned'] = liste_genres_films

#NETTOYAGE ACTEURS FILMS
acteurs_films = data_films['Acteurs'].fillna("Inconnu").str.split(',').explode()
acteurs_films_liste = acteurs_films.sort_values().tolist()

# liste_explode = data_films.explode('Acteurs',ignore_index=False)
# liste_acteurs_films = liste_explode['Acteurs']
# data_films['casting'] = liste_acteurs_films

#NETTOYAGE ACTEURS SERIES
acteurs_series = data_series['Acteurs'].fillna("Inconnu").str.split(',').explode()
acteurs_series_liste = acteurs_series.sort_values().tolist()

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

#NETTOYAGE PUBLIC FILMS
# temp_public_films = data_films['Public'].str.replace("Tous publics","1")
# temp_public_films = temp_public_films.astype('float',errors='ignore')
# data_films['age_conseille'] = temp_public_films

# #NETTOYAGE PUBLIC SERIES
# temp_public_series = data_series['Public'].str.replace("Tous publics","1")
# temp_public_series = temp_public_series.str.replace("Tous publics avec avertissement","10")
# temp_public_series = temp_public_series.str.replace("TV-G","1")
# temp_public_series = temp_public_series.str.replace("TV-14","14")
# temp_public_series = temp_public_series.str.replace("TV-MA","18")
# temp_public_series = temp_public_series.str.replace("TV-PG","18")
# temp_public_series = temp_public_series.astype('float',errors='ignore')
# data_series['age_conseille'] = temp_public_series

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
if st.sidebar.checkbox('Genres du film'):
    genre_choisi = st.sidebar.multiselect(
        'Genres de film recherché',
        ['Action','Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'],
        ['Comedy', 'Romance'])
    # mask_film = data_films['type_cleaned'].str.contains(genre_choisi)
    # new_data_films = data_films[mask_film]
    # resultat_films = new_data_films['Titre']
    # st.success("RESULTAT - Voici la liste des films concernés :")
    # st.write(resultat_films)
    # st.write("Soit un total de",len(resultat_films),"films.")

#CRITERE ACTEURS
if st.sidebar.checkbox('Acteurs du film'):
    acteur_film = st.sidebar.selectbox(
        'Acteurs de film recherchés',
        (acteurs_films_liste),
        )
    mask_film = pd.Series(True, index=data_films.index)
    mask_film = data_films['Acteurs'].str.contains(acteur_film)
    new_data_films = data_films[mask_film]
    resultat_films = new_data_films['Titre']
    st.success("RESULTAT - Voici la liste des films concernés :")
    st.write(resultat_films)
    st.write("Soit un total de",len(resultat_films),"films.")

#CRITERE DUREE
if st.sidebar.checkbox('Durée du film'):
    data_filtered = st.container()
    duree_max_films = st.sidebar.number_input('Mettre la durée maximale (en minutes)',max_value=360, value=120, step=10, help='Une heure = 60 minutes')
    with data_filtered :
        mask_duree_film = data_films['time_cleaned'] < duree_max_films
    # st.success("RESULTAT - Voici la liste des films concernés :")
    # st.dataframe(data=data_films[mask_duree_film])
    # st.write("Soit un total de",len(data_films[mask_duree_film]),"films.")

#CRITERE NOTES
if st.sidebar.checkbox('Note du film'):
    data_filtered = st.container()
    note_min_films = st.sidebar.number_input('Mettre la note minimale',max_value=10.0,value=8.0,step=0.1)
    with data_filtered :
        mask_note_film = data_films['Note'] > note_min_films
    # st.success("RESULTAT - Voici la liste des films concernés :")
    # st.dataframe(data=data_films[mask_note_film])
    # st.write("Soit un total de",len(data_films[mask_note_film]),"films.")


#CRITERE PUBLIC
# if st.sidebar.checkbox('Age minimum conseillé'):
#     status = st.sidebar.radio("Sélectionner le public visé : ", ('Tous publics', 'Pour les moins de 14ans', 'Pour les moins de 16ans', 'Pour les moins de 18ans', 'Pour adultes uniquement' )) 
  
#     if (status == 'Tous publics'): 
#         mask_film = data_films['age_conseille'] < 10
#         new_data_films = data_films[mask_film]
#         resultat_films = new_data_films['Titre']
#         st.success("RESULTAT - Voici la liste des films concernés :")
#         st.write(resultat_films)
#         st.write("Soit un total de",len(resultat_films),"films.")  
#     elif (status == 'Pour les moins de 14 ans'): 
#         mask_film = data_films['age_conseille'] < 14
#         new_data_films = data_films[mask_film]
#         resultat_films = new_data_films['Titre']
#         st.success("RESULTAT - Voici la liste des films concernés :")
#         st.write(resultat_films)
#         st.write("Soit un total de",len(resultat_films),"films.") 
#     elif (status == 'Pour les moins de 16 ans'): 
#         mask_film = data_films['age_conseille'] < 16
#         new_data_films = data_films[mask_film]
#         resultat_films = new_data_films['Titre']
#         st.success("RESULTAT - Voici la liste des films concernés :")
#         st.write(resultat_films)
#         st.write("Soit un total de",len(resultat_films),"films.") 
#     elif (status == 'Pour les moins de 18 ans'): 
#         mask_film = data_films['age_conseille'] < 18
#         new_data_films = data_films[mask_film]
#         resultat_films = new_data_films['Titre']
#         st.success("RESULTAT - Voici la liste des films concernés :")
#         st.write(resultat_films)
#         st.write("Soit un total de",len(resultat_films),"films.") 
#     elif (status == 'Pour adultes uniquement'): 
#         mask_film = data_films['age_conseille'] >= 18
#         new_data_films = data_films[mask_film]
#         resultat_films = new_data_films['Titre']
#         st.success("RESULTAT - Voici la liste des films concernés :")
#         st.write(resultat_films)
#         st.write("Soit un total de",len(resultat_films),"films.")  

#BOUTTON DE RECHERCHE
if st.sidebar.button('Recherchez mon film !'):
    
    resultat_films = data_films[mask_duree_film & mask_note_film]
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
    genre_serie = st.sidebar.multiselect(
        'Genres de film recherché',
        ['Action','Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'],
        ['Comedy', 'Romance'])
    # st.success("Voici la liste des séries concernées du genre :")

#CRITERE ACTEURS
if st.sidebar.checkbox('Acteurs de la série'):
    acteur_serie = st.sidebar.selectbox(
        'Acteurs de la série recherchée',
        (acteurs_series_liste),
        )
    # st.write("You selected", len(acteur_serie), 'actors')
    # st.success("Voici la liste des séries concernées :")

#CRITERE DUREE
if st.sidebar.checkbox("Durée moyenne d'un épisode"):
    data_filtered = st.container()
    duree_max_series = st.sidebar.number_input('Mettre la durée maximale (en minutes)',max_value=180, value=55, step=5, help='Une heure = 60 minutes')
    with data_filtered :
        mask_duree_serie = data_series['time_cleaned'] < duree_max_series
    # st.success("RESULTAT - Voici la liste des séries concernées :")
    # st.dataframe(data=data_series[mask_duree_serie])
    # st.write("Soit un total de",len(data_series[mask_duree_serie]),"séries.")

#CRITERE NOMBRE EPISODES
if st.sidebar.checkbox("Nombre d'épisodes total"):
    data_filtered = st.container()
    episodes_max_series = st.sidebar.number_input("Mettre le nombre maximum d'épisodes",min_value=1, value=50)
    with data_filtered :
        mask_nb_episodes = data_series["Nombre d'épisodes"] < episodes_max_series
    # st.success("RESULTAT - Voici la liste des séries concernées :")
    # st.dataframe(data=data_series[mask_nb_episodes])
    # st.write("Soit un total de",len(data_series[mask_nb_episodes]),"séries.")

#CRITERE NOTES
if st.sidebar.checkbox('Note de la série'):
    data_filtered = st.container()
    note_min_series = st.sidebar.number_input('Mettre la note minimale',max_value=10.0,value=8.0,step=0.1)
    with data_filtered :
        mask_note_serie = data_series['Note'] > note_min_series
    # st.success("RESULTAT - Voici la liste des séries concernées :")
    # st.dataframe(data=data_series[mask_note_serie])
    # st.write("Soit un total de",len(data_series[mask_note_serie]),"séries.")

#CRITERE PUBLIC
# if st.sidebar.checkbox('Public'):
#     status = st.sidebar.radio("Sélectionner le public visé : ", ('Tous publics', 'A partir de 12ans', 'A partir de 13ans', 'A partir de 16ans', 'A partir de 18ans' )) 
  
#     if (status == 'A partir de 12 ans'): 
#         st.success("Voici la liste des films concernés :") 
#     elif (status == 'A partir de 14 ans'): 
#         st.success("Voici la liste des films concernés :")
#     elif (status == 'A partir de 16 ans'): 
#         st.success("Voici la liste des films concernés :")
#     elif (status == 'A partir de 18 ans'): 
#         st.success("Voici la liste des films concernés :")
#     else: 
#         st.success("Voici la liste des films concernés :") 

#BOUTTON DE RECHERCHE
if st.sidebar.button('Recherchez ma série !'):

    resultat_series = data_series[mask_duree_serie & mask_nb_episodes & mask_note_serie]
    with st.spinner('Recherche en cours...'):
        time.sleep(3)
    st.success("RESULTAT - Voici la liste des séries concernées :")
    st.dataframe(data=resultat_series)
    st.write("Soit un total de",len(resultat_series),"séries.")

# --- AUTRES UTILISATIONS POSSIBLES ---

#LOADING CHARGEMENT
# 'Recherche en cours...'

# # Add a placeholder
# latest_iteration = st.empty()
# bar = st.progress(0)

# for i in range(100):
#   # Update the progress bar with each iteration.
#   latest_iteration.text(f' {i+1} %')
#   bar.progress(i + 1)
#   time.sleep(0.1)

#AUTRE LOADING CHARGEMENT
# '...recherche terminée !'

    # with st.spinner('Recherche en cours...'):
    #     time.sleep(3)
    # st.success('Voici le résultat de votre recherche :')

#RESULTAT RECHERCHE

# st.success("Voici le résultat de votre recherche : ") 
# st.markdown("Liste des films correspondants...")
# st.info("Soit un total de ... films.") 
# st.warning("Il n'existe aucun film répondant aux critères demandés")  
# st.error("Une erreur est apparue durant le traitement de votre demande") 


#IMAGES EN COLONNES
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.header("A cat")
#     st.image("https://static.streamlit.io/examples/cat.jpg")
# with col2:
#     st.header("A dog")
#     st.image("https://static.streamlit.io/examples/dog.jpg")
# with col3:
#     st.header("An owl")
#     st.image("https://static.streamlit.io/examples/owl.jpg")

# st.line_chart({"data": [1, 5, 2, 6, 2, 1]})
# with st.expander("See explanation"):
#     st.write("""
#         The chart above shows some numbers I picked for you.
#         I rolled actual dice for these, so they're *guaranteed* to
#         be random.
#     """)
#     st.image("https://static.streamlit.io/examples/dice.jpg")

#METTRE DU TEXTE
# title = st.sidebar.text_input('Movie title', 'Life of Brian')
# st.write('The current movie title is', title)

#CONSIGNES JEREMY

# data_filtered = st.container()

# country = ["Italy","France"]
# mask = pd.Series(True, index=imdb.index)
# for i in country :
#     mask &= imdb['Origin country'].str.contains(i)