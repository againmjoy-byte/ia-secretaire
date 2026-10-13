import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime, timedelta

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

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Tu es la Secrétaire IA Virtuelle. Réponds de manière claire, directe et utile."
)

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
          
