import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_coinafrique(urls):
    resultats = []

    for url_base in urls:
        categorie = url_base.split("/categorie/")[-1].replace("-", " ").title()
        print(f"\n🔍 Scraping catégorie : {categorie}")

        page = 1
        while True:
            print(f"   → Page {page}")
            url = f"{url_base}?page={page}"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(f"⚠️ Erreur de chargement : {url}")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            cartes = soup.find_all("div", class_="card ad__card round small hoverable undefined")

            if not cartes:
                print("⛔ Aucune annonce trouvée sur cette page. Fin de la catégorie.")
                break

            for carte in cartes:
                # Nom
                a_tag = carte.find("a", class_="card-image ad__card-image waves-block waves-light")
                nom = a_tag.get("title", "").strip() if a_tag else "Nom non trouvé"

                # Prix
                prix_tag = carte.find("p", class_="ad__card-price")
                prix = prix_tag.text.strip() if prix_tag else "Prix non trouvé"

                # Adresse
                adresse_tag = carte.find("p", class_="ad__card-location")
                adresse = adresse_tag.text.strip() if adresse_tag else "Adresse non précisée"

                # Image
                img_tag = carte.find("img", class_="ad__card-img")
                image_lien = img_tag.get("src", "").strip() if img_tag else "Image non trouvée"

                # Ajouter à la liste
                resultats.append({
                    "Categorie": categorie,
                    "Nom": nom,
                    "Prix": prix,
                    "Adresse": adresse,
                    "Image_lien": image_lien
                })

            page += 1
            time.sleep(1)  # 💤 Pause pour ne pas surcharger le serveur

    df = pd.DataFrame(resultats)
    return df
