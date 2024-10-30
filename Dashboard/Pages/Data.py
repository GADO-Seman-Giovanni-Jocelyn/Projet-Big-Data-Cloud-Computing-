import streamlit as st
import pandas as pd
from PIL import Image
import boto3
import os
from dotenv import load_dotenv #dotenv_values
from pathlib import Path


# Charger les variables d'environnement
#dp = Path(__file__).resolve().parents[2] / '.env'
#load_dotenv(dotenv_path=dp)


# Récupération des informations depuis les variables d'environnement
aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
bucket_name = st.secrets["BUCKET_NAME"]
file_key =st.secrets["FILE_KEY"]


# Configuration de l'accès au bucket (compartiment)
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)
# Téléchargement du fichier et chargement en DataFrame
obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
s3_data = pd.read_csv(obj['Body'])

#Occuper toute la largeur de la page
st.set_page_config(layout="wide")

#st.markdown('<style> div.block-container{padding-top:1px; padding-bottom:5px}</style>', unsafe_allow_html=True)

image=Image.open('Images/book_logo.png')


with st.sidebar:
    
    st.image(image, width=200)
    st.sidebar.title("Filtres")
    filtre_cat = st.sidebar.selectbox("Filtrer par catégorie de livre", ['Tous'] + list(s3_data['categorie'].unique()))
    filtre_dispo = st.sidebar.selectbox("Filtrer par disponibilité", ['Tous'] + list(s3_data['availability'].unique()))
    filtre_date = st.sidebar.selectbox("Filtrer par la date", ['Tous'] + list(s3_data['date'].unique()))





html_title="""
  <style>
  .title-test{
  font-weight:bold;
  border-style:dash;
  border-color: red;
  border-width: medium;}
  </style>
  <center> <h1 class="title-test"> BookToScrape Scraper </center>"""
st.markdown(html_title, unsafe_allow_html=True)

st.divider()


# Appliquer les filtres de la barre latérale
data_filtre = s3_data.copy()

# Appliquer filtre de catégorie
if filtre_cat != 'Tous':
    data_filtre = data_filtre[data_filtre['categorie'] == filtre_cat]

# Appliquer filtre de disponibilité
if filtre_dispo != 'Tous':
    data_filtre = data_filtre[data_filtre['availability'] == filtre_dispo]

# Appliquer filtre de date
if filtre_date != 'Tous':
    data_filtre = data_filtre[data_filtre['date'] == filtre_date]



# Filtrer par plage de prix
min_val, max_val = st.slider('Sélectionner la plage de prix', 
                             min(s3_data['prix']), 
                             max(s3_data['prix']), 
                             (min(s3_data['prix']), max(s3_data['prix'])))
data_filtre = data_filtre[(data_filtre['prix'] >= min_val) & (data_filtre['prix'] <= max_val)]

# Filtrer par recherche
search_query = st.text_input("Rechercher dans les données :")
if search_query:
    data_filtre = data_filtre[data_filtre.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

# Afficher le DataFrame filtré
st.write(data_filtre)

#st.write(datat.head())

# Variables (articles, comments, spam)
liv_disp = data_filtre['nombre_de_livres_disponible'].sum()
prix_moyen = data_filtre['prix'].mean()

# Affichage des statistiques
col1, col2 = st.columns(2)

# Value box pour "Nombre de livres disponibles"
with col1:
    st.metric(label="Nombre de livres disponible", value=liv_disp)

# Value box pour "Prix moyen"
with col2:
    st.metric(label="Prix moyen", value=f"£{prix_moyen:.2f}")
    st.markdown(
        """
        <style>
        .stMetric {
            background-color: #ffcc00;
            border-radius: 5px;
            padding: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

st.divider()


    
