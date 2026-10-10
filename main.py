import streamlit as st
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
