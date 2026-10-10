import streamlit as st

# Titre de l'application
st.title("🤖 Secrétaire IA Multilingue")
st.subheader("Votre assistant intelligent pour Hôtels, Cliniques & Boutiques")

# Message de bienvenue
st.write("Bienvenue ! Je suis votre secrétaire virtuelle. Comment puis-je vous aider aujourd'hui ?")

# Choix du secteur
service = st.selectbox(
    "Choisissez le service souhaité :",
    ["Hôtel (Réservation de chambre)", "Clinique (Rendez-vous médical)", "Boutique (Renseignements & Produits)"]
)

# Zone de discussion
user_input = st.text_input("Posez votre question ou parlez dans votre langue :")

if user_input:
    st.success("Secrétaire IA à l'écoute")
    
