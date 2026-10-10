import os
import streamlit as st
import google.generativeai as genai

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Secrétaire IA Universelle & Multilingue",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 Secrétaire IA Universelle & Multilingue")
st.write("Votre assistante intelligente pour tous types d'activités (Ventes, Services, Réservations, etc.).")

# Récupération sécurisée de la clé API depuis les secrets de Streamlit Cloud
api_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    st.error("Erreur : Veuillez configurer votre clé 'GEMINI_API_KEY' dans les secrets de Streamlit Cloud.")
    st.stop()

# Configuration de l'API Google Gemini
genai.configure(api_key=api_key)

# Barre latérale pour configurer le rôle et les informations de l'activité
st.sidebar.header("⚙️ Configuration de l'activité")

domaine_activite = st.sidebar.text_area(
    "Domaine d'activité / Type d'entreprise :",
    value="Vente de produits locaux et prestations de services divers."
)

infos_stock_services = st.sidebar.text_area(
    "Inventaire, prix, services ou horaires :",
    value="- Produits disponibles en stock.\n- Horaires d'ouverture : 8h - 18h\n- Réservation et commande possibles 24h/24."
)

# Instructions système dynamiques pour l'IA
system_instruction = f"""
Tu es une secrétaire virtuelle universelle, polie et professionnelle.
Ton domaine d'activité actuel est : {domaine_activite}
Voici les informations de stock, de prix ou de services à respecter :
{infos_stock_services}

Règles à suivre :
1. Détecte la langue de l'interlocuteur et réponds exactement dans la même langue (français, langues locales ou autres).
2. Aide le client à trouver ce qu'il cherche, à passer commande ou à prendre un rendez-vous.
3. Sois naturelle, polie et efficace comme un(e) véritable secrétaire professionnel(le).
"""

# Initialisation du modèle Gemini avec streaming
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
    # Initialisation correcte du chat avec le modèle
    chat = model.start_chat(history=[])
except Exception as e:
    st.error(f"Erreur d'initialisation du modèle : {e}")
    st.stop()

# Initialisation de l'historique des messages dans la session Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salut ! Comment puis-je vous aider aujourd'hui ? (Vous pouvez me parler dans la langue de votre choix)."}
    ]

# Affichage de l'historique de discussion
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie utilisateur pour le chat
if prompt := st.chat_input("Posez votre question ou parlez dans votre langue..."):
    # Ajout du message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Génération de la réponse de l'assistant en streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            response = chat.send_message(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Une erreur s'est produite : {e}"
            message_placeholder.markdown(full_response)
            
    # Ajout de la réponse de l'assistant à l'historique
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
