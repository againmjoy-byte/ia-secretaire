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
# ==========================================
# SECTION AJOUTÉE EN BAS : MULTI-DOMAINES
# ==========================================
st.divider()
st.subheader("🏢 Configuration des Domaines & Secteurs d'Activité")
st.write("Gérez les informations spécifiques de votre établissement ci-dessous :")

domaine = st.selectbox(
    "Sélectionnez votre secteur :",
    [
        "🏨 Hôtel / Hébergement", 
        "🛍️ Boutique / Commerce (Boissons, etc.)", 
        "🏥 Clinique / Santé", 
        "🍽️ Restauration / Maquis", 
        "✂️ Coiffure, Beauté & Esthétique",
        "🧵 Ateliers de Mode & Couture",
        "🔧 Ateliers Techniques & Réparations",
        "🧺 Pressing & Services d'entretien",
        "🏦 Banques, Microfinances & Épargne (Petits copecks)"
    ]
)

if "Hôtel" in domaine:
    st.text_input("Nom de l'Hôtel :")
    st.number_input("Nombre de chambres libres :", min_value=0, value=5)
elif "Boutique" in domaine:
    st.text_input("Nom de la Boutique :")
    st.text_area("Produits disponibles (ex: Casiers de Coca-Cola) :")
elif "Banque" in domaine:
    st.text_input("Nom de la structure / Tontine :")
    st.selectbox("Type :", ["Épargne journalière (Petits copecks)", "Microfinance", "Tontine"])
else:
    st.text_input("Nom de l'établissement / atelier :")
    st.text_area("Précisions sur vos services :")

st.text_input("Numéro WhatsApp / Contact de l'établissement :")

if st.button("Enregistrer les paramètres du domaine"):
    st.success("Paramètres enregistrés avec succès !")
    prompt_final = f"""
Tu es une secrétaire virtuelle professionnelle, chaleureuse et multilingue.
Règles de comportement :
1. Accueille toujours le client poliment avec une formule de bienvenue.
2. Réponds ensuite précisément à sa question.
Question ou appel du client : {user_question}
""" 
# --- AJOUT DE LA PARTIE VOCALE ET INTERACTIONS ---
from gtts import gTTS

st.divider()
st.subheader("💬 Espace d'échanges (Texte ou Vocal)")

# Choix de la voix pour la secrétaire IA
voix_genre = st.selectbox("Voix de la secrétaire IA :", ["Féminine", "Masculine"])

# Choix du mode d'interaction
mode_entree = st.radio("Mode d'interaction :", ["Clavier (Écrire)", "Vocal (Parler)"], horizontal=True)

user_question = ""

if mode_entree == "Clavier (Écrire)":
    user_question = st.text_input("Posez votre question ici :")
else:
    audio_file = st.audio_input("Enregistrez votre message vocal :")
    if audio_file is not None:
        st.audio(audio_file)
        st.info("🎙️ Transcription de l'audio en cours...")
        try:
            transcription_response = model.generate_content([
                "Transcris cet enregistrement audio fidèlement en texte en français :",
                {"mime_type": audio_file.type, "data": audio_file.read()}
            ])
            user_question = transcription_response.text
            st.write(f"**Texte reconnu :** {user_question}")
        except Exception as e:
            st.error(f"Erreur lors de la transcription : {e}")

# Si on a une question (via texte ou vocal converti), on génère la réponse
if user_question:
    # On relance le modèle avec ton prompt final et la question
    try:
        with st.spinner("La secrétaire réfléchit..."):
            response = model.generate_content(prompt_final)
            reponse_texte = response.text
        
        st.success("Réponse de la Secrétaire IA :")
        st.write(reponse_texte)

        # Synthèse vocale (gTTS) pour écouter la réponse
        st.info("🔊 Génération de la réponse audio...")
        tts = gTTS(text=reponse_texte, lang='fr', slow=False)
        audio_path = "reponse_ia.mp3"
        tts.save(audio_path)
        
        st.audio(audio_path)

    except Exception as err:
        st.error(f"Une erreur est survenue lors de la réponse : {err}")
# --- CONFIGURATION TÉLÉPHONIQUE & CONTACT (AFRIQUE DE L'OUEST) ---
num_principal = st.text_input(
    "Numéro principal / WhatsApp (ex: +225 07 00 00 00, +229 97 00 00 00, +228 90 00 00 00) :"
)

activer_transfert = st.checkbox(
    "Activer la secrétaire IA sur transfert d'appel (GSM)", 
    value=True,
    help="L'IA prendra le relais en cas d'occupation ou de non-réponse, quel que soit l'opérateur."
)
# --- AJOUT DES DOMAINES IANO (SANS EFFACER LE CODE EXISTANT) ---

st.markdown("---")
st.subheader("🎯 Domaines d'action de IANO")

# Sélection rapide d'un domaine pour afficher son formulaire dédié sans tout scroller
domaine_actif = st.selectbox(
    "Sélectionnez un domaine spécifique pour l'IA :",
    ["Aucun / Général", "🏥 Santé & Assistance", "📄 Secrétariat & Administratif", "💼 Commerce & Vente"],
    key="select_domaine_iano"
)

if domaine_actif == "🏥 Santé & Assistance":
    st.info("💡 Formulaire Santé actif")
    req_sante = st.text_input("Précisez les symptômes ou la demande médicale pour le patient :")
elif domaine_actif == "📄 Secrétariat & Administratif":
    st.info("💡 Formulaire Administratif actif")
    req_admin = st.text_input("Quel document ou courrier officiel faut-il rédiger ?")
elif domaine_actif == "💼 Commerce & Vente":
    st.info("💡 Formulaire Commerce actif")
    req_commerce = st.text_input("Détails du produit, prix ou commande client :")
# --- TABLEAU DE BORD DES ESPACES MÉTIERS (IANO) ---

st.markdown("---")
st.markdown("## 🏢 Espaces Professionnels IANO")
st.write("Cliquez sur votre secteur pour accéder directement à votre espace de travail :")

# Grille de carreaux organisée en 3 colonnes
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏨 Espace Hôtel", use_container_width=True):
        st.session_state["espace_metier"] = "hotel"
    if st.button("✂️ Espace Coiffure", use_container_width=True):
        st.session_state["espace_metier"] = "coiffure"
    if st.button("🧺 Espace Pressing", use_container_width=True):
        st.session_state["espace_metier"] = "pressing"

with col2:
    if st.button("🛍️ Espace Boutique", use_container_width=True):
        st.session_state["espace_metier"] = "boutique"
    if st.button("🧵 Espace Mode & Couture", use_container_width=True):
        st.session_state["espace_metier"] = "couture"
    if st.button("🏦 Espace Banque / Copecs", use_container_width=True):
        st.session_state["espace_metier"] = "banque"

with col3:
    if st.button("🍽️ Espace Restauration", use_container_width=True):
        st.session_state["espace_metier"] = "restauration"
    if st.button("🔧 Espace Atelier Technique", use_container_width=True):
        st.session_state["espace_metier"] = "atelier"
    if st.button("🏥 Espace Clinique & Santé", use_container_width=True):
        st.session_state["espace_metier"] = "sante"

# Affichage dynamique et propre de l'espace cliqué avec ses formulaires
if "espace_metier" in st.session_state:
    metier = st.session_state["espace_metier"]
    st.markdown("---")
    
    if metier == "hotel":
        st.subheader("🏨 Espace Hôtel - Gestion & Réservations")
        st.text_input("Numéro de chambre / Nom du client :")
        st.text_area("Détails de la demande ou service demandé :")
    elif metier == "boutique":
        st.subheader("🛍️ Espace Boutique - Commerce")
        st.text_input("Nom de l'article ou produit recherché :")
        st.text_input("Prix ou quantité en stock :")
    elif metier == "restauration":
        st.subheader("🍽️ Espace Restauration / Maquis")
        st.text_input("Plat du jour ou commande de repas :")
    elif metier == "coiffure":
        st.subheader("✂️ Espace Coiffure & Esthétique")
        st.text_input("Type de prestation (tresses, soins, etc.) :")
    elif metier == "couture":
        st.subheader("🧵 Espace Mode & Couture")
        st.text_input("Mesures ou modèle de vêtement à confectionner :")
    elif metier == "atelier":
        st.subheader("🔧 Espace Atelier & Réparations")
        st.text_input("Description de la panne ou de l'appareil :")
    elif metier == "pressing":
        st.subheader("🧺 Espace Pressing & Entretien")
        st.text_input("Type d'habit ou consigne de lavage :")
    elif metier == "banque":
        st.subheader("🏦 Espace Banque / Microfinance (Copecs)")
        st.text_input("Type d'opération financière (Dépôt, Retrait, Épargne) :")
    elif metier == "sante":
        st.subheader("🏥 Espace Clinique & Santé")
        st.text_input("Nom du patient / Symptômes ou consultation :")
            # --- ESPACE UNIQUE IANO (SANS RIEN EFFACER) ---
st.markdown("---")
st.markdown("## 🏢 Espace Professionnel IANO")

secteur_actif = st.selectbox(
    "Sélectionnez votre secteur :",
    ["🏨 Hôtel", "🛍️ Boutique", "🍽️ Restauration", "✂️ Coiffure", "🧵 Couture", "🔧 Atelier"],
    key="menu_unique_iano"
)

if secteur_actif == "🏨 Hôtel":
    st.text_input("Client / Chambre :", key="champ_hotel")
elif secteur_actif == "🛍️ Boutique":
    st.text_input("Article :", key="champ_boutique")
elif secteur_actif == "🍽️ Restauration":
    st.text_input("Commande :", key="champ_resto")
elif secteur_actif == "✂️ Coiffure":
    st.text_input("Prestation :", key="champ_coiffure")
elif secteur_actif == "🧵 Couture":
    st.text_input("Mesures :", key="champ_couture")
elif secteur_actif == "🔧 Atelier":
    st.text_input("Réparation :", key="champ_atelier")

    
