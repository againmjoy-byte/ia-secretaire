import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Test Clé API", page_icon="🔍")

st.title("🔍 Test de connexion de ta clé")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ La clé API 'GEMINI_API_KEY' est introuvable dans les secrets Streamlit.")
else:
    genai.configure(api_key=api_key)
    
    if st.button("Lancer le test de ma clé"):
        try:
            st.write("Interrogation de Google pour voir tes modèles autorisés...")
            # On demande la liste exacte des modèles disponibles pour cette clé
            models_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            st.success("Connexion réussie ! Voici les modèles disponibles pour ta clé :")
            for mod in models_list:
                st.code(mod)
                
        except Exception as err:
            st.error(f"Échec de la connexion avec cette clé : {err}")
