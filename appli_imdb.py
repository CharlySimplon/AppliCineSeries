import streamlit as st
import numpy as np
import pandas as pd
import time

data_films = pd.read_csv("films.csv")
data_series = pd.read_csv("series.csv")

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

#LISTE FILMS
left_column.header("250 meilleurs films")
if left_column.checkbox('Montrer la liste des films'):
    titre_films = data_films['Titre']
    st.dataframe(titre_films, width=None, height=None)

#LISTE SERIES
right_column.header("250 meilleures séries")
if right_column.checkbox('Montrer la liste des séries'):
    titre_series = data_series['Titre']
    st.dataframe(titre_series, width=None, height=None)

#SIDEBAR FILMS

st.sidebar.subheader("RECHERCHER UN FILM")
st.sidebar.text("Choix par :")

if st.sidebar.checkbox('Titre du film'):
    titre_films = data_films['Titre']
    titre_film_choisi = st.sidebar.selectbox(
        'Titre du film : ',
        (titre_films)
    )
    mask_film = data_films['Titre'] == titre_film_choisi
    new_data_films = data_films[mask_film]
    st.success("RESULTAT - Voici les détails du film concerné :")
    st.write(new_data_films)

if st.sidebar.checkbox('Genres du film'):
    genre_choisi = st.sidebar.multiselect(
        'Genres de film recherché',
        ['Action','Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'],
        ['Comedy', 'Romance'])
    # st.success("Voici la liste des films concernés du genre :")

if st.sidebar.checkbox('Acteurs du film'):
    acteurs = st.sidebar.multiselect(
        'Genres de film recherché',
        ['Christian Bale', 'Morgan Freeman', 'Dustin Hoffman'],
        ['Dustin Hoffman'])
    # st.success("Voici la liste des films concernés :")


if st.sidebar.checkbox('Durée du film'):
    duree_max_films = st.sidebar.number_input('Mettre la durée maximale (en minutes)',max_value=360, value=120, step=10, help='Une heure = 60 minutes')
    mask_film = data_films['time_cleaned'] < duree_max_films
    new_data_films = data_films[mask_film]
    resultat_films = new_data_films['Titre']
    st.success("RESULTAT - Voici la liste des films concernés :")
    st.write(resultat_films)
    st.write("Soit un total de",len(resultat_films),"films.")

if st.sidebar.checkbox('Note du film'):
    note_min_films = st.sidebar.number_input('Mettre la note minimale',max_value=10.0,value=8.0,step=0.1)
    mask_film = data_films['Note'] > note_min_films
    new_data_films = data_films[mask_film]
    resultat_films = new_data_films['Titre']
    st.success("RESULTAT - Voici la liste des films concernés :")
    st.write(resultat_films)
    st.write("Soit un total de",len(resultat_films),"films.") 

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

#SIDEBAR SERIES
st.sidebar.subheader("RECHERCHER UNE SERIE")
st.sidebar.text("Choix par :")

if st.sidebar.checkbox('Titre de la série'):
    titre_series = data_series['Titre']
    titre_serie_choisie = st.sidebar.selectbox(
        'Titre de la série : ',
        (titre_series)
    )
    mask_serie = data_series['Titre'] == titre_serie_choisie
    new_data_series = data_series[mask_serie]
    st.success("RESULTAT - Voici les détails de la série concernée :")
    st.write(new_data_series)

if st.sidebar.checkbox('Genres de la série'):
    genre_serie = st.sidebar.multiselect(
        'Genres de film recherché',
        ['Action','Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'],
        ['Comedy', 'Romance'])
    # st.success("Voici la liste des séries concernées du genre :")

if st.sidebar.checkbox('Acteurs de la série'):
    acteurs_serie = st.sidebar.multiselect(
        'Genres de film recherché',
        ['Christian Bale', 'Morgan Freeman', 'Dustin Hoffman'],
        ['Dustin Hoffman'])
    # st.write("You selected", len(acteur_serie), 'actors')
    # st.success("Voici la liste des séries concernées :")

if st.sidebar.checkbox("Durée moyenne d'un épisode"):
    duree_max_series = st.sidebar.number_input('Mettre la durée maximale (en minutes)',max_value=180, value=55, step=5, help='Une heure = 60 minutes')
    mask_series = data_series['time_cleaned'] < duree_max_series
    new_data_series = data_series[mask_series]
    resultat_series = new_data_series['Titre']
    st.success("RESULTAT - Voici la liste des séries concernés :")
    st.write(resultat_series)
    st.write("Soit un total de",len(resultat_series),"séries.")

if st.sidebar.checkbox("Nombre d'épisodes total"):
    episodes_max_series = st.sidebar.number_input("Mettre le nombre maximum d'épisodes",min_value=1, value=50)
    mask_series = data_series["Nombre d'épisodes"] < episodes_max_series
    new_data_series = data_series[mask_series]
    resultat_series = new_data_series['Titre']
    st.success("RESULTAT - Voici la liste des séries concernés :")
    st.write(resultat_series)
    st.write("Soit un total de",len(resultat_series),"séries.")

if st.sidebar.checkbox('Note de la série'):
    note_min_series = st.sidebar.number_input('Mettre la note minimale',max_value=10.0,value=8.0,step=0.1)
    mask_series = data_series['Note'] > note_min_series
    new_data_series = data_series[mask_series]
    resultat_series = new_data_series['Titre']
    st.success("RESULTAT - Voici la liste des séries concernées :")
    st.write(resultat_series)
    st.write("Soit un total de",len(resultat_series),"séries.") 


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

# --- AUTRES UTILISATIONS POSSIBLES ---

#EN COLONNES
# left_column, right_column = st.columns(2)
# left_column.button('Press me!')

# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")


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

# my_var = st.sidebar.selectbox('Choisissez votre variable', ['choix_1', 'choix_2'])

# with data_filtered :
#   mask_to_display = data_films['Public'] == my_var
#   st.dataframe(data=data_films[mask_to_display])