import streamlit as st
from google import genai

st.set_page_config(page_title="Secrétaire IA", page_icon="🤖")

st.title("🤖 Secrétaire IA Multilingue")

# Vérification de la clé API dans les secrets Streamlit
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ La clé API 'GEMINI_API_KEY' est introuvable dans les secrets Streamlit.")
else:
    # Initialisation directe avec la nouvelle bibliothèque
    client = genai.Client(api_key=api_key)
    
    user_input = st.text_input("Posez votre question :", key="user_query")
    
    if user_input:
        st.write(f"**Vous :** {user_input}")
        try:
            # Appel direct au modèle flash
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input
            )
            st.write(f"**Secrétaire IA :** {response.text}")
        except Exception as err:
            st.error(f"Erreur technique : {err}")
