import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="IA Secrétaire", page_icon="🤖")

st.title("🤖 Secrétaire IA Multilingue")
st.write("Posez votre question ou parlez dans votre langue d'Afrique de l'Ouest")

# Configuration de la clé API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Saisie utilisateur
user_input = st.text_input("Votre message :", key="input_text")

if user_input:
    st.markdown(f"**Vous :** {user_input}")
    
    with st.spinner("L'assistant réfléchit..."):
        try:
            # Utilisation du modèle à jour
            model = genai.GenerativeModel('models/gemini-3.8-flash')
            
            # Génération de la réponse
            response = model.generate_content(user_input)
            
            st.markdown(f"**Secrétaire IA :** {response.text}")
            
        except Exception as e:
            st.error(fErreur lors de la génération : {e}")
