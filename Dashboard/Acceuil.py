# Importer les bibliothèques nécessaires
import streamlit as st
import pandas as pd
import plotly.express as px
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
data = pd.read_csv(obj['Body'])

print(data.columns)

# Configuration de la page
st.set_page_config(page_title="Dashboard",page_icon=":bookmark_tabs:", layout="wide")




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


# Importation de l'image à mettre sur le sidebar
image=Image.open('Images/book_logo.png')


# Ajout de l'image sur le sidebar
with st.sidebar:
     st.image(image, width=200)
     filtre_date = st.sidebar.selectbox("Filtrer par la date", ['Tous'] + list(data['date'].unique()))


#--------------------------------------------------
# Appliquer filtre de date
if filtre_date != 'Tous':
    data = data[data['date'] == filtre_date]

#---------------------------------------------------



# Création de la première partie comporatnt les informations globales
st.subheader('Informations globales', divider="rainbow")


# Première ligne avec 4 colonnes
col1, col2, col3 = st.columns(3,gap='medium')

# Calcul du nombre total de livres, du nombre de catégories et détermination de la catégorie la mieux notée
nb_livres = data['nombre_de_livres_disponible'].sum()
nb_cat = data['categorie'].nunique()
categorie_meilleure_note = data.groupby('categorie')['rating'].mean().idxmax()
meilleure_note = data.groupby('categorie')['rating'].mean().max()

# Affichage des informations dans la première colonne
with col1:
    st.info("Nombre total de livres", icon="📚")
    st.markdown(
        f"""
        <div style="background: linear-gradient(to bottom, #F2D24C, #E0B400); padding: 10px; border-radius: 5px; text-align: center;">
            <h3 style="color: white;">{nb_livres:,.0f}</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Affichage des informations dans la seconde colonne
with col2:
    st.info("Nombre de catégories", icon="ℹ️")
    st.markdown(
        f"""
        <div style="background: linear-gradient(to bottom, #2A3B5C, #0E1C36); padding: 10px; border-radius: 5px; text-align: center;">
            <h3 style="color: white;">{nb_cat:,.0f}</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Affichage des informations dans la troisième colonne
with col3:
    st.info("Catégorie la mieux notée", icon="🏆")
    st.markdown(
        f"""
        <div style="background:linear-gradient(to bottom, #3A3B3C, #252627) ; padding: 0.5px; border-radius: 5px; text-align: center; width: 250px; margin: auto;">
            <h4 style="color: white; font-size: 16px; margin: 0;">{categorie_meilleure_note}</h4>
            <h5 style="color: white; font-size: 14px; margin: 0;">⭐ {meilleure_note:.0f}/5</h5>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Ajout d'une ligne séparatrice
st.markdown("---")


# Deuxième ligne avec 3 colonnes
col1_, col2_, col3_ = st.columns(3)

# Calcul du prix minimal, maximal et médian des livres
prix_min = data['prix'].min()
prix_max = data['prix'].max()
prix_median = data['prix'].median()

# Affichage des informations dans la première colonne
with col1_:
    st.markdown(
        f"""
        <div style="background: linear-gradient(to bottom, #7089AE, #4D7298); padding: 0.5px; border-radius: 5px; text-align: center; width: 250px; margin: auto;">
            <h3 style="color: white; font-size: 16px; margin: 15px auto 0;"> Prix minimal </h3>
            <h3 style="color: white; font-size: 16px; margin: 3px auto 0;"> £ {prix_min:.0f}</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Affichage des informations dans la deuxième colonne
with col2_:
    st.markdown(
        f"""
        <div style="background: linear-gradient(to bottom, #4A7785, #326273); padding: 0.5px; border-radius: 5px; text-align: center; width: 250px; margin: auto;">
            <h3 style="color: white; font-size: 16px; margin: 15px auto 0;"> Prix médian </h3>
            <h3 style="color: white; font-size: 16px; margin: 3px auto 0;"> £ {prix_median:.0f}</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Affichage des informations dans la troisième colonne
with col3_:
    st.markdown(
        f"""
        <div style="background: linear-gradient(to bottom, #A3C4D1, #77A6B6); padding: 0.5px; border-radius: 5px; text-align: center; width: 250px; margin: auto;">
            <h3 style="color: white; font-size: 16px; margin: 15px auto 0;"> Prix maximal </h3>
            <h3 style="color: white; font-size: 16px; margin: 3px auto 0;"> £ {prix_max:.0f}</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Ajout d'une ligne séparatrice
st.markdown("---")


# Création de la deuxième partie comporatnt les graphiques
st.subheader('Graphiques', divider="grey")


# Première ligne avec 2 colonnes de largeur respective 0.6 et 0.4
col5, col6 = st.columns([0.6,0.4])


# Regroupement du nombres de livres disponibles par catégorie et affichage des 10 catégories ayant le plus de livres disponibles
grouped_data = data.groupby('categorie')['nombre_de_livres_disponible'].sum().reset_index()
top5_categories = grouped_data.nlargest(10, 'nombre_de_livres_disponible')

# Affichage des informations dans la première colonne
with col5:
    fig = px.pie(top5_categories, values='nombre_de_livres_disponible', names='categorie', hole=0.5, width=400, height=400)
    fig.update_traces(text = top5_categories['categorie'], textposition='inside')
    fig.update_layout(title="Répartition des livres disponibles par catégorie")
    st.plotly_chart(fig, use_container_width=True)

# Affichage des informations dans la seconde colonne
with col6:
    data['classe_bin'] = pd.cut(data['prix'], bins=range(0, 70, 10)).astype(str)
    custom_colors = ["#FFCC00", "#9CF6F6","#1B2D2A","#414066","#82816D"]
    fig = px.histogram(data, x='classe_bin',color='classe_bin', color_discrete_sequence=custom_colors) 
    fig.update_layout(
        title="Distribution du nombre de livres par classe de prix",
        xaxis_title="Prix des livres",
        yaxis_title="Nombre de livres",
        bargap=0.2,
        width=400,
        height=400,
        legend_title_text='')
    st.plotly_chart(fig, use_container_width=True)



# Ajout d'une ligne séparatrice
st.markdown("---")


# Création de la troisième partie comportant les informations détaillées sur les catégories et les prix moyens par catégorie
st.subheader('Nombre de livres et prix moyen par catégorie', divider="rainbow")

# Première ligne avec 2 colonnes
col7, col8=st.columns(2)

# Affichage des informations dans la première colonne
with col7:
    expander=st.expander("Nombre de livres par catégorie")
    data_n_cat=data[["categorie","nombre_de_livres_disponible"]].groupby(by="categorie")["nombre_de_livres_disponible"].sum()
    expander.write(data_n_cat)

# Affichage des informations dans la seconde colonne
with col8:
    expander=st.expander("Prix moyens des livres par catégorie")
    data_p_cat=data[["categorie","prix"]].groupby(by="categorie")["prix"].mean()
    data_p_cat = data_p_cat.apply(lambda x: f"£{x:.2f}")
    expander.write(data_p_cat)
