import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime, timedelta
from PIL import Image
# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Secrétaire IA & Gestion Multilingue",
    page_icon="🤖",
    layout="wide"
)

# --- 2. CONFIGURATION DE L'API GEMINI ---
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Clé API GEMINI_API_KEY manquante dans les secrets Streamlit.")
    st.stop()

model = genai.GenerativeModel("gemini-3.8-flash")


# --- 3. GESTION DE L'HISTORIQUE EN SESSION ---
if "historique_messages" not in st.session_state:
    st.session_state.historique_messages = []

# --- 4. INTERFACE UTILISATEUR : EN-TÊTE ---
st.title("🤖 Secrétaire IA - Tableau de Bord")
st.write("Espace de gestion des clients, de l'hôtel et des discussions.")

st.divider()

# --- 5. SECTION AFFICHAGE DE L'HISTORIQUE ET JOURNAL DE BORD ---
st.subheader("📋 Journal de bord & Historique des discussions")

if len(st.session_state.historique_messages) == 0:
    st.info("Aucun message pour le moment. Le journal est vide.")
else:
    for i, item in enumerate(st.session_state.historique_messages):
        with st.container():
            st.markdown(f"**Échange n°{i+1}**")
            st.text(f"Client : {item.get('client', 'Inconnu')}")
            st.write(f"**Question :** {item.get('question', '')}")
            st.info(f"Réponse de l'IA : {item.get('reponse', '')}")
            st.markdown("---")

# --- 6. ZONE DE SAISIE ET CHAT EN BAS ---
st.subheader("💬 Poser votre question")
user_input = st.chat_input("Écrivez votre message ici...")

if user_input:
    # Génération de la réponse via Gemini
    with st.spinner("Réponse en cours..."):
        try:
            response = model.generate_content(user_input)
            bot_reply = response.text
            
            # Enregistrement dans l'historique propre
            st.session_state.historique_messages.append({
                "client": "Gérant / Utilisateur",
                "question": user_input,
                "reponse": bot_reply,
                "temps": datetime.now()
            })
            
            # Affichage immédiat
            st.success("Vocal/Message analysé et consigné.")
            st.rerun()
            
        except Exception as e:
            st.error(f"Erreur lors de la génération : {e}")
          
# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Secrétaire IA - Gestion Professionnelle",
    page_icon="🤖",
    layout="wide"
)

# --- 2. CONFIGURATION DE L'API GEMINI ---
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Clé API GEMINI_API_KEY manquante dans les secrets Streamlit.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Tu es la Secrétaire IA Virtuelle professionnelle. Tu aides le gérant dans ses activités (hôtel, atelier, gestion). Réponds de manière claire, efficace et directe."
)

# --- 3. SYSTÈME D'AUTHENTIFICATION PAR CODE D'ABONNEMENT ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔑 Connexion Sécurisée")
    code_saisi = st.text_input("Entrez votre code d'abonnement :", type="password")
    
    # Code par défaut ou récupéré depuis les secrets
    code_valide = st.secrets.get("CODE_ACCES", "12345")
    
    if code_saisi:
        if code_saisi == code_valide:
            st.session_state.authenticated = True
            st.success("✅ Accès autorisé ! Bienvenue dans votre Secrétaire IA.")
            st.rerun()
        else:
            st.error("❌ Code d'abonnement incorrect.")
    st.stop()

# --- 4. GESTION DE L'HISTORIQUE EN SESSION ---
if "historique_messages" not in st.session_state:
    st.session_state.historique_messages = []

# --- 5. INTERFACE PRINCIPALE ---
st.title("🤖 Secrétaire IA Multilingue & Tableau de Bord")
st.write("Espace de gestion des clients, du suivi et des discussions.")

st.divider()

# Actions rapides ou modules de gestion
st.subheader("⚡ Accès Rapides & Modules")
col1, col2, col3 = st.columns(3)
action_rapide = None

with col1:
    if st.button("🏨 Gestion Hôtel"):
        action_rapide = "Aide-moi à gérer les réservations et clients de l'hôtel."
with col2:
    if st.button("🔧 Atelier Technique"):
        action_rapide = "Aide-moi à organiser le suivi de l'atelier technique."
with col3:
    if st.button("📊 Suivi Abonnements"):
        action_rapide = "Fais-moi un point sur la gestion des accès et abonnements."

st.divider()

# --- 6. JOURNAL DE BORD & HISTORIQUE ---
st.subheader("📋 Journal de bord & Historique des discussions")

if len(st.session_state.historique_messages) == 0:
    st.info("Aucun message pour le moment. Le journal est vide.")
else:
    for i, item in enumerate(st.session_state.historique_messages):
        with st.container():
            st.markdown(f"**Échange n°{i+1}** - *{item.get('temps').strftime('%H:%M:%S') if item.get('temps') else ''}*")
            st.write(f"**Question :** {item.get('question', '')}")
            st.info(f"**Réponse IA :** {item.get('reponse', '')}")
            st.markdown("---")

# --- 7. ZONE DE SAISIE (CHAT) ---
st.subheader("💬 Poser votre question")
user_input = st.chat_input("Écrivez votre message ou commande ici...")

# Si l'utilisateur clique sur un bouton rapide ou tape dans le chat
prompt_final = action_rapide or user_input

if prompt_final:
    with st.spinner("Réponse en cours..."):
        try:
            response = model.generate_content(prompt_final)
            bot_reply = response.text
            
            # Enregistrement dans l'historique
            st.session_state.historique_messages.append({
                "question": prompt_final,
                "reponse": bot_reply,
                "temps": datetime.now()
            })
            
            st.success("Traitement effectué.")
            st.rerun()
            
        except Exception as e:
            st.error(f"Erreur lors de la génération : {e}")
        
# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Secrétaire IA - Gestion Professionnelle",
    page_icon="🤖",
    layout="wide"
)

# --- 2. CONFIGURATION DE L'API GEMINI ---
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Clé API GEMINI_API_KEY manquante dans les secrets Streamlit.")
    st.stop()

genai.configure(api_key=api_key)

# Modèle stable configuré globalement
model = genai.GenerativeModel("gemini-1.5-flash")
# --- 3. SYSTÈME D'AUTHENTIFICATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔑 Connexion Sécurisée")
    code_saisi = st.text_input("Entrez votre code d'abonnement :", type="password")
    code_valide = st.secrets.get("CODE_ACCES", "12345")
    
    if code_saisi:
        if code_saisi == code_valide:
            st.session_state.authenticated = True
            st.success("✅ Accès autorisé ! Bienvenue dans votre Secrétaire IA.")
            st.rerun()
        else:
            st.error("❌ Code d'abonnement incorrect.")
    st.stop()

# --- 4. GESTION DE L'HISTORIQUE ---
if "historique_messages" not in st.session_state:
    st.session_state.historique_messages = []

# --- 5. INTERFACE PRINCIPALE ---
st.title("🤖 Secrétaire IA Multilingue & Tableau de Bord")
st.write("Espace de gestion des clients, de l'hôtel, de l'atelier et des discussions.")

st.divider()

# --- 6. JOURNAL DE BORD & HISTORIQUE ---
st.subheader("📋 Journal de bord & Historique des discussions")

if len(st.session_state.historique_messages) == 0:
    st.info("Aucun message pour le moment. Le journal est vide.")
else:
    for i, item in enumerate(st.session_state.historique_messages):
        with st.container():
            st.markdown(f"**Échange n°{i+1}**")
            st.write(f"**Question :** {item.get('question', '')}")
            st.info(f"**Réponse IA :** {item.get('reponse', '')}")
            st.markdown("---")

# --- 7. ZONE DE CHAT TEXTUELLE UNIQUE ---
st.subheader("💬 Poser votre question (Multilingue)")
user_input = st.chat_input("Écrivez votre message ou commande ici...", key="unique_chat_input")

if user_input:
    with st.spinner("Réponse en cours..."):
        try:
            response = model.generate_content(user_input)
            bot_reply = response.text
            
            st.session_state.historique_messages.append({
                "question": user_input,
                "reponse": bot_reply,
                "temps": datetime.now()
            })
            
            st.success("Réponse générée.")
            st.rerun()
            
        except Exception as e:
            st.error(f"Erreur : {e}")

# --- 8. ESPACE GÉRANT : ANALYSE DE PHOTOS ---
st.divider()
st.subheader("🛠️ Espace Gérant : Ajouter une photo (Menu, Hôtel, Atelier)")

uploaded_image = st.file_uploader("Télécharger une image pour la base", type=["jpg", "jpeg", "png"], key="unique_image_uploader")

if uploaded_image is not None:
    st.image(uploaded_image, caption="Photo transmise", use_container_width=True)
    description_photo = st.text_input("Explique à la secrétaire ce que c'est (ex: 'Menu du restaurant', 'Chambre d'hôtel')", key="unique_photo_desc")
    
    if st.button("Mémoriser cette photo", key="unique_photo_button"):
        with st.spinner("Analyse de l'image..."):
            try:
                img = Image.open(uploaded_image)
                prompt_img = f"Voici une photo envoyée par le gérant. Description : {description_photo}. Analyse cette image pour renseigner les clients."
                
                response = model.generate_content([prompt_img, img])
                bot_reply = response.text
                
                st.success("Photo mémorisée avec succès !")
                st.write(bot_reply)
                
                st.session_state.historique_messages.append({
                    "question": f"[Photo Gérant] {description_photo}",
                    "reponse": bot_reply,
                    "temps": datetime.now()
                })
            except Exception as e:
                st.error(f"Erreur image : {e}")
