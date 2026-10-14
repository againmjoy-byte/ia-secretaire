import pandas as pd
import streamlit as st
import datetime
from google import genai
from gtts import gTTS

# 1. Configuration de la page
st.set_page_config(page_title="Secrétaire IA Multilingue", page_icon="🤖")

# 2. Configuration de la clé API avec le client Google GenAI
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error("⚠️ La clé API 'GEMINI_API_KEY' est introuvable dans les secrets Streamlit.")
    st.stop()

client = genai.Client(api_key=api_key)

# 3. SÉCURITÉ & VÉRIFICATION DE L'ABONNEMENT
st.subheader("🔒 Accès Sécurisé - Secrétaire IA")

st.info("""
**Comment accéder à l'application ?**
* **1er Mois / Mise en service :** 40 000 FCFA
* **Abonnement mensuel :** 15 000 FCFA / mois

Effectuez votre paiement sur notre numéro Mobile Money : **72756375**, puis contactez-nous.
""")

code_client = st.text_input("Entrez votre code d'accès :")

if not code_client:
    st.warning("⚠️ Veuillez entrer votre code d'accès pour continuer.")
    st.stop()

# Codes d'accès de secours directs en cas de besoin
CODES_SECOURS = ["IANO-VIP-15K", "IANO-AI-8821", "IANO-AI-4309", "admin"]

# Vérification du code
acces_autorise = False

if code_client.strip() in CODES_SECOURS:
    acces_autorise = True
else:
    try:
        SHEET_URL = "https://docs.google.com/spreadsheets/d/1x_kC3p-ezkbeByctaCFY9JKlEQY9/export?format=csv"
        df_codes = pd.read_csv(SHEET_URL)
        if 'Code' in df_codes.columns:
            df_codes['code'] = df_codes['Code'].astype(str).str.strip()
            if not df_codes[df_codes['code'] == code_client.strip()].empty:
                acces_autorise = True
    except Exception:
        pass

if acces_autorise:
    st.success("✅ Accès autorisé ! Bienvenue dans votre Secrétaire IA.")
else:
    st.error("❌ Code invalide ou inconnu. Veuillez effectuer votre paiement Mobile Money.")
    st.stop()

# --- BARRE LATÉRALE ---
st.sidebar.success("✅ Compte IANO Abonné Actif")

# --- ZONE DE SAISIE POUR L'UTILISATEUR ---
user_question = st.text_input("Posez votre question :")

# --- SECTION : MULTI-DOMAINES ---
st.divider()
st.subheader("⚙️ Configuration des Domaines & Secteurs d'Activité")
st.write("Gérez les informations spécifiques de votre établissement ci-dessous :")

domaine = st.selectbox(
    "Sélectionnez votre secteur :",
    [
        "Hôtel / Hébergement",
        "Boutique / Commerce (Boissons, etc.)",
        "Clinique / Santé",
        "Restauration / Maquis",
        "Coiffure, Beauté & Esthétique",
        "Ateliers de Mode & Couture",
        "Ateliers Techniques & Réparations",
        "Pressings & Services d'Entretien",
        "Banques, Microfinances & Épargne"
    ]
)

if domaine == 'Hôtel / Hébergement':
    st.text_input("Nom de l'Hôtel :")
    st.number_input("Nombre de chambres libres :", min_value=0, value=10)
elif domaine == 'Boutique / Commerce (Boissons, etc.)':
    st.text_input("Nom de la Boutique :")
    st.text_area("Produits disponibles (Ex: Casiers de Coca-Cola)")
elif domaine == 'Banques, Microfinances & Épargne':
    st.text_input("Nom de la structure / Tontine :")
    st.selectbox("Type :", ["Épargne journalière", "Petits copecks"])
else:
    st.text_input("Nom de l'établissement / atelier :")
    st.text_area("Précisions sur vos services :")

st.text_input("Numéro WhatsApp / Contact de l'établissement :")

if st.button("Enregistrer les paramètres du domaine"):
    st.success("Paramètres enregistrés avec succès !")

prompt_final = f"""
Tu es une secrétaire virtuelle professionnelle, chaleureuse et multilingue, spécialisée dans le domaine : {domaine}.
Règles de comportement :
1. Accueille toujours le client poliment avec un mot de bienvenue.
2. Réponds ensuite précisément à sa question.
"""

# --- AJOUT DE LA PARTIE VOCALE ET INTERACTIONS AUDIO ---
st.divider()
st.subheader("🎙️ Espace d'échanges (Texte ou Vocal)")

mode_entree = st.radio("Mode d'interaction :", ["Clavier (Écrire)", "Vocal (Parler)"])

if mode_entree == "Vocal (Parler)":
    audio_file = st.audio_input("Enregistrez votre question...")
    if audio_file
  
