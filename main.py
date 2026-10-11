import pandas as pd
import streamlit as st
import datetime
import streamlit as st
import google.generativeai as genai

# 1. Configuration de la page (doit être le tout premier truc Streamlit)
st.set_page_config(page_title="Secrétaire IA Multilingue")

# 2. Configuration de la clé API en premier
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ La clé API 'GEMINI_API_KEY' est introuvable dans les secrets.")
else:
    genai.configure(api_key=api_key)

# 3. Création du modèle juste après la configuration de la clé
model = genai.GenerativeModel('gemini-2.5-flash')

# ==========================================
# 🔒 SÉCURITÉ & VÉRIFICATION DE L'ABONNEMENT
# ==========================================
st.subheader("🔒 Accès Sécurisé - Secrétaire IA")

st.info("""
**Comment accéder à l'application ?**
* **1er mois / Mise en service :** 40 000 FCFA
* **Abonnement mensuel :** 15 000 FCFA / mois

Effectuez votre paiement sur notre numéro Mobile Money : **72756375**, puis contactez-nous pour recevoir votre code d'accès personnel.
""")

code_client = st.text_input("Entrez votre code d'abonnement :", type="password")

# 1. Si rien n'est écrit, on bloque
if not code_client:
    st.warning("Veuillez entrer votre code d'accès ci-dessus pour débloquer l'application.")
    st.stop()

# 2. Chargement direct de ton Google Sheet public/partagé
try:
    sheet_url = "https://docs.google.com/spreadsheets/d/1x_kCd3p-eZkkeByctaCf9YJk1EQ2Y9fkUoz8f6uIDfs/export?format=csv"
    df_codes = pd.read_csv(sheet_url)
except Exception as e:
    df_codes = None

# 3. Vérification stricte
if df_codes is not None and 'code' in df_codes.columns:
    # Nettoyage et comparaison avec le code saisi (ex: "M Joy")
    client_row = df_codes[df_codes['code'].astype(str).str.strip() == code_client.strip()]
    
    if not client_row.empty:
        # Vérification de la date d'expiration
        if 'DateExpiration' in df_codes.columns:
            try:
                date_exp_str = str(client_row['DateExpiration'].values[0]).strip()
                date_expiration = datetime.datetime.strptime(date_exp_str[:10], "%Y-%m-%d").date()
                if datetime.date.today() > date_expiration:
                    st.error("❌ Votre abonnement a expiré. Veuillez effectuer votre renouvellement de 15 000 FCFA au **72756375**.")
                    st.stop()
            except Exception:
                pass
        st.success("✅ Accès autorisé ! Bienvenue dans votre Secrétaire IA.")
    else:
        st.error("❌ Code invalide ou inconnu. Veuillez effectuer votre paiement au **72756375**.")
        st.stop()
else:
    st.error("❌ Erreur de connexion à la base de données des abonnés.")
    st.stop()

# ==========================================
# TOUT LE RESTE DE TON APPLICATION COMMENCE ICI
# ==========================================


# --- AUTOMATISATION DE L'ESSAI GRATUIT ET SÉCURITÉ IANO ---

# Si c'est la toute première ouverture par le client, on démarre l'essai automatiquement
if "trial_start" not in st.session_state:
    st.session_state["trial_start"] = datetime.date.today()

if "abonne" not in st.session_state:
    st.session_state["abonne"] = False

# CALCUL DES JOURS ÉCOULÉS (Automatique)
jours_ecoules = (datetime.date.today() - st.session_state["trial_start"]).days
jours_restants = 30 - jours_ecoules

# CODES D'ABONNEMENT VALIDES (Créés par vous)
CODES_ABONNEMENTS = {
    "IANO-VIP-15K": "Client VIP",
    "IANO-A1-8821": "Client A1",
    "IANO-A2-4309": "Client A2"
}

# --- VÉRIFICATION DE L'ACCÈS ---

# SI LES 30 JOURS SONT DEPASSÉS ET QUE LE CLIENT N'A PAS PAYÉ : ON BLOQUE
if jours_ecoules > 30 and not st.session_state["abonne"]:
    st.title("🔒 Période d'essai terminée - IANO")
    st.error("⏳ Vos 30 jours d'essai gratuit sont écoulés.")
    st.write("Pour continuer à utiliser votre Secrétaire Multilingue IANO, veuillez renouveler votre abonnement.")
    
    code_client = st.text_input("🔑 Entrez votre code d'abonnement :", type="password")
    
    if st.button("Valider l'abonnement", use_container_width=True):
        if code_client in CODES_ABONNEMENTS:
            st.session_state["abonne"] = True
            st.success("✅ Abonnement activé avec succès ! Merci pour votre confiance.")
            st.rerun()
        else:
            st.error("❌ Code invalide. Veuillez effectuer votre paiement Mobile Money pour recevoir un code.")
            
    # Bloque l'application tant que l'abonnement n'est pas payé
    st.stop()

# --- BARRE LATÉRALE (Pendant l'essai ou l'abonnement) ---
if st.session_state["abonne"]:
    st.sidebar.success("⭐ Compte IANO Abonné Actif")
else:
    st.sidebar.info(f"⏳ Essai Gratuit IANO : **{max(0, jours_restants)} jours** restants")

# --- À PARTIR D'ICI, SE TROUVE TOUT VOTRE CODE EXISTANT (IA, VOCAL, ESPACES MÉTIERS) ---


import google.generativeai as genai

st.set_page_config(page_title="Secrétaire IA Multilingue", page_icon="🤖")

st.title("🤖 Secrétaire IA Multilingue")

# Récupération de la clé API depuis les secrets Streamlit
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ La clé API 'GEMINI_API_KEY' est introuvable dans les secrets Streamlit.")
else:
    genai.configure(api_key=api_key)

    # Zone de saisie pour l'utilisateur
    user_question = st.text_input("Posez votre question :")

    if user_question:
        st.write(f"**Vous :** {user_question}")
        try:
            # Utilisation du modèle actuel recommandé
            model = genai.GenerativeModel("gemini-3.8-flash")
            response = model.generate_content(user_question)
            
            st.success("Réponse :")
            st.write(response.text)
            
        except Exception as err:
            st.error(f"Erreur technique : {err}")
# ==========================================
# SECTION AJOUTÉE EN BAS : MULTI-DOMAINES
# ==========================================
st.divider()
st.subheader("🏢 Configuration des Domaines & Secteurs d'Activité")
st.write("Gérez les informations spécifiques de votre établissement ci-dessous :")

domaine = st.selectbox(
    "Sélectionnez votre secteur :",
    [
        "🏨 Hôtel / Hébergement", 
        "🛍️ Boutique / Commerce (Boissons, etc.)", 
        "🏥 Clinique / Santé", 
        "🍽️ Restauration / Maquis", 
        "✂️ Coiffure, Beauté & Esthétique",
        "🧵 Ateliers de Mode & Couture",
        "🔧 Ateliers Techniques & Réparations",
        "🧺 Pressing & Services d'entretien",
        "🏦 Banques, Microfinances & Épargne (Petits copecks)"
    ]
)

if "Hôtel" in domaine:
    st.text_input("Nom de l'Hôtel :")
    st.number_input("Nombre de chambres libres :", min_value=0, value=5)
elif "Boutique" in domaine:
    st.text_input("Nom de la Boutique :")
    st.text_area("Produits disponibles (ex: Casiers de Coca-Cola) :")
elif "Banque" in domaine:
    st.text_input("Nom de la structure / Tontine :")
    st.selectbox("Type :", ["Épargne journalière (Petits copecks)", "Microfinance", "Tontine"])
else:
    st.text_input("Nom de l'établissement / atelier :")
    st.text_area("Précisions sur vos services :")

st.text_input("Numéro WhatsApp / Contact de l'établissement :")

if st.button("Enregistrer les paramètres du domaine"):
    st.success("Paramètres enregistrés avec succès !")
    prompt_final = f"""
Tu es une secrétaire virtuelle professionnelle, chaleureuse et multilingue.
Règles de comportement :
1. Accueille toujours le client poliment avec une formule de bienvenue.
2. Réponds ensuite précisément à sa question.
Question ou appel du client : {user_question}
""" 
# --- AJOUT DE LA PARTIE VOCALE ET INTERACTIONS ---
from gtts import gTTS

st.divider()
st.subheader("💬 Espace d'échanges (Texte ou Vocal)")

# Choix de la voix pour la secrétaire IA
voix_genre = st.selectbox("Voix de la secrétaire IA :", ["Féminine", "Masculine"])

# Choix du mode d'interaction
mode_entree = st.radio("Mode d'interaction :", ["Clavier (Écrire)", "Vocal (Parler)"], horizontal=True)

user_question = ""

if mode_entree == "Clavier (Écrire)":
    user_question = st.text_input("Posez votre question ici :")
else:
    audio_file = st.audio_input("Enregistrez votre message vocal :")
    if audio_file is not None:
        st.audio(audio_file)
        st.info("🎙️ Transcription de l'audio en cours...")
        try:
            transcription_response = model.generate_content([
                "Transcris cet enregistrement audio fidèlement en texte en français :",
                {"mime_type": audio_file.type, "data": audio_file.read()}
            ])
            user_question = transcription_response.text
            st.write(f"**Texte reconnu :** {user_question}")
        except Exception as e:
            st.error(f"Erreur lors de la transcription : {e}")

# Si on a une question (via texte ou vocal converti), on génère la réponse
if user_question:
    # On relance le modèle avec ton prompt final et la question
    try:
        with st.spinner("La secrétaire réfléchit..."):
            response = model.generate_content(prompt_final)
            reponse_texte = response.text
        
        st.success("Réponse de la Secrétaire IA :")
        st.write(reponse_texte)

        # Synthèse vocale (gTTS) pour écouter la réponse
        st.info("🔊 Génération de la réponse audio...")
        tts = gTTS(text=reponse_texte, lang='fr', slow=False)
        audio_path = "reponse_ia.mp3"
        tts.save(audio_path)
        
        st.audio(audio_path)

    except Exception as err:
        st.error(f"Une erreur est survenue lors de la réponse : {err}")
# --- CONFIGURATION TÉLÉPHONIQUE & CONTACT (AFRIQUE DE L'OUEST) ---
num_principal = st.text_input(
    "Numéro principal / WhatsApp (ex: +225 07 00 00 00, +229 97 00 00 00, +228 90 00 00 00) :"
)

activer_transfert = st.checkbox(
    "Activer la secrétaire IA sur transfert d'appel (GSM)", 
    value=True,
    help="L'IA prendra le relais en cas d'occupation ou de non-réponse, quel que soit l'opérateur."
)
# --- CONNEXION BASE DE DONNÉES GOOGLE SHEETS ---
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1x_kCd3p-eZkkeByctaCf9YJk1EQ2Y9fkUoz8f6uIDfs/export?format=csv"

@st.cache_data(ttl=60)
def charger_codes_promo():
    try:
        df = pd.read_csv(GOOGLE_SHEET_URL)
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des abonnements : {e}")
        return None

# Chargement des données
df_codes = charger_codes_promo()
import datetime

