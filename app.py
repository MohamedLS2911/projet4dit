import streamlit as st
import pandas as pd
import scraper
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="App Scraping CoinAfrique", layout="wide")

st.title("🐾 Scraper CoinAfrique - Animaux")

# Onglets
tab1, tab2, tab3, tab4 = st.tabs(["📥 Scraper", "📁 Télécharger données Web Scraper", "📊 Dashboard", "📝 Évaluation"])

### 🧩 1. Scraping en live
with tab1:
    st.header("Scraping dynamique")
    st.markdown("Scrape les données en direct depuis CoinAfrique.")

    urls = [
        "https://sn.coinafrique.com/categorie/chiens",
        "https://sn.coinafrique.com/categorie/moutons",
        "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
        "https://sn.coinafrique.com/categorie/autres-animaux"
    ]

    if st.button("Lancer le scraping"):
        df_scraped = scraper.scrape_coinafrique(urls)
        df_scraped.to_csv("annonces_animaux.csv", index=False)
        st.success(f"{len(df_scraped)} annonces récupérées.")
        st.dataframe(df_scraped.head())

        st.download_button("📥 Télécharger les données",
                           data=df_scraped.to_csv(index=False),
                           file_name="annonces_animaux.csv",
                           mime="text/csv")

### 🧩 2. Télécharger fichier Web Scraper
with tab2:
    st.header("📁 Données Web Scraper (non nettoyées)")
    try:
        df_raw = pd.read_csv("annonces_animaux.csv")
        st.dataframe(df_raw.head())
        st.download_button("📥 Télécharger données brutes",
                           data=df_raw.to_csv(index=False),
                           file_name="annonces_animaux.csv",
                           mime="text/csv")
    except FileNotFoundError:
        st.warning("Fichier 'annonces_animaux.csv' non trouvé.")

### 🧩 3. Dashboard
with tab3:
    st.header("📊 Analyse des données (nettoyées)")
    try:
        df_clean = pd.read_csv("annonces_animaux.csv")

        st.subheader("Répartition des annonces par catégorie")
        fig1 = plt.figure(figsize=(10, 4))
        sns.countplot(data=df_clean, x="Categorie", order=df_clean["Categorie"].value_counts().index)
        st.pyplot(fig1)

        st.subheader("Répartition géographique")
        fig2 = plt.figure(figsize=(10, 4))
        sns.countplot(data=df_clean, y="Adresse", order=df_clean["Adresse"].value_counts().head(10).index)
        st.pyplot(fig2)

    except FileNotFoundError:
        st.warning("Fichier 'annonces_animaux.csv' non trouvé.")

### 🧩 4. Formulaire d'évaluation
with tab4:
    st.header("📝 Formulaire d’évaluation")

    with st.form("eval_form"):
        nom = st.text_input("Votre nom")
        note = st.slider("Note de l'app", 1, 5, 3)
        commentaire = st.text_area("Commentaire / Suggestion")
        submit = st.form_submit_button("Envoyer")

        if submit:
            new_feedback = pd.DataFrame([{
                "Nom": nom,
                "Note": note,
                "Commentaire": commentaire
            }])
            try:
                old = pd.read_csv("evaluation.csv")
                new_feedback = pd.concat([old, new_feedback], ignore_index=True)
            except FileNotFoundError:
                pass

            new_feedback.to_csv("evaluation.csv", index=False)
            st.success("Merci pour votre retour !")
