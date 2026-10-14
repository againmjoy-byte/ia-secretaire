import pandas as pd
import streamlit as st
import datetime
import google.generativeai as genai
from gtts import gTTS

# 1. Configuration de la page
st.set_page_config(page_title="Secrétaire IA Multilingue", page_icon="🤖")

# 2. Configuration de la clé API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.error("⚠️ La clé API 'GEMINI_API_KEY' est introuvable dans les secrets Streamlit.")
else:
    genai.configure(api_key=api_key)

# 3. Création du modèle
model = genai.GenerativeModel('gemini-2.5-flash')

# --- SÉCURITÉ & VÉRIFICATION DE L'ABONNEMENT ---
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

# Fonction de chargement des codes promo
def charger_codes_promo():
    try:
        SHEET_URL = "https://docs.google.com/spreadsheets/d/1x_kC3p-ezkbeByctaCFY9JKlEQY9"
        return pd.read_csv(SHEET_URL)
    except Exception as e:
        st.error(f"Erreur lors du chargement des codes : {e}")
        return None

df_codes = charger_codes_promo()

# Vérification stricte
if df_codes is not None and 'Code' in df_codes.columns:
    df_codes['code'] = df_codes['Code'].astype(str).str.strip()
    client_row = df_codes[df_codes['code'] == code_client.strip()]
    
    if not client_row.empty:
        if 'DateExpiration' in df_codes.columns:
            try:
                date_exp_str = str(client_row['DateExpiration'].values[0]).strip()
                date_expiration = datetime.datetime.strptime(date_exp_str, "%Y-%m-%d")
                if datetime.date.today() > date_expiration.date():
                    st.error("❌ Votre abonnement a expiré. Veuillez effectuer votre renouvellement.")
                    st.stop()
            except Exception:
                pass
        st.success("✅ Accès autorisé ! Bienvenue dans votre Secrétaire IA.")
    else:
        st.error("❌ Code invalide ou inconnu. Veuillez effectuer votre paiement Mobile Money.")
        st.stop()
else:
    st.error("❌ Erreur de connexion à la base de données d'abonnements.")
    st.stop()

# --- AUTOMATISATION DE L'ESSAI GRATUIT ET SÉCURITÉ ---
if "trial_start" not in st.session_state:
    st.session_state["trial_start"] = datetime.date.today()

if "abonne" not in st.session_state:
    st.session_state["abonne"] = False

jours_ecoulés = (datetime.date.today() - st.session_state["trial_start"]).days
jours_restants = 30 - jours_ecoulés

CODES_ABONNEMENTS = [
    "IANO-VIP-15K", "Client VIP",
    "IANO-AI-8821", "Client A1",
    "IANO-AI-4309", "Client A2"
]

# --- VÉRIFICATION DE L'ACCÈS ---
if jours_ecoulés > 30 and not st.session_state["abonne"]:
    st.title("🔒 Période d'essai terminée - IANO SECRÉTAIRE")
    st.error("❌ Vous avez dépassé vos 30 jours d'essai gratuit sur la plateforme.")
    st.write("Pour continuer à utiliser votre Secrétaire IA, veuillez activer votre abonnement.")
    
    code_client = st.text_input("Entrez votre code d'activation :")
    
    if st.button("Valider l'abonnement", use_container_width=True):
        if code_client in CODES_ABONNEMENTS:
            st.session_state["abonne"] = True
            st.success("✅ Abonnement activé avec succès ! Merci pour votre confiance.")
            st.rerun()
        else:
            st.error("❌ Code invalide. Veuillez réessayer.")
            
    st.stop()

# BARRE LATÉRALE
if st.session_state["abonne"]:
    st.sidebar.success("✅ Compte IANO Abonné Actif")
else:
    st.sidebar.info(f"⏳ Essai Gratuit IANO : **{max(0, jours_restants)}** jours restants sur 30")

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

prompt_final = """
Tu es une secrétaire virtuelle professionnelle, chaleureuse et multilingue.
Règles de comportement :
1. Accueille toujours le client poliment avec un mot de bienvenue.
2. Réponds ensuite précisément à sa question.
3. Question ou appel du client : {user_question}
"""

# --- AJOUT DE LA PARTIE VOCALE ET INTERACTIONS AUDIO ---
st.divider()
st.subheader("🎙️ Espace d'échanges (Texte ou Vocal)")

mode_entree = st.radio("Mode d'interaction :", ["Clavier (Écrire)", "Vocal (Parler)"])

if mode_entree == "Vocal (Parler)":
    audio_file = st.audio_input("Enregistrez votre question...")
    if audio_file is not None:
        st.info("🔄 Transcription de l'audio en cours...")
        try:
            transcription_response = model.generate_content([
                "Transcris cet enregistrement audio fidèlement en texte.",
                {"mime_type": "audio/file", "data": audio_file.getvalue()}
            ])
            user_question = transcription_response.text
            st.write(f"**Texte reconnu :** {user_question}")
        except Exception as e:
            st.error(f"Erreur lors de la transcription : {e}")

if user_question:
    try:
        with st.spinner("La secrétaire réfléchit..."):
            response = model.generate_content(prompt_final.format(user_question=user_question))
            reponse_ia = response.text
            
        st.success("Réponse de la Secrétaire IA :")
        st.write(reponse_ia)
        
        tts = gTTS(text=reponse_ia, lang='fr', slow=False)
        audio_path = "reponse_ia.mp3"
        tts.save(audio_path)
        
        st.audio(audio_path)
        
    except Exception as err:
        st.error(f"Une erreur est survenue lors de la réponse : {err}")

# --- MODULE DE GESTION DES APPELS & TÉLÉPHONIE ---
st.subheader("📞 Liaison Téléphone & Appels Entrants")

col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 Activer la permanence téléphonique"):
        st.success("La secrétaire IA est désormais active sur les transferts d'appels de votre ligne !")

with col2:
    st.markdown("[🔗 Tester l'appel / WhatsApp direct](https://wa.me/22872756375)")

st.markdown("### ⏱️ Réglage du transfert d'appel")

delai_secondes = st.slider(
    "Décrochage automatique par l'IA après combien de sonneries ?",
    min_value=5,
    max_value=30,
    value=15,
    step=5,
    help="Si le gérant ne décroche pas dans ce délai, l'IA répond automatiquement à l'appelant."
)

st.info(f"💡 L'IA prendra la main si le téléphone sonne plus de **{delai_secondes} secondes** sans réponse.")
