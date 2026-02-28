import pandas as pd
import re

INPUT_FILE  = r"c:\Users\pc\OneDrive\Documents\Projet_ML\mauritania-housing-ml\data\raw.csv"
OUTPUT_FILE = r"c:\Users\pc\OneDrive\Documents\Projet_ML\mauritania-housing-ml\data\cleaned.csv"

print("Lecture du fichier brut...")
df = pd.read_csv(INPUT_FILE, encoding="utf-8")

print(f"  → {len(df)} lignes chargées, {len(df.columns)} colonnes")
print(f"  → Colonnes : {list(df.columns)}")

# ── Nettoyage de la colonne 'description' ──────────────────────────────────────
def clean_description(text):
    if not isinstance(text, str):
        return text

    # Supprimer les sauts de ligne internes
    text = text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")

    # Supprimer les blocs de navigation répétitifs (menus, publicités, etc.)
    noise_patterns = [
        r"Real Estate\s+Search\s+Help Live Chat.*?Other",   # menu de navigation
        r"Similar Ads.*?Sponsored Deals.*?(?=\Z)",          # annonces similaires
        r"Sponsored Deals.*",                               # deals sponsorisés
        r"Overview\s+Report Ad",                            # boutons de navigation
        r"\d+ images?",                                     # compteur images
        r"Views\s+\d+",                                     # compteur vues
        r"Posted \d+\s+\w+\s+ago",                         # date de publication
        r"Features?(?:\s+\w+)+",                            # liste de features
        r"Lot Size.*?Street Size.*?Closest Landmark.*?Description",  # labels structurels
        r"Details\s+Land Title.*?(?=Rooms|Bathrooms|$)",    # section details
        r"Rooms\s+\d+",
        r"Balconies\s+\d+",
        r"Halls\s+\d+",
        r"Bathrooms\s+\d+",
        r"Land Title\s+(Yes|No)",
        r"Property Type\s+\w+",
        r"Similar Ads.*",
    ]
    for pattern in noise_patterns:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE | re.DOTALL)

    # Nettoyer les espaces multiples
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text

if "description" in df.columns:
    print("Nettoyage de la colonne 'description'...")
    df["description"] = df["description"].apply(clean_description)

# ── Nettoyage général ──────────────────────────────────────────────────────────
# Supprimer les lignes complètement vides
df.dropna(how="all", inplace=True)

# Supprimer les doublons
nb_avant = len(df)
df.drop_duplicates(inplace=True)
print(f"  → {nb_avant - len(df)} doublons supprimés")

# Normaliser la colonne prix (supprimer les virgules si elle est en string)
if "prix" in df.columns:
    df["prix"] = pd.to_numeric(df["prix"], errors="coerce")

# ── Sauvegarde ─────────────────────────────────────────────────────────────────
print(f"Sauvegarde vers : {OUTPUT_FILE}")
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print(f"✅ Terminé ! {len(df)} lignes sauvegardées dans cleaned.csv")
print(df.head(3).to_string())
