import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Secrétaire IA Multilingue", page_icon="🤖")

st.title("🌍 Secrétaire IA Universelle & Multilingue")
st.markdown("Votre assistante intelligente pour tous types d'activités (Ventes, Services, Réservations, etc.).")

# Récupération sécurisée de la clé API depuis les secrets Streamlit
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Erreur : Veuillez configurer votre clé 'GEMINI_API_KEY' dans les secrets de Streamlit Cloud.")
    st.stop()

# Configuration du domaine et des informations par le propriétaire/agent
st.sidebar.header("⚙️ Configuration de l'activité")
domaine_activite = st.sidebar.text_input("Domaine / Activité :", "Vente générale / Prestation de services")
infos_stock_dispo = st.sidebar.text_area("Disponibilités / Infos du stock (Chambres, articles, prix...) :", "Ex: 5 chambres disponibles à 15 000 FCFA, livraison gratuite à Lomé.")

# Choix de la langue ou consigne multilingue
st.sidebar.markdown("---")
st.sidebar.markdown("🗣️ *La secrétaire détecte et parle automatiquement votre langue (Français, Anglais, langues locales, etc.).*")

# Zone de discussion avec le client
st.markdown("### 💬 Discussion avec le client")

# Initialisation de l'historique des messages dans la session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des anciens messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Champ de saisie du client en bas de page
if prompt_client := st.chat_input("Posez votre question ou parlez dans votre langue..."):
    # Afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt_client})
    with st.chat_message("user"):
        st.markdown(prompt_client)

    # Génération de la réponse par l'IA en streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            chat = model.start_chat(history=[])

            system_instruction = f"""
            Tu es une secrétaire virtuelle universelle, professionnelle et multilingue.
            Ton domaine d'activité actuel est : {domaine_activite}.
            Voici les informations de stock, de prix ou de disponibilités fournies par ton patron : {infos_stock_dispo}.
            
            Règles à suivre :
            1. Détecte la langue de l'interlocuteur et réponds-lui dans cette même langue avec fluidité et courtoisie.
            2. Aide le client à trouver ce qu'il cherche, renseigne-le sur les disponibilités et aide à formuler la vente ou la réservation.
            3. Sois naturelle, polie et efficace comme une vraie secrétaire professionnelle.
            """
            
            # Utilisation du modèle Gemini avec streaming
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            
            # Création de l'historique pour le chat
            chat = model.start_history(history=[])
            
            # Appel en streaming
            response = model.generate_content(prompt_client, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
                
            message_placeholder.markdown(full_space := full_response)
            
        except Exception as e:
            full_response = f"Une erreur s'est produite : {e}"
            message_placeholder.markdown(full_response)

    # Sauvegarde de la réponse de l'assistant
    st.session_state.messages.append({"role": "assistant", "content": full_response})
