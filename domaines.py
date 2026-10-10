import streamlit as st

st.set_page_config(page_title="Sélection des Domaines - Secrétaire IA", layout="centered")

st.title("🏢 Configuration de votre Secteur d'Activité")
st.write("Choisissez votre domaine pour configurer votre assistant sur-mesure :")

# Menu de sélection des domaines
domaine = st.selectbox(
    "Sélectionnez votre domaine :",
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

st.divider()

# Formulaires dynamiques selon le choix
if "Hôtel" in domaine:
    st.subheader("🏨 Configuration Hôtel")
    nom = st.text_input("Nom de l'Hôtel :")
    chambres = st.number_input("Nombre de chambres libres :", min_value=0, value=5)
    etat = st.selectbox("État des chambres :", ["Propre & Prête", "Sale / En nettoyage"])
    
elif "Boutique" in domaine:
    st.subheader("🛍️ Configuration Boutique")
    nom = st.text_input("Nom de la Boutique :")
    produits = st.text_area("Produits disponibles (ex: Casiers de Coca-Cola) :")

elif "Banque" in domaine:
    st.subheader("🏦 Configuration Finance & Épargne")
    nom = st.text_input("Nom de la structure / Tontine :")
    type_service = st.selectbox("Type :", ["Épargne journalière (Petits copecks)", "Microfinance", "Tontine"])

else:
    st.subheader(f"🔧 Configuration : {domaine}")
    nom = st.text_input("Nom de l'établissement / atelier :")
    details = st.text_area("Précisions sur vos services :")

# Numéro de contact commun
telephone = st.text_input("Numéro WhatsApp / Contact pour recevoir les alertes :")

if st.button("💾 Enregistrer mes paramètres"):
    st.success(f"Bravo ! Les informations pour **{nom}** ({domaine}) ont bien été prises en compte.")
