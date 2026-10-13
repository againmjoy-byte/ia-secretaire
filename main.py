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
model = genai.GenerativeModel('gemini-3.8-flash')

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
# ==========================================
# 🏢 CONFIGURATION DU DOMAINE & BASE DE CONNAISSANCES (Tous secteurs : Hôtels, Cliniques, Ateliers, etc.)
# ==========================================
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Paramètres de l'Établissement")

# Choix ou saisie libre du secteur
secteur_activite = st.sidebar.selectbox(
    "Secteur d'activité :",
    ["🏨 Hôtel / Hébergement", "🏥 Clinique / Santé", "🔧 Atelier / Mécanique", "🍽️ Restaurant / Bar", "🛍️ Commerce / Autre"]
)

nom_structure = st.sidebar.text_input("Nom de votre structure :", "Mon Entreprise")

# La grande zone fourre-tout où le gérant met TOUT (prix, services, pièces, menus, horaires)
base_infos_client = st.sidebar.text_area(
    "Informations & Tarifs (Prix, prestations, dispos...) :",
    "Ex pour mécanicien : Vidange 5000 FCFA, Révision complète 20000 FCFA. Ouvert de 8h à 18h."
)

# Instruction système dynamique injectée directement dans ton IA Gemini
system_instruction = f"""
Tu es la secrétaire virtuelle professionnelle et courtoise pour '{nom_structure}' (Secteur : {secteur_activite}).
Voici les informations officielles, les prix et les règles fournis par le gérant :
{base_infos_client}

Ton rôle est d'accueillir les clients par message ou par vocal, de leur donner les prix exacts, de répondre à leurs questions sur les services et de les orienter au mieux selon les consignes ci-dessus.
"""

# Mise à jour du modèle avec les instructions du domaine
model = genai.GenerativeModel(
    model_name='gemini-3.8-flash',
    system_instruction=system_instruction
)
# --- MODULE DE GESTION DES APPELS & TÉLÉPHONIE ---
st.markdown("---")
st.subheader("📞 Liaison Téléphonique & Appels Entrants")

# Un bouton interactif pour simuler ou déclencher la connexion d'appel
col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 Activer la permanence téléphonique"):
        st.success("La secrétaire IA est désormais active sur les transferts d'appels de votre ligne !")

with col2:
    # Lien direct vers le numéro WhatsApp ou appel
    st.markdown("[💬 Tester l'appel / WhatsApp direct](https://wa.me/228...)")
    # --- CONFIGURATION DU DÉLAI DE DÉCROCHAGE ---
st.markdown("### ⏱️ Réglage du transfert d'appel")

delai_secondes = st.slider(
    "Décrochage automatique par l'IA après combien de secondes de sonnerie ?",
    min_value=5,
    max_value=30,
    value=15,
    step=5,
    help="Si le gérant ne décroche pas dans ce délai, l'IA répond automatiquement à l'appelant."
)

st.info(f"💡 L'IA prendra la main si le téléphone sonne plus de **{delai_secondes} secondes** sans réponse.")
# ==========================================
# 📊 TABLEAU DE BORD DU GÉRANT : HISTORIQUE & PRISE DE RELAIS IA
# ==========================================
st.markdown("---")
st.subheader("📊 Tableau de Bord du Gérant : Supervision & Relais IA")

st.markdown("""
* **Mode Surveillance / Relais :** Quand vous êtes absent ou occupé, l'IA consigne ici les échanges et prépare les réponses automatiques. 
* **Historique :** Visualisez tout ce qui s'est passé et reprenez le contrôle à tout moment en un clic.
""")

# Initialisation d'un historique dans Streamlit si ça n'existe pas encore
if 'historique_messages' not in st.session_state:
    st.session_state.historique_messages = []

# Section pour simuler l'arrivée d'un message client (ou le journal d'activité de l'IA)
st.markdown("### 📥 Activité récente des clients")

col1, col2 = st.columns(2)

with col1:
    nouveau_client_txt = st.text_input("Simuler un message entrant (Texte) :", placeholder="Ex: Bonjour, il y a de la place ?")
    if st.button("📨 Enregistrer & Laisser l'IA répondre"):
        if nouveau_client_txt:
            # L'IA génère la réponse automatique
            reponse_auto = model_assistant.generate_content(nouveau_client_txt).text
            # On ajoute à l'historique du gérant
            st.session_state.historique_messages.insert(0, {
                "type": "Texte",
                "client": nouveau_client_txt,
                "reponse": reponse_auto,
                "statut": "🤖 Géré par l'IA (En attente de validation finale)"
            })
            st.success("Message traité et consigné dans le tableau de bord !")

with col2:
    nouveau_client_vocal = st.file_uploader("Simuler un vocal entrant :", type=["mp3", "wav", "m4a"], key="vocal_entrant")
    if nouveau_client_vocal is not None:
        if st.button("🎙️ Traiter le vocal entrant"):
            audio_bytes = nouveau_client_vocal.read()
            prompt_audio = [
                "Écoute cette note vocale de client. Rédige une réponse professionnelle avec les tarifs de l'établissement :", 
                {"mime_type": nouveau_client_vocal.type, "data": audio_bytes}
            ]
            reponse_vocal_auto = model_assistant.generate_content(prompt_audio).text
            st.session_state.historique_messages.insert(0, {
                "type": "Vocal",
                "client": "[Note Vocale du Client]",
                "reponse": reponse_vocal_auto,
                "statut": "🤖 Géré par l'IA (Vocal)"
            })
            st.success("Vocal analysé et consigné !")

# Affichage de l'historique et du journal pour le gérant
st.markdown("---")
st.markdown("### 📋 Journal de bord & Historique des discussions")

if len(st.session_state.historique_messages) == 0:
    st.info("Aucun message pour le moment. Le journal est vide.")
else:
    for i, item in enumerate(st.session_state.historique_messages):
        with st.container():
            st.markdown(f"**Échange n°{len(st.session_state.historique_messages) - i}** — *Statut : {item['statut']}*")
            st.text(f"Client : {item['client']}")
            st.info(f"Réponse préparée par l'IA :\n\n{item['reponse']}")
            
            # Bouton pour envoyer sur WhatsApp en un clic
            import urllib.parse
            texte_encode = urllib.parse.quote(item['reponse'])
            num_clean = str(contact_tel_val).replace("+", "").replace(" ", "").strip()
            lien_whatsapp = f"https://wa.me/{num_clean}?text={texte_encode}"
            
            st.markdown(f'''
                <a href="{lien_whatsapp}" target="_blank">
                    <button style="background-color:#25D366; color:white; border:none; padding:8px 16px; border-radius:6px; font-weight:bold; cursor:pointer; font-size:14px;">
                        📲 Reprendre le relais et envoyer sur WhatsApp
                    </button>
                </a>
            ''', unsafe_allow_html=True)
            st.markdown("---")
            from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

# Initialisation de l'historique dans la session si ça n'existe pas
if "historique_appels" not in st.session_state:
    st.session_state["historique_appels"] = []

# Fonction pour ajouter une interaction avec l'heure actuelle
def enregistrer_interaction(question, reponse):
    maintenant = datetime.now()
    st.session_state["historique_appels"].append(
        {"temps": maintenant, "question": question, "reponse": reponse}
    )

# Nettoyage automatique des éléments de plus de 72 heures
limite_72h = datetime.now() - timedelta(hours=72)
st.session_state["historique_appels"] = [
    item
    for item in st.session_state["historique_appels"]
    if item["temps"] > limite_72h
]

from datetime import datetime, timedelta
import google.generativeai as genai
import pandas as pd
import streamlit as st

# ==========================================
# 1. CONFIGURATION DE LA PAGE & STYLE VISUEL
# ==========================================
st.set_page_config(
    page_title="Secrétaire IA - Tableau de Bord",
    page_icon="🎙️",
    layout="wide",
)

# Masquer les styles complexes pour un design très simple et épuré
st.markdown(
    """
    <style>
    .big-title { font-size: 28px; font-weight: bold; color: #1E3A8A; text-align: center; }
    .subtitle { font-size: 16px; color: #4B5563; text-align: center; margin-bottom: 20px; }
    .card { background-color: #F3F4F6; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
    </style>
""",
    unsafe_allow_allow_html=True,
)

# ==========================================
# 2. INITIALISATION DE L'IA ET DU RÔLE
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY")

SYSTEM_INSTRUCTION = """
Tu es la Secrétaire IA Virtuelle du gérant.
Ton rôle est d'aider le gérant et ses clients dans la gestion quotidienne de leur établissement (Hôtel, Atelier, Commerce, etc.).

RÈGLES IMPÉRATIVES DE RÉPONSE :
1. Réponds toujours de manière ultra-courte, claire et directe (pas de longs paragraphes ou de dissertations).
2. Si on te demande "À quoi tu sers ?" ou "Tu es destinée à faire quoi ?", réponds précisément :
   "Je suis votre Secrétaire IA Virtuelle. Je suis destinée à vous servir en secrétariat dans tous les domaines (gestion, accueil, information). Je peux parler presque toutes les langues, y compris les langues locales d'Afrique de l'Ouest (Éwé, Fon, Baoulé, Dioula, Wolof, etc.)."
3. Sois très chaleureuse, respectueuse et facile à comprendre.
"""

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", system_instruction=SYSTEM_INSTRUCTION
    )
else:
    st.error(
        "⚠️ Clé API Gemini non configurée dans les Secrets Streamlit.", icon="⚠️"
    )
    st.stop()

# ==========================================
# 3. GESTION DE L'HISTORIQUE (EFFACEMENT 72H)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Conserver uniquement les messages de moins de 72 heures (3 jours)
limite_72h = datetime.now() - timedelta(hours=72)
st.session_state.messages = [
    msg
    for msg in st.session_state.messages
    if msg.get("date", datetime.now()) > limite_72h
]

# ==========================================
# 4. TABLEAU DE BORD (INTERFACE VISUELLE)
# ==========================================

# En-tête simple et clair
st.markdown(
    '<div class="big-title">🎙️ Votre Secrétaire IA Personnelle</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">Discutez facilement avec votre IA ou posez vos questions ci-dessous</div>',
    unsafe_allow_html=True,
)

# Indicateurs visuels rapides (Statistiques simples)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🟢 Statut IA", value="En ligne")
with col2:
    st.metric(label="💬 Discuter", value="Français & Langues locales")
with col3:
    st.metric(
        label="⏳ Historique conservé",
        value=f"{len(st.session_state.messages)} échanges (72h max)",
    )

st.divider()

# Boutons d'accès rapide aux questions fréquentes (pour ceux qui ne veulent pas taper de texte)
st.subheader("💡 Questions rapides (cliquez pour poser) :")
btn_col1, btn_col2, btn_col3 = st.columns(3)

question_rapide = None
with btn_col1:
    if st.button("❓ À quoi tu sers ?", use_container_width=True):
        question_rapide = "Tu es destinée pour faire quoi ?"
with btn_col2:
    if st.button("🌍 Quelles langues parles-tu ?", use_container_width=True):
        question_rapide = "Quelles langues locales d'Afrique peux-tu parler ?"
with btn_col3:
    if st.button("🏨 Comment peux-tu m'aider ?", use_container_width=True):
        question_rapide = (
            "Comment peux-tu m'aider à gérer mon établissement ?"
        )

# Affichage des échanges précédents
st.subheader("💬 Espace de Discussion")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Zone de saisie utilisateur
user_input = st.chat_input("Écrivez votre message ici...")

# Si l'utilisateur clique sur un bouton rapide ou tape un message
prompt = question_rapide or user_input

if prompt:
    # 1. Enregistrer et afficher le message de l'utilisateur
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "date": datetime.now()}
    )
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Générer la réponse de l'IA
    with st.chat_message("assistant"):
        with st.spinner("La secrétaire répond..."):
            try:
                response = model.generate_content(prompt)
                bot_reply = response.text
                st.write(bot_reply)

                # Enregistrer la réponse de l'IA
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": bot_reply,
                        "date": datetime.now(),
                    }
                )
            except Exception as e:
                st.error("Erreur de connexion avec l'IA.")
from datetime import datetime, timedelta
import google.generativeai as genai
import streamlit as st

# ==========================================
# 1. CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Secrétaire IA - Tableau de Bord",
    page_icon="🎙️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .big-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; }
    .subtitle { font-size: 15px; color: #4B5563; text-align: center; margin-bottom: 20px; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. CONFIGURATION DE L'IA
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY")

SYSTEM_INSTRUCTION = """
Tu es la Secrétaire IA Virtuelle du gérant.
Ton rôle est d'aider le gérant et ses clients dans la gestion quotidienne de leur établissement.

RÈGLES DE RÉPONSE :
1. Réponds de manière ultra-courte, claire et directe.
2. Si on te demande "À quoi tu sers ?", réponds précisément :
   "Je suis votre Secrétaire IA Virtuelle. Je suis destinée à vous servir en secrétariat dans tous les domaines (gestion, accueil, information). Je peux parler presque toutes les langues, y compris les langues locales d'Afrique de l'Ouest (Éwé, Fon, Baoulé, Dioula, Wolof, etc.)."
3. Sois très chaleureuse et professionnelle.
"""

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", system_instruction=SYSTEM_INSTRUCTION
    )
else:
    st.error(
        "⚠️ Clé API Gemini non configurée dans les Secrets Streamlit.", icon="⚠️"
    )
    st.stop()

# ==========================================
# 3. GESTION DES MESSAGES & HISTORIQUE (72H)
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Filtrer les messages de moins de 72h
maintenant_actuel = datetime.now()
limite_72h = maintenant_actuel - timedelta(hours=72)

st.session_state.messages = [
    msg
    for msg in st.session_state.messages
    if msg.get("date", maintenant_actuel) > limite_72h
]

# ==========================================
# 4. INTERFACE GRAPHIQUE DU TABLEAU DE BORD
# ==========================================
st.markdown(
    '<div class="big-title">🎙️ Votre Secrétaire IA Personnelle</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">Tableau de bord simplifié pour le gérant</div>',
    unsafe_allow_html=True,
)

# Indicateurs visuels
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🟢 Statut", value="En ligne")
with col2:
    st.metric(label="💬 Mode", value="Multilingue")
with col3:
    st.metric(label="⏳ Historique", value=f"{len(st.session_state.messages)}")

st.divider()

# Boutons rapides pour poser des questions en un clic
st.subheader("💡 Actions rapides :")
b1, b2, b3 = st.columns(3)
question_rapide = None

with b1:
    if st.button("❓ À quoi tu sers ?", use_container_width=True):
        question_rapide = "À quoi tu sers ?"
with b2:
    if st.button("🌍 Langues parlées", use_container_width=True):
        question_rapide = "Quelles langues parles-tu ?"
with b3:
    if st.button("🏨 Aide gestion", use_container_width=True):
        question_rapide = (
            "Comment peux-tu m'aider à gérer mon établissement ?"
        )

st.subheader("💬 Discussion")

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Entrée utilisateur
user_input = st.chat_input("Écrivez votre message ici...")
prompt = question_rapide or user_input

if prompt:
    # Enregistrer la question de l'utilisateur
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "date": datetime.now()}
    )
    with st.chat_message("user"):
        st.write(prompt)

    # Générer la réponse
    with st.chat_message("assistant"):
        with st.spinner("Réponse en cours..."):
            try:
                response = model.generate_content(prompt)
                bot_reply = response.text
                st.write(bot_reply)

                # Enregistrer la réponse de l'IA
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": bot_reply,
                        "date": datetime.now(),
                    }
                )
            except Exception as e:
                st.error("Erreur lors de la génération de la réponse.")
                
