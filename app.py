import streamlit as st
acc = st.Page(page = "Dashboard/Acceuil.py", title = "Accueil")
dat = st.Page(page = "Dashboard/Pages/Data.py", title = "Données")

pg = st.navigation(pages = [acc, dat])

pg.run()
