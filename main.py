import streamlit as st
import google.generativeai as genai

# Configuration de la page Streamlit
st.set_page_config(page_title="IA Secrétaire", page_icon="🤖", layout="centered")

st.title("🤖 Secrétaire IA Multilingue")
st.caption("Posez votre question ou parlez dans votre langue d'Afrique de l'Ouest")

# Initialisation de l'API Gemini
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("🔑 Clé API GEMINI_API_KEY manquante dans les secrets Streamlit.")

# Historique des messages dans la session Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique de discussion
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Saisie de l'utilisateur
user_input = st.chat_input("Posez votre question ou parlez dans votre langue...")

if user_input:
    # 1. Afficher la question de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Générer la réponse avec l'IA
    with st.chat_message("assistant"):
        try:
            # Modèle à jour recommandé
            model = genai.GenerativeModel('models/gemini-3.8-flash')
            
            # Formater les contenus pour l'appel
            formatted_contents = [
                {"role": m["role"], "parts": [m["content"]]} 
                for m in st.session_state.messages
            ]
            
            response = model.generate_content(
                contents=formatted_contents
            )
            
            bot_reply = response.text
            st.markdown(bot_reply)
            
            # Sauvegarder la réponse dans l'historique
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            error_msg = f"Une erreur s'est produite : {e}"
            st.error(error_msg)
